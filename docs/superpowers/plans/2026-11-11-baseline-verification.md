# Baseline Installation and Verification Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Give every OpenCode defaults installation a portable content fingerprint, an installation receipt, safe retirement of content the baseline drops, and a read-only `--check` that shows whether an installation holds a selected baseline.

**Architecture:** Extend the existing standard-library `install.py` with `--fingerprint` and `--check` modes. All modes share the installer's managed-file list (`collect_files`) and merge rule (`merge_settings`), so they cannot disagree about what is managed. Install writes `opencode-defaults-receipt.json` last; the next install uses it to retire dropped content, and the check compares against it. `install.ps1` and `install.sh` only forward options.

**Tech Stack:** Python 3.10+ standard library (`hashlib`, `json`, `argparse`, `subprocess`, `shutil`, `dataclasses`), `unittest`, Windows PowerShell 5.1, POSIX `sh`.

**Spec:** [docs/baseline-verification-design.md](../../baseline-verification-design.md), plus the five amendments below. Task 1 writes them into the spec.

## Spec amendments

These came from three `/xm-spec-review` reports on 2026-11-11, and Patrick accepted trimmed #1 and #2–#5. Where they conflict with the spec text, they take precedence until Task 1 updates the spec.

1. **Keep `Local` reporting, but only to the first unowned item.** `--check` lists each local addition at the first level the baseline does not own and does not look inside it. Examples: `providers`, `mcp.servers.chrome-devtools`, `plugins (+1)`, `AGENTS.local.md`, `commands/add-notes.md`, `skills/custom-skill/`. `Local` lines never fail the check. They make unexpected additions visible: the Surface shows its expected workstation items, and `sim-funds` and `sim-prime-broker` should both show `Local none`. Intentional workspace differences belong in each simulator's repository.
2. **List order counts.** Configuration matches only when `merge_settings(installed, baseline) == installed`, including order. This replaces "ignoring order within `plugins`, `instructions`, and `skills`". OpenCode processes plugin entries, configured instructions and skill sources in order. A local entry placed where the installer would move it is drift, and reinstalling fixes it.
3. **`project-setup` reads the runtime version from `baseline.json`.** Its step 4 and README's requirement line replace `2.0.4+` with the exact version in `baseline.json`.
4. **Verify on Linux before rollout.** Skip the Windows-only tests on other platforms so the unit suite runs on Linux. Before any sim workspace is updated, run the suite, the `--fingerprint` comparison, and an isolated install, check, edit, check sequence on Linux. This replaces "Record the Linux result at rollout." The unit-test command never uses SSH.
5. **A damaged receipt stops installation.** A missing receipt means a first install. A receipt that exists but is unreadable, invalid or an unsupported format stops install and dry-run before any change, with recovery instructions; `--check` reports it as a finding. This replaces "Treat an unreadable or unknown-format receipt as absent."

## Global Constraints

- Python standard library only. `install.ps1` and `install.sh` remain the entry points. Existing destination resolution, merging, backups, `AGENTS.local.md` migration and the `opencode.jsonc` refusal stay as they are.
- `baseline.json` sits at the repository root and contains exactly `{"opencode": "2.2.7"}`.
- Receipt file: `opencode-defaults-receipt.json` in the destination.
- Fingerprint inputs: every `collect_files` source, plus `global/opencode.json` and `baseline.json`. Installer scripts, tests and docs are not inputs.
- `.gitattributes`: `* text=auto eol=lf`.
- Exit codes: `0` match; `1` any finding, install failure, or a check that could not complete; `2` usage error.
- Installing, checking and fingerprinting need no Git metadata, credentials or network access.
- Output names paths and setting paths only, never local setting values or file contents.
- Nothing is removed or overwritten without a backup under `<destination>/backups/harness-<timestamp>/`.
- Runtime probe: run `opencode --version`, looking on `PATH` and then in `~/.opencode/bin`. The version is the last whitespace-separated word, without a leading `v`.
- Each run reads one source folder and one destination, and never touches another workspace. Simulation requirements such as virtual time and hidden evaluation do not apply to this repository.
- The commands below are for Windows PowerShell 5.1, which does not support `&&`: run one command per line.

## Review Focus

1. Running `--check` on a destination that does not exist yet → findings and exit 1, without creating anything. Test in Task 5.
2. `opencode.json` with a UTF-8 BOM, invalid JSON, or an array at the top level → the BOM file passes; the others are a `Config unreadable` finding, without a Python traceback. Test in Task 5.
3. `opencode --version` output with Windows line endings, a `v` prefix, extra leading words, or a nonzero exit → either parsed correctly or reported as `failed`, never a crash. Test in Task 5.
4. A symlinked folder under `skills/` or `commands/` → listed once by name and never followed, so a loop cannot hang the check. Test in Task 6.
5. A fingerprint pasted with surrounding spaces or in uppercase → accepted after trimming and lowercasing. Test in Task 5.

---

### Task 1: Pre-flight and spec amendments

**Files:**
- Modify: `docs/baseline-verification-design.md`

- [ ] **Step 1: Confirm the starting point**

Run: `git status --short`
Expected: no changes to `README.md`, `AGENTS.md`, `install.py`, `install.ps1`, `.gitattributes`, `tests/`, `global/`, `.opencode/skills/` or `docs/`. If any appear, stop and ask Patrick. They belong to other work: do not stash, commit or discard them.

