"""Minimal stdio MCP server for Claude Desktop."""

from __future__ import annotations

import contextlib
import io
import json
import sys
import traceback
from typing import Any

from . import __version__
from . import bootstrap_agent_config
from .cli import print_chat_skill


def send(message: dict[str, Any]) -> None:
    sys.stdout.write(json.dumps(message, separators=(",", ":")) + "\n")
    sys.stdout.flush()


def log(message: str) -> None:
    print(message, file=sys.stderr, flush=True)


def valid_id(value: Any) -> bool:
    return isinstance(value, (str, int, float)) and not isinstance(value, bool)


def text_result(text: str, is_error: bool = False) -> dict[str, Any]:
    return {"content": [{"type": "text", "text": text}], "isError": is_error}


def capture_stdout(fn: Any, *args: Any, **kwargs: Any) -> tuple[int, str]:
    buffer = io.StringIO()
    with contextlib.redirect_stdout(buffer):
        code = fn(*args, **kwargs)
    return int(code or 0), buffer.getvalue()


def tool_schemas() -> list[dict[str, Any]]:
    return [
        {
            "name": "init_agent_stack",
            "description": "Scaffold the commented Claude/Codex agent configuration stack into a local project directory.",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "target": {
                        "type": "string",
                        "description": "Local project directory to initialize. Defaults to the current directory.",
                    },
                    "project_name": {
                        "type": "string",
                        "description": "Project name to write into CLAUDE.md.",
                    },
                    "domain": {
                        "type": "string",
                        "description": "One-line project description for CLAUDE.md.",
                    },
                    "force": {
                        "type": "boolean",
                        "description": "Overwrite existing generated files.",
                        "default": False,
                    },
                },
            },
        },
        {
            "name": "print_claude_chat_skill",
            "description": "Print the Claude chat Skill markdown file for agent-stack-init.",
            "inputSchema": {"type": "object", "properties": {}},
        },
    ]


def call_tool(name: str, arguments: dict[str, Any]) -> dict[str, Any]:
    if name == "init_agent_stack":
        forwarded = ["--target", str(arguments.get("target") or ".")]
        if arguments.get("project_name"):
            forwarded.extend(["--project-name", str(arguments["project_name"])])
        if arguments.get("domain"):
            forwarded.extend(["--domain", str(arguments["domain"])])
        if arguments.get("force"):
            forwarded.append("--force")
        code, output = capture_stdout(bootstrap_agent_config.main, forwarded)
        return text_result(output.strip() or f"agent-stack-init exited with {code}", code != 0)

    if name == "print_claude_chat_skill":
        code, output = capture_stdout(print_chat_skill, object())
        return text_result(output.strip() or f"print-chat-skill exited with {code}", code != 0)

    return text_result(f"Unknown tool: {name}", True)


def handle(message: dict[str, Any]) -> None:
    method = message.get("method")
    msg_id = message.get("id")
    has_valid_id = valid_id(msg_id)

    if method == "initialize":
        if not has_valid_id:
            log("Ignoring initialize request without a valid JSON-RPC id.")
            return
        send(
            {
                "jsonrpc": "2.0",
                "id": msg_id,
                "result": {
                    "protocolVersion": "2024-11-05",
                    "capabilities": {"tools": {}},
                    "serverInfo": {"name": "agent-stack-init", "version": __version__},
                },
            }
        )
        return

    if method == "tools/list":
        if not has_valid_id:
            log("Ignoring tools/list request without a valid JSON-RPC id.")
            return
        send({"jsonrpc": "2.0", "id": msg_id, "result": {"tools": tool_schemas()}})
        return

    if method == "tools/call":
        if not has_valid_id:
            log("Ignoring tools/call request without a valid JSON-RPC id.")
            return
        params = message.get("params") or {}
        result = call_tool(str(params.get("name") or ""), params.get("arguments") or {})
        send({"jsonrpc": "2.0", "id": msg_id, "result": result})
        return

    if method == "ping":
        if not has_valid_id:
            return
        send({"jsonrpc": "2.0", "id": msg_id, "result": {}})
        return

    if has_valid_id:
        log(f"Ignoring unsupported MCP method: {method}")
        send({"jsonrpc": "2.0", "id": msg_id, "result": {}})


def main() -> int:
    for line in sys.stdin:
        if not line.strip():
            continue
        try:
            decoded = json.loads(line)
            if isinstance(decoded, list):
                for message in decoded:
                    if isinstance(message, dict):
                        handle(message)
                    else:
                        log(f"Ignoring non-object MCP batch item: {message!r}")
            elif isinstance(decoded, dict):
                handle(decoded)
            else:
                log(f"Ignoring non-object MCP message: {decoded!r}")
        except Exception as exc:  # pragma: no cover - defensive server boundary
            log(f"agent-stack-init MCP server ignored invalid input: {exc}")
            log(traceback.format_exc())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
