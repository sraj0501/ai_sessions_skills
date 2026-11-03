# Team knowledge sync

The shared view is a published snapshot of reviewed command knowledge. Local
capture, the WAL, playback, queues, and private Markdown stay on each developer's
machine. A client uploads only candidates selected by WAL event ID. An upload
receipt means **received**, not **published**. A central operator reviews and
publishes one revision. Clients verify every file before switching to it under
`.runtime/team/revisions/<sha256>/`. Local knowledge is not overwritten. CLI,
MCP, and HTTP knowledge search include the installed team revision.

```text
developer WAL -> selected IDs -> sanitized candidates -> central inbox
                                                    |          |
                                              receipt     review/dedup
                                                               |
                                      versioned Markdown + hashes + manifest
                                                               |
                                   developer A <- verified pull -> developer B
```

## Deploy the server

Use Python 3.10+ and a private data directory outside Git. Set
`AI_SKILLS_TEAM_TOKENS` in the **server process environment** to a JSON object
mapping each developer's `machine-id` to a distinct random token of at least
32 characters. Keep it in a secret manager, never in `config.json` or source
control. For local testing, `AI_SKILLS_TEAM_TOKEN` enables one shared token. Bind
the server to loopback and expose it through an HTTPS reverse proxy with access
controls. Back up `inbox/`, `revisions/`, and the `current` pointer.

```sh
python tool/bin/team_server.py serve --root /srv/ai-skills-team --host 127.0.0.1 --port 8765
```

The service accepts `POST /v1/candidates` and serves `GET /v1/manifest` and
`GET /v1/files/<revision>/<name>`. All endpoints require a bearer token. Its
filesystem must be private; pattern screening is not a guarantee that a
candidate contains no sensitive information.

## Sync from a developer machine

Set `AI_SKILLS_TEAM_URL` to the HTTPS origin and `AI_SKILLS_TEAM_TOKEN` to that
machine's assigned token using a secure environment or secret manager. Loopback HTTP works
for local testing. Find event IDs with `wal.py inspect`, review the selected
commands, and put approved IDs in a local file, one per line. Keep the file
outside Git or under `.runtime/`.

```sh
python tool/bin/wal.py inspect
python tool/bin/team_sync.py sync --allow .runtime/team/approved-ids.txt
python tool/bin/team_sync.py status
python tool/bin/team_sync.py pull
python tool/bin/search.py git status
```

`sync` validates selected events before upload. It omits raw payload, output,
task context, and playback, and rejects common secret and absolute path patterns.
It saves server receipts under `.runtime/team/receipts.jsonl`, then pulls the
latest publication. Repeating a sync is safe because candidate IDs are stable.
`pull` downloads without uploading. If upload succeeds but download fails, the
receipt remains and the previous installed revision stays active. Retry `pull`
or the whole `sync`.

For a daily team run, schedule `sync --allow <reviewed-id-file>` on each client
and `pull` after publication. The approved ID file may retain older IDs; repeated
uploads are deduplicated. Selection stays explicit because WAL commands can be
private. Automating selection requires a team sharing policy and stronger
secret screening.

## Central review and publication

```sh
python tool/bin/team_server.py status --root /srv/ai-skills-team
python tool/bin/team_server.py report --root /srv/ai-skills-team
python tool/bin/team_server.py propose --root /srv/ai-skills-team --output /srv/review/proposal-2026-11-03 --writer model
python tool/bin/wal_review.py diff --current /srv/ai-skills-team/revisions/CURRENT_SHA --proposal /srv/review/proposal-2026-11-03
python tool/bin/team_server.py publish --root /srv/ai-skills-team --proposal /srv/review/proposal-2026-11-03 --approved-sha SHA_FROM_REVIEW
```

The proposal contains all received candidates, so each publication is a full
snapshot. `propose` does not overwrite an existing directory. `--writer model`
uses the configured central text writer. `--writer stub` is for deterministic
tests only; its prose is a fixture. Review the candidate grouping, commands,
Markdown, and digest before `publish`. For the first publication, compare with
an empty directory. The digest is printed by `wal_review.py diff`. A changed
proposal fails publication until reviewed again. To leave a candidate pending,
make a reviewed proposal containing accepted entries plus all previously
published entries.

| Event | Server state | Client state | Next action |
| --- | --- | --- | --- |
| Upload accepted | Candidate in inbox | Receipt saved | Review and publish |
| Upload timeout | Candidate may be present | Receipt unknown | Retry `sync` |
| Review pending | Candidate in inbox | Previous team revision | Resolve review |
| Publication complete | Immutable revision | Previous revision until pull | Run `pull` |
| Download/hash failure | Revision intact | Previous revision active | Repair and retry |

Clients do not start a background sync service. Use Task Scheduler on Windows
or systemd timers or cron on Linux with the same CLI arguments. Provide the
token through a secret manager, never as a command argument or checked-in file.
