---
description: Receive and apply public shared defaults here, with backups
agent: build
subagent: false
model: openai/gpt-6.1-sol#low
---

Receive and apply the published shared harness in this workspace. Arguments: $ARGUMENTS

This command accepts no arguments. If any were supplied, explain the usage and stop.
Invocation authorizes replacing shared files/settings with public `main`, backing
up overwritten/retired items, and applying the repository's OpenCode CLI pin.
Workspace-only additions and project files remain local. There is no send,
proposal, pull request, or review step.

Use one shell call to run the Python program below with `uv run --no-project python`
or an available Python 3.10+ interpreter. Use PowerShell's here-string piped to
Python on Windows, or a quoted heredoc on POSIX. Keep the current working directory.

```python
import os
from pathlib import Path
import subprocess
import sys

source = Path.home() / '.local/share/opencode-defaults'
os.environ['GIT_TERMINAL_PROMPT'] = '0'
os.environ['GCM_INTERACTIVE'] = 'never'
if not source.exists():
    source.parent.mkdir(parents=True, exist_ok=True)
    subprocess.run(['git', '-c', 'credential.helper=', '-c', 'core.askPass=',
                    'clone', '--quiet', '--branch', 'main',
                    'https://github.com/patrickreidy6/opencode-defaults.git', str(source)], check=True)
raise SystemExit(subprocess.run([sys.executable, str(source / 'shared_harness.py'),
                                'update', '--project', str(Path.cwd())]).returncode)
```

Report the received revision, result and backup location concisely. Relay any
service-restart instruction: do not restart the service owning this session.
If any stage failed, distinguish what was already applied from what failed;
never claim success or attempt a manual repair. Do not push, create a PR, change
other workspaces, inspect credentials, or start a planning/review workflow.
