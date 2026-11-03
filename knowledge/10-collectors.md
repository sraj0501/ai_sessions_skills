# `10-collectors.md`

> Auto-maintained by the ai_session_skills background writer. One `###` entry
> per distinct action. `sig` comments are dedupe keys — never delete them.

## Documenting changes

### Append proposed architecture notes to overview file
<!-- sig: 172c493476ee -->
<!-- sig: 419be7b56516 -->
<!-- sig: cb0b0de72200 -->
<!-- sig: 7280be001ca8 -->
<!-- sig: d25614999162 -->
<!-- sig: d11b688e33d8 -->

```bash
cat >> architecture/00-overview.md <<'EOF'
```

- **What it does:** This command uses a here-document to append the content between the starting and ending 'EOF' markers directly into the architecture/00-overview.md file.
- **Why:** It allows for multi-line, structured documentation updates to be added to a specific file without needing to manually edit it or use a text editor.
- **Example:** cat >> architecture/00-overview.md <<'EOF' ### 2026-10-23 Proposed architecture documentation only — nothing merged, deployed or running. | Change | What changed | Where to read more | |---|---|---| | **Proposed independent complete-ETL data pipeline** *(proposed, not implemented; no live change)* | The collector repository now documents a plan under which it evolves into the **Delivery Metrics Data Pipeline**, owning the complete ETL lifecycle: one source extraction, immutable Bronze/Silver/environment-specific Gold, pipelin EOF
- **Notes:** The single quotes around 'EOF' prevent shell variable expansion within the appended content, ensuring the text is written literally.
