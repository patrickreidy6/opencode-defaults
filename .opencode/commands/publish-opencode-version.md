---
description: Publish the installed OpenCode CLI version to the defaults repository
agent: build
subagent: false
model: openai/gpt-6.1-sol#low
---

Publish the installed OpenCode CLI version to the defaults repository's public
`main` branch. The arguments supplied were `$ARGUMENTS`.

This command takes no arguments. If any were supplied, report the usage and stop.

From the root of this project, run `uv run --no-project python publish_opencode_version.py`
in one shell call, using an available Python 3.10+ interpreter if `uv` is
unavailable. The script reads the installed version and handles the pin, commit,
push, and verification.

Relay the script's result, including the version, full main revision and any
checkout notice. If the script fails, report its error and stop.