Run: `git ls-files global/commands`
Expected: five `xm-*.md` files, confirming the `/xm-*` work has been committed.

Run: `opencode --version`
Expected: `opencode v2.2.7`. If it differs, stop and ask Patrick whether to pin that version instead.

- [ ] **Step 2: Write the five amendments into the spec**

- Status line → "Approved for planning 2026-11-11, with the review amendments recorded under Decisions."
- "Goals and limits", fourth bullet → "Local additions survive and never fail the check, unless placed where the installer would reorder them."
- "Installation receipt": replace "Treat an unreadable or unknown-format receipt as absent." with amendment 5.
- "Check command": replace the sentence that ignores order with amendment 2. Rewrite the local-additions paragraph using amendment 1, keeping "names only", one sorted line per item, and never a finding. Add the `Local none` expectation for the sim workspaces.
- "Files and verification": add `.opencode/skills/project-setup/SKILL.md` (amendment 3). Replace "Record the Linux result at rollout." with amendment 4. Mark the `/xm-*` sequencing note as done.
- "Decisions": record the three reviews and Patrick's choice: trimmed #1 and #2–#5.

- [ ] **Step 3: Commit**

```powershell
git add docs/baseline-verification-design.md
git commit -m "docs: fold spec review amendments into baseline design"
```

---

### Task 2: Baseline identity and `--fingerprint`

**Files:**
- Create: `baseline.json`, `tests/test_baseline.py`
- Modify: `.gitattributes`, `install.py`, `tests/test_install.py` (`test_commands_install_back_up_and_preserve_local_files`)

**Interfaces:**
- Produces in `install.py`:
  - `BASELINE_FILE = "baseline.json"`
  - `class BaselineError(Exception)` — raised when `baseline.json` is missing, is not a JSON object, has an empty or non-string `opencode`, or contains any other key.
  - `load_baseline(repo_root: Path) -> str` — returns the pinned version.
  - `sha256_file(path: Path) -> str` — lowercase hex.
  - `managed_files(repo_root: Path) -> dict[str, Path]` — maps each destination-relative POSIX path to its source file, built from `collect_files`.
  - `fingerprint_inputs(repo_root: Path) -> list[tuple[str, Path]]` — source-relative POSIX paths and files, sorted by path.
  - `compute_fingerprint(repo_root: Path) -> str`
  - `main()` accepts `--fingerprint`. It cannot be combined with `--dry-run` or `--destination` (usage error). Every mode calls `load_baseline` before changing anything; a `BaselineError` prints a message to stderr and exits 1.
- Produces in `tests/test_baseline.py`, as module-level helpers for Tasks 3–7:
  - `REPO_ROOT: Path`
  - `DEFAULT_SOURCE: dict[str, bytes]` — fixed bytes. Do not edit it after this task, because `FIXTURE_FINGERPRINT` depends on it; later tests build variants with `{**DEFAULT_SOURCE, ...}`.
    - `baseline.json`: `b'{"opencode": "2.2.7"}\n'`
    - `global/AGENTS.md`: `b"# Test defaults\n"`
    - `global/opencode.json`: `b'{"model": "openai/gpt-6-astra", "agents": {"title": {"model": "openai/gpt-6.1-sol#medium"}}, "plugins": ["managed-plugin"], "instructions": ["~/.config/opencode/AGENTS.local.md"], "mcp": {"servers": {"context7": {"type": "remote", "url": "https://mcp.context7.com/mcp"}}}}\n'`
    - `global/commands/xm-demo.md`: `b"Demo $ARGUMENTS.\n"`
    - `.opencode/skills/demo/SKILL.md`: `b"---\nname: demo\ndescription: Demo\n---\nBody\n"`
  - `make_source(root: Path, files: dict[str, bytes] | None = None) -> Path` — writes `files` (default `DEFAULT_SOURCE`), copies `REPO_ROOT / "install.py"` into `root`, and returns `root`.
  - `run_installer(source: Path, *args: str, env: dict[str, str] | None = None) -> subprocess.CompletedProcess[str]` — runs `sys.executable source/install.py` with `source` as the working directory, capturing text output.
  - `cli_env(tmp: Path, version: str | None, *, output: str | None = None, exit_code: int = 0, in_home: bool = False, isolate: bool = True) -> dict[str, str]` — returns a copy of `os.environ` with a fake OpenCode CLI.
    - When `isolate` is true, `HOME` and `USERPROFILE` become `tmp/"home"`, and `PATH` becomes `tmp/"bin"` plus the original entries in which `shutil.which("opencode", path=entry)` finds nothing.
    - When `isolate` is false, the environment is unchanged except that `tmp/"bin"` is added to the front of `PATH`.
    - When `version` is given, write a fake that prints `output or f"opencode v{version}"` and exits with `exit_code`. Put it in `tmp/"bin"`, or in `tmp/"home"/".opencode"/"bin"` when `in_home` is true. On Windows it is `opencode.cmd` (`@echo off`, `echo ...`, `exit /b N`); elsewhere it is a `#!/bin/sh` script named `opencode` with mode `0o755`.
  - `snapshot(root: Path) -> dict[str, tuple[bytes, int]]` — maps each file's relative POSIX path to its bytes and `st_mtime_ns`; returns `{}` when `root` is missing.
  - `section(output: str, name: str) -> list[str]` — the stdout lines whose first word is `name`.

`cli_env`, `snapshot` and `section` are first used in Task 5, but define them here with the other helpers.

