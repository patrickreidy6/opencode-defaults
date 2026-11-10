---
name: skill-authoring
description: Use when creating, importing, reviewing, or validating Agent Skills (SKILL.md) or packaging reusable agentic workflows in OpenCode.
---

# Skill Authoring (Agent Skills Open Standard)

Follow the open [Agent Skills specification](https://agentskills.io/specification) (<https://agentskills.io/home>) so skills stay portable, token-efficient, and compatible across OpenCode and other skills-capable harnesses. Load the built-in `opencode` skill when configuring OpenCode discovery or permissions.

## Placement
- **Project-specific workflows:** `<repo>/.opencode/skills/<name>/SKILL.md`
- **Personal cross-project defaults:** Maintain in `pr4/.opencode/skills/<name>/SKILL.md` and deploy globally via `pr4`'s installer (`~/.config/opencode/skills/`).
- Inspect existing skills before adding a new one; extend an existing skill when its trigger domain already covers the task.

## Directory Layout & Progressive Disclosure
Agents load skills in three stages to protect context:
1. **Discovery (~20-50 tokens):** Only `name` and `description` load at session startup.
2. **Activation (< 5000 tokens, < 500 lines):** Full `SKILL.md` body loads when the task matches `description`.
3. **Execution (on demand):** Supporting files load or run only when `SKILL.md` directs the agent to them.

```text
<skill-name>/
├── SKILL.md          # Required: YAML frontmatter + concise instructions
├── scripts/          # Optional: self-contained helpers invoked via explicit interpreter
├── references/       # Optional: detailed docs loaded only when needed
└── assets/           # Optional: templates, schemas, static files
```

Keep file links relative and one level deep from `SKILL.md` (for example, `[references/api.md](references/api.md)`), avoiding nested reference chains. Invoke scripts via their interpreter (`uv run python scripts/tool.py`, `bash scripts/tool.sh`) rather than relying on executable file bits.

## Frontmatter Rules
- `name` (required): 1-64 characters; lowercase `a-z`, `0-9`, and single hyphens (`-`) only; no leading, trailing, or consecutive hyphens; **must match the parent directory name**.
- `description` (required): 1-1024 characters; state specifically **when to use** the skill and what it covers (third person, keyword-rich, without summarizing the whole workflow in the description).
- Optional fields: `license`, `compatibility` (1-500 chars when environment constraints matter), `metadata` (string-to-string map; quote numeric values).
- `allowed-tools` is ignored by OpenCode; configure tool access in OpenCode `permissions` instead.

## Validation
Preserve upstream licenses and attribution beside imported skills. Validate every created or edited skill against the reference validator:

```sh
uv run --no-project --with "git+https://github.com/agentskills/agentskills.git#subdirectory=skills-ref" python -m skills_ref.cli validate .opencode/skills/<name>
```

(Invoking via `python -m skills_ref.cli` works identically on Linux/Docker and on Windows 11 systems with Smart App Control enabled, where unsigned `uvx` `.exe` wrappers are blocked.) Also verify that every linked file in `references/`, `scripts/`, and `assets/` exists, and use `/reload` in OpenCode if metadata does not refresh immediately.
