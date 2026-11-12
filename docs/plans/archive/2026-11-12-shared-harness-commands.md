# Shared Harness Commands Implementation Plan

**Status:** Complete and archived on 2026-11-12. Moved from `docs/superpowers/plans/2026-11-12-shared-harness-commands.md`.

**Approval source:** The approved requirements are recorded in this plan's Contract and execution record, not a separate spec. The [baseline design](../../specs/baseline-verification-design.md) describes the earlier verifier and subsequent workflow change; it is related context, not a retrospective approval source.

Implemented 2026-11-12: receive-only public-repository updates, behavior 2. Executed inline with one final review. The current checkout was used with the user's consent; concurrent model-workflow changes were kept separate.

## Contract
- Bootstrap once from the public `patrickreidy6/opencode-defaults` repository into `~/.local/share/opencode-defaults`, outside business source repositories.
- `/shared-harness-drift` refreshes only that clean source cache, then reports upstream changes since the receipt, workspace edits since the receipt, workspace-only additions, project-local harness files, and runtime differences. Differences are information, not errors. No installed/project files change.
- `/shared-harness-update` refreshes from `origin/main`, uses the freshly fetched updater, resets shared items to the selected published version with backups, removes previously managed retired items even when edited, and preserves workspace-only additions. No push, proposal, PR or cross-workspace operation.
- Shared config ownership follows existing merge rules. Root-array membership is by value; new local entries survive. Dropped atomic MCP definitions are managed as a whole. Unknown files/settings are never globally reset.
- The updater reuses installer verification/receipt/backup logic. Corrupt receipts and dirty/diverged source caches stop rather than being silently replaced.
- The runtime pin is applied through `opencode upgrade <version>` when necessary, then verified. Reload configuration after install; if the CLI was upgraded, report the terminal service-restart step rather than kill the running command's own service.
- Names/statuses only in reports; avoid dumping config values or credentials. Project information is an inventory of applicable ancestor instructions/config and `.opencode` extensions, not an assertion of effective runtime equivalence.
- No private-repo tokens, central artifact delivery, or ops-infra fleet management is required. Keep useful offline installer/check interfaces and historical evidence.

## Tasks
### Task 1: Reset shared ownership on update
- [x] Add failing tests for edited retired file/setting removal with backups and unowned additions retained.
- [x] Extend existing retirement/install functions with an internal `reset_shared` option; ordinary install remains backward compatible.
- [x] Verify focused tests and existing suite.

### Task 2: Deterministic receive-only driver and slash commands
- [x] Add Git-fixture tests: fresh upstream, local edits vs upstream changes, dirty/diverged source refusal, no remote mutation, reexecution of current upstream code, neutral drift, project inventory, failed upgrade/reload reporting.
- [x] Implement `shared_harness.py` using existing `install.py` functions. Refresh only the configured public `main` clone without credential prompts or rewriting local commits. Execute fetched code in a child process after refresh.
- [x] Add both low-cost slash-command prompts to `global/commands/`, using one platform-appropriate shell invocation and the dedicated source checkout.
- [x] Verify offline fixture behavior and fresh command installation.

### Task 3: Public workflow documentation and verification
- [x] Update README, project-setup guidance and current baseline design scope. Supersede archive/fleet/Local-none assumptions; retain historical records as history.
- [x] Verify anonymous upstream access, Windows/Linux suites, isolated drift/update and installed command registration. One independent final review, then focused fixes if needed.
- [x] Commit scoped changes. Publication/real-workspace bootstrap were explicitly authorized and completed.

## Acceptance
Local shared edits show before update; update backs them up and replaces/removes them. Unknown global additions and project-local files survive byte-for-byte. Changed local setup is not modified by drift. Fetch/network/receipt/runtime failures are explicit. Reports distinguish upstream changes from workspace changes. Both commands pull only; source repository and sibling workspaces are never written.

## Verification and deployment record

Code commits: `7cb3be0` and `c609f09`. Repository visibility was changed to public with authorization; both unauthenticated GitHub API access and credential-helper-disabled Git reads succeeded. A scan of 147 reachable historical blobs found no matches for the selected common credential patterns; this was not an exhaustive guarantee about sensitive information.

- Windows: `uv run --no-project python -m unittest discover -s tests -q` — 126 tests, OK, 10 platform/privilege skips.
- Linux (`workspace-smoke`, unique executable `/workspace` scratch with isolated HOME/TMPDIR): `python3 -m unittest discover -s tests -q` — 126 tests, OK, 3 Windows-only skips. Scratch removed afterward.
- `skills_ref.cli validate .opencode/skills/project-setup` — valid.
- Review corrections were verified RED→GREEN: do not migrate receipt-owned shared AGENTS edits into active local instructions during reset; retain restart notices after later failures; include ancestor configuration above Git roots and outside Git repositories.
- Existing private-access support was documentation, not an authentication subsystem. The primary workflow now uses anonymous public fetches; receipt/backups/fingerprints and the offline verifier remain useful and were retained.

The user authorized publishing and one-time bootstrap in both business workspaces. Both anonymously cloned public `main` at `c609f0938d99322c0033e0d335b4bb743ccf742f` to `/home/builder/.local/share/opencode-defaults`, upgraded the CLI from 2.2.6 to the 2.2.7 pin, installed verified receipts and registered both global commands at `/workspace`. Protected `AGENTS.local.md`, `service.json`, `cli.json`, and `commands/add-notes.md` hashes were preserved. Both installed fingerprints were `791af5f0f9fe1571bcfffcd7f36f27ca52de4773f619b9cbfea1cf13d3c69753`.

Actual slash-command executions through each workspace's OpenCode command API:

| Workspace | Command | Session | Result |
|---|---|---|---|
| sim-funds | shared-harness-drift | `ses_e2fe16db0ffeBgBAqq4S6x55jQ` | succeeded; one shell call, exit 0 |
| sim-funds | shared-harness-update | `ses_e2fe15437ffe4xmVJfa56Ha85i` | succeeded; one shell call, exit 0, backup created |
| sim-prime-broker | shared-harness-drift | `ses_e2fe13826ffeXymOr4gOUtcmgH` | succeeded; one shell call, exit 0 |
| sim-prime-broker | shared-harness-update | `ses_e2fe121daffeMpXgAEZK6lckpM` | succeeded; one shell call, exit 0, backup created |

Every assistant message in these four fresh sessions used `openai/gpt-6.1-sol#low`. Recorded model costs summed to approximately $0.11; this small fresh-session sample is not a fixed per-use price. Drift showed matching installed/default fingerprints and no current shared, local or project additions; differences remain permitted.

The binary upgrade does not restart the running OpenCode background service. Run `opencode service restart` in each workspace terminal when ready to activate the new server binary. Commands were successfully exercised before that restart. Provider/runtime integration beyond those executions was not audited.

Minor limitation retained from review: an interrupted installer may not print the exact backup directory. Existing backups remain under the destination's `backups/harness-*`; inspect the newest directory when recovering a partial installation. No automatic rollback or separate review/send workflow was added.
