# Agent Stack Init

`agent-stack-init` is a reusable bootstrap kit for Claude Code and Codex projects.
It scaffolds a commented agent configuration stack so new repos start with memory,
rules, subagents, hooks, slash commands, MCP examples, and headless automation
examples already in place.

It supports three surfaces:

- Claude chat Skill: generates the boilerplate as text/artifacts in the chat box.
- Claude Code commands: runs from Claude Code with `/agent-stack-init`.
- Claude Code Skill: installs into local Claude Code skill config.
- Claude Desktop MCP: exposes `agent-stack-init` as local Desktop tools.
- Codex skill/CLI: installs and scaffolds from a terminal or Codex session.

## What Was Done

- Created the reusable Codex skill at `skills/agent-stack-init/`.
- Added a deterministic bootstrap script at
  `skills/agent-stack-init/scripts/bootstrap_agent_config.py`.
- Generated this repo's local agent stack under `.claude/`.
- Added Claude Code slash commands for `/agent-stack-init` and
  `/new-agent-project`.
- Installed the renamed Codex skill globally at
  `~/.codex/skills/agent-stack-init`.
- Installed the Claude Code user commands globally at `~/.claude/commands`.
- Removed the old `agent-config-bootstrap` name and stale `/init-agent-stack`
  command.

## Quick Use

From Claude Code, run:

```text
/agent-stack-init "Short description of this project"
```

To create a new folder and initialize it:

```text
/new-agent-project my-new-app "Short description of the new project"
```

From Codex, start a new session and ask naturally:

```text
Initialize this repo with the agent stack.
```

From Claude chat, use the chat Skill and ask:

```text
Generate an agent stack for a TypeScript retrieval service.
```

## Install From Another Endpoint

Best option after pushing this repo to GitHub or another git host:

```bash
pipx install "git+https://github.com/gx-55/agent_init.git"
agent-stack-init install
```

Without `pipx`:

```bash
python3 -m pip install --user "git+https://github.com/gx-55/agent_init.git"
agent-stack-init install
```

Run without permanently installing the CLI:

```bash
uvx --from "git+https://github.com/gx-55/agent_init.git" agent-stack-init install
```

Clone and install:

```bash
git clone https://github.com/gx-55/agent_init.git
cd agent_init
./install.sh
```

Remote install script pattern:

```bash
export AGENT_STACK_INIT_REPO_URL="https://github.com/gx-55/agent_init.git"
curl -fsSL https://raw.githubusercontent.com/gx-55/agent_init/main/install.sh | bash
```

## Manual Script Use

After package install, scaffold the current repo:

```bash
agent-stack-init init --target .
```

Scaffold another repo:

```bash
agent-stack-init init \
  --target /path/to/repo \
  --project-name my-project \
  --domain "Short project description"
```

Overwrite existing generated files only when you mean it:

```bash
agent-stack-init init --target . --force
```

Source-checkout fallback:

```bash
python3 skills/agent-stack-init/scripts/bootstrap_agent_config.py --target .
```

## Install Commands

After package install, install Codex and Claude Code local integrations:

```bash
agent-stack-init install
```

This writes local filesystem config:

- `~/.codex/skills/agent-stack-init`
- `~/.claude/skills/agent-stack-init`
- `~/.claude/commands/agent-stack-init.md`
- `~/.claude/commands/new-agent-project.md`
- `~/Library/Application Support/Claude/claude_desktop_config.json` on macOS

The Claude Desktop config adds an MCP server named `agent-stack-init`. Restart
Claude Desktop after installing.

Install or refresh the Codex skill:

```bash
agent-stack-init install-codex-skill
```

Install or refresh the Claude Code skill:

```bash
agent-stack-init install-claude-code-skill
```

Install or refresh Claude Code user commands:

```bash
agent-stack-init install-claude-commands
```

Install or refresh the Claude Desktop MCP server only:

```bash
agent-stack-init install-claude-desktop
```

Use a custom Desktop config path:

```bash
agent-stack-init install-claude-desktop --config /path/to/claude_desktop_config.json
```

The installer intentionally skips a global `/init` alias because Claude Code may
reserve `/init`. To add that alias anyway:

```bash
agent-stack-init install-claude-commands --with-init-alias
```

The original shell installers are still available under `skills/agent-stack-init/scripts/`
for source-checkout workflows.

## Claude Chat Skill

Claude chat Skills are different from Claude Code slash commands. The chat Skill
does not run commands on your machine; it teaches Claude chat how to generate the
same boilerplate as copyable text or downloadable artifacts.

Important: Claude.ai chat Skills live in your Claude account, not in local
`~/.claude` config. Local installers cannot register a custom Skill in the Claude
web UI. Build the zip, then upload and enable it in Claude chat's Skills UI.

Build the uploadable Skill zip:

```bash
agent-stack-init build-chat-skill
```

Default output:

```text
dist/agent-stack-init-claude-chat-skill.zip
```

Source version:

```text
claude-chat-skill/agent-stack-init/SKILL.md
```

Upload the zip wherever your Claude chat plan exposes custom Skills. Keep
`/agent-stack-init` for Claude Code; use the chat Skill when you want Claude to
generate the files in the text box.

## Claude Desktop MCP Tools

Claude Desktop can use local tools through MCP. `agent-stack-init install`
updates Claude Desktop's config with this server:

```json
{
  "mcpServers": {
    "agent-stack-init": {
      "command": "/path/to/python",
      "args": ["-m", "agent_stack_init.mcp_server"],
      "env": {}
    }
  }
}
```

Available Desktop tools:

- `init_agent_stack`: scaffold the config stack into a local project folder.
- `build_claude_chat_skill`: build the uploadable Claude chat Skill zip.

After installing or changing the config, quit and restart Claude Desktop.

## Generated Stack

The bootstrapper creates:

- `CLAUDE.md`: short root memory with comments showing what to customize.
- `.claude/rules/*.md`: path-scoped rules for retrieval, answers, tests, and UI.
- `.claude/agents/*.md`: custom subagents for review, prompt audit, evals, and PR readiness.
- `.claude/commands/*.md`: project slash commands.
- `.claude/tools/bootstrap_agent_config.py`: local self-refresh copy of the bootstrapper.
- `.claude/hooks/gate_git_push.sh`: protected-branch push gate example.
- `.claude/settings.example.jsonc`: commented hook configuration.
- `.claude/mcp.example.jsonc`: small MCP server template.
- `.github/workflows/claude-nightly-evals.example.yml`: headless automation example.
- `docs/agent-stack.md`: short guide for adapting the stack.

## After Init

Edit `CLAUDE.md` first. Keep it short and behavioral.

Delete rule files for directories your project does not have. Review hooks before
enabling them in live settings. Keep MCP servers limited to tools you actually
use.
