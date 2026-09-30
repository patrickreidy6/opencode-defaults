# Deep Research Skill for OpenCode

A task-scaled workflow for comprehensive, citation-backed research. OpenCode discovers the skill at `.opencode/skills/deep-research/SKILL.md`.

Upstream: https://github.com/199-biotechnologies/claude-deep-research-skill

The local guidance follows OpenAI's [Rethinking skills and prompts for GPT-6 Astra](https://developers.openai.com/blog/rethinking-skills-and-prompts-for-gpt-6-astra): narrow triggers, progressive disclosure, flexible methods, and explicit completion criteria.

## Use

Ask for a comprehensive investigation and specify the decision or deliverable, for example:

> Deep research the storage options for our analytics workload. Recommend one based on operating cost and maintenance effort, with evidence and key uncertainties.

Use `researcher` for a focused multi-source answer. A simple comparison or documentation lookup does not need the full report workflow.

## Behavior

- Reads supporting references only when relevant to the current task.
- Scales research to the evidence and question, without source quotas, word-count modes, or mandatory agent teams.
- Continues through the requested deliverable and relevant checks.
- Defaults to a cited Markdown response; saves files and produces HTML or PDF when requested.
- Preserves source provenance and distinguishes findings from inference and uncertainty.

## Supporting resources

| Resource | Use |
|---|---|
| [Methodology](reference/methodology.md) | Broad investigations and conflicting evidence |
| [Report assembly](reference/report-assembly.md) | Report structure, citations, and saved artifacts |
| [Quality checks](reference/quality-gates.md) | Evidence review and validator limitations |
| [HTML/PDF generation](reference/html-generation.md) | Requested formatted artifacts |
| [Continuation](reference/continuation.md) | Work spanning sessions or context windows |
| [Report outline](templates/report_template.md) | Optional starting structure |
| [HTML template](templates/mckinsey_report_template.html) | Optional compact corporate layout |

The bundled scripts are optional utilities. `validate_report.py` targets the original long-form layout and retains legacy length/source-count warnings. `verify_citations.py` checks metadata and accessibility, not claim support. `md_to_html.py` prints only previews from its CLI; use its conversion function for full content. See the linked references before using them.

Basic research uses the tools already available in OpenCode. Additional rendering dependencies are relevant only when producing those formats. Restart OpenCode after changing skill files to refresh loaded instructions.

## License

MIT - modify as needed for your workflow.
