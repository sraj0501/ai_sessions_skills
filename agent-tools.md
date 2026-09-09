# Agent tools

> Auto-maintained by the ai_session_skills background writer. One `###` entry
> per distinct action. `sig` comments are dedupe keys — never delete them.

Coding agents (Devin, Claude Code, Codex, Copilot, OpenCode, Cursor) expose
native tools that replace some shell commands. This file records what each tool
does and the CLI command it stands in for, so the knowledge transfers whether
the work is done by an agent or by hand. Tool names differ per harness —
`exec`/`Bash`/`bash`/`Shell` are the same action.

## Searching

Search tools (`grep`/`Grep`, `glob`/`Glob`) are ripgrep under the hood; each
distinct flag combination is captured into `shell.md` as its `rg` equivalent
(see the "Searching" section there). Prefer these tools over shelling out to
`rg`: they are permission-pre-approved and their output is size-capped.

## Editing files

### Make a targeted change to an existing file
<!-- sig: 6aa1ed147f8a -->

```text
edit(file_path, old_string, new_string)   # CLI equivalent: sed -i / patch
```

- **What it does:** Performs an exact string replacement in one file. Fails if `old_string` is not unique or does not match byte-for-byte, so a stale assumption becomes an error instead of a silent wrong edit.
- **Why:** Safer than `sed -i` (no regex surprises, no whole-file rewrite) and cheaper than rewriting the file.
- **Notes:** The file must be read first. Include surrounding context to disambiguate, or use `replace_all` for a rename across the file.

### Create a new file or fully rewrite one
<!-- sig: ec249f1db878 -->

```text
write(file_path, content)                 # CLI equivalent: cat > file <<'EOF'
```

- **What it does:** Writes the file, creating it or overwriting it entirely.
- **Why:** Right for new files; for existing files prefer `edit`, which cannot accidentally drop content that was not in context.
- **Notes:** Read an existing file before overwriting it.

### Apply a multi-file patch
<!-- sig: b3dc4acc16be -->

```text
apply_patch(patch)                        # CLI equivalent: git apply / patch -p1
```

- **What it does:** Applies a diff-style patch across one or more files in a single operation.
- **Why:** Keeps related edits atomic — either the whole change lands or none of it does.
