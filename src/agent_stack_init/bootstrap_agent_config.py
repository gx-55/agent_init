#!/usr/bin/env python3
"""Create commented agent configuration boilerplate for a project."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from textwrap import dedent


def slugify(value: str) -> str:
    cleaned = []
    previous_dash = False
    for char in value.lower():
        if char.isalnum():
            cleaned.append(char)
            previous_dash = False
        elif not previous_dash:
            cleaned.append("-")
            previous_dash = True
    return "".join(cleaned).strip("-") or "project"


def write_file(path: Path, content: str, force: bool) -> str:
    if path.exists() and not force:
        return f"skip existing {path}"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")
    return f"write {path}"


def executable(path: Path) -> None:
    mode = path.stat().st_mode
    path.chmod(mode | 0o111)


def root_memory(project_name: str, domain: str) -> str:
    slug = slugify(project_name)
    return dedent(
        f"""\
        # {slug}
        <!-- Keep this root memory short. It is loaded at every session start. -->
        {domain}

        ## Layout
        <!-- Replace these paths with the directories that matter in this repo. -->
        - `services/retrieval/`  - chunking, embedding, reranker, citation packing
        - `services/answer/`     - prompt templates, generator node, guardrails
        - `shared/`              - schemas, tracing, settings
        - `evals/`               - golden sets, runners, scoring

        ## Build & test
        <!-- Keep commands exact. Delete commands that do not work in this repo. -->
        - Install:           `uv sync`
        - Unit tests:        `uv run pytest -q`
        - Eval harness:      `uv run python -m evals.run --suite citations`
        - Lint + types:      `uv run ruff format . && uv run mypy .`

        ## Canonical conventions
        <!-- Write behavioral rules, not aspirations. -->
        - The canonical answer prompt lives at `services/answer/prompts/v4.md`.
          Do not edit frozen prompt versions unless updating regression snapshots.
        - All LLM outputs must be validated with typed schemas. No raw dict returns
          from generator nodes.
        - Retrieval results must carry stable citation ids. Answer generation must
          emit citations using those exact ids.

        ## Guardrails
        <!-- These lines should prevent common agent mistakes. Tune aggressively. -->
        - Never bump a model version string without updating its eval snapshot in
          the same commit.
        - Never introduce network calls inside unit tests. Use fixtures and fakes.
        - Prefer editing existing modules over adding new top-level packages.
        - If a change touches `services/retrieval/`, read `.claude/rules/retrieval.md`
          before planning.
        - Keep functions focused. Split by responsibility when behavior branches.

        ## Before opening a PR
        <!-- Replace with the checks your team actually requires. -->
        - Run the relevant tests or evals and include the result in the PR body.
        - Update `CHANGELOG.md` under `## Unreleased` when user-facing behavior changes.
        - Use the PR readiness subagent in `.claude/agents/pr-checklist.md`.
        """
    )


def retrieval_rules() -> str:
    return dedent(
        """\
        ---
        name: retrieval-rules
        description: Conventions for retrieval code. Loaded only for matching paths.
        globs:
          - "services/retrieval/**"
          - "tests/retrieval/**"
        ---
        # Retrieval Service Rules

        ## Chunking
        - Use the project canonical chunker for all document ingest.
        - Document chunk-size or overlap changes in an ADR or eval note.

        ## Reranker
        - Implement the existing reranker interface. Do not parallel it.
        - Cap reranking input size. Reranker latency is usually an SLO risk.

        ## Citations
        - Every returned chunk must carry a stable citation id.
        - Use the shared citation helper. Do not hand-roll citation ids.
        - If citation id semantics change, update answer citation packing in the same diff.

        ## Tests
        - Retrieval unit tests must not hit embedding or search APIs.
        - Gate integration tests behind an explicit marker.
        """
    )


def answer_rules() -> str:
    return dedent(
        """\
        ---
        name: answer-rules
        description: Conventions for answer generation, prompts, schemas, and citations.
        globs:
          - "services/answer/**"
          - "tests/answer/**"
        ---
        # Answer Generation Rules

        ## Prompts
        - Edit only the current prompt version unless the user explicitly asks for a migration.
        - Keep old prompt versions frozen for regression comparisons.

        ## Structured Output
        - Validate LLM outputs with typed schemas before returning them.
        - Do not pass raw provider responses across service boundaries.

        ## Citations
        - Answers must cite only ids present in the retrieval context.
        - Unsupported claims should be removed or marked as insufficient evidence.
        """
    )


def tests_rules() -> str:
    return dedent(
        """\
        ---
        name: test-rules
        description: Test-suite conventions and network boundaries.
        globs:
          - "tests/**"
          - "evals/**"
        ---
        # Test and Eval Rules

        ## Unit Tests
        - Unit tests must be deterministic and offline.
        - Use fixtures or fakes for model, embedding, database, and network behavior.

        ## Evals
        - Add focused eval cases for behavior changes that affect retrieval or generation.
        - Store expected citation ids or expected evidence text explicitly.
        - Include eval diffs in PR notes when eval outputs change.
        """
    )


def frontend_rules() -> str:
    return dedent(
        """\
        ---
        name: frontend-rules
        description: Frontend conventions. Delete this file if the repo has no UI.
        globs:
          - "app/**"
          - "src/**"
          - "components/**"
          - "pages/**"
        ---
        # Frontend Rules

        ## UI
        - Match existing components, spacing, and interaction patterns before adding new ones.
        - Use icon buttons for common tools when the project has an icon library.
        - Keep operational dashboards dense, calm, and scannable.

        ## Verification
        - Check responsive layouts for text overflow and overlapping controls.
        - Start the dev server and provide the local URL when changing app behavior.
        """
    )


def agent(name: str, body: str) -> str:
    return dedent(body).strip() + "\n"


def settings_json() -> str:
    data = {
        "hooks": {
            "PreToolUse": [
                {
                    "matcher": "Bash",
                    "hooks": [
                        {"type": "command", "command": ".claude/hooks/gate_git_push.sh"}
                    ],
                }
            ],
            "PostToolUse": [
                {
                    "matcher": "Write|Edit|MultiEdit",
                    "hooks": [
                        {
                            "type": "command",
                            "command": "uv run ruff format $CLAUDE_TOOL_FILE_PATH >/dev/null 2>&1 || true",
                        }
                    ],
                }
            ],
            "PermissionDenied": [
                {
                    "hooks": [
                        {
                            "type": "command",
                            "command": "mkdir -p .claude/logs && jq -c . >> .claude/logs/denied.jsonl",
                        }
                    ]
                }
            ],
        }
    }
    return json.dumps(data, indent=2) + "\n"


def settings_jsonc() -> str:
    return dedent(
        """\
        {
          // Copy this file to the Claude settings location your team uses after review.
          // JSON itself does not allow comments, so keep this file as documentation and
          // use settings.example.json as the machine-readable version.
          "hooks": {
            "PreToolUse": [
              {
                // Runs before Bash tool calls. The script below defers protected pushes.
                "matcher": "Bash",
                "hooks": [
                  {
                    "type": "command",
                    "command": ".claude/hooks/gate_git_push.sh"
                  }
                ]
              }
            ],
            "PostToolUse": [
              {
                // Keep this formatter quiet and non-blocking. Replace with your formatter.
                "matcher": "Write|Edit|MultiEdit",
                "hooks": [
                  {
                    "type": "command",
                    "command": "uv run ruff format $CLAUDE_TOOL_FILE_PATH >/dev/null 2>&1 || true"
                  }
                ]
              }
            ],
            "PermissionDenied": [
              {
                // Audit denied operations. Ensure jq is installed before enabling.
                "hooks": [
                  {
                    "type": "command",
                    "command": "mkdir -p .claude/logs && jq -c . >> .claude/logs/denied.jsonl"
                  }
                ]
              }
            ]
          }
        }
        """
    )


def mcp_jsonc(project_slug: str) -> str:
    return dedent(
        f"""\
        {{
          // Keep this list small. Tool schemas consume context.
          "mcpServers": {{
            "github": {{
              "command": "npx",
              "args": ["-y", "@modelcontextprotocol/server-github"],
              "env": {{
                "GITHUB_PERSONAL_ACCESS_TOKEN": "${{GITHUB_TOKEN}}"
              }}
            }},
            "filesystem": {{
              "command": "npx",
              "args": [
                "-y",
                "@modelcontextprotocol/server-filesystem",
                "${{PWD}}"
              ]
            }},
            "context7": {{
              "command": "npx",
              "args": ["-y", "@upstash/context7-mcp@latest"]
            }},
            "brave-search": {{
              "command": "npx",
              "args": ["-y", "@modelcontextprotocol/server-brave-search"],
              "env": {{
                "BRAVE_API_KEY": "${{BRAVE_API_KEY}}"
              }}
            }},
            "project-memory": {{
              // Replace with your preferred code graph or memory server.
              "command": "npx",
              "args": ["-y", "@vexp/mcp-server@latest"],
              "env": {{
                "VEXP_PROJECT": "{project_slug}",
                "VEXP_MEMORY_DIR": ".vexp"
              }}
            }}
          }}
        }}
        """
    )


def hook_script() -> str:
    return dedent(
        """\
        #!/usr/bin/env bash
        # Defer git pushes to protected branches. Review before enabling in CI.
        set -euo pipefail

        payload="$(cat)"
        cmd="$(printf '%s' "$payload" | jq -r '.tool_input.command // empty')"

        case "$cmd" in
          *"git push"*"origin main"*|*"git push"*" main"*|*"git push"*"origin master"*|*"git push"*" master"*)
            jq -nc '{
              "permissionDecision": "defer",
              "reason": "Push to a protected branch requires human approval."
            }'
            ;;
          *)
            jq -nc '{"permissionDecision": "allow"}'
            ;;
        esac
        """
    )


def workflow() -> str:
    return dedent(
        """\
        name: claude-nightly-evals

        on:
          # Enable after secrets, hooks, and allowlists are reviewed.
          workflow_dispatch:
          # schedule:
          #   - cron: "0 7 * * *"

        jobs:
          run-evals-and-open-pr:
            runs-on: ubuntu-latest
            permissions:
              contents: write
              pull-requests: write
            env:
              ANTHROPIC_API_KEY: ${{ secrets.ANTHROPIC_API_KEY }}
              GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
            steps:
              - uses: actions/checkout@v4
              - uses: astral-sh/setup-uv@v3
              - run: uv sync

              - name: Install Claude Code
                run: npm i -g @anthropic-ai/claude-code@latest

              - name: Run nightly eval and draft PR
                id: claude
                run: |
                  set -o pipefail
                  claude -p \\
                    --bare \\
                    --output-format stream-json \\
                    --allowedTools "Bash(uv run:*),Read,Grep,Glob,Write,Edit,mcp__github__*" \\
                    --append-system-prompt "Run evals, make the smallest safe fix, and open a draft PR if regressions appear." \\
                    "Run the citation eval suite. If any case regresses, implement the minimal fix and open a draft PR against main." \\
                  | tee claude.ndjson

                  if grep -q '"permissionDecision":"defer"' claude.ndjson; then
                    echo "deferred=true" >> "$GITHUB_OUTPUT"
                  fi

              - name: Resume after deferred approval
                if: steps.claude.outputs.deferred == 'true'
                run: |
                  SESSION_ID="$(jq -r 'select(.type=="deferred") | .session_id' claude.ndjson | head -n1)"
                  claude --resume "$SESSION_ID" \\
                    --append-system-prompt "Approved. Continue." \\
                    --output-format stream-json
        """
    )


def command_agent_stack_init() -> str:
    return dedent(
        """\
        ---
        description: Generate or refresh the commented Claude/Codex agent configuration stack for this project.
        argument-hint: [optional project description]
        ---

        Initialize this repository with the local agent configuration stack.

        User arguments:
        $ARGUMENTS

        Steps:
        1. Infer the project name from the repository folder unless the user supplied one.
        2. Use the user arguments as the project domain description when present.
        3. Run `.claude/tools/bootstrap_agent_config.py --target .` with `--project-name` and `--domain`.
        4. Do not use `--force` unless the user explicitly asked to refresh or overwrite existing generated files.
        5. After generation, inspect `CLAUDE.md`, `.claude/rules/`, and `docs/agent-stack.md`.
        6. Summarize which files were created or skipped and list the first comments the user should edit.
        """
    )


def command_init_alias() -> str:
    return dedent(
        """\
        ---
        description: Init-style alias for the agent configuration stack. Use /project:agent-stack-init if /init is reserved.
        argument-hint: [optional project description]
        ---

        Run the same workflow as `agent-stack-init`.

        If this command name conflicts with a built-in `/init`, tell the user to invoke:

        `/project:agent-stack-init`

        Then initialize the repository with `.claude/tools/bootstrap_agent_config.py --target .`, using `$ARGUMENTS` as the optional project description.
        """
    )


def command_new_agent_project() -> str:
    return dedent(
        """\
        ---
        description: Create a new project folder and immediately add the commented Claude/Codex agent configuration stack.
        argument-hint: <project-folder> [project description]
        ---

        Create a new project and install the agent configuration stack.

        User arguments:
        $ARGUMENTS

        Steps:
        1. Parse the first argument as the target project folder.
        2. Treat the rest of the arguments as the project description.
        3. Create the target folder if it does not exist.
        4. Run this repository's bootstrapper into that folder. If the new folder already has `.claude/tools/bootstrap_agent_config.py`, prefer that local copy.
        5. Do not overwrite existing files unless the user explicitly asks.
        6. Summarize the created folder and the generated setup files.
        """
    )


def local_skill() -> str:
    return dedent(
        """\
        ---
        name: new-rag-eval
        description: Add a new RAG or citation evaluation case, wire it into the eval harness, run the focused case, and summarize the result. Use when the user asks to add an eval, cover a regression, or verify citation behavior.
        ---

        # New RAG Eval

        ## Inputs

        Gather the query, expected citation ids or expected evidence text, and optional production trace id.

        ## Steps

        1. Read the local eval template if one exists.
        2. Create a kebab-case case file in the citation eval suite.
        3. Run the smallest focused eval command available.
        4. Summarize pass/fail, citation grounding, unsupported claims, and latency outliers.
        5. If failure is expected today, add a short note to the case file.

        ## Boundaries

        - Do not edit unrelated eval suites.
        - Do not open a PR from this skill.
        - Do not introduce network calls into unit tests.
        """
    )


def guide(project_name: str) -> str:
    return dedent(
        f"""\
        # Agent Stack Setup

        This repo contains editable boilerplate for a lean agent configuration stack.

        ## First Edits

        1. Edit `CLAUDE.md` until every line changes agent behavior for `{project_name}`.
        2. Delete `.claude/rules/*.md` files that do not match real directories.
        3. Replace example commands in `CLAUDE.md` with commands that pass locally.
        4. Review `.claude/hooks/gate_git_push.sh` before enabling it in live settings.
        5. Keep `.claude/mcp.example.jsonc` small; remove servers you do not actually use.

        ## Files With Comments

        - Use `*.jsonc` files as the commented source of truth.
        - Use matching `*.json` files when a tool needs strict JSON.
        - Keep generated workflow files as `.example.yml` until secrets and permissions are ready.

        ## Claude Code Commands

        Project commands are generated in `.claude/commands/`.

        - Use `/project:agent-stack-init` to generate or refresh this stack.
        - Use `/project:new-agent-project` when starting a new folder from Claude Code.
        - `.claude/commands/init.md` is an init-style alias, but many Claude Code setups reserve `/init` as a built-in command. Prefer the explicit project command when in doubt.

        To install global Claude Code user commands from the package:

        ```bash
        agent-stack-init install-claude-commands
        ```

        This installs `/agent-stack-init` and `/new-agent-project`. Re-run with
        `--with-init-alias` only if you intentionally want to add a user `/init` alias.

        ## Codex Skill Install

        To make natural language requests trigger this bootstrap workflow in future Codex
        sessions, install the `agent-stack-init` skill into Codex's skills directory:

        ```bash
        agent-stack-init install-codex-skill
        ```

        ## Operating Rule

        The stack should reduce repeated explanation. If a file becomes a second wiki, split it
        into path-scoped rules, a local skill, or a short subagent prompt.
        """
    )


def build_files(target: Path, project_name: str, domain: str) -> dict[Path, str]:
    slug = slugify(project_name)
    bootstrap_source = Path(__file__).read_text(encoding="utf-8")
    return {
        target / "CLAUDE.md": root_memory(project_name, domain),
        target / ".claude/rules/retrieval.md": retrieval_rules(),
        target / ".claude/rules/answer.md": answer_rules(),
        target / ".claude/rules/tests.md": tests_rules(),
        target / ".claude/rules/frontend.md": frontend_rules(),
        target / ".claude/agents/retrieval-reviewer.md": agent(
            "retrieval-reviewer",
            """\
            ---
            name: retrieval-reviewer
            description: Reviews retrieval changes for chunking, reranker, citation contract, and test regressions. Read-only.
            tools: Read, Grep, Glob, Bash(git diff:*), Bash(uv run pytest:*)
            model: sonnet
            ---
            You are a retrieval-service reviewer.

            Scope:
            - Review only retrieval files and their tests.
            - Ignore unrelated files even when they appear in the diff.

            Checklist:
            1. Confirm chunking uses the project canonical entry point.
            2. Confirm reranker interface changes update every implementation.
            3. Confirm returned chunks carry stable citation ids from the shared helper.
            4. Confirm unit tests do not call network services.
            5. Confirm eval snapshots or notes are updated when behavior changes.

            Output:
            - Verdict: pass / needs-changes / blocker.
            - Findings with file path and one-line fix.
            """,
        ),
        target / ".claude/agents/prompt-auditor.md": agent(
            "prompt-auditor",
            """\
            ---
            name: prompt-auditor
            description: Reviews prompt changes for regression, citation, schema, and safety issues. Read-only.
            tools: Read, Grep, Glob, Bash(git diff:*)
            model: sonnet
            ---
            Review prompt changes only.

            Flag:
            - Removed citation requirements.
            - Output shape that no longer matches schemas.
            - Prompt version changes without snapshots.
            - New unsupported claims or hidden chain-of-thought requests.

            Output concise findings with file paths and fixes.
            """,
        ),
        target / ".claude/agents/eval-runner.md": agent(
            "eval-runner",
            """\
            ---
            name: eval-runner
            description: Runs focused evals and summarizes structured results.
            tools: Read, Grep, Glob, Bash(uv run python -m evals.run:*), Bash(uv run pytest:*)
            model: sonnet
            ---
            Run the smallest relevant eval or test command.

            Summarize:
            - Command run.
            - Pass/fail status.
            - Metric deltas.
            - Failing cases and likely owner files.

            Do not edit files.
            """,
        ),
        target / ".claude/agents/pr-checklist.md": agent(
            "pr-checklist",
            """\
            ---
            name: pr-checklist
            description: Checks readiness before opening a PR.
            tools: Read, Grep, Glob, Bash(git diff:*), Bash(git status:*), Bash(uv run pytest:*)
            model: sonnet
            ---
            Review the current diff for PR readiness.

            Check:
            - Tests or evals are updated for behavior changes.
            - Changelog or release notes are updated when needed.
            - No secrets, debug prints, or broad unrelated refactors.
            - PR body can include commands run and eval output.

            Output blockers first, then a draft PR checklist.
            """,
        ),
        target / ".claude/commands/agent-stack-init.md": command_agent_stack_init(),
        target / ".claude/commands/init.md": command_init_alias(),
        target / ".claude/commands/new-agent-project.md": command_new_agent_project(),
        target / ".claude/skills/new-rag-eval/SKILL.md": local_skill(),
        target / ".claude/hooks/gate_git_push.sh": hook_script(),
        target / ".claude/tools/bootstrap_agent_config.py": bootstrap_source,
        target / ".claude/settings.example.jsonc": settings_jsonc(),
        target / ".claude/settings.example.json": settings_json(),
        target / ".claude/mcp.example.jsonc": mcp_jsonc(slug),
        target / ".github/workflows/claude-nightly-evals.example.yml": workflow(),
        target / "docs/agent-stack.md": guide(project_name),
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--target", default=".", help="Repository root to scaffold into.")
    parser.add_argument("--project-name", default=None, help="Project name for CLAUDE.md.")
    parser.add_argument(
        "--domain",
        default="Short project description. Replace this with the product, service, or repo purpose.",
        help="One-line domain description for CLAUDE.md.",
    )
    parser.add_argument("--force", action="store_true", help="Overwrite existing generated files.")
    args = parser.parse_args(argv)

    target = Path(args.target).expanduser().resolve()
    project_name = args.project_name or target.name
    files = build_files(target, project_name, args.domain)

    actions = [write_file(path, content, args.force) for path, content in files.items()]
    hook = target / ".claude/hooks/gate_git_push.sh"
    if hook.exists():
        executable(hook)
    tool = target / ".claude/tools/bootstrap_agent_config.py"
    if tool.exists():
        executable(tool)

    print("\n".join(actions))
    print(f"\nGenerated agent stack for {project_name} at {target}")
    print("Next: edit CLAUDE.md, delete unused rules, and review .claude/settings.example.jsonc.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
