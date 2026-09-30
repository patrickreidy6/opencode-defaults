# HTML and PDF Reports

Use only when the deliverable includes HTML or PDF. Keep the researched content as the source of truth and preserve citations through conversion.

## HTML

The [bundled HTML template](../templates/mckinsey_report_template.html) provides a compact corporate report style. Use it when it suits the brief; otherwise follow the user's design requirements. A metrics dashboard is useful only when the findings contain meaningful, supported metrics.

For the bundled template, populate these placeholders:

| Placeholder | Content |
|---|---|
| `{{TITLE}}` | Report title |
| `{{DATE}}` | Generation date |
| `{{SOURCE_COUNT}}` | Number of unique cited sources |
| `{{METRICS_DASHBOARD}}` | Supported metrics markup, or an empty string |
| `{{CONTENT}}` | Main report HTML |
| `{{BIBLIOGRAPHY}}` | Complete bibliography HTML |

[md_to_html.py](../scripts/md_to_html.py) exposes `convert_markdown_to_html(markdown_text)`, returning `(content_html, bibliography_html)`. Import the function if using this converter: its command-line entry point prints truncated previews, not a complete HTML document. It splits at the literal `## Bibliography`, so place the bibliography last or handle later sections separately.

The converter handles a limited Markdown subset. Inspect the generated headings, tables, links, bibliography entries, and section nesting. Do not assume that conversion preserves every element correctly.

For the bundled template, run with `.opencode/skills/deep-research/` as the working directory:

```powershell
C:/Python314/python.exe -X utf8 scripts/verify_html.py --html "path/to/report.html" --md "path/to/report.md"
```

This validator expects the bundled template's class names and checks rough section and citation coverage. For custom HTML, use checks suited to that structure. Inspect the rendered artifact with available preview tools and correct clipped content, broken links, missing citations, and layout problems.

## PDF

Use the available renderer appropriate to the environment. For WeasyPrint, consult [print-layout guidance](weasyprint_guidelines.md) for relevant layout patterns and current documentation for version-specific support.

With WeasyPrint installed, a basic conversion is:

```powershell
weasyprint "path/to/report.html" "path/to/report.pdf"
```

Inspect pagination, long tables, headings, and bibliography legibility in the generated PDF. Page-break rules should suit the actual content; a table longer than a page must be allowed to split. Completion means the requested file exists and has been inspected to the extent supported by available tools. Report any rendering or inspection blocker accurately.