- [ ] **Step 1: Write the failing tests** in `tests/test_baseline.py`, class `FingerprintTests`:

```python
def test_fixed_fixture_value(self):  # DEFAULT_SOURCE -> recorded constant
    self.assertEqual(install.compute_fingerprint(make_source(tmp)), FIXTURE_FINGERPRINT)
def test_stable_and_ignores_non_inputs(self):
    # same value twice; adding README.md or tests/x.py, or editing the copied install.py, leaves it unchanged
def test_each_input_changes_value(self):
    # for every key in DEFAULT_SOURCE: append b"x" in a fresh copy -> value differs
def test_copy_without_git_matches_repo(self):
    # shutil.copytree(REPO_ROOT, tmp/"copy", ignore=shutil.ignore_patterns(".git")) -> equal fingerprints
def test_repo_inputs_have_no_crlf(self):
    for rel, path in install.fingerprint_inputs(REPO_ROOT):
        self.assertNotIn(b"\r\n", path.read_bytes(), rel)
def test_fingerprint_mode_prints_only_the_value(self):
    res = run_installer(src, "--fingerprint")
    self.assertEqual((res.returncode, res.stdout), (0, install.compute_fingerprint(src) + "\n"))
def test_bad_baseline_stops_every_mode_without_changes(self):
    # subTests: baseline.json missing, b"[]", b'{"opencode": ""}', b'{"opencode": "2.2.7", "x": 1}'
    # install, --dry-run and --fingerprint each -> returncode 1, "baseline.json" in stderr, snapshot(dest) == {}
def test_fingerprint_usage_errors(self):
    # --fingerprint --dry-run, --fingerprint --destination X -> returncode 2
```

Set `FIXTURE_FINGERPRINT = "<recorded in Step 4>"` for now.

- [ ] **Step 2: Run the tests to confirm they fail**

Run: `uv run --no-project python -m unittest discover -s tests -k FingerprintTests -v`
Expected: failures or errors, such as `module 'install' has no attribute 'compute_fingerprint'`.

- [ ] **Step 3: Implement**

- Add `baseline.json` containing `{"opencode": "2.2.7"}` and an LF line ending.
- Change `.gitattributes` line 2 to `* text=auto eol=lf`. Update its comment to say LF keeps the fingerprint identical across checkouts and archives.
- Add the `install.py` interfaces above. Use this fixed fingerprint format, which produces the same lines as `sha256sum`, sorted by path:

```python
manifest = "".join(f"{sha256_file(path)}  {rel}\n" for rel, path in fingerprint_inputs(repo_root))
return hashlib.sha256(manifest.encode("utf-8")).hexdigest()
```

- Add `baseline.json` to the synthetic source in `test_commands_install_back_up_and_preserve_local_files`.

- [ ] **Step 4: Record and cross-check `FIXTURE_FINGERPRINT`**

Create `DEFAULT_SOURCE` in a scratch folder under `$env:LOCALAPPDATA\Temp\opencode\` with `make_source`, then run `--fingerprint` there. Confirm the value independently in Git Bash from that folder:

```sh
sha256sum .opencode/skills/demo/SKILL.md baseline.json global/AGENTS.md global/commands/xm-demo.md global/opencode.json | LC_ALL=C sort -k2 | sha256sum
```

The two values must match. Paste the value into `FIXTURE_FINGERPRINT`, then delete the scratch folder.

- [ ] **Step 5: Run the whole suite**

Run: `uv run --no-project python -m unittest discover -s tests -v`
Expected: all tests pass.

Run: `git ls-files --eol`
Expected: every text file shows `i/lf w/lf`.

- [ ] **Step 6: Commit**

```powershell
git add baseline.json .gitattributes install.py tests/test_baseline.py tests/test_install.py
git commit -m "feat: add baseline.json and portable content fingerprint"
```

---

### Task 3: Installation receipt; a damaged receipt stops installation

**Files:**
- Modify: `install.py`, `tests/test_baseline.py`

**Interfaces:**
- Consumes: Task 2's `load_baseline`, `managed_files`, `compute_fingerprint` and `sha256_file`.
- Produces in `install.py`:
  - `RECEIPT_NAME = "opencode-defaults-receipt.json"`, `RECEIPT_FORMAT = 1`
  - `@dataclass(frozen=True) class Receipt: fingerprint: str; files: dict[str, str]; config: dict[str, Any]` — `files` maps each destination-relative POSIX path to its SHA-256; `config` is the parsed `global/opencode.json` that was installed.
  - `class ReceiptError(Exception)` — its message gives the reason.
  - `read_receipt(destination: Path) -> Receipt | None` — returns `None` only when the file does not exist. Raises `ReceiptError` when:
    - the file is unreadable or is not JSON;
    - `format` is not the integer `1`;
    - `fingerprint` or any file hash is not 64 lowercase hex characters;
    - `config` is not an object;
    - a `files` path is empty, absolute, contains `\` or a drive letter, has a `..` part, or resolves outside the destination.
  - `write_receipt(destination: Path, receipt: Receipt) -> None` — writes JSON keys `format`, `fingerprint`, `files` and `config`, with `indent=2`, `sort_keys=True` and LF line endings. Write `RECEIPT_NAME + ".tmp"` first, then replace the receipt with `os.replace`.
  - `verify_installed(destination: Path, expected: dict[str, str]) -> list[str]` — returns sorted relative paths that are missing or whose installed hash differs from `expected`.
  - `run_install(repo_root: Path, destination: Path, *, dry_run: bool) -> int` — the existing installation logic, moved out of `main`.

**Install order:**

1. Load `baseline.json`.
2. Refuse `opencode.jsonc`.
3. Call `read_receipt`. If it raises `ReceiptError`, exit 1 without writing anything, in dry-run as well. The stderr message names the receipt path and the reason, then says: "Restore it from `<destination>/backups/harness-*/opencode-defaults-receipt.json`, or move it aside to install without retirement history; content retired since the last install then stays behind as local additions."
4. Run the existing steps: merge settings, migrate `AGENTS.md`, prune retired files, and copy managed files.
5. Call `verify_installed`. If it returns any paths, list them on stderr, exit 1, and leave the receipt untouched.
6. Back up the previous receipt into the same backup folder.
7. Call `write_receipt`.

- [ ] **Step 1: Write the failing tests**, class `ReceiptTests`:

```python
def test_install_writes_receipt(self):
    # format 1; fingerprint == compute_fingerprint(src); files == {rel: sha256 of source} for managed_files(src);
    # config == json.loads(DEFAULT_SOURCE["global/opencode.json"])
