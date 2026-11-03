# Pdftotext

> Auto-maintained by the ai_session_skills background writer. One `###` entry
> per distinct action. `sig` comments are dedupe keys — never delete them.

## Text extraction

### Convert a PDF file to standard output text
<!-- sig: f7621f82346e -->

```bash
pdftotext pdf/delivery-progress-2026-09-21.pdf -
```

- **What it does:** This command extracts text content from the specified PDF file, sending the resulting plain text to standard output.
- **Why:** It pipes the extracted text directly to another utility like `rg` for immediate searching, avoiding the creation of an intermediate text file.
- **Example:** pdftotext pdf/delivery-progress-2026-09-21.pdf - | rg -n '104 points|109 points'
- **Notes:** The hyphen (-) as the output file specifies that the output should go to stdout, which is necessary for piping.
