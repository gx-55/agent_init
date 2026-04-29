# Agent Stack Init

`agent-stack-init` is a reusable bootstrap kit for Claude Code and Codex projects.
It scaffolds a commented agent configuration stack so new repos start with memory,
rules, subagents, hooks, slash commands, MCP examples, and headless automation
examples already in place.

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

## Install From Another Endpoint

Best option after pushing this repo to GitHub or another git host:

```bash
pipx install "git+https://github.com/YOUR_ORG/agent-stack-init.git"
agent-stack-init install
```

Without `pipx`:

```bash
python3 -m pip install --user "git+https://github.com/YOUR_ORG/agent-stack-init.git"
agent-stack-init install
```

Run without permanently installing the CLI:

```bash
uvx --from "git+https://github.com/YOUR_ORG/agent-stack-init.git" agent-stack-init install
```

Clone and install:

```bash
git clone https://github.com/YOUR_ORG/agent-stack-init.git
cd agent-stack-init
./install.sh
```

Remote install script pattern:

```bash
export AGENT_STACK_INIT_REPO_URL="https://github.com/YOUR_ORG/agent-stack-init.git"
curl -fsSL https://raw.githubusercontent.com/YOUR_ORG/agent-stack-init/main/install.sh | bash
```

Replace `YOUR_ORG/agent-stack-init` with the endpoint where you publish this repo.

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

After package install, install both Codex and Claude Code integrations:

```bash
agent-stack-init install
```

Install or refresh the Codex skill:

```bash
agent-stack-init install-codex-skill
```

Install or refresh Claude Code user commands:

```bash
agent-stack-init install-claude-commands
```

The installer intentionally skips a global `/init` alias because Claude Code may
reserve `/init`. To add that alias anyway:

```bash
agent-stack-init install-claude-commands --with-init-alias
```

The original shell installers are still available under `skills/agent-stack-init/scripts/`
for source-checkout workflows.

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
