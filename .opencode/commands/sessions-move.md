---
description: Move root-level session files into the sessions directory.
agent: build
---

Move every Markdown file matching `session-*.md` from the repository root into `sessions/`.

- Create `sessions/` if it does not exist.
- Only move matching files located directly in the repository root.
- Preserve each filename.
- Do not overwrite an existing destination file. Leave conflicts in place and report them.
- Report which files were moved and which, if any, were skipped.
