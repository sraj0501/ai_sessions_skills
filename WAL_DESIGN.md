# Command knowledge event log (accepted design and implementation status)

## Decision

Use an append-only, write-ahead event log as the source of truth for reusable
command knowledge. A knowledge base is a materialized view built from those
events. Capture each command together with the visible context needed to
interpret it: the task or issue, working directory and project, prior relevant
observations, the command's complete result when the harness supplies it, and
the agent's visible evaluation and next decision when available. Never infer
private reasoning. Retain repeats, failures, and events the current writer
would skip.

Given the full retained log, a future model and versioned prompt can regenerate
the knowledge base or propose a new version. The result need not be byte-for-byte
identical: model prose and judgment can differ. The capture evidence, stable
event identities, and deterministic routing/deduplication inputs remain
replayable. No model can recover context or output that a harness did not send
or that was never recorded. Local logs need backups; losing both the knowledge
base and its log cannot be recovered by replay.

This design applies to the reusable command knowledge base. Resolution playback
remains a separate, complete teaching record. Playback events must not be
summarized, deduplicated, or passed to the knowledge writer.

## Why a WAL

The current capture path computes a signature, drops known commands, and queues
only new ones. After writing, the queue record is normally removed. The
Markdown knowledge base retains commands, prose, and signature markers, but it
cannot reconstruct every original command, output, skip decision, or writer
input. A WAL should become the durable source of capture evidence; the
knowledge base should be a rebuildable view of that evidence.

## Local capture contract

1. For every tool event **delivered by a harness**, durably append one immutable
   event before signature deduplication, filtering, queueing, or writing. Record
   repeated and failed commands. Give each event a schema version and a unique
   `(machine_id, event_id)` pair, timestamp, harness, session, project, exact
   command or tool arguments, output and exit status when supplied, task or
   issue context, visible evaluation notes when supplied, and the original
   payload. Mark absent fields as absent; never fabricate output or reasoning.
2. Keep exact local evidence separate from a derived knowledge candidate.
   Candidate normalization and signature calculation can change over time;
   the WAL event cannot. Record which normalizer and writer versions produced
   each candidate and entry.
3. Use daily SQLite segments with durable transactions and event checksums.
   A hook must acknowledge
   capture only after the record is durable. If a harness never dispatches a
   hook, the WAL cannot recover that action; the live harness test remains open.
4. Keep the local WAL out of Git. It may contain tokens, paths, private output,
   and user data. Set file permissions, retention, encryption, and backup rules
   explicitly. A command-only WAL is insufficient to reconstruct why a fix was
   chosen; outputs and visible evaluations require harness support or explicit
   notes.

## Replay and stronger-model review

- `rebuild` reads WAL events in stable order, validates checksums and schema,
  reconstructs candidates with a selected normalizer version, and writes a
  fresh knowledge base in a separate directory. It can include previously
  skipped events and apply a new model and prompt. Never overwrite the current
  knowledge base during a trial rebuild.
- `review` compares old and proposed entries by stable candidate identity and
  signature. Preserve provenance and the old revision. Promote a revision only
  after validation and human review. Rebuilding can recover what was recorded,
  not data omitted by old hooks or captures before the WAL existed.
- Test replay deterministically with a fixed writer stub first. Then compare
  different models on the same frozen event set so quality changes are
  attributable to the model and prompt.

## Team consolidation

Each person keeps a local WAL and runtime. A submission step reads a bounded
range of local event IDs, detects secrets, applies a team sharing policy, and
creates sanitized candidate envelopes. The shared service or repository stores
the submitted candidates with stable IDs and provenance, so retries are
idempotent. Raw playback transcripts and chat databases are never submitted
automatically.

The central processor groups candidates by signature, then checks meaning:
signature equality is a useful first pass, not proof that two commands have
identical purpose. It keeps distinct arguments and examples as evidence,
routes one proposed entry per reusable action, and opens a reviewable change to
the central knowledge Git repository. Team members pull approved Markdown.
One central writer publishes changes; individual machines do not push directly
to the same branch. The WAL is the evidence store, while Git holds the reviewed
knowledge view. A remote event store or Git-backed candidate inbox can serve
as the central ingest layer, but it needs access control, encryption, retention,
and a documented secret-screening policy before rollout.

## Implementation order and acceptance

1. Add the local WAL and tests proving duplicate and failed commands are logged
   before the current dedupe path, without changing existing writer behavior.
2. Add inspect, integrity-check, and offline replay commands. Verify a fresh
   knowledge directory can be rebuilt from a frozen fixture using a stub writer.
3. Add writer provenance and a stronger-model review workflow with a diff and
   explicit promotion step.
4. Add sanitized, idempotent team submission and central merge/review. Test two
   machines submitting the same action, unique variants, retries, and conflicts.
5. Complete the live harness embedding test for exact output, session binding,
   and visible evaluations before claiming full-fidelity capture.

## Implemented now

- `tool/bin/wal.py` commits checksummed local events to one SQLite database per
  UTC day in `.runtime/wal/events/` before normal capture filtering and dedupe.
  It also reads the earlier per-event JSON layout without a migration.
  `AI_SKILLS_WAL` or `wal_dir` can place the log outside the knowledge base.
  The machine ID is local to `.runtime/wal/machine-id`. `inspect` and `verify`
  read the event log. A failed append returns a nonzero hook status rather than
  claiming the event was captured. The Codex IDE fallback also logs its
  completed command actions before queueing them.
- Queue records carry the WAL event ID, machine ID, and normalizer version.
  `.runtime/writer-provenance.jsonl` records the writer mode, backend, model,
  version, prompt hash, signature, event identity, and outcome for written
  records.
- `wal_rebuild.py` validates the WAL, regenerates candidates, and writes a new
  directory using a deterministic stub or the configured text model. Its
  manifest records per-candidate provenance. `wal_review.py diff` compares the
  proposal with current Markdown; `promote` requires the reviewed proposal
  digest and backs up replaced files. Promotion overlays proposed files and
  leaves unrelated current files intact.
- `wal_team.py export` requires an explicit event-ID allow-list, omits raw
  payloads, results, task text, and playback, and rejects common secret and
  absolute path patterns. `ingest` uses stable candidate IDs for idempotent retries;
  `report` groups candidates by signature for meaning review; `propose` builds
  a separate central draft. A human reviews the bundle and proposed Markdown
  before sharing or publishing. The Git repository for approved central
  knowledge can be managed by the team; there is no hosted sync service.

## Remaining work and limits

- Full-fidelity live harness embedding remains a TODO. Hooks cannot record
  output or visible evaluations they do not receive. The Codex IDE adapter
  retains its observed item only, which may omit that context.
- The current normalizer may omit a command from the derived KB even though
  its raw event is safe in the WAL. A later normalizer version can revisit it.
- Automatic secret detection is incomplete. Exported bundles require human
  review before transfer; local WAL files should be backed up to a protected,
  encrypted store under the team's retention policy. The tool never prunes or
  uploads raw WAL files automatically. Do not copy `machine-id` between
  installations.
- Semantic grouping is presented for review; there is no automatic claim that
  same-signature commands mean the same thing. A central publisher remains a
  team workflow, not an unattended push to one branch.