def test_repeat_install_keeps_receipt_and_backs_up_previous(self):
    # 2nd install: receipt bytes identical; backups/harness-*/opencode-defaults-receipt.json exists
def test_dry_run_writes_no_receipt(self):  # snapshot(dest) unchanged
def test_damaged_receipt_stops_install_and_dry_run(self):
    # subTests: b"not json", format 2, fingerprint "XYZ", files {"../escape": hash}, files {"/abs": hash},
    # files {"C:/x": hash}, config [] -> install and --dry-run: returncode 1,
    # RECEIPT_NAME and "backups" in stderr, snapshot(dest) identical before/after
def test_failed_verification_keeps_old_receipt(self):
    # in-process: install.run_install(src, dest, dry_run=False); then with
    # mock.patch("install.verify_installed", return_value=["AGENTS.md"]) -> run_install(...) == 1,
    # receipt bytes unchanged
```

- [ ] **Step 2: Run the tests to confirm they fail**

Run: `uv run --no-project python -m unittest discover -s tests -k ReceiptTests -v`
Expected: failures, because no receipt is written or `install` has no `read_receipt`.

- [ ] **Step 3: Implement** the interfaces and install order above.

- [ ] **Step 4: Run the whole suite**

Run: `uv run --no-project python -m unittest discover -s tests -v`
Expected: all tests pass, including the unchanged existing installer tests.

- [ ] **Step 5: Commit**

```powershell
git add install.py tests/test_baseline.py
git commit -m "feat: write installation receipt and stop on a damaged one"
```

---

### Task 4: Retire content the baseline no longer ships

**Files:**
- Modify: `install.py`, `tests/test_baseline.py`

**Interfaces:**
- Consumes: `Receipt`, `read_receipt`, `managed_files`, `sha256_file`, `backup_file` and `merge_settings`.
- Produces in `install.py`:
  - `plan_file_retirement(destination: Path, receipt: Receipt, managed: set[str]) -> tuple[list[str], list[str]]` — returns two lists: unchanged retired files to remove, and locally changed retired files to keep. It covers receipt files that are no longer in `managed` but still exist. A file is unchanged when its hash still matches the receipt.
  - `retire_settings(current: dict[str, Any], previous: dict[str, Any], incoming: dict[str, Any]) -> tuple[dict[str, Any], list[str], list[str]]` — returns a cleaned copy of `current`, plus the display paths removed and kept. It never changes its inputs.

`retire_settings` follows these rules while walking `previous`. Display paths use dot notation.

- **Root `plugins`, `instructions` and `skills`:** remove from `current` each entry that is in `previous` but no longer in `incoming`, and display `plugins (-N)`. Remove a list that this leaves empty.
- **`mcp.servers.<name>` missing from `incoming`:** remove it when `current` matches `previous`; otherwise keep it and name `mcp.servers.<name>`.
- **Objects:** when an object exists in `previous` and `current`, and `incoming` has an object or nothing at that path, recurse into it. Remove an object that this leaves empty, but keep one that was already empty.
- **Other values missing from `incoming`:** remove a value that still equals `previous`; otherwise keep it and name it.
- **Keys still in `incoming`, or whose type changed:** leave them to `merge_settings`.

When a receipt exists, installation runs `retire_settings(current_cfg, receipt.config, incoming_cfg)` before `merge_settings`. After copying the managed files, it backs up and deletes each unchanged retired file. It then removes any parent folders left empty, without removing the destination itself.

The hard-coded `RETIRED_PR4_*` cleanup runs only when there is no receipt. The installer prints each kept file or setting once, as "Kept locally changed retired …: <path>". Dry-run prints what it would remove and keep, and writes nothing.

- [ ] **Step 1: Write the failing tests**, class `RetirementTests`. Sources A and B are variants of `DEFAULT_SOURCE`; install A, then B, into the same destination.

```python
def test_untouched_retired_files_removed_with_backup(self):
    # A adds global/commands/xm-old.md and .opencode/skills/old/SKILL.md + references/r.md; B drops them
    # -> files and skills/old/ gone; skills/ and commands/ remain; backups hold all three; receipt lacks them
