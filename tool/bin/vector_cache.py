"""Required local Ollama embeddings and incremental SQLite vector cache."""
from __future__ import annotations

import hashlib
import json
import math
import re
import sqlite3
import sys
from contextlib import closing
from pathlib import Path
from urllib import request

import cfg

VERSION = 1
MAX_INPUT_CHARS = 1800
BATCH_SIZE = 8
SIG_RE = re.compile(r"<!--\s*sig:\s*[0-9a-f]{6,40}\s*-->", re.IGNORECASE)


def _embedding_text(value: str) -> str:
    return SIG_RE.sub("", value)[:MAX_INPUT_CHARS]


def _settings() -> tuple[str, str]:
    model = cfg.env("AI_SKILLS_EMBED_MODEL").strip()
    if not model:
        raise RuntimeError("AI_SKILLS_EMBED_MODEL is required in .env (for example, nomic-embed-text:latest)")
    url = cfg.env("AI_SKILLS_EMBED_URL", "http://localhost:11434/api/embed").strip()
    if not url:
        raise RuntimeError("AI_SKILLS_EMBED_URL must not be empty")
    return model, url


def _embed(model: str, url: str, texts: list[str]) -> list[list[float]]:
    payload = json.dumps({"model": model, "input": texts, "truncate": False}).encode("utf-8")
    req = request.Request(url, data=payload, headers={"Content-Type": "application/json"})
    try:
        with request.urlopen(req, timeout=90) as response:
            vectors = json.load(response)["embeddings"]
    except (OSError, ValueError, KeyError) as exc:
        raise RuntimeError(f"embedding model {model!r} is unavailable at {url}: {exc}") from exc
    if len(vectors) != len(texts) or not all(v and all(math.isfinite(x) for x in v)
                                               for v in vectors):
        raise RuntimeError(f"embedding model {model!r} returned invalid vectors")
    return vectors


def _cosine(left: list[float], right: list[float]) -> float:
    if len(left) != len(right):
        raise RuntimeError("embedding dimensions changed; remove the vector cache and retry")
    denominator = math.sqrt(sum(x * x for x in left) * sum(x * x for x in right))
    return sum(a * b for a, b in zip(left, right)) / denominator if denominator else 0.0


def rank(database: Path, records: list[tuple[str, str]], question: str,
         limit: int, lexical_order: list[str] | None = None,
         prune: bool = False) -> list[str]:
    """Embed changed documents, then fuse semantic and exact-text rankings."""
    model, url = _settings()
    if not records:
        return []
    database.parent.mkdir(parents=True, exist_ok=True)
    with closing(sqlite3.connect(database, timeout=30)) as db:
        db.execute("CREATE TABLE IF NOT EXISTS vectors (key TEXT PRIMARY KEY, digest TEXT NOT NULL, "
                   "model TEXT NOT NULL, version INTEGER NOT NULL, vector TEXT NOT NULL)")
        cached = {key: (digest, name, version, vector) for key, digest, name, version, vector
                  in db.execute("SELECT key, digest, model, version, vector FROM vectors")}
        prepared = [(key, _embedding_text(text),
                     hashlib.sha256(_embedding_text(text).encode("utf-8")).hexdigest())
                    for key, text in records]
        changed = [(key, text, digest) for key, text, digest in prepared
                   if key not in cached or cached[key][:3] != (digest, model, VERSION)]
        for start in range(0, len(changed), BATCH_SIZE):
            batch = changed[start:start + BATCH_SIZE]
            vectors = _embed(model, url, [text for _, text, _ in batch])
            db.executemany("INSERT OR REPLACE INTO vectors VALUES (?, ?, ?, ?, ?)",
                           [(key, digest, model, VERSION, json.dumps(vector))
                            for (key, _, digest), vector in zip(batch, vectors)])
            db.commit()
            if sys.stderr.isatty() and (start == 0 or (start + len(batch)) % 40 == 0
                                         or start + len(batch) == len(changed)):
                print(f"Embedding index: {start + len(batch)}/{len(changed)} entries",
                      file=sys.stderr, flush=True)
        if prune:
            current = {key for key, _, _ in prepared}
            db.executemany("DELETE FROM vectors WHERE key=?",
                           [(key,) for key in cached if key not in current])
            db.commit()
        stored = {key: json.loads(vector) for key, vector in
                  db.execute("SELECT key, vector FROM vectors")}
    query_vector = _embed(model, url, [_embedding_text(question)])[0]
    semantic = sorted((key for key, _ in records),
                      key=lambda key: _cosine(stored[key], query_vector), reverse=True)
    semantic_rank = {key: position for position, key in enumerate(semantic)}
    lexical_rank = {key: position for position, key in enumerate(lexical_order or [])}
    def score(key: str) -> float:
        value = 1 / (10 + semantic_rank[key])
        if key in lexical_rank:
            value += 1 / (10 + lexical_rank[key])
        return value
    return sorted(semantic, key=score, reverse=True)[:limit]
