# Agent Stack Setup

This repo contains editable boilerplate for a lean agent configuration stack.

## First Edits

1. Edit `CLAUDE.md` until every line changes agent behavior for `claude-initiate`.
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

To install global Claude Code user commands from the skill source repo:

```bash
skills/agent-stack-init/scripts/install_claude_commands.sh
```

This installs `/agent-stack-init` and `/new-agent-project`. Re-run that script with
`--with-init-alias` only if you intentionally want to add a user `/init` alias.

## Codex Skill Install

To make natural language requests trigger this bootstrap workflow in future Codex
sessions, install the `agent-stack-init` skill source into Codex's skills
directory. From the repo that contains the skill source, run:

```bash
skills/agent-stack-init/scripts/install_codex_skill.sh
```

## Operating Rule

The stack should reduce repeated explanation. If a file becomes a second wiki, split it
into path-scoped rules, a local skill, or a short subagent prompt.
