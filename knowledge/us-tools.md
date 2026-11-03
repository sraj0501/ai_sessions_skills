# US Data Tools

> Auto-maintained by the ai_session_skills background writer. One `###` entry
> per distinct action. `sig` comments are dedupe keys — never delete them.

## Scripting automation

### Update specific sections within a markdown file
<!-- sig: 603e5af0a1ba -->

```bash
python3 - <<'EOF'
p='next-steps.md'
s=open(p).read()
def rep(old,new):
global s
assert s.count(old)==1, old[:60]
s=s.replace(old,new)
rep("correction (D-51), US-22, the dormant-code removal, and US-05 / US-06 / US-08\n",
"correction (D-51), US-22, the dormant-code removal, and US-05 / US-06 / US-08\n**Updated:** 25 September 2026, after closing US-05/06/08 on the board, D-69,\nD-72, D-73 and the repository half of D-67. US-43 and US-44 parked by the owner\n")
old_start=s.index("| # | Action | Why now |\n")
old_end=s.index("| 6 | Revoke the old ADO PAT | Expired is not revoked |\n")
```

- **What it does:** This script reads the content of next-steps.md into a variable, defines a replacement function, and then uses that function to substitute a specific old string with a new, updated string within the content.
- **Why:** It allows for programmatic, targeted updates to structured documentation files, ensuring that multiple related items are updated consistently in one pass.
- **Example:** python3 - <<'EOF' p='next-steps.md' s=open(p).read() def rep(old,new): global s assert s.count(old)==1, old[:60] s=s.replace(old,new) rep("old text", "new text") EOF
- **Notes:** The script uses a here-document (<<'EOF') to pass multi-line Python code to the interpreter. The `assert s.count(old)==1` line will cause the script to fail if the old string appears more than once.
