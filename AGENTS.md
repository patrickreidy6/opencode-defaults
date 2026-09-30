# OpenCode Harness (pr4)

This repository maintains personal global OpenCode defaults. It is not an application runtime dependency.

## Source layout
- `global/opencode.json`: portable settings merged into the user's existing global config.
- `global/AGENTS.md`: general rules installed globally. This file contains harness-repo-specific guidance instead.
- `global/guides/`: on-demand instructions installed with the harness.
- `.opencode/skills/` and `.opencode/commands/`: shared source assets, installed under global `skills/` and `commands/`.
- `preferences/`: optional UI/data guidance; project rules take precedence.
- `presets/blender/`: opt-in configuration for a separate Blender workspace.

## Maintenance
- Load `customize-opencode` and check https://opencode.ai/config.json before changing configuration.
- Follow [global/guides/skill-authoring.md](global/guides/skill-authoring.md) and fetch the current specification for skill work.
- Preserve licenses, attribution, and resource links. Keep application-specific skills in their app repo.
- Use `powershell -NoProfile -File ./install.ps1 -WhatIf` to preview and `powershell -NoProfile -File ./install.ps1` to deploy.
- Test installer changes against an isolated `-Destination` first. Check that unknown config keys and local authentication settings survive and existing files are backed up.
- Validate skills with `skills-ref validate .opencode/skills/<name>` or the documented uvx fallback. Check discovery from a separate app repo after installation.
- Credentials, authentication stores, `.env` files, and install backups never belong in this repo.
- Quit and restart OpenCode after installation or any configuration-time change.
