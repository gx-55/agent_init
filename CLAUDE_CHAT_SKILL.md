---
name: agent-stack-init
description: Generate a complete commented Claude Code and Codex agent configuration stack in chat. Use when the user asks to initialize a project, create agent boilerplate, set up CLAUDE.md, path-scoped rules, custom subagents, hooks, MCP examples, Claude Code commands, Codex skills, or packageable setup files from the Claude chat text box.
---

# Agent Stack Init

## Purpose

Help the user create an agent configuration stack from Claude chat. Claude chat
does not write directly to the user's local filesystem, so generate files as
copyable markdown blocks or, when file/artifact creation is available, create a
downloadable archive.

## Default Output

When the user asks to initialize a project, produce:

1. A short explanation of what will be generated.
2. A file tree.
3. One fenced code block per file, with the path immediately before each block.
4. A short "install locally" command block at the end.

Keep generated files commented so the user can edit them.

## Files To Generate

Generate this stack unless the user asks for a smaller one:

- `CLAUDE.md`: short root memory, under 200 lines, with comments explaining what to replace.
- `.claude/rules/retrieval.md`: path-scoped retrieval rules.
- `.claude/rules/answer.md`: answer-generation and citation rules.
- `.claude/rules/tests.md`: offline unit test and eval rules.
- `.claude/rules/frontend.md`: optional frontend rules; mark it safe to delete.
- `.claude/agents/retrieval-reviewer.md`: read-only retrieval reviewer.
- `.claude/agents/prompt-auditor.md`: read-only prompt reviewer.
- `.claude/agents/eval-runner.md`: eval runner subagent.
- `.claude/agents/pr-checklist.md`: PR readiness reviewer.
- `.claude/commands/agent-stack-init.md`: Claude Code project slash command.
- `.claude/commands/new-agent-project.md`: Claude Code project command for creating a new folder.
- `.claude/hooks/gate_git_push.sh`: protected branch push gate.
- `.claude/settings.example.jsonc`: commented settings example.
- `.claude/settings.example.json`: strict JSON version of settings.
- `.claude/mcp.example.jsonc`: small MCP server template.
- `.github/workflows/claude-nightly-evals.example.yml`: headless automation example.
- `docs/agent-stack.md`: short guide for editing the stack.

## Adaptation Rules

- Ask for the project name and one-line domain only if they are missing and the
  user did not provide enough context.
- Keep root memory concise and imperative.
- Prefer placeholders and comments over pretending to know the user's project.
- Tell the user to delete irrelevant rule files.
- Explain that Claude chat Skills generate text/artifacts; Claude Code commands
  are separate files under `.claude/commands/`.

## Optional Package Path

If the user asks for something installable from GitHub or another endpoint,
recommend this package command after publishing the repo:

```bash
pipx install "git+https://github.com/OWNER/REPO.git"
agent-stack-init install
```

Explain that `agent-stack-init install` installs persistent local Codex, Claude
Code, and Claude Desktop integrations, while `agent-stack-init init --target .`
initializes a specific project.
