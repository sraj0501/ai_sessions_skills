# Change

> Auto-maintained by the ai_session_skills background writer. One `###` entry
> per distinct action. `sig` comments are dedupe keys — never delete them.

## File modification

### Update a specific date range in a markdown file
<!-- sig: 6669dc537922 -->
<!-- sig: 3c1f9751235a -->
<!-- sig: c513e03d18cd -->
<!-- sig: 93991a6ae781 -->
<!-- sig: e286d0a921ad -->
<!-- sig: f57fcec85acd -->
<!-- sig: 99a55badc9b0 -->
<!-- sig: 6cff1de86e44 -->
<!-- sig: bc499cc4c181 -->
<!-- sig: 56717cfd4a05 -->
<!-- sig: 7f72a663c415 -->
<!-- sig: 18373d2ca936 -->
<!-- sig: 4b0875265f8d -->
<!-- sig: 0a762771382e -->
<!-- sig: d4799f54b1f1 -->
<!-- sig: 3b098f2d8087 -->
<!-- sig: 78fdf8c25a78 -->
<!-- sig: 484bf7040f35 -->
<!-- sig: 6ca80b3f33fc -->
<!-- sig: 7b512450760f -->
<!-- sig: 4aa23603f20e -->
<!-- sig: cdad14a63eee -->
<!-- sig: 1b16d170fa67 -->
<!-- sig: e5d5749a3f86 -->
<!-- sig: 226ebe0d06f3 -->
<!-- sig: 9e70cf0f20f0 -->
<!-- sig: 3bf2ad104959 -->
<!-- sig: 6a61ad83c7f2 -->
<!-- sig: a5dbf68591bc -->
<!-- sig: 9d10c79cdf49 -->
<!-- sig: 5ffc6146e52f -->
<!-- sig: 5b4bf4bbb6ab -->
<!-- sig: d5dc733ce2db -->
<!-- sig: 23b5164c22e1 -->
<!-- sig: 1073719e9b6a -->
<!-- sig: 384f9fdf9a02 -->
<!-- sig: bf35e56abd76 -->
<!-- sig: 91e8415e2e95 -->
<!-- sig: 49546ba7b56c -->
<!-- sig: 13eafd082e2e -->
<!-- sig: 403c23df356b -->
<!-- sig: 8c425b4151b7 -->
<!-- sig: 88b6a320a949 -->
<!-- sig: 798709e18617 -->
<!-- sig: 58e5e40daa0c -->
<!-- sig: 761d08aa4f34 -->
<!-- sig: daef1a805831 -->
<!-- sig: c8d21fc7cae6 -->
<!-- sig: 89b71ea57980 -->
<!-- sig: 282b11de0b41 -->
<!-- sig: 5b1e6caf6190 -->
<!-- sig: 606ee310dc16 -->
<!-- sig: 840eae5a2af6 -->
<!-- sig: c6419c65d055 -->
<!-- sig: f3963839e26c -->
<!-- sig: 9f0040f8d868 -->
<!-- sig: 0d16702f135e -->
<!-- sig: 6e373c6f1438 -->
<!-- sig: 6ab597aa151c -->
<!-- sig: d8554e8cbaa4 -->
<!-- sig: b6f452aace5e -->
<!-- sig: 62ac74b0e747 -->
<!-- sig: 63844e203a4f -->

```bash
sed -i '' 's/(change log: 2026-09-28 to 2026-10-16)/(change log: 2026-09-28 to 2026-10-21)/' architecture/00-overview.md
cat >> architecture/00-overview.md <<'EOF'
```

- **What it does:** The first command uses sed to perform an in-place substitution on architecture/00-overview.md, replacing the old date range with the new one. The second command appends new content to the same file.
- **Why:** This sequence allows for both updating existing metadata (the date range) and appending new, structured content (the commit log entry) in a single operation.
- **Example:** sed -i '' 's/(change log: 2026-09-28 to 2026-10-16)/(change log: 2026-09-28 to 2026-10-21)/' architecture/00-overview.md && cat >> architecture/00-overview.md <<'EOF'
- **Notes:** The '-i ''' option in sed is necessary for in-place editing on macOS/BSD systems. The 'EOF' marker must match the delimiter used in the here-document.
