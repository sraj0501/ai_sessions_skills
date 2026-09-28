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

### Convert HTML files to PDF and extract page count
<!-- sig: a2d424fa846b -->

```bash
for f in 'pdf/*.pdf;' do pdftotext '$f' -
done;
```

- **What it does:** This loop iterates over all files matching 'pdf/*.pdf;' and pipes the content of each PDF file to pdftotext, which then processes it.
- **Why:** The initial part of the command uses a loop structure to process multiple files sequentially, which is necessary for batch operations like this.
- **Example:** The loop processes all files matching the pattern 'pdf/*.pdf;' found in the current directory.
- **Notes:** The command structure is complex, involving multiple chained commands and loops. The initial part of the full command handles the PDF generation and the subsequent loop processes the resulting PDFs.

### Convert an HTML file to a PDF and then extract text
<!-- sig: 3efdb6b27779 -->

```bash
'/Applications/Microsoft Edge.app/Contents/MacOS/Microsoft Edge' --headless --disable-gpu --no-pdf-header-footer '--print-to-pdf=pdf/$f.pdf' 'file:///tmp/$f.html' '2>/dev/null;' pdftotext 'pdf/$f.pdf' -
```

- **What it does:** Launches Microsoft Edge in headless mode to print the content of a local HTML file to a PDF, and then pipes that generated PDF into pdftotext to extract plain text.
- **Why:** This sequence automates the process of creating a high-fidelity PDF representation of an HTML document and immediately extracting its raw text content for further processing.
- **Example:** '/Applications/Microsoft Edge.app/Contents/MacOS/Microsoft Edge' --headless --disable-gpu --no-pdf-header-footer '--print-to-pdf=pdf/report.pdf' 'file:///tmp/report.html' '2>/dev/null;' pdftotext 'pdf/report.pdf' -
- **Notes:** The command relies on the shell variable `$f` being set to a filename, and the output of the Edge command is piped to pdftotext via standard input (-).
