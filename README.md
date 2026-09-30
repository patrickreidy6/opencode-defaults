# OpenCode Harness (pr4)

Personal OpenCode defaults, reusable skills, commands, and optional preferences. This is the source of truth for the global harness installed at `~/.config/opencode/`.

## Install or update

Requires Windows PowerShell 5.1+, OpenCode, and Git. Clone this repo and run from its root:

```powershell
powershell -NoProfile -File ./install.ps1 -WhatIf
powershell -NoProfile -File ./install.ps1
```

**Quit and restart OpenCode after installation.** Configuration and skill metadata are loaded at startup.

The installer:
- Merges tracked defaults into the existing `opencode.json`, preserving unrelated settings and local authentication configuration. Tracked values win on conflicts.
- Installs general instructions, preferences, guides, shared skills, and commands.
- Backs up overwritten files under `~/.config/opencode/backups/harness-<timestamp>/`.
- Leaves unrelated files and authentication stores in place. The deployable config contains no credentials.

Use `-Destination <directory>` to test an installation in isolation. If `opencode.jsonc` already exists, reconcile it first: the installer stops rather than introducing competing global configs. To restore an installation, close OpenCode, restore backed-up files to their matching paths, and remove only newly installed harness-owned files if necessary.

Pull updates here and rerun the installer. Make durable changes in this repo rather than only in the installed copies.

## What is shared

| Source | Installed location / purpose |
|---|---|
| `global/opencode.json` | Model defaults, Context7, Gmail, existing OpenTelemetry preference |
| `global/AGENTS.md` | General working rules; project-specific rules remain in project repos |
| `global/guides/` | On-demand skill authoring instructions |
| `.opencode/skills/` | Global `skills/`: coder, design, writer, researcher, deep-research, frontend-design |
| `.opencode/commands/` | Global `commands/`, including `/sessions-move` |
| `preferences/` | UI and analytical-data preferences, read when relevant |
| `presets/blender/` | Optional workspace config and beginner guide; not installed globally |

Project `opencode.json` settings override global defaults. Project instructions and existing architectures take precedence over generic UI/data preferences. The trading-only Cerebras and Massive skills live in pr6, not here.

Gmail authentication remains machine-local. Existing OAuth settings are preserved; a fresh machine must configure/authenticate its own Gmail integration. The harness does not copy `.env`, provider credentials, or token stores from another machine.

For Blender, copy the two files in `presets/blender/` to a new dedicated workspace and start OpenCode there. Install `uvx` and enable the Blender add-on as described in the preset guide. Merge the preset instead of overwriting configuration in an existing workspace.

## Validation

Use the current [OpenCode schema](https://opencode.ai/config.json) and [Agent Skills specification](https://agentskills.io/specification). Validate each shared skill, for example:

```powershell
uvx --from "git+https://github.com/agentskills/agentskills.git#subdirectory=skills-ref" skills-ref validate .opencode/skills/design
```

Also check resource links and discovery from another repo (`opencode debug skill`). Avoid sharing resolved configuration output because it can contain local authentication settings. Research helper dependencies in `.opencode/skills/deep-research/requirements.txt` are optional and only needed for those utilities.

Upstream skill licenses and attribution are retained beside the skills.

## Related repos

- [pr3 — media](https://github.com/patrickreidy6/pr3)
- [pr5 — travel](https://github.com/patrickreidy6/pr5)
- [pr6 — trader](https://github.com/patrickreidy6/pr6)
- [pr2 — historical archive](https://github.com/patrickreidy6/pr2)

Extracted with a fresh history on September 30, 2026. The original monorepo history, session transcripts, and retired experiments remain in pr2.
