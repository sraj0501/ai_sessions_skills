# Project Memory: Command Knowledge and Resolution Playback

## Purpose

Command knowledge captures eligible actions in a local WAL and maintains a
searchable Markdown view. Topic placement is decided per new action by a text
model using a short, locally embedded candidate list. Older small topics can
be consolidated through a reviewed proposal.

Playback is a manually activated teaching record of one issue resolution. It
preserves every observed command and tool action in execution order, their
outputs when supplied by the harness, and the primary agent's recorded visible
evaluations. The resulting Markdown
should let a junior developer understand what was tested, what the evidence
showed, why the next step followed, and how the fix was verified.

Playback is separate from the command knowledge base. Its events bypass
signature normalization, deduplication, the watcher writer, and all model
distillation. The normal knowledge workflow operates when playback is inactive.

## Current implementation

- `tool/bin/playback.py`: `start`, `note`, `stop`, `status`, and `finalize`.
  `migrate` moves older top-level Markdown into per-recording runtime folders.
- `tool/bin/playback_capture.py`: stores the original matching hook payload.
- `tool/bin/playback_worker.py`: renders a local Markdown timeline after stop.
- `tool/bin/capture.py`: sends matching events to playback before knowledge
  normalization, then skips knowledge capture for those events.
- `tool/bin/ide_capture.py`: sends completed Codex IDE command items to playback
  when hook delivery is unavailable.
- `tool/skill/BODY.md`: tells the primary agent to record visible intent,
  observation, decision, and outcome notes verbatim during playback.
- `tool/bin/playback_query.py`: lists stored recordings and returns exact
  ordered event pages with stable step numbers. Per-recording state is kept
  under `.runtime/playback/<id>/state.json` after newer sessions begin.
- `tool/bin/playback_index.py` and `vector_cache.py`: keep incremental local
  SQLite text and embedding indexes. The configured Ollama embedding model is
  required for semantic knowledge and playback question search. Full event
  output remains in the recording; indexed model prompts use compact evidence.
- `tool/bin/playback_reason.py`: reconstructs missing step inferences later with
  local or Ollama cloud models. It labels them `Reconstructed later`, skips
  existing reasoning, and requires `--overwrite` to replace it in prompts.
- `tool/bin/runtime_backup.py`: compresses durable runtime evidence into a
  verified ZIP, omitting logs and rebuildable indexes. Restore requires a new
  target directory. Archives are private and unencrypted.
- `tool/bin/search_mcp.py`: MCP tools for command knowledge search,
  playback discovery, compact or exact playback reading, and bounded management of
  capture, reasoning, backup, routing, reviewed topic consolidation, and team knowledge. Long
  operations return pollable jobs under `.runtime/mcp_jobs/`.
  `tool/install_search.py`
  registers the server at user scope with detected local coding harnesses and
  Claude Desktop Chat.
- `tool/bin/search_http.py`: HTTP OpenAPI view over the same read-only search
  and playback functions for harnesses that cannot launch stdio MCP.
- `tool/bin/distill.py`: checks for matching actions across all topic files,
  retrieves a small embedding-ranked topic shortlist, and asks the text model
  to place each new action. Prior binary routes are hints. An uncertain route
  leaves the WAL record for retry.
- `tool/bin/knowledge_organize.py`: proposes model-guided moves for older small
  topic files. Reviewed selections require an exact digest and file hashes;
  apply creates a compressed local backup and preserves signature markers.
  It proposes whole-file moves only when every entry agrees on an existing
  destination. The agent or user must review each proposed move; a small local
  model has suggested unrelated destinations in a broad batch.
- `tool/bin/chat_backend.py`, `ask.py`, and `playback_chat.py`: use
  OpenAI-compatible Chat Completions endpoints. Configuration comes from the
  process environment or a private `.env` beside `config.json`. The playback
  client walks through five compact steps per request by default or answers a
  question from five locally retrieved steps by default. It does not carry prior
  pages into later model requests. Local embedding is still required when the
  answer model uses Ollama cloud.

Each recording keeps its raw event spool, rendered `playback.md`, optional
reconstructed reasoning, and indexes under `.runtime/playback/<id>/`. The
runtime, private `.env`, and default `backups/` are gitignored because they may
contain private data. Never commit them or share raw archives through team sync.