def test_locally_changed_retired_file_kept_and_named_once(self):
    # edit commands/xm-old.md before installing B -> file kept; stdout.count("commands/xm-old.md") == 1
def test_untouched_retired_settings_removed(self):
    # A config adds agents.old.model, mcp.servers.old {...}, plugins "p-old"; B drops them
    # local "providers" and plugin "p-local" survive; "old" not in agents; "old" not in mcp.servers
def test_locally_changed_retired_settings_kept_and_named(self):
    # change agents.old.model and mcp.servers.old.url locally -> both kept; stdout names
    # "agents.old.model" and "mcp.servers.old"
def test_objects_emptied_by_removal_are_removed(self):
    # A has only {"agents": {"old": {"model": "x"}}}; B {} -> "agents" absent; a local "experimental": {} survives
def test_dry_run_lists_retirement_without_changes(self):
    # B --dry-run names commands/xm-old.md; snapshot(dest) unchanged
def test_hard_coded_retirement_only_without_receipt(self):
    # no receipt: commands/sessions-move.md removed, unknown commands/mine.md kept
    # with receipt: a re-created commands/sessions-move.md survives reinstall
```

- [ ] **Step 2: Run the tests to confirm they fail**

Run: `uv run --no-project python -m unittest discover -s tests -k RetirementTests -v`
Expected: failures, because retired files and settings remain.

- [ ] **Step 3: Implement** the interfaces and installation changes above.

- [ ] **Step 4: Run the whole suite**

Run: `uv run --no-project python -m unittest discover -s tests -v`
Expected: all tests pass.

- [ ] **Step 5: Commit**

```powershell
git add install.py tests/test_baseline.py
git commit -m "feat: retire content dropped from the baseline using the receipt"
```

---

### Task 5: Read-only `--check`

**Files:**
- Modify: `install.py`, `tests/test_baseline.py`

**Interfaces:**
- Consumes: `load_baseline`, `compute_fingerprint`, `managed_files`, `read_receipt` and `sha256_file` from Tasks 2–3, plus `merge_settings` and `default_destination`.
- Produces in `install.py`:
  - `probe_opencode_version(timeout: float = 10.0) -> tuple[Literal["ok", "missing", "failed"], str]` — finds `shutil.which("opencode")`, or else `shutil.which("opencode", path=str(Path.home() / ".opencode" / "bin"))`, then runs `[exe, "--version"]`. It returns `failed` on a timeout, `OSError`, nonzero exit or empty output, and reads the version as described in Global Constraints.
  - `config_drift_paths(installed: dict[str, Any], expected: dict[str, Any]) -> list[str]` — sorted dot paths where the two differ. Lists are compared whole and in order; each `mcp.servers.<name>` is compared as one unit.
  - `run_check(repo_root: Path, destination: Path, expect: str | None) -> int`
  - `CHECK_SCOPE_NOTE = "Covers the installed global baseline only; project or system overrides, plugin loading, MCP connectivity, provider access and model behavior are not checked."`
  - `main()` adds `--check` and `--expect FINGERPRINT`.
    - `--check`, `--dry-run` and `--fingerprint` cannot be combined.
    - `--expect` requires `--check`. Its value is trimmed and lowercased, then must be 64 hex characters.
    - Violations call `parser.error`, which exits 2.

**Check behavior:**

- Print one item per line: the section name, one space, then the item. Sections appear in this order: `Destination`, `Baseline`, `Receipt`, `Files`, `Config`, `Runtime`, `Local`, `Result`, followed by `CHECK_SCOPE_NOTE`. Until Task 6, print `Local none`. Sort items within each section.
- Finding formats:
  - `Baseline mismatch`
  - `Receipt missing`, `Receipt invalid` or `Receipt differs`
  - `Files missing <path>` or `Files edited <path>`
  - `Config differs <path>`, `Config missing opencode.json`, `Config unreadable opencode.json` or `Config present opencode.jsonc`
  - `Runtime missing`, `Runtime failed` or `Runtime mismatch <found> (baseline <pinned>)`
- A section without findings prints `ok`.
- `Result MATCH` exits 0. `Result DRIFT, N findings` exits 1.
- Configuration matches when `merge_settings(installed, baseline) == installed`.
- A `BaselineError` prints the error and `Result could not complete`, then exits 1.
- The check never writes or creates anything.

- [ ] **Step 1: Write the failing tests**, class `CheckTests`. Unless a test says otherwise, use `env=cli_env(tmp, "2.2.7")`.

```python
def test_check_passes_after_install(self):
    # returncode 0; section(out, "Result") == ["Result MATCH"]; CHECK_SCOPE_NOTE in out
def test_expect_match_mismatch_and_pasted_value(self):  # Review Focus 5
    # --expect fp -> 0; --expect "0"*64 -> 1 with "mismatch"; --expect f"  {fp.upper()}  " -> 0
def test_receipt_findings(self):
    # missing; invalid (b"not json") reported and the rest still checked; differs (installed from A, checked from B)
def test_file_findings(self):
    # delete commands/xm-demo.md -> "missing commands/xm-demo.md"; append to skills/demo/SKILL.md -> "edited ..."
def test_config_drift_cases(self):
    # subTests, each -> exit 1 and the named path in a Config line:
    # model changed -> "model"; mcp.servers.context7 altered or removed -> "mcp.servers.context7";
    # "small_model" added -> "small_model"; instructions entry removed -> "instructions";
    # local plugin inserted before "managed-plugin" -> "plugins";
    # with a source variant whose plugins hold a pinned Superpowers ref, a second Superpowers ref -> "plugins"
