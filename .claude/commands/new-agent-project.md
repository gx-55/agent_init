---
description: Create a new project folder and immediately add the commented Claude/Codex agent configuration stack.
argument-hint: <project-folder> [project description]
allowed-tools: Bash(mkdir:*), Bash(python3:*), Read, Grep, Glob, Edit, Write
---

Create a new project and install the agent configuration stack.

User arguments:
$ARGUMENTS

Steps:
1. Parse the first argument as the target project folder.
2. Treat the rest of the arguments as the project description.
3. Create the target folder if it does not exist.
4. Run this repository's bootstrapper into that folder. If the new folder already has `.claude/tools/bootstrap_agent_config.py`, prefer that local copy.
5. Do not overwrite existing files unless the user explicitly asks.
6. Summarize the created folder and the generated setup files.