The current reviewed consolidation placed `lsof`, `date`, and `kill` in
`knowledge/shell.md`; `py` and `python.exe` in `knowledge/python.md`; and
`godot` in `knowledge/godot-engine.md`. `grep`, `sed`, and `awk` were already
represented in the shell topic. This is knowledge content, not a hardcoded
command-to-topic rule. The writer checks for an exact action across all files,
then asks the model to route each new action using a short list of candidates
from local embeddings. Previous routes are hints. An unavailable or uncertain
answer leaves the WAL record for retry.

## Fidelity rules

- Never normalize, truncate, or deduplicate playback commands or outputs.
- Preserve repeated actions and the order in which they occurred.
- Treat primary agent notes as the only source for evaluation and reasoning.
  Private chain of thought is unavailable. Later generated inferences must be
  labelled as reconstructed and never presented as original agent reasoning.
- Mark missing output, intent, observation, decision, or outcome as
  `Not recorded` where applicable.
- Keep playback control commands out of the timeline.
- Bind a recording to the invoking session when a session ID is available.

## Remaining verification and improvements

- **TODO — live harness embedding test remains open.** Install the updated
  hooks and skill, restart each harness, trust hooks where required, resolve a
  reproducible failing issue, and compare the agent session against the
  rendered playback event by event. Check full output, stable session ID,
  verbatim intent/observation/decision/outcome notes, failed commands, repeated
  commands, and the verified fix. The Codex IDE history format is internal and
  may omit visible agent messages or command output.
- Capture visible agent messages automatically where a harness exposes them,
  while excluding private reasoning records. Manual `note` commands currently
  supply the primary agent's evaluation.
- Strengthen concurrent start/stop and late-hook handling beyond the current
  unique-file spool and atomic file replacement.
- Keep the current event transcript complete even if a future renderer offers
  navigation, grouping, or teaching annotations.
- Playback query tools are read-only. Chat answers and later reasoning derive
  from retrieved steps; neither alters the event log or rendered transcript.
  Generated reasoning is stored separately and can replace earlier generated
  text in prompts only when `--overwrite` is explicit.
- A model server is not a coding harness. The chat client can read existing
  playback through a compatible chat endpoint; recording new actions requires
  the calling harness to deliver capture events. Local coding harnesses can
  use MCP or HTTP OpenAPI to query playback.

Tests: `tool/tests/test_playback.py`, `tool/tests/test_portable.py`, and
`tool/tests/test_search_tools.py`. The full unit suite passed 211 tests on
Windows in November 2026.
The protocol-based playback client has a real Ollama tool-calling smoke check in
`tool/tests/smoke_chat_playback.py`; it passed with `qwen3.5:9b` on this
machine. That verifies reading and explaining a synthetic recording, not
delivery of capture events from a live coding harness.

## Locked knowledge log and team decisions

The accepted contract and implementation status are in
[WAL_DESIGN.md](WAL_DESIGN.md). This applies to the reusable command knowledge
base, not to resolution playback.

- Append each harness-delivered tool event to a durable, immutable local log
  **before** filtering, normalization, signature deduplication, or writing.
  Keep repeats, failures, skipped actions, original payloads, full commands,
  results, task context, and visible evaluations when supplied. Mark missing
  evidence as missing; never invent private reasoning.
- Treat the event log as the source of truth and Markdown knowledge as a
  rebuildable view. Retain stable event IDs, schema and provenance. A selected
  future model and versioned prompt may reevaluate the same evidence and
  propose a new view. Regenerated prose need not be identical, and omitted
  hook data or events captured before the log exists cannot be recovered.
- Keep raw logs local, access controlled, backed up, and outside Git. Submit
  only policy-approved, sanitized, idempotent candidate envelopes to the team.
  A central processor deduplicates by signature **and meaning** and publishes
  reviewed knowledge through one writer. Individual clients pull that view.
- Keep playback complete and separate. Its events never pass through the
  reusable knowledge writer or any distillation step.

The immutable local WAL, offline/model rebuild, review overlay, and explicit
sanitized team candidate exchange are implemented. The queue still discards
known signatures, but the WAL retains the original evidence. Live harness
fidelity, a hosted sync service, and fully automatic semantic merging remain
open.
