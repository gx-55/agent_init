---
description: Init-style alias for the agent configuration stack. Use /project:agent-stack-init if /init is reserved.
argument-hint: [optional project description]
allowed-tools: Bash(python3 .claude/tools/bootstrap_agent_config.py:*), Read, Grep, Glob, Edit, Write
---

Run the same workflow as `agent-stack-init`.

If this command name conflicts with a built-in `/init`, tell the user to invoke:

`/project:agent-stack-init`

Then initialize the repository with `.claude/tools/bootstrap_agent_config.py --target .`, using `$ARGUMENTS` as the optional project description.
