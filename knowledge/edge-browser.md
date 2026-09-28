# Edge Browser

> Auto-maintained by the ai_session_skills background writer. One `###` entry
> per distinct action. `sig` comments are dedupe keys — never delete them.

## Generating reports

### Convert markdown files to PDF and create thumbnails
<!-- sig: cf38435d1e1a -->

```bash
for f in current-plan-2026-09-28 known-issues-summary-2026-09-28 delivery-progress-2026-09-21; do pandoc "$f.md" -f gfm -t html5 -s --metadata pagetitle="$(head -1 $f.md | sed 's/^# //')" -c /tmp/cto-print.css --embed-resources -o "/tmp/$f.html" && "$EDGE" --headless --disable-gpu --no-pdf-header-footer --print-to-pdf="pdf/$f.pdf" "file:///tmp/$f.html" 2>/dev/null; echo "$f: $(pdfinfo pdf/$f.pdf | rg Pages)"; done; pdftoppm -png -r 50 -f 1 -l 1 pdf/known-issues-summary-2026-09-28.pdf /tmp/pdfthumb2/ki2; pdftoppm -png -r 50 -f 1 -l 1 pdf/delivery-progress-2026-09-21.pdf /tmp/pdfthumb2/dp2
```

- **What it does:** This loop processes multiple markdown files, converting each to an HTML file, then using Edge to print that HTML content to a PDF. Finally, it uses pdftoppm to generate thumbnail images from the resulting PDFs.
- **Why:** This sequence automates the entire process of generating multiple structured reports from source markdown files, ensuring both the full PDF and a set of thumbnail previews are created.
- **Example:** Running the full loop structure to process all specified markdown files into PDFs and thumbnails.
- **Notes:** The loop iterates over the files listed in the 'for' statement. The first part uses pandoc to create temporary HTML files, which are then passed to Edge for PDF generation. The second part uses pdftoppm to extract 50 DPI PNG thumbnails from the generated PDFs.
