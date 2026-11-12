# Baseline Installation and Verification Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Give every OpenCode defaults installation a portable content fingerprint, an installation receipt, safe retirement of content the baseline drops, and a read-only `--check` that shows whether an installation holds a selected baseline.

**Architecture:** Extend the existing standard-library `install.py` with `--fingerprint` and `--check` modes. All modes share the installer's managed-file list (`collect_files`) and merge rule (`merge_settings`), so they cannot disagree about what is managed. Install writes `opencode-defaults-receipt.json` last; the next install uses it to retire dropped content, and the check compares against it. `install.ps1` and `install.sh` only forward options.

**Tech Stack:** Python 3.10+ standard library (`hashlib`, `json`, `argparse`, `subprocess`, `shutil`, `dataclasses`), `unittest`, Windows PowerShell 5.1, POSIX `sh`.

**Spec:** [docs/baseline-verification-design.md](../../baseline-verification-design.md), plus the five amendments below. Task 1 writes them into the spec.

**Revision:** Both requested reviews have been reconciled into this draft. Awaiting implementation approval. Commands and tests below are planned verification, not results.

## Review reconciliation

The technical and simplification reviewers reported the same unchanged inputs: plan Git blob hash `22f4578ae34547177486711f1f7a3d5a22b97bc7`, spec Git blob hash `83baa335e235b41f42fa81355003c49e735e6c44`. Their repository HEADs differed; the reviewed plan and spec contents did not. Those hashes identify the pre-revision draft.

- Address all seven technical finding groups: explicit empty `--expect` rejection; retirement before incoming copies; precise local-reporting rules; the complete scope note; explicit text-mode fingerprint cross-check; input/receipt/path validation; and pre-flight/test-fixture corrections.
- Treat claims about native output formatting as portability concerns: accept both `2.2.7` and `opencode v2.2.7`, and select `sha256sum -t` explicitly. Neither requires assuming one platform's output is universal.
- Accept all three optional simplifications: combine check and local reporting into Task 5, isolate CLI tests with a fake-only PATH, and use a small synthetic copy for the no-Git unit test. Keep the real archive comparison in acceptance.
- Preserve trimmed `Local` reporting. Scan roots are containers; report their children, ignore directly empty directories, and stop at a nonempty unowned directory. Do not recursively classify that directory's contents just to determine whether every descendant is empty.
- Require a successful Linux check with the pinned runtime before declaring rollout readiness. A missing runtime is useful negative-test evidence, but leaves live Linux acceptance pending.

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
4. A symlinked folder under `skills/` or `commands/` → listed once by name and never followed; a symlink at a managed path is a file finding. Test in Task 5.
5. A fingerprint pasted with surrounding spaces or in uppercase → accepted after trimming and lowercasing; an explicitly empty or whitespace-only value is usage error 2. Test in Tasks 5–6.

---

### Task 1: Pre-flight and spec amendments

**Files:**
- Modify: `docs/baseline-verification-design.md`
- Retain in the implementation history: this approved plan.

- [ ] **Step 1: Confirm the starting point**

Run: `git status --short`
Inspect the diff before editing overlapping files. This plan's own untracked or modified path is expected and is not a blocker. Preserve unrelated work. If another unfinished change overlaps the installer, its tests, the setup skill or documentation being edited, coordinate that overlap before touching it; do not stash, commit or discard somebody else's changes.

Run: `git ls-files global/commands`
Expected: five `xm-*.md` files, confirming the `/xm-*` work has been committed.

Run: `opencode --version`
Accept output whose last word, after removing one leading `v`, is `2.2.7` (including `2.2.7` and `opencode v2.2.7`). Record an absent or different runtime as an acceptance prerequisite; keep the approved `2.2.7` pin. Implementation tests use an isolated fake CLI.

- [ ] **Step 2: Write the five amendments into the spec**

- Status line → "Approved for planning 2026-11-11, with the review amendments recorded under Decisions."
- "Goals and limits", fourth bullet → "Local additions survive and never fail the check, unless placed where the installer would reorder them."
- "Installation receipt": replace "Treat an unreadable or unknown-format receipt as absent." with amendment 5.
- "Check command": replace the sentence that ignores order with amendment 2. Remove the earlier scratch experiment's claim that unordered matching establishes the final comparison rule. Rewrite the local-additions paragraph using amendment 1, keeping "names only", one sorted line per item, and never a finding. Add the `Local none` expectation for the sim workspaces.
- "Files and verification": add `.opencode/skills/project-setup/SKILL.md` (amendment 3). Replace "Record the Linux result at rollout." with amendment 4. Mark the `/xm-*` sequencing note as done.
- "Decisions": record the three reviews and Patrick's choice: trimmed #1 and #2–#5.

- [ ] **Step 3: Commit**

