# OpenCode Defaults (`opencode-defaults`)

This repository maintains personal global OpenCode V2 defaults across Windows workstations, Linux hosts, and Docker workspace containers. It is not an application runtime dependency.

## Source Layout
- `global/opencode.json`: portable OpenCode V2 defaults merged into `~/.config/opencode/opencode.json` (or `$XDG_CONFIG_HOME/opencode/opencode.json`).
- `global/AGENTS.md`: concise, OS-neutral global rules installed as `AGENTS.md`. Machine-specific instructions belong in `~/.config/opencode/AGENTS.local.md` (loaded via `instructions` when present). This root file holds `opencode-defaults`-specific maintenance guidance instead.
- `.opencode/skills/`: shared personal Agent Skills (`writer`, `frontend-design` + `references/ui-preferences.md`, `data-preferences`, `skill-authoring`, `naming-files`, `naming-directories`, `socratic-tutor`), installed under global `skills/`.
- `install.py` (`install.ps1` / `install.sh`): cross-platform Python 3 standard-library installer with backup, `$XDG_CONFIG_HOME` resolution, V1 cleanup, and array-union merging.
- `tests/test_install.py`: automated stdlib `unittest` suite for installer behavior.

## Maintenance
- Load the built-in `opencode` skill and consult <https://opencode.ai/v2/docs/config> before changing OpenCode configuration.
- Load `skill-authoring` and check <https://agentskills.io/specification> when adding or editing skills. Keep `global/AGENTS.md` short and OS-neutral; package detailed domain defaults as progressive-disclosure skills instead.
- Preserve upstream skill licenses and attribution. Keep project-specific MCP servers, plugins, and domain skills inside their owning project repo (`<repo>/opencode.json` and `<repo>/.opencode/skills/`).
- Preview and deploy:
  - Windows: `powershell -NoProfile -ExecutionPolicy Bypass -File ./install.ps1 -WhatIf` then `powershell -NoProfile -ExecutionPolicy Bypass -File ./install.ps1` (or `uv run --no-project python ./install.py`)
  - Linux / Docker: `sh ./install.sh --dry-run` then `sh ./install.sh` (or `python3 ./install.py`)
- Run `uv run --no-project python -m unittest discover -s tests -v` (or `python3 -m unittest discover -s tests -v`) and test against an isolated `--destination` after installer edits.
- Validate changed skills with `uv run --no-project --with "git+https://github.com/agentskills/agentskills.git#subdirectory=skills-ref" python -m skills_ref.cli validate .opencode/skills/<name>`.
- Never commit credentials, OAuth tokens, `.env` files, or install backups.
