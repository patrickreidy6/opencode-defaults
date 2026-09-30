# Skill authoring and maintenance

Use the current [Agent Skills specification](https://agentskills.io/specification) as the source of truth. Fetch it for the task; if unavailable, state that the latest specification could not be checked and follow these rules. Load the built-in `customize-opencode` skill for OpenCode discovery, configuration, and permissions.

## Structure
- Inspect existing skills before adding one; extend an existing workflow when it already covers the task. Keep activation conditions distinct.
- Project skills live at `.opencode/skills/<name>/SKILL.md`. Shared personal skills are maintained in pr4 and deployed globally by `install.ps1`.
- Use YAML frontmatter followed by Markdown. Required `name`: 1–64 lowercase ASCII letters/numbers with single hyphen separators; no leading, trailing, or consecutive hyphens. Match the directory name.
- Required `description`: a non-empty string of at most 1024 characters explaining what the skill does and when to use it. Distinguish nearby workflows.
- Optional fields: `license`, `compatibility` (1–500 characters when present), and `metadata` (string-to-string mapping). Quote numeric-looking values.
- `allowed-tools` is an experimental space-separated string. OpenCode ignores it; use actual OpenCode permission settings for tool access.
- Keep `SKILL.md` under 500 lines and aim below 5000 tokens. Use actionable instructions, examples, and completion checks.
- Use progressive disclosure: detailed guidance in `references/`, executable helpers in `scripts/`, and templates/static resources in `assets/`. Existing third-party layouts may be preserved. Create directories only when needed, link directly from `SKILL.md`, and avoid nested reference chains.

## Maintenance and validation
- Inspect existing resources and preserve intended behavior, licenses, and attribution. Check links and callers after moves.
- Validate every added or changed skill:

```powershell
skills-ref validate .opencode/skills/<name>
```

If unavailable:

```powershell
uvx --from "git+https://github.com/agentskills/agentskills.git#subdirectory=skills-ref" skills-ref validate .opencode/skills/<name>
```

- Report blocked validation explicitly. Format validation is not workflow validation: also check resources exist, review a representative activating request and a nearby non-activating request, and run relevant checks for changed helpers.
- After configuration-time changes, tell the user to quit and restart OpenCode so discovery and metadata refresh.
