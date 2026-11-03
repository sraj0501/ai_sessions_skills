"""Required embeddings, incremental cache, and hybrid retrieval."""
from __future__ import annotations

import os
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "bin"))
import vector_cache


class VectorCacheTests(unittest.TestCase):
    def test_missing_model_fails_clearly(self):
        with patch.dict(os.environ, {"AI_SKILLS_EMBED_MODEL": ""}):
            with self.assertRaisesRegex(RuntimeError, "AI_SKILLS_EMBED_MODEL"):
                vector_cache.rank(Path("unused.sqlite3"), [("a", "text")], "question", 1)

    def test_changed_entries_reembed_and_exact_terms_help_ranking(self):
        calls = []

        def embed(_model, _url, texts):
            calls.append(texts)
            return [[float("commit" in text), float("container" in text), 1.0]
                    for text in texts]

        with tempfile.TemporaryDirectory() as temp, \
                patch.dict(os.environ, {"AI_SKILLS_EMBED_MODEL": "test-model"}), \
                patch.object(vector_cache, "_embed", side_effect=embed):
            database = Path(temp) / "vectors.sqlite3"
            records = [("a", "git commit changes"), ("b", "start container")]
            first = vector_cache.rank(database, records, "commit", 1, ["a"])
            self.assertEqual(first, ["a"])
            self.assertEqual([len(batch) for batch in calls], [2, 1])
            vector_cache.rank(database, records, "commit", 1, ["a"])
            self.assertEqual([len(batch) for batch in calls], [2, 1, 1])
            records[1] = ("b", "start container with docker")
            vector_cache.rank(database, records, "commit", 1, ["a"])
            self.assertEqual([len(batch) for batch in calls], [2, 1, 1, 1, 1])

    def test_signature_comments_never_reach_embedding_model(self):
        inputs = []

        def embed(_model, _url, texts):
            inputs.extend(texts)
            return [[1.0, 0.0] for _ in texts]

        with tempfile.TemporaryDirectory() as temp, \
                patch.dict(os.environ, {"AI_SKILLS_EMBED_MODEL": "test-model"}), \
                patch.object(vector_cache, "_embed", side_effect=embed):
            vector_cache.rank(Path(temp) / "vectors.sqlite3",
                              [("entry", "### Inspect\n<!-- sig: abcdef123456 -->\ngit diff")],
                              "inspect <!-- sig: deadbeefcafe -->", 1)
        self.assertEqual(inputs, ["### Inspect\n\ngit diff", "inspect "])


if __name__ == "__main__":
    unittest.main()
