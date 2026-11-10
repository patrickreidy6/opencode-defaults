# OpenCode Harness (pr4)

Lean, cross-platform OpenCode V2 base defaults for Windows PCs, Linux hosts (`amd-halo`), and Docker workspace containers (`ops-infra`).

## What Is Included

| Source | Installed location / purpose |
|---|---|
| `global/opencode.json` | Native OpenCode V2 defaults: `openai/gpt-6-astra`, title model `openai/gpt-5.6-sol`, `superpowers` plugin, `context7` MCP, and optional `~/.config/opencode/AGENTS.local.md` |
| `global/AGENTS.md` | Short, OS-neutral global working and communication rules |
| `.opencode/skills/writer/` | Concise, practical prose voice for emails, messages, and docs |
| `.opencode/skills/frontend-design/` | Visual UI design craft + `references/ui-preferences.md` for greenfield interfaces |
| `.opencode/skills/data-preferences/` | Analytical data defaults: local/NAS first (Google Cloud / Drive 5 TB when cloud is needed, not S3), raw CSV + Parquet + Polars + DuckDB |
| `.opencode/skills/skill-authoring/` | [Agent Skills](https://agentskills.io/home) progressive-disclosure spec, OpenCode V2 layout, and `skills-ref` validation |
| `.opencode/skills/naming-files/` | Concise lowercase hyphenated file and date-prefix naming rules |
| `.opencode/skills/naming-directories/` | Concise lowercase hyphenated directory, hierarchy, and `.tmp` naming rules |

Domain-specific MCP servers, plugins, and skills stay out of this base harness so unrelated workspaces pay zero extra context tokens.

## Install or Update

Requires OpenCode V2 (`2.0.4+`), Git, and Python 3 (or `uv`).

**Windows (PowerShell):**
```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File ./install.ps1 -WhatIf
powershell -NoProfile -ExecutionPolicy Bypass -File ./install.ps1
```

**Linux / Halo Docker Workspaces (`bash` / `sh`):**
```sh
sh ./install.sh --dry-run
sh ./install.sh
```

In `ops-infra` containers where `/home/builder` is persistent and `/home/builder/.local/bin` is on `PATH`, install OpenCode V2 and link its binary once per workspace:
```sh
curl -fsSL https://opencode.ai/v2/install | bash
ln -sf "$HOME/.opencode/bin/opencode" "$HOME/.local/bin/opencode"
sh ./install.sh
```
(`opencode upgrade` resolves symlinks via `realPath`, so `~/.local/bin/opencode -> ~/.opencode/bin/opencode` preserves automatic `curl` updates while working in non-login SSH shells.)

### Installer Behavior
- Resolves destination to `--destination`, else `$XDG_CONFIG_HOME/opencode`, else `~/.config/opencode`.
- Deep-merges `opencode.json` objects and **unions arrays** (`plugins`, `instructions`, `skills`) so machine-local plugins and auth settings survive.
- Preserves any pre-existing non-`pr4` `AGENTS.md` into `AGENTS.local.md` (which OpenCode loads automatically when present and skips silently on machines/containers where absent).
- Backs up overwritten files under `<destination>/backups/harness-<timestamp>/` and leaves unrelated files (`service.json`, `cli.json`, local `commands/`) untouched.

## Starting a New Project Repo With Extra MCPs or Plugins

Once `pr4` is installed globally on a machine or container, every repo automatically inherits `superpowers`, `context7`, your model defaults, and global skills. You do **not** copy `pr4` files into new repositories.

When starting a new repo (for example, a website repo `xyz` that needs extra MCP servers `abc` and `def`), declare **only** the project-specific additions in `xyz/opencode.json`:

```json
{
  "$schema": "https://opencode.ai/config.json",
  "mcp": {
    "servers": {
      "abc": {
        "type": "remote",
        "url": "https://mcp.example.com/abc"
      },
      "def": {
        "type": "local",
        "command": ["npx", "-y", "@example/def-mcp"]
      }
    }
  }
}
```

(Or run `opencode mcp add abc --url ...` from inside `xyz`.) OpenCode V2 merges `~/.config/opencode/opencode.json` + `xyz/opencode.json` at runtime, so `xyz` gets `superpowers` + `context7` + `abc` + `def` while all other workspaces remain lean.

## Validation

Run the installer unit tests:
```sh
uv run --no-project python -m unittest discover -s tests -v
```

Validate each skill against the [Agent Skills specification](https://agentskills.io/specification):
```sh
uv run --no-project --with "git+https://github.com/agentskills/agentskills.git#subdirectory=skills-ref" python -m skills_ref.cli validate .opencode/skills/writer
uv run --no-project --with "git+https://github.com/agentskills/agentskills.git#subdirectory=skills-ref" python -m skills_ref.cli validate .opencode/skills/frontend-design
uv run --no-project --with "git+https://github.com/agentskills/agentskills.git#subdirectory=skills-ref" python -m skills_ref.cli validate .opencode/skills/data-preferences
uv run --no-project --with "git+https://github.com/agentskills/agentskills.git#subdirectory=skills-ref" python -m skills_ref.cli validate .opencode/skills/skill-authoring
uv run --no-project --with "git+https://github.com/agentskills/agentskills.git#subdirectory=skills-ref" python -m skills_ref.cli validate .opencode/skills/naming-files
uv run --no-project --with "git+https://github.com/agentskills/agentskills.git#subdirectory=skills-ref" python -m skills_ref.cli validate .opencode/skills/naming-directories
```

## Related Repos
- [pr3 — media](https://github.com/patrickreidy6/pr3)
- [pr5 — travel](https://github.com/patrickreidy6/pr5)
- [pr6 — trader](https://github.com/patrickreidy6/pr6)
- [pr7 — organization & workflow](https://github.com/patrickreidy6/pr7)
- [ops-infra — Halo workspaces](https://github.com/patrickreidy6/ops-infra)
