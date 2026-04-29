# Agent Configuration Stack Reference

Use this reference when adapting the generated boilerplate.

## Layer Priorities

1. Root memory should be a hot cache, not a wiki. Keep it short, imperative, and specific enough to change behavior.
2. Path-scoped rules keep specialized conventions out of ambient context until matching files are touched.
3. Custom subagents are useful for repeated review or execution roles with narrow scope.
4. Skills package stable workflows that deserve their own instructions and resources.
5. Hooks add deterministic checks around tool use. Keep them simple, auditable, and boring.
6. MCP/server configs should be small. Every extra tool schema has context cost.
7. Headless automation should use narrow tool allowlists and deferred permission gates for risky actions.

## Invocation Layer

- Codex discovers skills from its configured skills directory. Install reusable skills there when you want natural language triggers.
- Claude Code project slash commands usually live under `.claude/commands/`. Prefer a clearly named command such as `agent-stack-init` because `/init` can be a built-in command in many setups.
- Keep command files as prompts that run local tools, not huge manuals. The generated command should call `.claude/tools/bootstrap_agent_config.py` and then ask the agent to trim the generated files to the real repo.

## Editing Heuristics

- Replace descriptive advice with literal rules.
- Prefer project-specific file paths over general style statements.
- Delete unused boilerplate quickly; unused rules become stale context.
- Keep examples commented until the team has validated them.
- Put generated/example settings in `*.example.*` files first, then copy into live settings when ready.
