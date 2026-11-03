#!/usr/bin/env python3
"""Read-only command knowledge and playback tools over MCP stdio."""
from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import cfg
import search
import playback_query


TOOL = {
    "name": "search_command_knowledge",
    "description": (
        "Search the user's documented command knowledge. Use for questions about "
        "commands, CLI workflows, or prior solutions. Returns exact commands, "
        "explanations, and source file locations. Read-only; no model or network call."
    ),
    "inputSchema": {
        "type": "object",
        "properties": {
            "query": {"type": "string", "description": "Keywords such as 'git staged diff'"},
            "topic": {"type": "string", "description": "Optional technology filename, such as git"},
            "limit": {"type": "integer", "minimum": 1, "maximum": 20, "default": 5},
        },
        "required": ["query"],
        "additionalProperties": False,
    },
    "annotations": {"readOnlyHint": True, "destructiveHint": False, "idempotentHint": True},
}

PLAYBACK_LIST = {
    "name": "list_resolution_playbacks",
    "description": "List locally recorded issue-resolution playbacks with their IDs and status.",
    "inputSchema": {"type": "object", "properties": {
        "limit": {"type": "integer", "minimum": 1, "maximum": 100, "default": 20}},
        "additionalProperties": False},
    "annotations": {"readOnlyHint": True, "destructiveHint": False},
}
PLAYBACK_READ = {
    "name": "read_resolution_playback",
    "description": ("Read exact ordered playback steps: original tool payloads, command output, "
                    "agent observations and decisions. Use next_start to read every step. "
                    "Do not invent missing output or private reasoning."),
    "inputSchema": {"type": "object", "properties": {
        "id": {"type": "string", "description": "Playback ID from list_resolution_playbacks"},
        "start": {"type": "integer", "minimum": 1, "default": 1},
        "limit": {"type": "integer", "minimum": 1, "maximum": 20, "default": 10}},
        "required": ["id"], "additionalProperties": False},
    "annotations": {"readOnlyHint": True, "destructiveHint": False},
}
TOOLS = [TOOL, PLAYBACK_LIST, PLAYBACK_READ]


def call_tool(name: str, args: dict) -> dict:
    if name == TOOL["name"]:
        return lookup(**args)
    if name == PLAYBACK_LIST["name"]:
        return playback_query.recordings(**args)
    if name == PLAYBACK_READ["name"]:
        options = dict(args)
        ident = options.pop("id")
        return playback_query.timeline(ident, **options)
    raise ValueError("Unknown tool")


def lookup(query: str, topic: str = "", limit: int = 5) -> dict:
    if not isinstance(query, str) or not query.strip():
        raise ValueError("query must be a nonempty string")
    if not isinstance(topic, str):
        raise ValueError("topic must be a string")
    if type(limit) is not int or not 1 <= limit <= 20:
        raise ValueError("limit must be an integer from 1 to 20")
    matches = search.search(cfg.kb_dir(), query, topic)
    return {
        "query": query,
        "total": len(matches),
        "matches": [{
            "heading": item["heading"],
            "commands": item["commands"],
            "entry": item["body"],
            "source": str(item["path"]),
            "line": item["line"],
        } for item in matches[:limit]],
    }


def dispatch(message: dict) -> dict | None:
    if "id" not in message:
        return None
    method = message.get("method")
    params = message.get("params") or {}
    if method == "initialize":
        version = params.get("protocolVersion", "2025-06-18")
        result = {"protocolVersion": version, "capabilities": {"tools": {}},
                  "serverInfo": {"name": "session-skills-search", "version": "1.0.0"}}
    elif method == "ping":
        result = {}
    elif method == "tools/list":
        result = {"tools": TOOLS}
    elif method == "tools/call":
        if params.get("name") not in {item["name"] for item in TOOLS}:
            return {"jsonrpc": "2.0", "id": message["id"], "error":
                    {"code": -32602, "message": "Unknown tool"}}
        try:
            args = params.get("arguments") or {}
            found = call_tool(params["name"], args)
            result = {"content": [{"type": "text", "text": json.dumps(found, ensure_ascii=False)}],
                      "structuredContent": found}
        except (TypeError, ValueError) as exc:
            result = {"content": [{"type": "text", "text": str(exc)}], "isError": True}
    else:
        return {"jsonrpc": "2.0", "id": message["id"], "error":
                {"code": -32601, "message": "Method not found"}}
    return {"jsonrpc": "2.0", "id": message["id"], "result": result}


def main() -> None:
    for line in sys.stdin:
        try:
            message = json.loads(line)
            response = dispatch(message)
        except (json.JSONDecodeError, TypeError, AttributeError):
            response = {"jsonrpc": "2.0", "id": None, "error":
                        {"code": -32700, "message": "Invalid request"}}
        if response is not None:
            sys.stdout.write(json.dumps(response, ensure_ascii=False) + "\n")
            sys.stdout.flush()


if __name__ == "__main__":
    main()
