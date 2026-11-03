"""OpenAI-compatible Chat Completions transport for tool-calling models."""
from __future__ import annotations

import json
import os
from urllib import request


class ChatBackend:
    def __init__(self, url: str, model: str, api_key_env: str = ""):
        if not url:
            raise ValueError("chat completions URL is required")
        if not model:
            raise ValueError("model is required")
        self.url = url
        self.model = model
        self.api_key_env = api_key_env

    def complete(self, messages: list[dict], tools: list[dict]) -> dict:
        payload = json.dumps({"model": self.model, "messages": messages, "tools": tools,
                              "stream": False}).encode("utf-8")
        headers = {"Content-Type": "application/json"}
        if self.api_key_env:
            token = os.environ.get(self.api_key_env)
            if not token:
                raise ValueError("missing API key environment variable: " + self.api_key_env)
            headers["Authorization"] = "Bearer " + token
        req = request.Request(self.url, data=payload, headers=headers)
        with request.urlopen(req, timeout=180) as response:
            result = json.load(response)
        return result["choices"][0]["message"]

    def tool_result(self, call: dict, content: dict) -> dict:
        rendered = json.dumps(content, ensure_ascii=False)
        return {"role": "tool", "tool_call_id": call["id"], "content": rendered}
