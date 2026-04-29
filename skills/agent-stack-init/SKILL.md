---
name: agent-stack-init
description: Scaffold or install a commented Claude/Codex agent configuration stack for a software project. Use when setting up or refreshing project memory files, path-scoped rules, custom subagents, hooks, MCP/server examples, headless automation examples, slash commands for /init-style project setup, or editable agent workflow boilerplate.
---

# Agent Stack Init

## Workflow

Use `scripts/bootstrap_agent_config.py` to create an editable configuration stack in the target repository.

Default command:

```bash
python3 skills/agent-stack-init/scripts/bootstrap_agent_config.py --target .
```

After the skill is installed into Codex, natural requests such as "initialize this repo with the agent stack", "set up Claude/Codex project config", or "when I create a project, add the boilerplate" should trigger this skill.

Customize the generated root memory:

```bash
python3 skills/agent-stack-init/scripts/bootstrap_agent_config.py \
  --target /path/to/repo \
  --project-name citation-rag \
  --domain "Retrieval + answer-generation service"
```

Overwrite existing generated files only when the user explicitly wants a refresh:

```bash
python3 skills/agent-stack-init/scripts/bootstrap_agent_config.py --target . --force
```

## What It Creates

- `CLAUDE.md`: short root memory template with imperative rules and comments showing what to edit.
- `.claude/rules/*.md`: path-scoped rules for retrieval, answer generation, tests, and frontend work.
- `.claude/agents/*.md`: compact custom subagents for review, prompt auditing, eval running, and PR readiness.
- `.claude/skills/new-rag-eval/SKILL.md`: a local project skill for adding RAG/citation eval cases.
- `.claude/hooks/gate_git_push.sh`: pre-tool hook script that defers pushes to protected branches.
- `.claude/tools/bootstrap_agent_config.py`: local copy of the bootstrapper so the project can refresh itself.
- `.claude/commands/*.md`: Claude Code slash-command prompts for project initialization.
- `.claude/settings.example.jsonc` and `.claude/settings.example.json`: commented and machine-readable hook examples.
- `.claude/mcp.example.jsonc`: small commented five-server MCP template.
- `.github/workflows/claude-nightly-evals.example.yml`: commented headless/nightly automation example.
- `docs/agent-stack.md`: short guide for trimming and adapting the stack.

## After Running

Tell the user to edit the comments before relying on the setup. Emphasize these checks:

1. Keep `CLAUDE.md` short and behavioral.
2. Delete rule files for directories the project does not have.
3. Keep MCP servers to the few tools the project really needs.
4. Review hook scripts before enabling them in a real settings file.
5. Treat examples as starting points, not universal truth.

## Plugging In

- Codex: install this skill into `${CODEX_HOME:-$HOME/.codex}/skills/agent-stack-init`.
- Claude Code user commands: run `scripts/install_claude_commands.sh` from this skill source to install `/agent-stack-init` and `/new-agent-project`.
- Claude Code project commands: generated files under `.claude/commands/` can be invoked as project slash commands, commonly `/project:agent-stack-init` or `/project:new-agent-project`.
- Built-in `/init`: do not rely on overriding it. If the local Claude Code version supports a project `init` command, `.claude/commands/init.md` provides an init-style prompt; otherwise use `/agent-stack-init` or `/project:agent-stack-init`.

Read `references/config-stack.md` only when the user wants the rationale behind the layers or asks how to adapt the generated files.
