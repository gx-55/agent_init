#!/usr/bin/env bash
# Defer git pushes to protected branches. Review before enabling in CI.
set -euo pipefail

payload="$(cat)"
cmd="$(printf '%s' "$payload" | jq -r '.tool_input.command // empty')"

case "$cmd" in
  *"git push"*"origin main"*|*"git push"*" main"*|*"git push"*"origin master"*|*"git push"*" master"*)
    jq -nc '{
      "permissionDecision": "defer",
      "reason": "Push to a protected branch requires human approval."
    }'
    ;;
  *)
    jq -nc '{"permissionDecision": "allow"}'
    ;;
esac
