# Report Assembly

Use when structuring a research report or delivering a saved artifact.

## Match the deliverable

Honor the user's format, length, and destination. Otherwise, deliver a cited Markdown response. When a file is requested without a destination, use an appropriate project output directory and state the path. Produce HTML or PDF when requested; see [HTML/PDF generation](html-generation.md).

Scale the structure to the question. A useful report normally contains the answer, supporting findings, material limitations, and sources. Recommendations, a methodology appendix, or a claims-evidence table belong where they help the reader or satisfy the brief.

The [report template](../templates/report_template.md) is an optional outline. Rename, combine, or omit sections to fit the deliverable. Length follows the evidence and the reader's needs, not a mode or per-section quota.

## Citations

Place citations near the claims they support. Linked citations work for a short answer. For a long report, numbered citations can make repeated references easier to follow.

When using numbered citations:

- Keep a stable mapping between each number and its source.
- Include a complete bibliography entry for every citation used in the body.
- Record the real title, author or organization, publication date when known, and URL. Include an access date for changing web content.
- Use actual source metadata; mark an unavailable date as undated rather than guessing.

For the bundled validators, use `## Bibliography` with entries beginning `[N]` on their own lines. They expect consecutive numbering and recognize entries shaped as `[N] Author (Year). "Title". Publication. URL`.

## Assemble and finish

Write incrementally when a report is too large to compose reliably in one edit. Preserve citation mappings across sections; persist working state only when useful for continuation. There is no fixed word threshold or tool-call size requirement beyond the active tools' limits.

Before delivering, make sure the assembled artifact answers the question, contains the complete cited sources, and has no draft instructions or missing sections. Use [quality checks](quality-gates.md) appropriate to the format, fix issues they reveal, and return the requested artifact with its path when saved.
