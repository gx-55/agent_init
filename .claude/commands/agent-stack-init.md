---
description: Generate or refresh the commented Claude/Codex agent configuration stack for this project.
argument-hint: [optional project description]
---

Initialize this repository with the local agent configuration stack.

User arguments:
$ARGUMENTS

Steps:
1. Infer the project name from the repository folder unless the user supplied one.
2. Use the user arguments as the project domain description when present.
3. Run `.claude/tools/bootstrap_agent_config.py --target .` with `--project-name` and `--domain`.
4. Do not use `--force` unless the user explicitly asked to refresh or overwrite existing generated files.
5. After generation, inspect `CLAUDE.md`, `.claude/rules/`, and `docs/agent-stack.md`.
6. Summarize which files were created or skipped and list the first comments the user should edit.