def test_reorder_is_fixed_by_reinstall(self):
    # local plugin first -> exit 1; reinstall -> check exit 0; plugins == ["managed-plugin", "p-local"]
def test_properly_placed_local_additions_pass(self):
    # append plugin, add providers {...}, mcp.servers.local {...}, commands/mine.md -> exit 0
def test_pass_implies_reinstall_changes_nothing(self):
    # from the passing state above: snapshot managed files, parsed opencode.json and receipt; reinstall; all equal
def test_opencode_jsonc_is_a_finding(self):
def test_runtime_findings(self):  # Review Focus 3
    # cli_env(tmp, None) -> "Runtime missing"; version "2.2.5" -> "mismatch 2.2.5 (baseline 2.2.7)";
    # exit_code=3 -> "failed"; output="OpenCode CLI version v2.2.7" -> ok;
    # in_home=True (fake only in HOME/.opencode/bin) -> ok
def test_check_on_missing_destination(self):  # Review Focus 1
    # returncode 1; destination still does not exist
def test_bom_invalid_and_non_object_config(self):  # Review Focus 2
    # BOM-encoded opencode.json -> passes; b"{" and b"[]" -> "Config unreadable opencode.json"; "Traceback" not in stderr
def test_bad_baseline_check_could_not_complete(self):
    # baseline.json missing -> returncode 1, "could not complete" in stdout
def test_check_is_read_only(self):
    # drifted destination: snapshot before == after
def test_check_uses_default_destination(self):
    # XDG_CONFIG_HOME=tmp/xdg; install and check without --destination -> 0
def test_check_usage_errors(self):
    # --expect alone, --check --dry-run, --check --fingerprint, --check --expect nothex -> 2
```

- [ ] **Step 2: Run the tests to confirm they fail**

Run: `uv run --no-project python -m unittest discover -s tests -k CheckTests -v`
Expected: failures with `unrecognized arguments: --check`.

- [ ] **Step 3: Implement** the interfaces and check behavior above.

- [ ] **Step 4: Run the whole suite**

Run: `uv run --no-project python -m unittest discover -s tests -v`
Expected: all tests pass.

- [ ] **Step 5: Commit**

```powershell
git add install.py tests/test_baseline.py
git commit -m "feat: add read-only --check against the selected baseline"
```

---

### Task 6: List local additions at the first unowned level

**Files:**
- Modify: `install.py`, `tests/test_baseline.py`

**Interfaces:**
- Consumes: `run_check` and `managed_files`.
- Produces in `install.py`:
  - `LOCAL_SCAN_DIRS = ("agents", "commands", "skills", "plugins")`
  - `list_local_additions(destination: Path, installed_cfg: dict[str, Any] | None, baseline_cfg: dict[str, Any], managed: set[str]) -> list[str]` — returns a sorted list.

**Rules:**

- **Configuration** is skipped when `installed_cfg` is `None`.
  - List a key absent from the baseline at its level by its dot path, and do not look inside it.
  - Look inside objects both configurations contain, except under `mcp.servers`, where only server names are compared.
  - For root `plugins`, `instructions` and `skills`, list `<key> (+N)`, where N is the number of entries absent from the baseline.
- **Files** are checked under each `LOCAL_SCAN_DIRS` folder:
  - List a folder containing no managed file once, as `<path>/`, without looking inside it.
  - List an unmanaged file by its path.
  - List a symlink by name and never follow it.
- **`AGENTS.local.md`** is listed when present. Nothing else in the destination root is scanned.

`run_check` prints one `Local <item>` line for each addition, or `Local none` when there are none. These lines never count as findings.

- [ ] **Step 1: Write the failing tests**, class `LocalTests`:

```python
def test_config_reported_at_first_boundary(self):
    # providers.openrouter.settings.apiKey="secret-value", mcp.servers.chrome-devtools, agents.title.temperature,
    # one extra plugin -> Local lines exactly ["Local agents.title.temperature", "Local mcp.servers.chrome-devtools",
    # "Local plugins (+1)", "Local providers"]; "secret-value" not in stdout; returncode 0
def test_files_and_folders(self):
    # commands/add-notes.md, skills/custom-skill/SKILL.md + ref.md, plugins/x.ts, AGENTS.local.md
    # -> commands/add-notes.md, skills/custom-skill/, plugins/, AGENTS.local.md listed once each;
    # managed files, backups/, receipt and service.json not listed
def test_clean_install_prints_local_none(self):
def test_symlinked_directory_listed_not_followed(self):  # Review Focus 4
    # skills/loop -> symlink to skills/; self.skipTest when os.symlink raises OSError
    # -> "Local skills/loop" once; returns promptly
def test_kept_retired_file_shows_as_local(self):
    # Task 4's locally changed retired file -> listed under Local; check exit 0
