# Research Quality Checks

Use to audit a report's evidence or choose an appropriate bundled validator.

## What completion requires

- The answer addresses the scoped questions and distinguishes evidence, inference, and unresolved uncertainty.
- Material claims are supported by sources actually inspected. Check that dates, units, populations, and qualifications match the claim being made.
- Decision-relevant counterevidence is addressed rather than omitted.
- Citations resolve to identifiable sources, and numbered citations have matching bibliography entries.
- The deliverable is complete in the requested format, without draft placeholders or omitted content.

Depth, source count, and prose-to-bullet ratio are not universal quality thresholds. A narrow fact may need one authoritative source; a contested conclusion may need several independent lines of evidence.

## Bundled tools

Run commands with the working directory set to `.opencode/skills/deep-research/`; replace the example report path with the actual path.

### Structured Markdown reports

```powershell
C:/Python314/python.exe -X utf8 scripts/validate_report.py --report "path/to/report.md"
```

[validate_report.py](../scripts/validate_report.py) checks the bundled long-form report layout, numbered citations, bibliography consistency, placeholders, and relative links. It expects headings for Executive Summary, Introduction, Main Analysis, Synthesis, Limitations, Recommendations, Bibliography, and Methodology. Its source-count and length warnings reflect the older template, not requirements for every research task.

Use this validator when that layout fits the requested deliverable. For another format, inspect equivalent structural and citation properties directly rather than expanding the report just to satisfy its template assumptions.

### Citation metadata and accessibility

```powershell
C:/Python314/python.exe -X utf8 scripts/verify_citations.py --report "path/to/report.md"
```

[verify_citations.py](../scripts/verify_citations.py) checks DOI metadata and URL accessibility and flags heuristic title patterns. It makes network requests. A successful URL check does not verify that the source supports a claim, and a failed request or generic title does not establish fabrication. Review findings against the source itself. The default mode can exit successfully with unverified citations; inspect its output, not just the exit code.

### HTML artifacts

For the bundled HTML template, use [verify_html.py](../scripts/verify_html.py) as described in [HTML/PDF generation](html-generation.md). It checks template structure and rough content preservation, not full rendering or factual accuracy.

## Resolve findings

Fix actual content, citation, and rendering defects and rerun affected checks. Continue while the next action can resolve a concrete issue; stop repeating checks that already pass. If blocked by inaccessible evidence or unavailable tooling, state exactly what remains unverified and how it limits the result. Do not label the deliverable fully verified on the strength of a script exit code alone.
