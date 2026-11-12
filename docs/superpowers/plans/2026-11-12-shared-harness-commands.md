# Shared Harness Commands Implementation Plan

Approved approach: receive-only public-repository updates, behavior 2. Execute inline with one final review. User chose the existing checkout earlier; preserve unrelated work in `docs/cross-model-workflow-design.md`.

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
- [ ] Add failing tests for edited retired file/setting removal with backups and unowned additions retained.
- [ ] Extend existing retirement/install functions with an internal `reset_shared` option; ordinary install remains backward compatible.
- [ ] Verify focused tests and existing suite.

### Task 2: Deterministic receive-only driver and slash commands
- [ ] Add Git-fixture tests: fresh upstream, local edits vs upstream changes, dirty/diverged source refusal, no remote mutation, reexecution of current upstream code, neutral drift, project inventory, failed upgrade/reload reporting.
- [ ] Implement `shared_harness.py` using existing `install.py` functions. Refresh only the configured public `main` clone without credential prompts or rewriting local commits. Execute fetched code in a child process after refresh.
- [ ] Add both low-cost slash-command prompts to `global/commands/`, using one platform-appropriate shell invocation and the dedicated source checkout.
- [ ] Verify offline fixture behavior and fresh command installation.

### Task 3: Public workflow documentation and verification
- [ ] Update README, project-setup guidance and current baseline design scope. Supersede archive/fleet/Local-none assumptions; retain historical records as history.
- [ ] Verify anonymous upstream access, Windows/Linux suites, isolated drift/update and installed command registration. One independent final review, then focused fixes if needed.
- [ ] Commit scoped changes. Publication/real-workspace bootstrap are explicit rollout operations; report what was actually deployed.

## Acceptance
Local shared edits show before update; update backs them up and replaces/removes them. Unknown global additions and project-local files survive byte-for-byte. Changed local setup is not modified by drift. Fetch/network/receipt/runtime failures are explicit. Reports distinguish upstream changes from workspace changes. Both commands pull only; source repository and sibling workspaces are never written.
