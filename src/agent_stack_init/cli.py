"""Command line interface for installing and running agent-stack-init."""

from __future__ import annotations

import argparse
import shutil
import stat
from pathlib import Path

from . import __version__
from . import bootstrap_agent_config


def chmod_executable(path: Path) -> None:
    mode = path.stat().st_mode
    path.chmod(mode | stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH)


def skill_text() -> str:
    return """---
name: agent-stack-init
description: Scaffold or install a commented Claude/Codex agent configuration stack for a software project. Use when setting up or refreshing project memory files, path-scoped rules, custom subagents, hooks, MCP/server examples, headless automation examples, slash commands for /init-style project setup, or editable agent workflow boilerplate.
---

# Agent Stack Init

Use the `agent-stack-init` CLI to create an editable configuration stack.

Default command:

```bash
agent-stack-init init --target .
```

Natural requests such as "initialize this repo with the agent stack", "set up Claude/Codex project config", or "when I create a project, add the boilerplate" should trigger this skill.

The CLI creates `CLAUDE.md`, `.claude/rules/`, `.claude/agents/`, `.claude/commands/`, hook examples, MCP examples, and headless automation examples.

After running, edit comments in `CLAUDE.md`, delete irrelevant rule files, and review hooks before enabling them.
"""


def openai_yaml() -> str:
    return """display_name: Agent Stack Init
short_description: Scaffold commented agent config boilerplate.
default_prompt: Set up an editable agent configuration stack for this project.
"""


def install_codex_skill(args: argparse.Namespace) -> int:
    codex_home = Path(args.codex_home).expanduser()
    target = codex_home / "skills" / "agent-stack-init"
    if target.exists():
        shutil.rmtree(target)
    (target / "agents").mkdir(parents=True, exist_ok=True)
    (target / "SKILL.md").write_text(skill_text(), encoding="utf-8")
    (target / "agents" / "openai.yaml").write_text(openai_yaml(), encoding="utf-8")
    print(f"Installed Codex skill to {target}")
    print("Restart Codex or start a new session so the skill metadata is loaded.")
    return 0


def claude_command_init(bootstrap: Path) -> str:
    return f"""---
description: Generate or refresh the commented Claude/Codex agent configuration stack for the current project.
argument-hint: [optional project description]
---

Initialize this repository with the reusable agent configuration stack.

User arguments:
$ARGUMENTS

Run:

```bash
agent-stack-init init --target . --domain "$ARGUMENTS"
```

Do not use `--force` unless the user explicitly asked to overwrite existing generated files. Summarize created/skipped files and tell the user to edit comments in `CLAUDE.md`, `.claude/rules/`, and `.claude/settings.example.jsonc`.
"""


def claude_command_new_project() -> str:
    return """---
description: Create a new project folder and immediately add the commented Claude/Codex agent configuration stack.
argument-hint: <project-folder> [project description]
---

Create a new project folder and install the reusable agent configuration stack.

User arguments:
$ARGUMENTS

Steps:
1. Parse the first argument as the target folder.
2. Treat the rest as the project description.
3. Create the folder if needed.
4. Run `agent-stack-init init --target "<target-folder>" --project-name "<folder-name>" --domain "<description>"`.
5. Do not overwrite existing files unless the user explicitly asks.
6. Summarize the new project path and the next files to edit.
"""


def claude_command_alias() -> str:
    return """---
description: Init-style alias for the agent configuration stack. Use only if your Claude Code setup does not reserve /init.
argument-hint: [optional project description]
---

Run the same workflow as `/agent-stack-init`. If this conflicts with a built-in command, use `/agent-stack-init` instead.

User arguments:
$ARGUMENTS

Run `agent-stack-init init --target . --domain "$ARGUMENTS"`.
"""


def install_claude_commands(args: argparse.Namespace) -> int:
    claude_home = Path(args.claude_home).expanduser()
    command_dir = claude_home / "commands"
    command_dir.mkdir(parents=True, exist_ok=True)
    bootstrap = Path(bootstrap_agent_config.__file__).resolve()

    (command_dir / "agent-stack-init.md").write_text(
        claude_command_init(bootstrap), encoding="utf-8"
    )
    (command_dir / "new-agent-project.md").write_text(
        claude_command_new_project(), encoding="utf-8"
    )
    if args.with_init_alias:
        (command_dir / "init.md").write_text(claude_command_alias(), encoding="utf-8")

    print(f"Installed Claude Code commands to {command_dir}")
    print("Commands: /agent-stack-init and /new-agent-project")
    if args.with_init_alias:
        print("Also installed: /init alias")
    else:
        print("Skipped /init alias to avoid shadowing Claude Code built-ins.")
    return 0


def init_project(args: argparse.Namespace) -> int:
    forwarded = ["--target", args.target]
    if args.project_name:
        forwarded.extend(["--project-name", args.project_name])
    if args.domain:
        forwarded.extend(["--domain", args.domain])
    if args.force:
        forwarded.append("--force")
    return bootstrap_agent_config.main(forwarded)


def install_all(args: argparse.Namespace) -> int:
    install_codex_skill(args)
    install_claude_commands(args)
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="agent-stack-init")
    parser.add_argument("--version", action="version", version=f"%(prog)s {__version__}")
    subparsers = parser.add_subparsers(dest="command", required=True)

    init = subparsers.add_parser("init", help="Scaffold a target project.")
    init.add_argument("--target", default=".", help="Repository root to scaffold into.")
    init.add_argument("--project-name", default=None, help="Project name for CLAUDE.md.")
    init.add_argument(
        "--domain",
        default=None,
        help="One-line domain description for CLAUDE.md.",
    )
    init.add_argument("--force", action="store_true", help="Overwrite existing files.")
    init.set_defaults(func=init_project)

    codex = subparsers.add_parser("install-codex-skill", help="Install Codex skill.")
    codex.add_argument("--codex-home", default="~/.codex")
    codex.set_defaults(func=install_codex_skill)

    claude = subparsers.add_parser(
        "install-claude-commands", help="Install Claude Code user slash commands."
    )
    claude.add_argument("--claude-home", default="~/.claude")
    claude.add_argument("--with-init-alias", action="store_true")
    claude.set_defaults(func=install_claude_commands)

    all_cmd = subparsers.add_parser("install", help="Install Codex skill and Claude commands.")
    all_cmd.add_argument("--codex-home", default="~/.codex")
    all_cmd.add_argument("--claude-home", default="~/.claude")
    all_cmd.add_argument("--with-init-alias", action="store_true")
    all_cmd.set_defaults(func=install_all)

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