```

- [ ] **Step 2: Run the tests to confirm they fail**

Run: `uv run --no-project python -m unittest discover -s tests -k LocalTests -v`
Expected: failures, because only `Local none` is printed.

- [ ] **Step 3: Implement** `list_local_additions` and use it in `run_check`.

- [ ] **Step 4: Run the whole suite**

Run: `uv run --no-project python -m unittest discover -s tests -v`
Expected: all tests pass.

- [ ] **Step 5: Commit**

```powershell
git add install.py tests/test_baseline.py
git commit -m "feat: list local additions at the first unowned boundary"
```

---

### Task 7: Add wrapper modes and run the suite on Linux

**Files:**
- Modify: `install.ps1`, `tests/test_install.py`, `tests/test_baseline.py`

**Interfaces:**
- Consumes: the `install.py` options `--check`, `--expect`, `--fingerprint`, `--dry-run` and `--destination`.
- Produces: `install.ps1` parameters `[switch]$Check`, `[switch]$Fingerprint` and `[string]$Expect = ''`, passed through as `--check`, `--fingerprint` and `--expect <value>`.
  - `-WhatIf` still maps to `--dry-run`.
  - `install.py` validates combinations.
  - Exit codes pass through as they do today.
  - `install.sh` is unchanged.

- [ ] **Step 1: Write the failing tests**

In `tests/test_install.py`, split `test_wrappers_ps1_and_sh` into two tests that keep their current assertions:

- `test_ps1_wrapper`, with `@unittest.skipUnless(sys.platform == "win32", ...)`.
- `test_sh_wrapper`, skipped when `shutil.which("sh")` finds nothing and, on Windows, `C:\Program Files\Git\bin\sh.exe` is also absent.

In `tests/test_baseline.py`, add class `WrapperTests`. Use `cli_env(tmp, "2.2.7", isolate=False)` so `uv` still resolves:

```python
@unittest.skipUnless(sys.platform == "win32", "Windows PowerShell")
def test_ps1_modes(self):
    # -Fingerprint stdout == run_installer(REPO_ROOT, "--fingerprint").stdout
    # install to tmp, then -Check -Expect fp -> 0; -Check on an empty folder -> 1; -Expect without -Check -> 2
def test_sh_modes(self):  # same skip rule as test_sh_wrapper
    # same three outcomes via sh ./install.sh
```

- [ ] **Step 2: Run the tests to confirm they fail**

Run: `uv run --no-project python -m unittest discover -s tests -k WrapperTests -v`
Expected: `test_ps1_modes` fails because `-Fingerprint` is not a parameter.

- [ ] **Step 3: Implement** the `install.ps1` parameters.

- [ ] **Step 4: Run the whole suite**

Run: `uv run --no-project python -m unittest discover -s tests -v`
Expected: all tests pass.

- [ ] **Step 5: Commit**

```powershell
git add install.ps1 tests/test_install.py tests/test_baseline.py
git commit -m "feat: expose check and fingerprint modes in both wrappers"
```

---

### Task 8: Update documentation and the `project-setup` runtime version

**Files:**
- Modify: `README.md`, `AGENTS.md`, `.opencode/skills/project-setup/SKILL.md`, `docs/cross-model-workflow-design.md`

- [ ] **Step 1: Update `project-setup` step 4**

Replace "Verify `opencode` V2 (`2.0.4+`)". The new text checks that `opencode --version` equals the `opencode` value in the defaults source's `baseline.json`. If OpenCode is missing or the version differs, load `opencode` and install that exact version with `curl -fsSL https://opencode.ai/v2/install | bash -s -- --version <version>` or `opencode upgrade <version>`. Keep the rest of the step.

- [ ] **Step 2: Update the README**

- Requirement line: the exact OpenCode version in `baseline.json`, plus Python 3.10+ or `uv`. Git is needed only for cloning.
- Halo install block:
  - Pass `--version <version from baseline.json>` to the OpenCode install script.
  - Explain that a workspace without repository access receives an extracted archive of the selected commit from `ops-infra`. The installer does not need `.git`.
- Add a "Baseline and Check" section covering:
  - `--fingerprint`, `--check` and `--check --expect`, with `-Fingerprint`, `-Check` and `-Expect` for PowerShell, plus their exit codes.
  - What `Local` lines mean: the Surface shows its workstation items, while `sim-funds` and `sim-prime-broker` should show `Local none`.
  - Changing the baseline: edit, test, commit, run `--fingerprint`, then record the commit, fingerprint and CLI version in `ops-infra`.
  - Updating `baseline.json` after any OpenCode upgrade, because the check reports a runtime mismatch on upgraded machines until then.
  - The scope limits from `CHECK_SCOPE_NOTE`, and that the check detects accidental drift but is not tamper-proof.
- Installer Behavior:
  - Replace "Managed command names are replaced on update…" with receipt-based retirement: unchanged retired content is removed with a backup, while locally changed content is kept and named.
  - Describe the damaged-receipt stop and name the receipt file.
- Superpowers upgrade step 4: rerun the installer, then run `--check --expect`.

- [ ] **Step 3: Update `AGENTS.md`**

- Source Layout: add `baseline.json` (the pinned OpenCode version, also part of the fingerprint), and add `tests/test_baseline.py` to the `install.py` line.
- Maintenance: end the test line with "… and run install, then `--check`, against an isolated `--destination` after installer edits."
- Trim wording elsewhere so the file grows by no more than these items.

- [ ] **Step 4: Update the cross-model design**

Replace the "Removing or renaming a command" bullet: the receipt removes an unchanged retired command on the next install, so no `install.py` change is needed.

- [ ] **Step 5: Verify**

Run: `uv run --no-project --with "git+https://github.com/agentskills/agentskills.git#subdirectory=skills-ref" python -m skills_ref.cli validate .opencode/skills/project-setup`
Expected: the skill validates. This command needs network access to fetch `skills-ref`.

