# Agent Stack Init

`agent-stack-init` is a small Python CLI package that installs and exposes a
project bootstrapper for Claude Desktop, Claude Code, Codex, and Claude chat.

It generates a commented agent configuration stack for a target project:

- `CLAUDE.md`
- `.claude/rules/*.md`
- `.claude/agents/*.md`
- `.claude/commands/*.md`
- `.claude/hooks/gate_git_push.sh`
- `.claude/settings.example.json(c)`
- `.claude/mcp.example.jsonc`
- `.github/workflows/claude-nightly-evals.example.yml`
- `docs/agent-stack.md`

## Install

From GitHub:

```bash
python3 -m pip install --user "git+https://github.com/gx-55/agent_init.git"
```

Then install local integrations:

```bash
agent-stack-init install
```

If your Python user bin is not on `PATH`, run the command by full path:

```bash
~/Library/Python/3.9/bin/agent-stack-init install
```

## What Install Does

`agent-stack-init install` writes local config for:

- Codex skill: `~/.codex/skills/agent-stack-init`
- Claude Code skill: `~/.claude/skills/agent-stack-init`
- Claude Code commands:
  - `~/.claude/commands/agent-stack-init.md`
  - `~/.claude/commands/new-agent-project.md`
- Claude Desktop MCP server:
  - macOS: `~/Library/Application Support/Claude/claude_desktop_config.json`

Restart Claude Desktop or Claude Code after installing.

## Use

Initialize the current project:

```bash
agent-stack-init init --target .
```

Initialize another project:

```bash
agent-stack-init init \
  --target /path/to/repo \
  --project-name my-project \
  --domain "Short project description"
```

Overwrite existing generated files:

```bash
agent-stack-init init --target . --force
```

## Claude Desktop

The installer adds an MCP server named `agent-stack-init`.

Available tools:

- `init_agent_stack`: scaffold the config stack into a local folder.
- `print_claude_chat_skill`: print the Claude chat Skill markdown.

After install, restart Claude Desktop and ask:

```text
Use agent-stack-init to initialize /path/to/my/project.
```

## Claude Code

The installer adds:

```text
/agent-stack-init
/new-agent-project
```

Use:

```text
/agent-stack-init "Short project description"
```

## Claude Chat Skill

Claude chat Skills are account/UI artifacts, not local config. This repo keeps
the chat Skill as a plain file:

```text
CLAUDE_CHAT_SKILL.md
```

Upload or paste that file into Claude chat's Skills UI if your plan supports
custom Skills. No zip is required.

## Commands

```bash
agent-stack-init install
agent-stack-init install-codex-skill
agent-stack-init install-claude-code-skill
agent-stack-init install-claude-commands
agent-stack-init install-claude-desktop
agent-stack-init init --target .
agent-stack-init print-chat-skill
```

## Repo Structure

```text
.
├── CLAUDE_CHAT_SKILL.md
├── LICENSE
├── README.md
├── install.sh
├── pyproject.toml
└── src/
    └── agent_stack_init/
        ├── __init__.py
        ├── bootstrap_agent_config.py
        ├── cli.py
        └── mcp_server.py
```