```powershell
git add docs/baseline-verification-design.md docs/superpowers/plans/2026-11-11-baseline-verification.md
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
  - `class BaselineError(Exception)` — raised when `baseline.json` is missing, unreadable, invalid UTF-8/JSON, not an object, or does not contain exactly one `opencode` key with a nonempty, non-whitespace string value.
  - `load_baseline(repo_root: Path) -> str` — returns the stripped pinned version. Convert `OSError`, `UnicodeDecodeError` and `json.JSONDecodeError` into a concise filename/reason error; do not print file contents or a traceback.
  - `sha256_file(path: Path) -> str` — lowercase hex.
  - `managed_files(repo_root: Path) -> dict[str, Path]` — maps each destination-relative POSIX path to its source file, built from `collect_files`.
  - `fingerprint_inputs(repo_root: Path) -> list[tuple[str, Path]]` — source-relative POSIX paths and files, sorted by path.
  - `compute_fingerprint(repo_root: Path) -> str` — hashes raw input bytes; parsing `baseline.json` is the caller's responsibility. Source-file read failures become a concise error and exit 1 at the CLI boundary.
  - `main()` accepts `--fingerprint`. It cannot be combined with `--dry-run` or `--destination` (usage error). Every mode calls `load_baseline` before changing anything; a `BaselineError` prints a message to stderr and exits 1.
- Produces in `tests/test_baseline.py`, as module-level helpers for Tasks 3–6:
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
    - When `isolate` is true, `HOME` and `USERPROFILE` become `tmp/"home"`, and `PATH` contains only `tmp/"bin"`. Python is invoked through absolute `sys.executable`; the POSIX fake uses absolute `/bin/sh`. Retain Windows `SystemRoot` and `ComSpec` from the copied environment.
    - When `isolate` is false, the environment is unchanged except that `tmp/"bin"` is added to the front of `PATH`.
    - When `version` is given, print `output if output is not None else f"opencode v{version}"` and exit with `exit_code`. Put the fake in `tmp/"bin"`, or `tmp/"home"/".opencode"/"bin"` when `in_home` is true. On Windows use `opencode.cmd` with `@echo off` and `exit /b N`; emit no output command for an empty string, and use `echo(` for nonempty lines so whitespace does not become `ECHO is off.`. Elsewhere use a `#!/bin/sh` script named `opencode` with mode `0o755`. Each test case gets fresh temporary directories so an earlier fake cannot affect the missing-runtime case.
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
def test_synthetic_copy_without_git_matches(self):
    # copy make_source(tmp/"source") to tmp/"copy"; neither contains .git;
    # both --fingerprint CLI calls exit 0 with the same fixed fingerprint
def test_repo_inputs_have_no_crlf(self):
    for rel, path in install.fingerprint_inputs(REPO_ROOT):
        self.assertNotIn(b"\r\n", path.read_bytes(), rel)
def test_fingerprint_mode_prints_only_the_value(self):
    res = run_installer(src, "--fingerprint")
    self.assertEqual((res.returncode, res.stdout), (0, install.compute_fingerprint(src) + "\n"))
def test_bad_baseline_stops_every_mode_without_changes(self):
    # subTests: baseline.json missing, b"{", b"[]", invalid UTF-8, {}, {"opencode": 1},
    # {"opencode": ""}, {"opencode": "  "}, {"opencode": "2.2.7", "x": 1}
    # install, --dry-run and --fingerprint each -> returncode 1, "baseline.json" in stderr,
    # no traceback, destination remains absent; repeat against a populated destination and assert no writes
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
- Add the `install.py` interfaces above. Use this fixed fingerprint format, which produces the same lines as `sha256sum -t`, sorted by POSIX source path:

```python
manifest = "".join(f"{sha256_file(path)}  {rel}\n" for rel, path in fingerprint_inputs(repo_root))
return hashlib.sha256(manifest.encode("utf-8")).hexdigest()
```

- Add `baseline.json` to the synthetic source in `test_commands_install_back_up_and_preserve_local_files`.

- [ ] **Step 4: Record and cross-check `FIXTURE_FINGERPRINT`**

Create `DEFAULT_SOURCE` in a scratch folder under `$env:LOCALAPPDATA\Temp\opencode\` with `make_source`, then run `--fingerprint` there. Confirm the value independently in Git Bash from that folder:

```sh
sha256sum -t .opencode/skills/demo/SKILL.md baseline.json global/AGENTS.md global/commands/xm-demo.md global/opencode.json | LC_ALL=C sort -k2 | sha256sum -t
```

Compare the first 64-character digest from each command. `-t` explicitly selects the two-space manifest separator on Git Bash; all fixture input bytes are LF-only. Paste the matching value into `FIXTURE_FINGERPRINT`, then delete only the scratch folder created for this test.

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
  - `read_receipt(destination: Path) -> Receipt | None` — returns `None` only for genuine absence, established with `lstat` rather than `is_file`. A directory, symlink (including a broken one), unreadable file, invalid UTF-8/JSON or unsupported structure raises `ReceiptError`. Validate:
    - the top level is an object containing the four required fields; `files` and `config` are objects;
    - `type(format) is int` and its value is `1` (JSON `true` is invalid);
    - `fingerprint`, every file key and every hash have the expected string types; each hash is 64 lowercase hex characters;
    - every file path is a canonical, nonempty POSIX relative path: no absolute path, backslash, colon, `.` or `..` component, or resolution outside the destination. Do not follow a symlink in a managed path or its parent components. Classify such a receipt as invalid before mutation.
    - messages contain a path and safe reason, never receipt or local configuration values. A valid historical receipt may differ from the incoming baseline; that is an upgrade, not a format error.
  - `write_receipt(destination: Path, receipt: Receipt) -> None` — writes JSON keys `format`, `fingerprint`, `files` and `config`, with `indent=2`, `sort_keys=True` and LF line endings. Use a uniquely created temporary sibling and `os.replace`; clean up only that newly created temporary file on failure. Never truncate a pre-existing `.tmp` file.
  - `verify_installed(destination: Path, expected: dict[str, str]) -> list[str]` — returns sorted relative paths that are missing, unreadable, not non-symlink regular files, or whose installed hash differs from `expected`.
  - `run_install(repo_root: Path, destination: Path, *, dry_run: bool) -> int` — the existing installation logic, moved out of `main`.

**Install order:**

1. Load `baseline.json`.
2. Refuse `opencode.jsonc`.
3. Call `read_receipt`. If it raises `ReceiptError`, exit 1 without writing anything, in dry-run as well. Name the path and safe reason, then say: "Restore a verified receipt from `<destination>/backups/harness-*/opencode-defaults-receipt.json`. If no valid backup exists, preserve the damaged receipt and reconcile ownership manually before deliberately bootstrapping without it; automatic retirement history will be lost." Do not auto-delete or replace it. Construct the expected new receipt from the incoming source now; if an existing receipt claims this same fingerprint but has different file/config metadata, stop as inconsistent history.
4. Read and validate the source and installed JSON objects, compute the intended merge, and validate paths before writes. Run the existing migration/backup steps; back up and prune retired files **before** copying incoming managed files. Task 4 extends that retirement stage.
5. Call `verify_installed` and re-read `opencode.json` to confirm it equals the intended merged object, including list order. On failure list paths only, exit 1, and leave the old receipt untouched. Ordinary write/replace/read errors also exit 1 without a traceback; this is not a transactional rollback of already changed files.
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
    # subTests: b"not json", [], format 2/true, files [], non-string hash, fingerprint "XYZ",
    # files {"../escape": hash}, {"/abs": hash}, {"C:/x": hash}, config [], receipt path a directory
    # -> install and --dry-run: returncode 1, RECEIPT_NAME and "backups" in stderr,
    # no traceback, snapshot(dest) identical before/after
def test_broken_receipt_symlink_is_not_bootstrap(self):
    # when supported: broken symlink at receipt path -> exit 1 before writes; link remains
def test_receipt_read_error_stops_before_writes(self):
    # mock the receipt file read raising PermissionError; no backup/copy/replace call occurs
def test_same_fingerprint_with_wrong_metadata_stops_install(self):
    # retain fingerprint but alter files/config -> exit 1 before writes; old receipt unchanged
def test_failed_verification_keeps_old_receipt(self):
    # in-process: install.run_install(src, dest, dry_run=False); then with
    # mock.patch("install.verify_installed", return_value=["AGENTS.md"]) -> run_install(...) == 1,
    # receipt bytes unchanged
def test_written_config_is_verified_before_receipt(self):
    # simulate a readable but incorrect written config -> exit 1 naming opencode.json; old receipt unchanged
def test_failed_receipt_replace_keeps_previous(self):
    # mock os.replace to raise OSError -> exit 1; old receipt unchanged; only newly created temp removed
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
  - `plan_file_retirement(destination: Path, receipt: Receipt, managed: set[str]) -> tuple[list[str], list[str]]` — returns two lists: unchanged retired files to remove, and locally changed retired files to keep. It covers receipt files that are no longer in `managed` but still exist. Missing files need no action. Hash regular, non-symlink files only; unreadable/unsafe targets stop installation before mutation. A file is unchanged when its hash still matches the receipt.
  - `retire_settings(current: dict[str, Any], previous: dict[str, Any], incoming: dict[str, Any]) -> tuple[dict[str, Any], list[str], list[str]]` — returns a cleaned copy of `current`, plus the display paths removed and kept. It never changes its inputs.

`retire_settings` follows these rules while walking `previous`. Display paths use dot notation.

- **Missing current key:** skip it without a removed/kept notice; the user already deleted it.
- **Root `plugins`, `instructions` and `skills`:** when the current and previous values are lists, remove entries still equal to previous entries that are absent from the incoming list (or whose list was dropped). Use equality-based membership, not sets: plugin entries can be objects. Count only actual removals as `<key> (-N)` and remove a list this makes empty; preserve a list that was already empty.
- **`mcp.servers.<name>` missing from `incoming`:** remove it when `current` matches `previous`; otherwise keep it and name `mcp.servers.<name>`.
- **Objects:** when an object exists in `previous` and `current`, and `incoming` has an object or nothing at that path, recurse into it. Remove an object that this leaves empty, but keep one that was already empty.
- **Other values missing from `incoming`:** remove a value that still equals `previous`; otherwise keep it and name it.
- **Dropped key whose current type differs from the old value:** keep and name it as locally changed retired content. Do not treat it as already deleted.
- **Keys still in `incoming` with a replacement value/type:** leave replacement to `merge_settings`; continue recursing through compatible objects so individually retired children are handled.

When a receipt exists, installation runs `retire_settings(current_cfg, receipt.config, incoming_cfg)` before `merge_settings`. Back up and delete unchanged retired files, and prune emptied parent folders, **before** copying incoming files. Never remove the destination itself. This order preserves old backup bytes and prevents a Windows case-only rename from deleting the incoming copy. If a retained old spelling aliases an incoming active managed target on the filesystem, apply the existing managed-file backup/replacement rule; do not call that same physical file a preserved local addition.

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
def test_already_deleted_retired_settings_are_ignored(self):
    # delete retired scalar/list/server keys before upgrade -> no KeyError and no kept/removed notice for them
def test_type_changed_retired_setting_is_kept(self):
    # A agents.old is an object; local value becomes a string; B drops it -> kept with one safe path notice
def test_case_only_command_rename_preserves_incoming_and_backup(self):
    # A commands/XM-Old.md has old bytes; B commands/xm-old.md has different bytes
    # -> install 0, new bytes present, backup holds old bytes, new receipt names only incoming spelling
    # run on Windows and Linux; on a case-insensitive filesystem assert only one directory entry remains
    # locally edited alias variant: incoming active target is replaced with backup, never claimed as kept Local
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

### Task 5: Complete read-only check with bounded local reporting

**Files:**
- Modify: `install.py`, `tests/test_baseline.py`

**Interfaces:**
- Consumes: `load_baseline`, `compute_fingerprint`, `managed_files`, `read_receipt` and `sha256_file` from Tasks 2–3, plus `merge_settings` and `default_destination`.
- Produces in `install.py`:
  - `probe_opencode_version(timeout: float = 10.0) -> tuple[Literal["ok", "missing", "failed"], str]` — finds `shutil.which("opencode")`, or else `shutil.which("opencode", path=str(Path.home() / ".opencode" / "bin"))`, then runs `[exe, "--version"]`. It returns `failed` on timeout, `OSError`, nonzero exit, empty stdout, or an empty parsed token after removing `v`. Accept bare/prefixed versions and CRLF. A discovered but failing PATH executable is not bypassed by trying a second installation. Suppress raw subprocess stdout/stderr on failure.
  - `config_drift_paths(installed: dict[str, Any], expected: dict[str, Any]) -> list[str]` — sorted dot paths where the two differ. Lists are compared whole and in order; each `mcp.servers.<name>` is compared as one unit.
  - `run_check(repo_root: Path, destination: Path, expect: str | None) -> int`
  - `CHECK_SCOPE_NOTE = "Covers the installed global baseline and CLI version only; the running server version, project or system overrides, environment substitutions, plugin loading, MCP connectivity, provider access and model behavior are not checked. Detects accidental drift only (not tamper-proof)."`
  - `LOCAL_SCAN_DIRS = ("agents", "commands", "skills", "plugins")`
  - `list_local_additions(destination: Path, installed_cfg: dict[str, Any] | None, baseline_cfg: dict[str, Any], managed: set[str]) -> list[str]` — returns sorted, unique names using the bounded rules below.
  - `main()` adds `--check` and `--expect FINGERPRINT`.
    - `--check`, `--dry-run` and `--fingerprint` cannot be combined.
    - `--expect` defaults to `None`; test presence using `args.expect is not None`. When supplied it requires `--check` and, after trimming/lowercasing, exactly 64 hex characters. Explicit `""` or whitespace-only values are errors, never an omitted pin.
    - Violations call `parser.error`, which exits 2.

**Check behavior:**

- Print one item per line: the section name, one space, then the item. Sections appear in this order: `Destination`, `Baseline`, `Receipt`, `Files`, `Config`, `Runtime`, `Local`, `Result`, followed by `CHECK_SCOPE_NOTE`. Sort items within each section. Include the computed fingerprint in the Baseline section.
- Finding formats:
  - `Baseline mismatch`
  - `Receipt missing`, `Receipt invalid` or `Receipt differs`
  - `Files missing <path>`, `Files edited <path>`, `Files unreadable <path>` or `Files invalid <path>` (wrong type, symlink, or unsafe ancestor)
  - `Config differs <path>`, `Config missing opencode.json`, `Config unreadable opencode.json` or `Config present opencode.jsonc`
  - `Runtime missing`, `Runtime failed` or `Runtime mismatch <found> (baseline <pinned>)`
- Receipt checking compares the complete expected receipt (`fingerprint`, `files` and `config`), not only its fingerprint. A parseable receipt with matching fingerprint but stale file/config metadata is `Receipt differs`. Actual installed files and configuration are checked independently of that receipt.
- Inspect managed paths before opening them; do not follow symlinks or symlinked parents. A missing file, directory in place of a file, read error, or loop produces a finding and no traceback. `opencode.json` must be a readable JSON object; accept a UTF-8 BOM, and do not dump malformed text or values.
- A non-Local section without findings prints `ok`. Print `Local <item>` for each addition, or `Local none` if there are none. Local presence does not increment the finding count.
- `Result MATCH` exits 0. `Result DRIFT, N findings` exits 1.
- Configuration matches when `merge_settings(installed, baseline) == installed`.
- A `BaselineError` or an inspection error that prevents completing the report prints a safe path/reason and `Result could not complete`, then exits 1. Do not print `Local none` when enumeration failed.
- The check never writes or creates anything.

**Bounded local-reporting rules:**

- Skip configuration inspection when `installed_cfg` is `None`.
- Handle list-valued root `plugins`, `instructions` and `skills` **before** the absent-key rule. Compare against the baseline list, using `[]` when absent. Count entries absent by equality-based membership (`item not in base_list`), never a set; object-form plugins are valid. Emit `<key> (+N)` only for `N > 0`; an empty local `skills: []` produces no Local line. A wrongly typed managed value remains a Config finding.
- For other keys, emit an absent key at its first unowned dot path and stop there. Recurse only into objects both configs own. At `mcp.servers`, compare server names only; changes inside an owned server are Config findings.
- Treat `agents/`, `commands/`, `skills/` and `plugins/` as container roots, inspecting their immediate children rather than reporting the root as one addition. A missing or empty root has no additions.
- Walk deeper only along prefixes that contain managed paths. Report each unowned file once. For an unowned directory, inspect only whether it has an immediate entry: skip it if directly empty; otherwise emit `<path>/` and stop. Do not recursively enumerate an unowned subtree. A directory containing only subdirectories still counts as nonempty.
- Inspect symlinks before file/directory checks; list an unowned symlink by name without following it, including broken links. A symlink at a managed path is a Files finding and is not duplicated under Local. Apply the same rule to a symlink replacing a scan root.
- List `AGENTS.local.md` when present (including a broken symlink). Do not scan other destination-root files such as the receipt, `service.json` or backups. Discovery failures are incomplete verification, not evidence of no additions.

- [ ] **Step 1: Write the failing tests**, classes `CheckTests` and `LocalTests`. Unless a test says otherwise, use `env=cli_env(tmp, "2.2.7")`.

```python
def test_check_passes_after_install(self):
    # returncode 0; section(out, "Result") == ["Result MATCH"]; CHECK_SCOPE_NOTE in out
def test_expect_match_mismatch_and_pasted_value(self):  # Review Focus 5
    # --expect fp -> 0; --expect "0"*64 -> 1 with "mismatch"; --expect f"  {fp.upper()}  " -> 0
def test_receipt_findings(self):
    # missing; invalid (b"not json") reported and the rest still checked; differs (installed from A, checked from B)
    # keep fingerprint unchanged but edit files/config metadata -> Receipt differs and exit 1
def test_file_findings(self):
    # delete commands/xm-demo.md -> "missing commands/xm-demo.md"; append to skills/demo/SKILL.md -> "edited ..."
    # directory or supported symlink at a managed path -> invalid; a mocked read error -> unreadable;
    # each exits 1 without traceback or following a link
def test_config_drift_cases(self):
    # subTests, each -> exit 1 and the named path in a Config line:
    # model changed -> "model"; mcp.servers.context7 altered or removed -> "mcp.servers.context7";
    # "small_model" added -> "small_model"; instructions entry removed -> "instructions";
    # local plugin inserted before "managed-plugin" -> "plugins";
    # with a source variant whose plugins hold a pinned Superpowers ref, a second Superpowers ref -> "plugins"
def test_reorder_is_fixed_by_reinstall(self):
    # subTests for plugins, instructions, and a source variant with a managed skills list:
    # put a local entry first -> exit 1 naming that list; reinstall -> exit 0 and managed entries precede local
def test_properly_placed_local_additions_pass(self):
    # append plugin, add providers {...}, mcp.servers.local {...}, commands/mine.md -> exit 0
def test_pass_implies_reinstall_changes_nothing(self):
    # from the passing state above: snapshot managed files, parsed opencode.json and receipt; reinstall; all equal
def test_opencode_jsonc_is_a_finding(self):
    # create alongside otherwise valid install -> Config present opencode.jsonc, exit 1, no writes
def test_runtime_findings(self):  # Review Focus 3
    # cli_env(tmp, None) -> "Runtime missing"; version "2.2.5" -> "mismatch 2.2.5 (baseline 2.2.7)";
    # exit_code=3, output="", output="   " or output="v" -> "failed";
    # bare "2.2.7", "opencode v2.2.7\r\n", "OpenCode CLI version v2.2.7" -> ok;
    # in_home=True (fake only in HOME/.opencode/bin) -> ok
    # unit-test probe with subprocess.run raising TimeoutExpired/OSError -> failed, no raw error output
def test_check_on_missing_destination(self):  # Review Focus 1
    # returncode 1; destination still does not exist
def test_bom_invalid_and_non_object_config(self):  # Review Focus 2
    # BOM-encoded opencode.json -> passes; b"{" and b"[]" -> "Config unreadable opencode.json"; "Traceback" not in stderr
def test_bad_baseline_check_could_not_complete(self):
    # baseline.json missing -> returncode 1, "could not complete" in stdout
def test_check_is_read_only(self):
    # drifted destination: snapshot before == after
def test_local_scan_failure_is_not_local_none(self):
    # mock directory enumeration raising PermissionError -> exit 1, could not complete; no Local none claim
def test_check_uses_default_destination(self):
    # XDG_CONFIG_HOME=tmp/xdg; install and check without --destination -> 0
def test_check_usage_errors(self):
    # --expect alone, --check --dry-run, --check --fingerprint, --check --expect nothex,
    # --check --expect "", --check --expect "   " -> 2 before inspecting or changing the destination
```

For `LocalTests`, use these cases:

```python
def test_config_reported_at_first_boundary(self):
    # providers.openrouter.settings.apiKey="secret-value", mcp.servers.chrome-devtools, agents.title.temperature,
    # one extra plugin -> Local lines exactly ["Local agents.title.temperature", "Local mcp.servers.chrome-devtools",
    # "Local plugins (+1)", "Local providers"]; "secret-value" not in stdout; returncode 0
def test_absent_root_skills_list_and_object_plugin(self):
    # skills=["~/extra"], append {"package": "local-plugin", "options": {"private": "secret"}}
    # -> Local skills (+1), Local plugins (+1), exit 0; no nested values in output
    # skills=[] -> no Local skills line and no error
def test_files_and_folders(self):
    # commands/add-notes.md, skills/custom-skill/SKILL.md + ref.md, plugins/x.ts, AGENTS.local.md
    # -> commands/add-notes.md, skills/custom-skill/, plugins/x.ts, AGENTS.local.md listed once each;
    # managed files, backups/, receipt and service.json not listed
def test_clean_install_prints_local_none(self):
    # valid fresh install -> exactly Local none; repeat with empty agents/, plugins/ and skills/empty/ -> same
def test_unowned_directory_is_not_recursively_classified(self):
    # skills/custom/ has a nested directory -> only Local skills/custom/;
    # assert no recursive read/list calls inside that first nonempty unowned directory
def test_symlinked_directory_listed_not_followed(self):  # Review Focus 4
    # skills/loop -> symlink to skills/; self.skipTest when os.symlink raises OSError
    # -> "Local skills/loop" once; returns promptly
def test_kept_retired_file_shows_as_local(self):
    # Task 4's locally changed retired file -> listed under Local; check exit 0
```

- [ ] **Step 2: Run the tests to confirm they fail**

Run: `uv run --no-project python -m unittest discover -s tests -p test_baseline.py -v`
Expected: new CheckTests and LocalTests fail because `--check` and the reporting helpers are absent.

- [ ] **Step 3: Implement** the probe, checker and bounded local reporting together. Do not commit a temporary checker that always prints `Local none`.

- [ ] **Step 4: Run the whole suite**

Run: `uv run --no-project python -m unittest discover -s tests -v`
Expected: all tests pass.

- [ ] **Step 5: Commit**

```powershell
git add install.py tests/test_baseline.py
git commit -m "feat: check the selected baseline and report bounded local additions"
```

---

### Task 6: Add wrapper modes and make wrapper tests portable

**Files:**
- Modify: `install.ps1`, `tests/test_install.py`, `tests/test_baseline.py`

**Interfaces:**
- Consumes: the `install.py` options `--check`, `--expect`, `--fingerprint`, `--dry-run` and `--destination`.
- Produces: `install.ps1` parameters `[switch]$Check`, `[switch]$Fingerprint` and `[string]$Expect = ''`, passed through as `--check`, `--fingerprint` and `--expect <value>`.
  - Test `$PSBoundParameters.ContainsKey('Expect')`, not whether the value is nonempty. When bound, append a single `"--expect=$Expect"` argument so PowerShell 5.1 cannot drop an empty native argument. Python then rejects an explicit empty/whitespace pin with exit 2. An omitted `Expect` adds no argument.
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
    # -Check -Expect "" and -Check -Expect "   " -> 2, never Result MATCH
    # exercise an explicitly bound empty PowerShell string as well as CLI invocation
def test_sh_modes(self):  # same skip rule as test_sh_wrapper
    # same outcomes via sh ./install.sh, including --check --expect "" and whitespace -> 2
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

### Task 7: Update documentation and the `project-setup` runtime version

**Files:**
- Modify: `README.md`, `AGENTS.md`, `.opencode/skills/project-setup/SKILL.md`, `docs/cross-model-workflow-design.md`

- [ ] **Step 1: Update `project-setup` step 4**

Load `skill-authoring` and consult the Agent Skills specification as required by `AGENTS.md`. Replace "Verify `opencode` V2 (`2.0.4+`)". The new text compares the parsed version from `opencode --version` with the `opencode` value in the defaults source's `baseline.json`. If OpenCode is missing or the version differs, load `opencode` and install that exact version with `curl -fsSL https://opencode.ai/v2/install | bash -s -- --version <version>` or `opencode upgrade <version>`. Keep the rest of the step; automatic use of the new check inside the skill remains deferred.

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

### Task 8: Windows and Linux acceptance

This task tests the committed build end to end. It changes no code and records actual results in the spec. Both platforms must demonstrate a positive check followed by detection of an edited file before rollout is declared ready. A missing runtime or unavailable Linux host leaves that acceptance pending.

**Files:**
- Modify: `docs/baseline-verification-design.md`, adding a "Verified" section

- [ ] **Step 1: Test Windows with an isolated destination**

```powershell
$ErrorActionPreference = 'Stop'
$tmp = Join-Path $env:LOCALAPPDATA ('Temp\opencode\baseline-verify-' + [guid]::NewGuid().ToString('N') + '.tmp')
New-Item -ItemType Directory -Path $tmp | Out-Null
New-Item -ItemType Directory -Path "$tmp\src" | Out-Null
git archive --format=tar -o "$tmp\src.tar" HEAD
if ($LASTEXITCODE -ne 0) { throw 'Archive creation failed' }
tar -xf "$tmp\src.tar" -C "$tmp\src"
if ($LASTEXITCODE -ne 0) { throw 'Archive extraction failed' }
$archiveOutput = @(uv run --no-project python "$tmp\src\install.py" --fingerprint)
if ($LASTEXITCODE -ne 0 -or $archiveOutput.Count -ne 1) { throw 'Archive fingerprint failed' }
$fp = $archiveOutput[0].Trim()
if ($fp -notmatch '^[0-9a-f]{64}$') { throw 'Invalid archive fingerprint' }
$checkoutOutput = @(uv run --no-project python install.py --fingerprint)
if ($LASTEXITCODE -ne 0 -or $checkoutOutput.Count -ne 1 -or $checkoutOutput[0].Trim() -ne $fp) { throw 'Checkout/archive fingerprint mismatch' }
powershell -NoProfile -ExecutionPolicy Bypass -File "$tmp\src\install.ps1" -Destination "$tmp\dest"
if ($LASTEXITCODE -ne 0) { throw 'Isolated Windows install failed' }
powershell -NoProfile -ExecutionPolicy Bypass -File "$tmp\src\install.ps1" -Check -Expect $fp -Destination "$tmp\dest"
if ($LASTEXITCODE -ne 0) { throw 'Windows positive check failed; inspect findings' }
Add-Content -LiteralPath "$tmp\dest\skills\writer\SKILL.md" -Value 'edit'
powershell -NoProfile -ExecutionPolicy Bypass -File "$tmp\src\install.ps1" -Check -Expect $fp -Destination "$tmp\dest"
if ($LASTEXITCODE -ne 1) { throw 'Windows edit was not reported as drift' }
```

Expected:
- The checkout and archive fingerprints are equal.
- The first check shows `Result MATCH`, `Local none` and exits 0.
- The second check's sole finding is `Files edited skills/writer/SKILL.md`, and it exits 1.

Do not run the installer against the real `~/.config/opencode`; deployment is a separate step.

- [ ] **Step 2: Confirm the Linux test container is reachable**

This uses the disposable `workspace-smoke` container through its existing SSH alias.

Run: `ssh workspace-smoke "hostname; id -un; python3 --version"`
Expected: the smoke container's hostname, `builder`, and Python 3.10 or later.

If the container is unreachable, report Linux verification as pending. `ops-infra` supplies the reachable test environment and pinned runtime; this task does not provision or upgrade a container. The last recorded smoke environment had no OpenCode, so that prerequisite may still be outstanding. The unit suite uses a fake runtime and can pass independently; it does not establish live runtime readiness.

- [ ] **Step 3: Run the Linux checks**

```powershell
$remoteOutput = @(ssh workspace-smoke 'mktemp -d /tmp/opencode-baseline-verify-XXXXXX')
if ($LASTEXITCODE -ne 0 -or $remoteOutput.Count -ne 1) { throw 'Linux scratch creation failed' }
$linuxTmp = $remoteOutput[0].Trim()
if ($linuxTmp -notmatch '^/tmp/opencode-baseline-verify-[A-Za-z0-9]+$') { throw 'Unexpected Linux scratch path' }
ssh workspace-smoke "mkdir '$linuxTmp/src'"
if ($LASTEXITCODE -ne 0) { throw 'Linux source directory creation failed' }
$transfer = 'ssh workspace-smoke "tar -xf - -C {0}/src" < "{1}\src.tar"' -f $linuxTmp, $tmp
cmd /d /c $transfer
if ($LASTEXITCODE -ne 0) { throw 'Archive transfer failed' }
ssh workspace-smoke "cd '$linuxTmp/src' && python3 -m unittest discover -s tests -v"
if ($LASTEXITCODE -ne 0) { throw 'Linux unit suite failed' }
$linuxOutput = @(ssh workspace-smoke "sh '$linuxTmp/src/install.sh' --fingerprint")
if ($LASTEXITCODE -ne 0 -or $linuxOutput.Count -ne 1 -or $linuxOutput[0].Trim() -ne $fp) { throw 'Windows/Linux fingerprint mismatch' }
ssh workspace-smoke "sh '$linuxTmp/src/install.sh' --destination '$linuxTmp/dest'"
if ($LASTEXITCODE -ne 0) { throw 'Isolated Linux install failed' }
ssh workspace-smoke "sh '$linuxTmp/src/install.sh' --check --expect '$fp' --destination '$linuxTmp/dest'"
if ($LASTEXITCODE -ne 0) { throw 'Linux positive check incomplete; inspect findings and arrange the pinned runtime through ops-infra if needed' }
ssh workspace-smoke "printf 'edit\n' >> '$linuxTmp/dest/skills/writer/SKILL.md'"
if ($LASTEXITCODE -ne 0) { throw 'Linux edit fixture failed' }
ssh workspace-smoke "sh '$linuxTmp/src/install.sh' --check --expect '$fp' --destination '$linuxTmp/dest'"
if ($LASTEXITCODE -ne 1) { throw 'Linux edit was not reported as drift' }
```

`cmd /d /c` keeps the archive stream binary; quote the local archive path, as shown, rather than piping bytes through Windows PowerShell 5.1. The `&&` runs inside the remote Linux shell. Keep SSH outside the unit-test command and do not erase a fixed pre-existing temporary directory.

Expected:
- The unit suite passes, with platform/permission-dependent skips recorded, and `FIXTURE_FINGERPRINT` passes on both platforms.
- The Linux `--fingerprint` equals `$fp`.
- The first check shows the expected baseline, valid receipt/files/configuration, runtime `2.2.7`, `Local none`, `Result MATCH`, and exits 0.
- The second check's sole finding is `Files edited skills/writer/SKILL.md`, and it exits 1.
- A missing/mismatched runtime is not a substitute for the positive case. Record unit/fingerprint evidence already obtained, leave live Linux acceptance pending, and complete this sequence after the prerequisite is supplied.

- [ ] **Step 4: Record the results**

Add a "Verified" section to the spec with:
- the date, commit and fingerprint;
- the Windows and Linux commands, exit codes, fixture fingerprint parity and any skips;
- the OpenCode runtime found in `workspace-smoke`, and explicit pending status for any incomplete acceptance.

The recorded sim rollout used OpenCode 2.2.5; describe that as historical evidence unless live state has been checked. After recording results, remove only the unique temporary directories created above. On a failed run, retain them until the diagnostics have been reviewed; never clean up unrelated paths.

```powershell
ssh workspace-smoke "rm -rf -- '$linuxTmp'"
if ($LASTEXITCODE -ne 0) { throw 'Linux scratch cleanup failed' }
Remove-Item -LiteralPath $tmp -Recurse -Force
```

- [ ] **Step 5: Commit**

```powershell
git add docs/baseline-verification-design.md
git commit -m "docs: record Windows and Linux baseline verification"
```

---

Rollout to `sim-funds` and `sim-prime-broker` belongs to `ops-infra` and starts after Task 8's Windows and Linux acceptance both pass. It covers delivering the source, installing the pinned CLI, running the installer, and running `--check --expect` with `Local none` expected.

## Planning self-review

- Spec coverage: identity and LF portability are in Task 2; receipt integrity/atomic publication in Task 3; backed-up retirement in Task 4; ordered checks, runtime probe and bounded Local output in Task 5; wrappers in Task 6; aligned instructions in Task 7; cross-platform acceptance in Task 8.
- Shared contracts: Tasks 3–6 reuse the declared fingerprint, receipt, collector and merge interfaces; there is no separate ownership catalog or temporary always-empty Local report.
- Review corrections have planned regression cases, including empty pins, case-only renames, malformed receipts, object plugins and first-unowned-directory handling. Pre-revision review hashes are recorded above, not presented as hashes of this revised file.
- Verification commands have been checked by reading for scope and consistency. They have not been executed during planning; no passing runtime, unit-test or SSH result is claimed.
