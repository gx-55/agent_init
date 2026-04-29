#!/usr/bin/env bash
# Install this skill where Codex can auto-discover it.
set -euo pipefail

source_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
codex_home="${CODEX_HOME:-$HOME/.codex}"
target_dir="$codex_home/skills/agent-stack-init"

mkdir -p "$(dirname "$target_dir")"
rm -rf "$target_dir"
cp -R "$source_dir" "$target_dir"

printf 'Installed agent-stack-init skill to %s\n' "$target_dir"
printf 'Restart Codex or start a new session so the skill metadata is loaded.\n'
