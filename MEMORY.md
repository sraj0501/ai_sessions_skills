# Project Memory: Playback Next Steps

## Status

Playback is planned but not implemented. It is a separate, manually activated
feature and must not change the normal command-knowledge workflow.

## Product contract

- `playback start [title]` starts playback for the invoking agent thread only.
- `playback status` reports `inactive`, `recording`, `processing`, `complete`,
  or `failed` and shows the output path when available.
- `playback stop` stops recording immediately, queues asynchronous
  finalization, and returns without waiting for a local model.
- Playback control commands are excluded from the recorded timeline.
- When playback is inactive, no playback instructions, recording, worker, or
  local-model processing runs. Existing knowledge capture is unchanged.
- Normal `session.py start/stop` controls for the knowledge pipeline remain
  independent from playback controls.

## Fidelity contract

The primary, capable model is the authoritative author of playback meaning.
While playback is active, it must provide short, visible summaries around
consequential actions:

1. **Intent:** why the next command or tool action is being run.
2. **Observation:** what the result showed.
3. **Decision:** what was concluded and what should happen next.
4. **Outcome:** how the issue was fixed and how the fix was verified.

Private chain-of-thought is neither available nor recorded. Playback captures
the primary model's visible reasoning summaries verbatim. Ollama, llama.cpp,
or another local model may organize and label that text, but must not invent,
paraphrase, or fill missing reasoning. Every rendered reasoning statement must
reference a source event and be validated as an exact transcript substring.
Missing reasoning is rendered as `Not recorded`.

Harnesses that cannot expose visible assistant messages may provide a clearly
labelled command-only playback, but must not claim full-fidelity reasoning.

## Recorded content

Each playback preserves:

- Complete original commands, without signature normalization or truncation.
- Repeated commands and their exact execution order.
- Timestamp, harness, session, project, working directory, and exit status.
- Concise command-result evidence.
- Material patch, file-edit, search, and other tool events.
- Primary-authored intent, observation, decision, outcome, and verification.

The durable result is one Markdown file per playback, for example:

```text
playbacks/2026-09-09_21-14-03_fix-authentication-timeout.md
```

The file contains metadata, a short authoritative outcome, and a chronological
timeline. Each timeline entry contains only the fields needed to understand
the progression: `Why`, exact `Command` or tool action, `Result`, `Understood`,
and `Next`.

Playback files should be local and gitignored by default because exact commands
and outputs may contain credentials or sensitive paths. They must never be
automatically committed or pushed.

## Asynchronous architecture

```text
existing post-tool hook
        |
        +-- existing knowledge capture (unchanged)
        |
        +-- fast playback event spool, only when active
                        |
                        +-- detached playback worker
                                |
                                +-- Ollama / llama.cpp formatting
                                |
                                +-- one Markdown playback file
```

The hook hot path performs no model call. It writes a small immutable event to
`.runtime/playback-spool/` and exits. Unique event files avoid a contested
append lock; harness ordinals determine order when available, with timestamp
and process sequence as fallbacks.

The detached worker performs transcript association, local-model formatting,
validation, retries, and final rendering. If the local model is unavailable,
the main thread remains unaffected and raw events remain queued. After the
retry limit, the worker may produce a deterministic command-only playback with
unavailable fields explicitly marked.

## Session behavior

- Starting playback binds it to the invoking harness session. Other active
  agent sessions remain unaffected.
- Only the bound session's events are accepted.
- Stopping moves the recording to `processing`; it does not synchronously
  render the file.
- A short settling period may capture the primary model's closing visible
  summary before finalization.
- Interrupted sessions retain their spool and can be resumed, finalized as
  partial, or explicitly discarded later.

## Local-model role

Refactor the existing local writer transport into a shared module and support:

- Ollama's local HTTP API.
- llama.cpp's OpenAI-compatible local server.
- A configurable generic local HTTP endpoint.

Use deterministic generation and validated structured output. The local model
may classify or arrange primary-authored text, but final prose must remain
extractive. Semantic summaries that are not authored by the primary model are
not accepted.

## Planned implementation

### New files

- `tool/bin/playback.py`: manual CLI and playback state transitions.
- `tool/bin/playback_capture.py`: fast, lossless event spooling.
- `tool/bin/playback_worker.py`: detached processing and final rendering.
- `tool/bin/local_model.py`: shared Ollama, llama.cpp, and local HTTP client.
- `tool/prompts/PLAYBACK_EVENT_PROMPT.md`: extractive event classification.
- `tool/prompts/PLAYBACK_SUMMARY_PROMPT.md`: extractive final organization.
- `tool/tests/test_playback.py`: lifecycle, fidelity, and concurrency tests.

### Existing files to update

- `tool/bin/capture.py`: spool original playback payloads before knowledge
  normalization, truncation, and deduplication.
- `tool/bin/session.py`: supervise the playback worker without coupling the two
  feature lifecycles.
- `tool/bin/ide_capture.py`: read ordered visible agent messages and supported
  tool results; never ingest private `reasoning` records.
- `tool/bin/cfg.py`: add playback paths, limits, and local backend settings.
- `tool/bin/doctor.py`: report playback state, queue, worker, and model health.
- `tool/install.py`: install the playback-aware skill and required hooks.
- `tool/skill/BODY.md` and `tool/README.md`: document activation, fidelity,
  privacy, failure behavior, and commands.

## Implementation order

1. Add playback configuration, state machine, CLI, and session binding.
2. Add lossless event spooling before the existing knowledge normalization.
3. Add deterministic command-only rendering and crash recovery.
4. Add detached worker lifecycle with immediate `start` and `stop` returns.
5. Extract local-model transport and add Ollama and llama.cpp backends.
6. Add primary-authored reasoning capture and exact-substring validation.
7. Add Codex visible-transcript enrichment, followed by other harness adapters.
8. Update installation, diagnostics, documentation, and installed skill text.
9. Run unit tests and Windows/POSIX smoke tests.

## Acceptance criteria

- Playback changes model behavior only between `playback start` and
  `playback stop` in the bound thread.
- No Ollama or llama.cpp call occurs on the main hook or agent execution path.
- Starting and stopping return immediately after state changes are persisted.
- Commands are complete, ordered, repeated when actually repeated, and not
  passed through knowledge deduplication.
- Every reasoning claim is verbatim primary-model text with a source event.
- Missing reasoning is disclosed instead of inferred by a smaller model.
- Concurrent hooks and worker restarts cannot lose or reorder recorded events.
- A completed recording produces exactly one durable Markdown artifact.
- Existing knowledge capture, routing, distillation, pause controls, and files
  behave exactly as before.
