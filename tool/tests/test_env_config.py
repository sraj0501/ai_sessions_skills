"""Private .env settings and explicit override precedence."""
from __future__ import annotations

import json
import os
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "bin"))
import cfg
import distill


class TestEnvConfig(unittest.TestCase):
    def test_model_url_and_chat_settings_from_env_file(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "config.json").write_text(json.dumps({"writer": {
                "text_backends": {"ollama": {"model": "json-model"}}}}), encoding="utf-8")
            (root / ".env").write_text(
                '# comment\nexport AI_SKILLS_OLLAMA_MODEL="file-model"\n'
                'AI_SKILLS_OLLAMA_URL=http://127.0.0.1:11434/api/generate\n'
                'AI_SKILLS_CHAT_URL=http://local/v1/chat/completions # comment\n'
                'AI_SKILLS_CHAT_API_KEY="secret value"\n', encoding="utf-8")
            with patch.dict(os.environ, {"AI_SKILLS_CONFIG": str(root / "config.json"),
                                       "USERPROFILE": str(root), "APPDATA": str(root)},
                            clear=True):
                spec = cfg.load()["writer"]["text_backends"]["ollama"]
                self.assertEqual(spec["model"], "file-model")
                self.assertEqual(spec["url"], "http://127.0.0.1:11434/api/generate")
                self.assertEqual(cfg.chat_settings(),
                                 ("http://local/v1/chat/completions", "file-model",
                                  "AI_SKILLS_CHAT_API_KEY"))
                self.assertNotIn("secret value", json.dumps(cfg.load()))
                self.assertEqual(cfg.env("AI_SKILLS_CHAT_API_KEY"), "secret value")

    def test_process_environment_wins_and_explicit_file_path(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "private.env"
            path.write_text("AI_SKILLS_OLLAMA_MODEL=file-model\n", encoding="utf-8")
            with patch.dict(os.environ, {"AI_SKILLS_ENV_FILE": str(path),
                                       "AI_SKILLS_OLLAMA_MODEL": "process-model"}):
                self.assertEqual(cfg.env("AI_SKILLS_OLLAMA_MODEL"), "process-model")
                self.assertEqual(cfg.load()["writer"]["text_backends"]["ollama"]["model"],
                                 "process-model")

    def test_ollama_request_uses_private_bearer_token(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "private.env"
            path.write_text("AI_SKILLS_OLLAMA_API_KEY=private-token\n", encoding="utf-8")
            response = unittest.mock.MagicMock()
            response.read.return_value = b'{"response":"done"}'
            response.__enter__.return_value = response
            with patch.dict(os.environ, {"AI_SKILLS_ENV_FILE": str(path)}), \
                    patch.object(distill.urllib.request, "urlopen", return_value=response) as open_url:
                result = distill.run_http({"url": "http://localhost/api/generate", "model": "m"},
                                          "prompt", 1, Path(tmp))
            self.assertEqual(result, "done")
            self.assertEqual(open_url.call_args.args[0].get_header("Authorization"),
                             "Bearer private-token")


if __name__ == "__main__":
    unittest.main()
