# PDF Generation

> Auto-maintained by the ai_session_skills background writer. One `###` entry
> per distinct action. `sig` comments are dedupe keys — never delete them.

## Generating PDFs

### Convert multiple HTML files to PDF documents
<!-- sig: 1b1af9542966 -->

```bash
for f in current-plan-2026-09-28 known-issues-summary-2026-09-28 delivery-progress-2026-09-21; do $EDGE --headless --disable-gpu --no-pdf-header-footer '--print-to-pdf=pdf/$f.pdf' 'file:///tmp/$f.html' '2>/dev/null;' echo '$f: $(pdfinfo pdf/$f.pdf | rg Pages);' 'done;'
ls -la pdf/
```

- **What it does:** This loop iterates over specified Markdown files, converts each to HTML using pandoc, and then uses the Edge browser in headless mode to print the resulting HTML to a PDF file in the pdf/ directory. Finally, it lists the contents of the pdf/ directory.
- **Why:** This sequence automates the entire process of generating multiple, consistently formatted PDF reports from source Markdown files without manual intervention.
- **Example:** Running the full loop structure to process all specified files and then listing the resulting PDFs.
- **Notes:** The loop relies on the previous pandoc step having successfully created the temporary HTML file at /tmp/$f.html. The '2>/dev/null' suppresses potential console output from the Edge process.
