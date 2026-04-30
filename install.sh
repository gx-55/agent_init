#!/usr/bin/env bash
# Install agent-stack-init from a git checkout, source archive, or configured git endpoint.
set -euo pipefail

script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
repo_dir="$script_dir"

if [[ ! -f "$repo_dir/pyproject.toml" ]]; then
  if [[ -z "${AGENT_STACK_INIT_REPO_URL:-}" ]]; then
    printf 'This script is not running inside a source checkout.\n' >&2
    printf 'Set AGENT_STACK_INIT_REPO_URL to a git endpoint, then run again.\n' >&2
    printf 'Example: AGENT_STACK_INIT_REPO_URL=https://github.com/you/agent-stack-init.git bash install.sh\n' >&2
    exit 1
  fi

  repo_dir="$(mktemp -d)"
  git clone --depth 1 "$AGENT_STACK_INIT_REPO_URL" "$repo_dir"
fi

if command -v pipx >/dev/null 2>&1; then
  pipx install --force "$repo_dir"
else
  install_home="${AGENT_STACK_INIT_HOME:-$HOME/.local/share/agent-stack-init}"
  venv_dir="$install_home/venv"
  bin_dir="$HOME/.local/bin"

  printf 'pipx not found. Installing into private virtualenv: %s\n' "$venv_dir"
  python3 -m venv "$venv_dir"
  "$venv_dir/bin/python" -m pip install --upgrade pip
  "$venv_dir/bin/python" -m pip install --upgrade "$repo_dir"
  mkdir -p "$bin_dir"
  ln -sf "$venv_dir/bin/agent-stack-init" "$bin_dir/agent-stack-init"
  printf 'Linked CLI to %s/agent-stack-init\n' "$bin_dir"
fi

if command -v agent-stack-init >/dev/null 2>&1; then
  agent-stack-init install
elif [[ -x "$HOME/.local/bin/agent-stack-init" ]]; then
  "$HOME/.local/bin/agent-stack-init" install
elif [[ -x "${AGENT_STACK_INIT_HOME:-$HOME/.local/share/agent-stack-init}/venv/bin/agent-stack-init" ]]; then
  "${AGENT_STACK_INIT_HOME:-$HOME/.local/share/agent-stack-init}/venv/bin/agent-stack-init" install
else
  printf 'agent-stack-init installed, but the CLI was not found on PATH.\n' >&2
  printf 'Try: ~/.local/bin/agent-stack-init install\n' >&2
  exit 1
fi
