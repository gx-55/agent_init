#!/usr/bin/env bash
# Install Claude Code user slash commands that call this bootstrapper.
set -euo pipefail

with_init_alias=false
if [[ "${1:-}" == "--with-init-alias" ]]; then
  with_init_alias=true
fi

script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
bootstrap_script="$script_dir/bootstrap_agent_config.py"
claude_home="${CLAUDE_HOME:-$HOME/.claude}"
command_dir="$claude_home/commands"

mkdir -p "$command_dir"

cat > "$command_dir/agent-stack-init.md" <<EOF
---
description: Generate or refresh the commented Claude/Codex agent configuration stack for the current project.
argument-hint: [optional project description]
allowed-tools: Bash(python3 $bootstrap_script:*), Read, Grep, Glob, Edit, Write
---

Initialize this repository with the reusable agent configuration stack.

User arguments:
\$ARGUMENTS

Steps:
1. Infer the project name from the current folder unless the user supplied one.
2. Use the user arguments as the project domain description when present.
3. Run:

\`\`\`bash
python3 $bootstrap_script --target . --project-name "<inferred-name>" --domain "<description>"
\`\`\`

4. Do not add \`--force\` unless the user explicitly asked to overwrite existing generated files.
5. Summarize the created/skipped files and tell the user to edit comments in \`CLAUDE.md\`, \`.claude/rules/\`, and \`.claude/settings.example.jsonc\`.
EOF

cat > "$command_dir/new-agent-project.md" <<EOF
---
description: Create a new project folder and immediately add the commented Claude/Codex agent configuration stack.
argument-hint: <project-folder> [project description]
allowed-tools: Bash(mkdir:*), Bash(python3 $bootstrap_script:*), Read, Grep, Glob, Edit, Write
---

Create a new project folder and install the reusable agent configuration stack.

User arguments:
\$ARGUMENTS

Steps:
1. Parse the first argument as the target folder.
2. Treat the rest as the project description.
3. Create the folder if needed.
4. Run:

\`\`\`bash
python3 $bootstrap_script --target "<target-folder>" --project-name "<folder-name>" --domain "<description>"
\`\`\`

5. Do not overwrite existing files unless the user explicitly asks.
6. Summarize the new project path and the next files to edit.
EOF

if [[ "$with_init_alias" == "true" ]]; then
  cat > "$command_dir/init.md" <<EOF
---
description: Init-style alias for the agent configuration stack. Use only if your Claude Code setup does not reserve /init.
argument-hint: [optional project description]
allowed-tools: Bash(python3 $bootstrap_script:*), Read, Grep, Glob, Edit, Write
---

Run the same workflow as \`/agent-stack-init\`. If this conflicts with a built-in command, use \`/agent-stack-init\` instead.

User arguments:
\$ARGUMENTS

Run:

\`\`\`bash
python3 $bootstrap_script --target . --project-name "<inferred-name>" --domain "<description>"
\`\`\`
EOF
fi

printf 'Installed Claude Code commands to %s\n' "$command_dir"
printf 'Commands: /agent-stack-init and /new-agent-project\n'
if [[ "$with_init_alias" == "true" ]]; then
  printf 'Also installed: /init alias\n'
else
  printf 'Skipped /init alias to avoid shadowing Claude Code built-ins. Re-run with --with-init-alias if you want it.\n'
fi