Run: `uv run --no-project python -m unittest discover -s tests -v`
Expected: all tests pass. `project-setup/SKILL.md` affects the repository fingerprint, but not `FIXTURE_FINGERPRINT`.

Run: `rg -n "2\.0\.4" README.md .opencode`
Expected: no matches.

- [ ] **Step 6: Commit**

```powershell
git add README.md AGENTS.md .opencode/skills/project-setup/SKILL.md docs/cross-model-workflow-design.md
git commit -m "docs: document baseline check and pin runtime from baseline.json"
```

---

### Task 9: Windows and Linux acceptance

This task tests the committed build end to end. It changes no code and records the results in the spec.

**Files:**
- Modify: `docs/baseline-verification-design.md`, adding a "Verified" section

- [ ] **Step 1: Test Windows with an isolated destination**

```powershell
$tmp = Join-Path $env:LOCALAPPDATA 'Temp\opencode\baseline-verify.tmp'
New-Item -ItemType Directory -Force -Path "$tmp\src" | Out-Null
git archive --format=tar -o "$tmp\src.tar" HEAD
tar -xf "$tmp\src.tar" -C "$tmp\src"
$fp = (uv run --no-project python "$tmp\src\install.py" --fingerprint).Trim()
uv run --no-project python install.py --fingerprint
powershell -NoProfile -ExecutionPolicy Bypass -File ./install.ps1 -Destination "$tmp\dest"
powershell -NoProfile -ExecutionPolicy Bypass -File ./install.ps1 -Check -Expect $fp -Destination "$tmp\dest"
"exit=$LASTEXITCODE"
Add-Content -LiteralPath "$tmp\dest\skills\writer\SKILL.md" -Value 'edit'
powershell -NoProfile -ExecutionPolicy Bypass -File ./install.ps1 -Check -Expect $fp -Destination "$tmp\dest"
"exit=$LASTEXITCODE"
```

Expected:
- The checkout and archive fingerprints are equal.
- The first check shows `Result MATCH`, `Local none` and `exit=0`.
- The second check shows `Files edited skills/writer/SKILL.md` and `exit=1`.

Do not run the installer against the real `~/.config/opencode`; deployment is a separate step.

- [ ] **Step 2: Confirm the Linux test container is reachable**

This uses the disposable `workspace-smoke` container through its existing SSH alias.

Run: `ssh workspace-smoke "hostname; id -un; python3 --version"`
Expected: the smoke container's hostname, `builder`, and Python 3.10 or later.

If the container is unreachable, stop and report the Linux verification as pending. Do not start or change containers; that work belongs to `ops-infra`.

- [ ] **Step 3: Run the Linux checks**

```powershell
ssh workspace-smoke "rm -rf /tmp/baseline-verify.tmp; mkdir -p /tmp/baseline-verify.tmp/src"
cmd /c "ssh workspace-smoke tar -xf - -C /tmp/baseline-verify.tmp/src < $tmp\src.tar"
ssh workspace-smoke "cd /tmp/baseline-verify.tmp/src && python3 -m unittest discover -s tests -v"
ssh workspace-smoke "sh /tmp/baseline-verify.tmp/src/install.sh --fingerprint"
ssh workspace-smoke "sh /tmp/baseline-verify.tmp/src/install.sh --destination /tmp/baseline-verify.tmp/dest"
ssh workspace-smoke "sh /tmp/baseline-verify.tmp/src/install.sh --check --expect $fp --destination /tmp/baseline-verify.tmp/dest; echo exit=`$?"
ssh workspace-smoke "printf 'edit\n' >> /tmp/baseline-verify.tmp/dest/skills/writer/SKILL.md"
ssh workspace-smoke "sh /tmp/baseline-verify.tmp/src/install.sh --check --expect $fp --destination /tmp/baseline-verify.tmp/dest; echo exit=`$?"
ssh workspace-smoke "rm -rf /tmp/baseline-verify.tmp"
Remove-Item -LiteralPath $tmp -Recurse -Force
```

`cmd /c` keeps the archive stream binary; Windows PowerShell 5.1 pipes would corrupt it. The `&&` above runs inside the remote Linux shell, not in PowerShell.

Expected:
- The unit suite passes, with only Windows-only tests skipped and `FIXTURE_FINGERPRINT` passing on Linux.
- The Linux `--fingerprint` equals `$fp`.
- The first check shows `Baseline`, `Receipt`, `Files` and `Config` as `ok`, and `Local none`.
- If OpenCode 2.2.7 is absent from the container, `Runtime missing` is the only finding and the check prints `exit=1`. Otherwise it prints `exit=0`.
- The second check adds `Files edited skills/writer/SKILL.md`.

- [ ] **Step 4: Record the results**

Add a "Verified" section to the spec with:
- the date, commit and fingerprint;
- the Windows and Linux results;
- the OpenCode runtime found in `workspace-smoke`.

Also note that `sim-funds` and `sim-prime-broker` were last recorded running OpenCode 2.2.5. They will report `Runtime mismatch` until rollout upgrades them.

- [ ] **Step 5: Commit**

```powershell
git add docs/baseline-verification-design.md
git commit -m "docs: record Windows and Linux baseline verification"
```

---

Rollout to `sim-funds` and `sim-prime-broker` belongs to `ops-infra` and starts after Task 9. It covers delivering the source, installing the pinned CLI, running the installer, and running `--check --expect` with `Local none` expected.
