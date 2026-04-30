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

Recommended on macOS/Homebrew Python:

```bash
brew install pipx
pipx ensurepath
pipx install "git+https://github.com/gx-55/agent_init.git"
```

Then install local integrations:

```bash
agent-stack-init install
```

If your shell has not picked up the new PATH yet, either restart the terminal or
run:

```bash
~/.local/bin/agent-stack-init install
```

One-command source install:

```bash
export AGENT_STACK_INIT_REPO_URL="https://github.com/gx-55/agent_init.git"
curl -fsSL https://raw.githubusercontent.com/gx-55/agent_init/main/install.sh | bash
```

The installer uses `pipx` when available. If `pipx` is not installed, it creates
a private virtualenv under `~/.local/share/agent-stack-init/venv` and links the
CLI to `~/.local/bin/agent-stack-init`. It does not use `pip install --user`, so
it avoids PEP 668 / externally-managed Python errors.

Manual virtualenv fallback:

```bash
python3 -m venv ~/.local/share/agent-stack-init/venv
~/.local/share/agent-stack-init/venv/bin/python -m pip install \
  "git+https://github.com/gx-55/agent_init.git"
~/.local/share/agent-stack-init/venv/bin/agent-stack-init install
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

Claude Desktop does not expose a Claude Code-style current project directory to
MCP servers. The model must fill `target` with the actual project directory. If
you do not provide one, Claude should ask for it before using the tool.

After install, restart Claude Desktop and ask:

```text
Use agent-stack-init to initialize /Users/me/code/my-project.
```

Or:

```text
Use agent-stack-init to initialize my project. The project directory is /Users/me/code/my-project.
```

If Claude Desktop reports an MCP validation error, update and reinstall:

```bash
pipx upgrade agent-stack-init
agent-stack-init install-claude-desktop
```

If you used the installer fallback instead of `pipx`:

```bash
export AGENT_STACK_INIT_REPO_URL="https://github.com/gx-55/agent_init.git"
curl -fsSL https://raw.githubusercontent.com/gx-55/agent_init/main/install.sh | bash
```

## Claude Code

The Claude Code command line is still a first-class part of this package.

The repo does not keep `.claude/commands/` checked in anymore because those are
generated files. Instead, install them onto your machine with:

```bash
agent-stack-init install-claude-commands
```

or as part of the full install:

```bash
agent-stack-init install
```

That writes:

```text
~/.claude/commands/agent-stack-init.md
~/.claude/commands/new-agent-project.md
```

After restarting Claude Code, use:

```text
/agent-stack-init "Short project description"
/new-agent-project my-new-app "Short project description"
```

Generated projects also receive project-local command files under
`.claude/commands/`, so `/project:agent-stack-init` works inside initialized
repos when Claude Code supports project command namespaces.

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
