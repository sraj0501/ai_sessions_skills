#!/usr/bin/env python3
"""Read-only OpenAPI tool server for HTTP-based harnesses such as Open WebUI."""
from __future__ import annotations

import argparse
import hmac
import json
import sys
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import parse_qs, unquote, urlsplit

sys.path.insert(0, str(Path(__file__).resolve().parent))
from search_mcp import call_tool
import cfg


def specification() -> dict:
    parameters = lambda name, where="query", required=False, kind="string": {
        "name": name, "in": where, "required": required,
        "schema": {"type": kind}}
    response = {"200": {"description": "Exact local evidence as JSON",
                        "content": {"application/json": {"schema": {"type": "object"}}}}}
    return {"openapi": "3.0.3", "info": {"title": "Session Skills read-only tools",
                                      "version": "1.0.0"},
            "paths": {
                "/search": {"get": {"operationId": "search_command_knowledge",
                    "summary": "Search documented commands, explanations, and source locations",
                    "parameters": [parameters("query", required=True), parameters("topic"),
                                   parameters("limit", kind="integer")], "responses": response}},
                "/playbacks": {"get": {"operationId": "list_resolution_playbacks",
                    "summary": "List local issue-resolution recordings",
                    "parameters": [parameters("limit", kind="integer")], "responses": response}},
                "/playbacks/{id}/steps": {"get": {"operationId": "read_resolution_playback",
                    "summary": "Read exact ordered commands, outputs, observations, and decisions",
                    "parameters": [parameters("id", "path", True),
                                   parameters("start", kind="integer"),
                                   parameters("limit", kind="integer")], "responses": response}},
            }}


class Handler(BaseHTTPRequestHandler):
    def do_GET(self) -> None:
        token = cfg.env("AI_SKILLS_SEARCH_TOKEN")
        if token and not hmac.compare_digest(self.headers.get("Authorization", ""),
                                             "Bearer " + token):
            self.send_json({"error": "unauthorized"}, 401)
            return
        parsed = urlsplit(self.path)
        args = {key: values[-1] for key, values in parse_qs(parsed.query).items()}
        try:
            if parsed.path == "/openapi.json":
                result = specification()
            elif parsed.path == "/search":
                for key in ("limit",):
                    if key in args:
                        args[key] = int(args[key])
                result = call_tool("search_command_knowledge", args)
            elif parsed.path == "/playbacks":
                if "limit" in args:
                    args["limit"] = int(args["limit"])
                result = call_tool("list_resolution_playbacks", args)
            elif parsed.path.startswith("/playbacks/") and parsed.path.endswith("/steps"):
                ident = unquote(parsed.path[len("/playbacks/"):-len("/steps")])
                args["id"] = ident
                for key in ("start", "limit"):
                    if key in args:
                        args[key] = int(args[key])
                result = call_tool("read_resolution_playback", args)
            else:
                self.send_json({"error": "not found"}, 404)
                return
        except (TypeError, ValueError) as exc:
            self.send_json({"error": str(exc)}, 400)
            return
        self.send_json(result)

    def send_json(self, value: dict, status: int = 200) -> None:
        body = json.dumps(value, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, fmt: str, *args) -> None:
        # Query text and playback IDs can be sensitive; do not log HTTP paths.
        pass


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=8766)
    args = parser.parse_args()
    if args.host not in ("127.0.0.1", "localhost") and not cfg.env(
            "AI_SKILLS_SEARCH_TOKEN"):
        parser.error("non-loopback binding requires AI_SKILLS_SEARCH_TOKEN")
    server = ThreadingHTTPServer((args.host, args.port), Handler)
    print("Read-only tools at http://%s:%s/openapi.json" % server.server_address,
          file=sys.stderr)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()


if __name__ == "__main__":
    main()
