# Command knowledge base

Browse a topic below. Each entry contains the command, what it does, why to
use it, and examples or notes. New topics are added to this table automatically.

Search from the repository root:

```powershell
python tool/bin/search.py git branch
python tool/bin/search.py connection --topic postgresql --full
```

Use multiple keywords to narrow the results. In VS Code, press **Ctrl+Shift+F**
and set **Files to include** to `knowledge/**/*.md`.

| Topic | Covers |
|---|---|
| [Git](git.md) | Branches, remotes, history, merging and diffs |
| [GitHub CLI](github-cli.md) | Pull requests, issues and repositories |
| [Shell](shell.md) | Files, text processing and operating-system commands |
| [Python](python.md) | Python tooling and environments |
| [Node](node.md) | Node, npm and TypeScript |
| [Docker](docker.md) | Containers and images |
| [Kubernetes](kubernetes.md) | Clusters and workloads |
| [PostgreSQL](postgresql.md) | Database commands |
| [Ollama](ollama.md) | Local models |
| [Homebrew](brew.md) | Package management |
| [systemd](systemd.md) | Linux services |
| [Agent tools](agent-tools.md) | Agent tools and equivalent commands |
| [`orbstack.md`](orbstack.md) | OrbStack Tool |
| [`statsync.md`](statsync.md) | Statsync Tool |

`_skipped.md` records actions the writer judged unsuitable for documentation.
`.routes.json` stores routing decisions. Capture logs and pending actions are
kept separately in the repository's `.runtime/` folder.
