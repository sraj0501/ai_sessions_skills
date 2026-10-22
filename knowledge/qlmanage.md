# Qlmanage

> Auto-maintained by the ai_session_skills background writer. One `###` entry
> per distinct action. `sig` comments are dedupe keys — never delete them.

## Application Management

### Render HTML content to a log file
<!-- sig: d6caad72e3a2 -->
<!-- sig: e6b10e6ddd32 -->

```bash
qlmanage -t -s 1600 -o /tmp '/Users/sraj/git_apps/epam/Work/PHUS-INN/devin-session-notes/UI mockups/concept-c-executive-insight.html' '>/tmp/concept-c-ql.log' '2>&1;'
cat '/tmp/concept-c-ql.log;'
ls -l /tmp/concept-c-executive-insight.html.png '2>/dev/null'
```

- **What it does:** The first command uses qlmanage to process the HTML file, directing both standard output and standard error into /tmp/concept-c-ql.log. The subsequent commands then display the log content and list the associated PNG file.
- **Why:** This sequence is used to render a specific HTML mockup into a log file for inspection, and then verify the existence and details of its corresponding image asset.
- **Example:** qlmanage -t -s 1600 -o /tmp '/Users/sraj/git_apps/epam/Work/PHUS-INN/devin-session-notes/UI mockups/concept-c-executive-insight.html' '>/tmp/concept-c-ql.log' '2>&1;' followed by cat '/tmp/concept-c-ql.log;'
- **Notes:** The initial command redirects output to /tmp/concept-c-ql.log, which is then read by cat. The final ls command suppresses errors for the PNG file.
