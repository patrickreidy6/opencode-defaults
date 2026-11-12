# OpenCode Defaults (`opencode-defaults`)

This repository maintains personal global OpenCode V2 defaults across Windows workstations, Linux hosts, and Docker workspace containers. It is not an application runtime dependency.

## Source Layout
- `global/opencode.json`: portable V2 defaults; Astra default/general/explore, Sol title, and `/xm-*` agent permissions. Merged into `~/.config/opencode/opencode.json` (or `$XDG_CONFIG_HOME/opencode/opencode.json`).
- `baseline.json`: pinned OpenCode CLI version, also part of the baseline fingerprint.
- `global/commands/*.md`: opt-in cross-model commands installed under global `commands/`; usage in README.md; design and live check in `docs/cross-model-workflow-design.md`.
- `global/AGENTS.md`: OS-neutral global rules installed as `AGENTS.md`. Machine-specific instructions belong in `~/.config/opencode/AGENTS.local.md` (loaded via `instructions` when present). This root file holds repository maintenance guidance.
- `.opencode/skills/`: shared personal Agent Skills (`writer`, `frontend-design` + `references/ui-preferences.md`, `data-preferences`, `project-setup` + `references/preferred-devtools.md`, `skill-authoring`, `naming-files`, `naming-directories`, `socratic-tutor`), installed under global `skills/`.
- `install.py` (`install.ps1` / `install.sh`): stdlib installer with backup, XDG resolution, V1 cleanup and array-union merging; tested by `tests/test_install.py` and `tests/test_baseline.py`.

## Maintenance
- Load the built-in `opencode` skill and consult <https://opencode.ai/v2/docs/config> before changing OpenCode configuration.
- Load `skill-authoring` and check <https://agentskills.io/specification> when adding or editing skills. Keep `global/AGENTS.md` short and OS-neutral; package detailed domain defaults as progressive-disclosure skills instead.
- Preserve upstream skill licenses and attribution. Keep project-specific MCP servers, plugins, and domain skills inside their owning project repo (`<repo>/opencode.json` and `<repo>/.opencode/skills/`).
- Preview and deploy:
  - Windows: `powershell -NoProfile -ExecutionPolicy Bypass -File ./install.ps1 -WhatIf` then `powershell -NoProfile -ExecutionPolicy Bypass -File ./install.ps1` (or `uv run --no-project python ./install.py`)
  - Linux / Docker: `sh ./install.sh --dry-run` then `sh ./install.sh` (or `python3 ./install.py`)
- Run `uv run --no-project python -m unittest discover -s tests -v` (or `python3 -m unittest discover -s tests -v`) and run install, then `--check`, against an isolated `--destination` after installer edits.
- Validate changed skills with `uv run --no-project --with "git+https://github.com/agentskills/agentskills.git#subdirectory=skills-ref" python -m skills_ref.cli validate .opencode/skills/<name>`.
- Never commit credentials, OAuth tokens, `.env` files, or install backups.
