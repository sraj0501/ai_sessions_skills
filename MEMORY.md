# Project Memory: Resolution Playback

## Purpose

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
- `tool/bin/search_mcp.py`: read-only MCP tools for command knowledge search,
  playback discovery, and exact playback reading. `tool/install_search.py`
  registers the server at user scope with detected local coding harnesses and
  Claude Desktop Chat.
- `tool/bin/search_http.py`: HTTP OpenAPI view over the same read-only search
  and playback functions for harnesses that cannot launch stdio MCP.
- `tool/bin/chat_backend.py`, `ask.py`, and `playback_chat.py`: a single
  OpenAI-compatible Chat Completions function-calling client for model servers;
  playback retains conversation history for follow-up questions.

The raw event spool is in `.runtime/playback/`; finished files are in
`playbacks/`. Both locations are gitignored because exact commands and outputs
may contain private data. Playback files are never committed automatically.

## Fidelity rules

- Never normalize, truncate, or deduplicate playback commands or outputs.
- Preserve repeated actions and the order in which they occurred.
- Treat primary agent notes as the only source for evaluation and reasoning.
  Private chain of thought is unavailable; never invent or paraphrase it.
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
- Playback query tools are read-only. Model explanations are derived from
  retrieved steps and do not alter the event log or rendered transcript.
- A model server is not a coding harness. The chat client can read existing
  playback through a compatible chat endpoint; recording new actions requires
  the calling harness to deliver capture events. Local coding harnesses can
  use MCP or HTTP OpenAPI to query playback.

Tests: `tool/tests/test_playback.py` and `tool/tests/test_portable.py`.
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
