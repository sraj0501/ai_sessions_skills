# Edge Browser

> Auto-maintained by the ai_session_skills background writer. One `###` entry
> per distinct action. `sig` comments are dedupe keys — never delete them.

## Generating reports

### Convert markdown files to PDF and create thumbnails
<!-- sig: cf38435d1e1a -->
<!-- sig: 694db6332e52 -->
<!-- sig: 61459149e234 -->
<!-- sig: 66112298c2e6 -->
<!-- sig: 2d7cc3d534ee -->
<!-- sig: b28e32f767b2 -->
<!-- sig: ef792daa8357 -->
<!-- sig: 609ecd152f0c -->
<!-- sig: 82329cee49f7 -->
<!-- sig: 1babf767e004 -->
<!-- sig: 8f9cc852b4e5 -->
<!-- sig: f47db36eb084 -->
<!-- sig: f691316350ad -->
<!-- sig: 56e29579fb94 -->
<!-- sig: 8446378bb50c -->
<!-- sig: 576edd6345d2 -->
<!-- sig: 341721829920 -->
<!-- sig: 7d7350433a52 -->
<!-- sig: 3a7a8ed2b2ef -->
<!-- sig: bf6842d3402c -->
<!-- sig: 7d299e1ae0bf -->
<!-- sig: 8e78e513a076 -->
<!-- sig: 46ab33845966 -->
<!-- sig: fd2b12bf7780 -->
<!-- sig: ab8c1b238163 -->
<!-- sig: 1e04a72bcb61 -->
<!-- sig: 3bdb3c7d91de -->
<!-- sig: 68785bf89d89 -->
<!-- sig: 44133a6751fb -->
<!-- sig: fd09fc6ac463 -->
<!-- sig: eb99d7134410 -->
<!-- sig: acc5448f24a0 -->
<!-- sig: 597bc3da63b1 -->
<!-- sig: f4a15f47a2d1 -->
<!-- sig: 95c2b5d0818e -->
<!-- sig: 0c0aeccbe2dd -->
<!-- sig: c8faaac5fb14 -->
<!-- sig: aff39afe356b -->
<!-- sig: 7412b0cecc0b -->
<!-- sig: 41e8433a888c -->
<!-- sig: b513db92d453 -->
<!-- sig: 0de0590177dd -->
<!-- sig: 0ed7bf5fb74b -->

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
<!-- sig: 1d46973eeeef -->

```bash
'/Applications/Microsoft Edge.app/Contents/MacOS/Microsoft Edge' --headless --disable-gpu --no-pdf-header-footer '--print-to-pdf=pdf/$f.pdf' 'file:///tmp/$f.html' '2>/dev/null;' pdftotext 'pdf/$f.pdf' -
```

- **What it does:** Launches Microsoft Edge in headless mode to print the content of a local HTML file to a PDF, and then pipes that generated PDF into pdftotext to extract plain text.
- **Why:** This sequence automates the process of creating a high-fidelity PDF representation of an HTML document and immediately extracting its raw text content for further processing.
- **Example:** '/Applications/Microsoft Edge.app/Contents/MacOS/Microsoft Edge' --headless --disable-gpu --no-pdf-header-footer '--print-to-pdf=pdf/report.pdf' 'file:///tmp/report.html' '2>/dev/null;' pdftotext 'pdf/report.pdf' -
- **Notes:** The command relies on the shell variable `$f` being set to a filename, and the output of the Edge command is piped to pdftotext via standard input (-).

## Automated testing

### Capture a screenshot of a specific webpage
<!-- sig: 83db911231e3 -->

```bash
'$EDGE' --headless --disable-gpu --hide-scrollbars --screenshot=/tmp/conceptc-shots/c-1600.png --window-size=1600,1200 '$F' '2>&1'
```

- **What it does:** Launches the Edge browser in headless mode to render the content of the file specified by '$F', saving a screenshot to the path provided.
- **Why:** This allows automated testing or content capture without needing a visible browser UI, which is faster and more reliable for scripting.
- **Example:** '$EDGE' --headless --disable-gpu --hide-scrollbars --screenshot=/tmp/conceptc-shots/c-1600.png --window-size=1600,1200 'file:///Users/sraj/git_apps/epam/Work/PHUS-INN/devin-session-notes/UI%20mockups/concept-c-executive-insight.html' '2>&1'
- **Notes:** The output is redirected to stderr ('2>&1'), and the screenshot is saved to the specified path.

### Launch headless browser for debugging
<!-- sig: 050ac1b10352 -->

```bash
'/Applications/Microsoft Edge.app/Contents/MacOS/Microsoft Edge' --headless --disable-gpu --remote-debugging-port=9333 --user-data-dir=/tmp/edge-cdp about:blank > /tmp/edge-cdp.log 2>&1
```

- **What it does:** Executes Microsoft Edge in headless mode, disabling GPU usage and setting up a remote debugging port on 9333. It directs all standard output and standard error to /tmp/edge-cdp.log.
- **Why:** This allows automated scripts to control the browser instance programmatically via the CDP protocol without rendering a visible UI.
- **Example:** '/Applications/Microsoft Edge.app/Contents/MacOS/Microsoft Edge' --headless --disable-gpu --remote-debugging-port=9333 --user-data-dir=/tmp/edge-cdp about:blank > /tmp/edge-cdp.log 2>&1
- **Notes:** The --user-data-dir=/tmp/edge-cdp specifies a temporary profile directory for the session.
