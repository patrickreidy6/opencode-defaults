# Cross-model workflow: design record

Design record for the opt-in `/xm-*` commands, with dated verification below. Usage and the per-command model table are in the [README](../../README.md#opt-in-cross-model-workflow). Implemented in [`global/commands/`](../../global/commands/), the `xm-planner` and `xm-reviewer` agents in [`global/opencode.json`](../../global/opencode.json), and the command copy step in [`install.py`](../../install.py). The [completed initial plan](../plans/archive/cross-model-commands.md) records conversation approval; this maintained design is not a retrospective replacement for that approval source.

## Intent

Add review by a different model vendor at each stage of spec-driven work, for the few projects where the extra cost is justified: foundational specs and new codebases. Ordinary Plan and Superpowers sessions remain the default; cross-model reviews run only when a command is typed. All workflows share the document convention below unless repository instructions specify otherwise.

The scope-focused refinements address Patrick's reported experience of Anthropic/Superpowers sessions asking too many questions and expanding secondary features and data fields. Astra should judge whether the build has reached a worthwhile scope for its subject matter, with a bias toward justified cuts that preserve the core payoff. Planning should preserve that balance and resolve routine technical choices without another round of product-design questions.

## Decisions

- **Commands carry the models.** Plan writing and each review are slash commands with a pinned model. Authoring and execution are ordinary sessions on a model selected with `/models`. Nothing chains the stages; the user starts each one.
- **A different vendor reviews each artifact.**

  | Artifact | Written by | Reviewed by |
  |---|---|---|
  | Spec | Claude Fable 5.2 | GPT-6 Astra |
  | Plan | Claude Fable 5.2 | Gemini 4 Carbon (technical) and GPT-6 Astra (simplification) |
  | Code | GPT-6 Astra, including `general` workers | Claude Fable 5.2 |

- **Reviewers report and the author revises.** Review commands return findings and do not edit the artifact. The spec review ends with an explicit handoff requiring the authoring session to present scope recommendations and wait for the user's choices before editing.
- **Spec review judges the build's value and size.** Astra identifies the core payoff, challenges unnecessary features and data fields, and recommends what to remove, shrink or defer. Essential gaps matter when they threaten the intended outcome. The report recommends a build boundary rather than assigning a generic readiness verdict. Unlike plan simplification, it may challenge the proposed requirements themselves.
- **Planning preserves the approved scope.** Fable produces cohesive tasks, precise shared contracts and meaningful checks for a capable Astra executor. It carries forward exclusions and deferrals, justifies consequential implementation additions, and leaves routine coding choices open. The command overrides the generic `writing-plans` template's fixed review-case quota, exhaustive test-code prescriptions and execution-method menu.
- **When both plan reviews are requested, they run on one unchanged draft.** Each reports the plan and spec content hashes and tells the parent to wait if its companion is running, so both are reconciled in one revision. A single requested review does not create a wait for an unrequested companion.
- **High-volume work stays on OpenAI.** OpenAI usage draws on prepaid credits; Anthropic and Google are billed per call. Execution, `general` workers, `explore` and `title` run on OpenAI models, and Anthropic and Google handle the low-volume authoring and review stages.
- **An omitted path is never guessed.** Discover only top-level Markdown documents in the applicable new and legacy directories, excluding archives, nested documents, `README.md`, `index.md` and other indexes. Spec commands inspect both `docs/specs/` and `docs/superpowers/specs/`; plan reviews inspect both `docs/plans/` and `docs/superpowers/plans/`; code review inspects all four. Proceed only when exactly one eligible candidate exists across those directories; otherwise list candidates and require an explicit path. The in-session planner retains its ability to use a spec explicitly selected in the conversation. Explicit missing paths fail without substitution.

## Reviewer perspectives and efficiency

The reviewer refinements agreed on 2026-11-12 are implemented in the command source files. Each perspective guides judgment while remaining calibrated to the project's actual goals, scale and resources.

| Command | Perspective and responsibility |
|---|---|
| [`xm-spec-review`](../../global/commands/xm-spec-review.md) | A pragmatic CTO accountable for business value, technical direction and operational efficiency. The existing scope-and-value review is otherwise unchanged. |
| [`xm-plan-review`](../../global/commands/xm-plan-review.md) | A hands-on principal engineer accountable for technical correctness, sound data modelling, efficient execution and reliable operation. Apply financial-data and evaluation-driven improvement expertise where relevant. The guiding question is: **Will this deliver the expected behavior accurately, efficiently, and reliably?** Expected behavior is grounded in the approved spec, intended workload and available resources. |
| [`xm-plan-simplify`](../../global/commands/xm-plan-simplify.md) | An experienced institutional-finance operations leader, accountable for useful, understandable outcomes with limited resources and minimal ongoing maintenance. Take the participant's identity and responsibilities from the project's instructions and approved spec. Challenge code, dependencies, infrastructure and processes whose value does not justify their complexity, while preserving expected behavior and necessary safeguards. |

**Efficiency means simple and fast.** The technical plan reviewer checks for avoidable work, repeated data access or computation, and data structures unsuited to the expected workload. Prefer the simplest approach that performs well at that scale. For a material concern, compare with a credible simpler or faster alternative and explain the tradeoff; there is no fixed number of alternatives. If performance uncertainty could change the design, recommend a focused check during implementation. Keep estimates distinct from measured evidence and avoid extra complexity for negligible gains.

Overlap between technical review and simplification is acceptable. Both may identify unnecessary complexity; the simplifier remains focused on reducing implementation and maintenance burden. Changing an approved requirement is a user decision, not an automatic simplification.

When a proposed simplification depends on uncertain domain knowledge, the simplifier consults authoritative sources to resolve that specific question. Unfamiliar complexity is not automatically unnecessary. This research remains within the existing bounded, read-only review with no delegation.

**Initial verification and rollout for these refinements:** source diffs were inspected and `git diff --check` passed. The existing models, permissions, input discovery, hash checks and handoffs were preserved. Live model behavior checks and global/container installation were not performed at that stage. Subsequent focused checks are recorded under [shared simulation guidance](#shared-simulation-guidance-2026-11-12). Earlier dated verification below applies to the earlier prompts and does not establish the behavior of these refinements.

## Shared simulation guidance, 2026-11-12

These refinements keep the shared harness useful across institutional-finance participants. The project's instructions and approved spec supply each participant's identity and responsibilities; the shared operations perspective does not assume a hedge-fund role or add another review stage.

- **Small, understandable scenarios:** the planner prefers a small, human-traceable example for generated or simulated data, reusing an existing example when it suffices. The technical reviewer checks intended relationships and event order as well as types and formats. These checks stay within the approved scenario and do not imply additional fields, broader asset coverage or a comprehensive financial model.
- **Preserve intended discrepancies:** coherent scenario behavior can include conflicting participant records, delayed observations and deliberately injected errors. Reviewers distinguish those intended differences from unintended inconsistencies; making every participant's records agree is not the goal.
- **Separate completion from evidence:** the shared verification rule distinguishes completed work, verified behavior and measured improvement, and requires disclosure of unperformed checks and unresolved findings that limit those claims. It applies to ordinary, XM and Superpowers work without changing the code-review verdicts or introducing a release gate.
- **Make improvement comparisons meaningful:** where improvement is claimed, the technical reviewer looks for retained, checked examples under comparable conditions. Changes to the scenario or scoring are identified separately from participant improvement. This does not require a new evaluation framework or mandatory benchmark suite.

**Verification on 2026-11-12, OpenCode 2.2.7:** the repository suite ran 126 tests (116 passed, 10 platform-specific skips). `git diff --check` and local documentation-link checks passed. An isolated dry run, installation and `--check` returned `MATCH` for baseline `49ab6cb23897e1972f931e59ceea3f9a1eda914554c754cfc36da96795b496aa`. Command frontmatter, model/permission configuration, spec review and code review were unchanged.

Six focused live calls exercised the revised guidance. The planner kept one task and two implementation files, with a traceable timeline and intentional participant discrepancy. Technical review caught a type-valid event applied one tick early; the coherent-plan review returned `READY` with an optional persistence check. The simplifier preserved the independent inputs and delayed observations. Evaluation review and an ordinary Build closeout separated completed work, failed/unperformed checks and improvement unproven under changed cases/scoring. All model selections, five expanded command bodies, required review hashes and protected-file checks matched. The planner wrote only its active plan; all ten sessions were idle at completion.

**Limits:** these are small, explicitly specified behavior checks, not an accuracy benchmark or proof of runtime isolation. The generated plan remained verbose and excluded an `AGENTS.md` update needed to document the check command; the simplifier flagged that conflict. The evaluation fixture omitted a referenced JSON input and used ambiguous aggregate-result wording. Its reviewer made some over-specific or unsupported recommendations; the causal reviewer also requested redundant contract detail. The supported result is detection of the targeted problems, not blanket correctness of every finding. No sibling/evaluator-file reads were observed, but comprehensive access isolation was not tested.

Exact inputs, source snapshots, raw reports, adjudications and validation details are retained in [the focused-check results](../../tests/fixtures/shared-guidance/results-2026-11-12.json). Full transcripts and one-off runners remain in `C:\Users\preid\AppData\Local\Temp\xm-guidance-live-20261112-111522`. Earlier verification records apply to their earlier prompts. Live workstation and container defaults were not updated.

## Code review verification and scope

The code-review refinements agreed on 2026-11-12 preserve the existing Fable 5.2 `high` reviewer, requirement discovery, read-only role and implementer handoff. The command's scope, verification and reporting rules override the corresponding Superpowers template rules; upstream skills remain unchanged.

- **Judge the final state.** Inspect committed, staged, unstaged and relevant untracked changes, then assess the combined working tree against the resolved base SHA. Do not report a committed defect that later local work already fixes.
- **Verify each finding.** After discovery, challenge each candidate against actual callers, guards, tests, documented intent, the base revision and the final state. Require a reachable trigger and concrete consequence. Drop speculative, handled, superseded, duplicate and unchanged pre-existing defects unless this change worsens them or makes them newly reachable. Do not invent a narrower input contract or dismiss supported boundary cases as unlikely; changed semantics can introduce a new obligation even when similar code existed before. Evidenced workload assumptions calibrate severity rather than erase a demonstrated contract violation.
- **Protect approved scope.** Respect exclusions and deferrals. A real correctness or security failure may matter even if the spec omitted its trigger; a new feature, style preference or unrelated refactor is not automatically a requirement. Do not inherit the template's exhaustive list of declined ideas or its invitation to polish.
- **Bind findings to inspected contents.** Record raw content hashes before reading requirements, instructions and code used as evidence, then recheck those hashes, missing paths, HEAD and changed/untracked path lists before reporting. The code reviewer uses `git hash-object --no-filters -- <path>` and its matching inspection permission, so clean filters neither execute nor hide byte changes. Report drift or an unavailable required check as `BLOCKED`. This detects observed drift; it is not an atomic snapshot or protection against transient changes between reads.
- **Separate review from execution evidence.** Report supplied test/static-analysis results with their source and covered revision/content; distinguish reported results from inspected evidence. Missing or stale results need an exact follow-up check. They are not, by themselves, proof of a code defect.

Verdicts have explicit meanings. `BLOCKED` takes precedence when essential scope/context is missing, a material unresolved question prevents reliable assessment, or snapshot checks fail/change. `NEEDS CHANGES` means stable, assessable scope with a substantiated Critical or Important defect. `READY` means no material findings within completed static-review scope; minor defects or execution-evidence gaps may remain. It is neither a passing test result nor permission to merge or deploy. Material fixes require a review of the updated state.

This follows the separation of finding discovery, verification and deduplication described in [Claude Code Review](https://code.claude.com/docs/en/code-review), and the evidence and severity calibration in its [customization guidance](https://code.claude.com/docs/en/code-review-customize). A single read-only reviewer remains the default. Model changes and additional reviewers should be justified by observed results rather than assumed to improve quality.

### Evaluation and rollout

The reusable [code-review fixtures](../../tests/fixtures/code-review/README.md) cover clean changes, approved intentional behavior, an edge case handled by a caller, an unchanged pre-existing bug, a committed bug fixed locally, and an actual cross-file regression. The builder checks each case's behavior and keeps expected findings outside the model-visible repositories. Compare old and proposed commands on the same cases and model, recording false positives, missed expected findings, cost, elapsed time and coverage/permission failures. Do not count fixture behavior checks or installer tests as evidence that an LLM review found the right issues.

**Verified on 2026-11-12, OpenCode 2.2.7:** the repository suite ran 126 tests (116 passed, 10 platform-specific skips). Independent fixture builds passed 13 tests and, after the numerical case below was added to the private oracle, 10 behavior probes. Their source hashes and deterministic commit IDs matched. `git diff --check` and local documentation-link checks passed.

Six paired live reviews compared the original prompt with the first revision on identical repository copies. Both found the deliberately planted payment-unit regression. The original prompt made two false Important findings on the correctly fixed working tree: superseded committed/staged code and missing test-run evidence. The revised prompt made neither. The other original fixture targets produced the expected decisions with both prompts. The revised prompt still offered nonblocking coverage suggestions.

The comparison also discovered a real numerical boundary defect in the caller-guard fixture: finite observations `[1e308, 1e308]` yield an infinite intermediate sum even though their mean is representable. The original reviewer mentioned it; the first revision incorrectly dismissed it using a scale assumption. The final prompt explicitly prohibits invented input restrictions and requires comparing old/new semantic obligations. Its focused reruns retained that Important finding, accepted the correctly fixed working tree and found the payment-unit regression, with no false material findings in those three runs. Only the private oracle/probe was expanded; the reviewed fixture code, tests and requirements were unchanged. A nonblocking out-of-contract validation question still appeared in the fixed-tree report.

| Focused check | Original prompt | First revision | Final refinement |
|---|---|---|---|
| Supported numerical boundary | Mentioned as Minor | Incorrectly dismissed | Important finding; `NEEDS CHANGES` |
| Correct final tree, broken HEAD/index | Incorrect `NEEDS CHANGES` | `READY` | `READY` |
| Cross-file cents/dollars regression | `NEEDS CHANGES` | `NEEDS CHANGES` | `NEEDS CHANGES` |
| File changes while status stays identical | Not run | Correct `BLOCKED` | Not rerun; snapshot rules unchanged |

The drift check changed `pricing.py` after its initial hash. The reviewer detected the changed hash despite unchanged HEAD/status and labelled subsequent observations provisional. All 16 runs used the intended model/variant and expanded command body. Transcript inspection confirmed the reported before/after hash pairs and final scope checks for the revised reviewers. The 15 non-drift runs preserved fixture files and Git state; all parent and child sessions were idle at completion. Recorded reviewer cost was $7.6660, with $0.0917 for parent sessions. These small checks establish specific behavior, not a general accuracy rate or pricing benchmark; cases 01/02/04 and drift were tested with the first revision, while cases 03/05/06 were rerun after the final refinement.

Raw reports, prompt versions, session IDs, timings, costs and adjudications are retained in [the evaluation results](../../tests/fixtures/code-review/results-2026-11-12.json). Full tool transcripts and the one-off runners are in `C:\Users\preid\AppData\Local\Temp\xm-code-review-20261112-103427`.

**Surface installation:** the final command SHA-256 is `8eb1f00b582f640985acb6a662edd61b618b4d3d1df20c4e558c3495e296ae9a`. It matches the installed file. The loaded agent registry contains the exact raw-byte hashing permission, and the command remains registered with Fable 5.2 `high`. The standard installer was run from a scoped source snapshot preserving the previously installed `xm-spec-review`, `xm-plan-review` and `xm-plan-simplify`, whose separate refinements remain pending. Only the code-review command, its required permission and the installation receipt changed; 22 other files and every other configuration value were preserved. Backups were created by the installer.

The scoped installation returned `MATCH` for baseline `729e35d014268efbd0d825ab3ccd26ef642bd6f41006647f25b6cbb7366adefe`. Checking against the full repository intentionally still reports the three pending prompt differences plus the receipt fingerprint. No container rollout or publication was performed for this revision.

## Shared spec and plan convention

The detailed convention lives in [`naming-files`](../../.opencode/skills/naming-files/SKILL.md) and applies to ordinary, XM and Superpowers work. Keep maintained specs at `docs/specs/<topic>-design.md`. Create plans at `docs/plans/YYYY-MM-DD-<topic>.md` using their creation date, with a spec link and clear status; revise an already selected active plan instead of making competing copies. Return exact saved paths and ready-to-use optional XM review commands.

After implementation and verification, the Build session marks the plan complete, moves it to `docs/plans/archive/` without renaming it, and repairs links. Maintained specs remain available in `docs/specs/`; they are not archived merely because implementation is complete. `.superpowers/sdd/` remains tool-managed execution state. This convention does not modify upstream Superpowers skills or migrate other repositories.

Explicit archived paths are valid review inputs. `/xm-plan-write <spec-or-plan-path>` also accepts an explicit active or archived plan and resolves its linked governing spec; if that spec cannot be resolved, request the exact spec path rather than inventing a spec or approval. When planning follow-up work from an archived plan, create a new active plan; do not revise the archive. An explicitly selected active legacy plan can still be revised in `docs/superpowers/plans/`. Preserve historical approval sources, commands and review hashes when organizing old documents; the [documentation index](../README.md) records this repository's migration.

## OpenCode behavior the design depends on

From the V2 [agents](https://opencode.ai/docs/agents/), [commands](https://opencode.ai/docs/commands/), [models](https://opencode.ai/docs/models/) and [permissions](https://opencode.ai/docs/permissions/) documentation:

- A session stores its own model, and selecting a primary agent does not change it. A command's `model` overrides every other model for that command, and a subagent uses its configured model. This is why the stages are commands and not primary agents with models attached.
- The root `model` keeps no `#variant`. Agent and command model references do.
- Variants belong to each model. Gemini 4 Carbon offers `low`, `medium` and `high` only, so its review is pinned to `high`. An unknown variant fails model resolution.
- The built-in `plan` agent may edit only files under `~/.opencode/plan`, so it cannot save a plan in a repository. `xm-planner` allows edits to `docs/plans/*.md` and `docs/superpowers/plans/*.md`, with explicit denies for both `archive/*` paths after the allow rules, and denies other edits, shell and delegation. OpenCode's [whole-value wildcards](https://opencode.ai/docs/permissions#matching) include `/`, and the last matching rule wins, so a plan-directory allow alone would also permit archive edits. New plans use `docs/plans/`; the legacy permission supports revisions to explicitly selected existing plans.
- The built-in `plan` agent has no shell restriction. `xm-reviewer` denies edits, delegation and questions, and allows only named Git inspection commands.

## Verified on 2026-11-11

Live runs used a scratch project with the harness installed into its `.opencode` directory, before the global install.

- All five commands completed, and every assistant message used the pinned provider, model and variant.
- `/xm-plan-write` saved the plan through an absolute path under the relative edit rule and changed no other file. Afterwards the session reported `anthropic/claude-opus-5-5#xhigh` and agent `xm-planner`.
- Both plan reviews reported the same plan and spec hashes, unchanged from start to finish, and ended with the wait-for-both line.
- The reviewers found the defects planted in the fixture: float arithmetic in a `Decimal` function, and unrequested infrastructure in the plan.
- OpenCode reported $0.15 to $0.65 per command on this fixture, whose spec was 14 lines. Treat that as a floor. Carbon was priced at $2/$10 per million tokens, an introductory rate the [OpenCode pricing page](https://opencode.ai/docs/console/models/) lists through 2026-11-30, with $4/$20 after.
- The global install left every config key outside `agents` unchanged, and `AGENTS.local.md`, `service.json` and `commands/add-notes.md` byte-for-byte. The live registry then showed the five commands and the model defaults.
- `tests/test_install.py` covers command delivery: dry run, backup, repeat runs and preservation of local commands (11 tests passing).

### Spec scope review refinement

- Two live fixtures tested the revised `/xm-spec-review`: a small category-total CLI and the same useful core burdened with a database, extra fields, queues, a web UI and speculative adapters. Astra recommended no substantive cuts to the right-sized spec and specific removals/deferrals from the overbuilt spec.
- Every reviewer message used `openai/gpt-6-astra#xhigh`. Both reports included the exact user-choice handoff; both Fable parent sessions presented the recommendations and waited for choices. Fixture files remained unchanged. Reviewer calls cost about $0.63 combined; these small examples are a behavior check, not a general quality benchmark.
- Local review session IDs: right-sized `ses_e32aadd7effev8oVAq2zQ3j5uY`; overbuilt `ses_e32aadd7fffe8bHwYj6fTrYonD`. The 11 installer tests also passed after the refinement.
- Installed the command on the Surface through the standard installer and added the same command plus its `xm-reviewer` profile to `sim-funds` and `sim-prime-broker`. Those containers had OpenCode 2.2.5 but no existing global commands or reviewer profile. Their other settings and service files were preserved. The Halo host and `workspace-smoke` had no OpenCode installation.
- All three installed command files matched SHA-256 `47a65e153563bfc6d1a07f4167b1847993cd8a5afb24eddd8eff293b9aeafdbf`. Live registries showed the new description and restricted child reviewer on the Surface and at both `/home/builder` and `/workspace` in each business container. Container verification covered installation and registration; the paid behavior checks ran on the Surface.

### Plan writing refinement

- A live `/xm-plan-write` run used an approved category-total CLI spec, a selected existing plan stub, and earlier conversation context proposing a database, extra fields, a dashboard and provider plugins. Opus revised only the selected plan, kept the superseded additions excluded, and produced one cohesive implementation task with concrete behavioral checks and no full test implementations.
- Every assistant message used `anthropic/claude-opus-5-5#xhigh`; the session remained in `xm-planner`. It made no shell, subagent or question calls, labelled verification commands as planned checks, and stopped with the optional review commands and a fresh Astra Build-session handoff.
- Session `ses_e328361dfffehih0s32b20qR8G` cost about $0.92. All 11 installer tests and `git diff --check` passed. This checks the revised prompt in isolation; it does not compare reasoning effort levels.
- **Installation completed 2026-11-12:** the refined `xm-plan-write` is installed on the Surface, `sim-funds` and `sim-prime-broker`. The containers also received the `xm-planner` profile and repository-pinned Superpowers plugin, which supplies the required `writing-plans` skill. Existing settings, the spec-review command and service files were preserved, with changed configuration backed up.
- All three installed plan-writer files matched the live-tested source SHA-256 `793769d0e9fcf231dda8164cb103af4ab3c37a3f95bc667ba01e0c249171d80a`. Verified the command, Opus 5.5 `xhigh` primary planner, restrictive planner permissions, active pinned Superpowers plugin and `writing-plans` skill in the Surface repository and at both `/home/builder` and `/workspace` in each container. These container checks establish installation and registration; the paid planning behavior check above ran on the Surface.

## Document organization and Surface rollout, 2026-11-12

The [document index](../README.md) records all seven moves and their approval provenance. Migration checks resolved 46 internal links and anchors, confirmed all 17 retained ignored Superpowers state files were byte-for-byte unchanged, and reproduced the original bodies of all four archived plans after reversing only added provenance/status notes and navigation repairs. Existing uncommitted Fable changes and historical installation evidence were preserved.

Validation used OpenCode 2.2.7 on Windows. The unit suite ran 126 tests: 116 passed and 10 platform-specific cases were skipped. Both changed skills (`naming-files` and `project-setup`) passed `skills-ref` validation. Isolated installation and the Surface installation both returned `MATCH` for baseline `e6b2d46ff2bddd21becdae05d3ee49aa6e3b89e2d7bd4f4c8c45cf7cde594e7e`.

Twelve focused live cases used scratch repositories with the shared instructions and installed harness. All five XM commands were exercised, with each command's assistant messages using its configured model and variant. All 41 file checks passed.

| Case | Observed result |
|---|---|
| New and legacy discovery | Spec review selected the sole top-level new spec; Carbon plan review selected the sole legacy plan and its linked legacy spec. Indexes and archives were excluded. |
| Ambiguity and missing input | Two eligible specs across new and legacy directories produced a candidate list and no selection. A missing explicit planner input failed without substitution or writes. |
| Plan writing and revision | Omitted-path planning created one dated active plan. A conversation-selected spec revised the selected legacy plan in place. Plans had status and resolving spec links, exact optional review commands, and stopped before implementation. |
| Archived inputs | Explicit archived simplify/code reviews left documents unchanged; code review found the planted float-arithmetic defect. Both a conversation-selected archive and a direct archived-plan argument produced new active plans with spec/provenance links, preserving archive bytes. |
| Planner permissions | Native write attempts succeeded for active plans in both supported directories. Both archives, nested archive paths, a spec and a source file returned `permission.rejected`; disk readback confirmed the denied files were unchanged. |
| Ordinary Superpowers | Brainstorming and `writing-plans` saved `docs/specs/total-by-category-design.md` and `docs/plans/2026-11-12-total-by-category.md`, with a resolving spec link, Draft status and exact optional XM commands. No product source files were created. |

The final direct-archive and new-plan cases used planner SHA-256 `270dabf28ab70d85ffe809de025860c0721aea8eac538637de1548438eabeeaf`; the earlier missing-input and selected-plan cases preceded the direct-plan-input refinement. The subsequent built-in Plan handoff clarification was checked against its live edit permissions and the skill validator. It does not widen that agent's permissions.

Useful session references: direct archive `ses_e2fd45848ffezGUsfCs8THNjTj`, new plan `ses_e2fd435f9ffeSFyk2goHfOnDhu`, permission probes `ses_e2fd49430ffeDEf340EL8FCDjg`, ordinary Superpowers `ses_e2fd48f40ffevHxd4NWWAPjiyv`, and legacy Carbon reviewer `ses_e2fd4daa7ffeMsVVcsh7X7TD9I`. Carbon reported unchanged plan hash `d170b31a5d8558fc658265fc1c66c335fcf15ed8` and spec hash `c010b7079ceea9ffc014300540c072662047c718`, plus the companion-review hold. The run used 17 sessions including parents and cost about $7.99. Scratch reports and fixture hashes are at `C:\Users\preid\AppData\Local\Temp\opencode-layout-live-20261112-093037`; all test sessions were idle at closeout. The expected ambiguous-selection parent form and automatic post-Carbon parent response were interrupted after capturing the reviewers' results.

This was a filing and compatibility check, not a general certification of Superpowers planning behavior. Its ordinary workflow amended a design detail after approval and ran in-memory sample checks; upstream skills were left unchanged. Carbon attempted a disallowed Python version check, then completed with the permitted read-only tools.

The Surface rollout used the standard preview and installer, with backups under `~/.config/opencode/backups/`. The loaded registry showed all five commands, Fable 5.2 `high` for `xm-planner`, both plan-directory allows followed by both archive denies, and the updated skills. All configuration outside `xm-planner` and 13 unaffected installed files were preserved, including `AGENTS.local.md` and `commands/add-notes.md`. No other repository or container was migrated, and this change was not published.

## Running the commands from a script

`opencode run "/name"` is reported upstream not to expand slash commands as of 2.2.6 ([#62626](https://github.com/anomalyco/opencode/issues/62626)); that was not retested. The session command API does run them, and the live runs above used it:

1. Create a session: `POST /api/session` with a `location.directory`. The check also passed `agent` and `model`.
2. Run the command: `POST /api/session/<id>/command` with `{"name": "xm-plan-review", "text": "<arguments>"}`.
3. Find the review's child session with `GET /api/session?parentID=<id>`. `/xm-plan-write` runs in the session itself.
4. `POST /api/experimental/session/<id>/wait` on the child, or on the session for `/xm-plan-write`, blocks until it is idle.
5. `GET /api/session/<id>` reports outcome, cost, agent and model. `GET /api/session/<id>/message` returns the messages, and each assistant message names the model that produced it.

`opencode api <method> <path> --data '<json>'` sends these through the background service. The wait endpoint is experimental.

## Changing models, prompts or permissions

- **Models.** A command's model is set in its `model:` line. The planner's also appears in `agents.xm-planner.model`. The README tables list all of them, and `tests/test_install.py` asserts the `title`, `explore` and `general` defaults. Confirm the variant exists for the new model.
- **Reviewer Git commands.** The `xm-reviewer` allow rules match the whole command, so a command must begin with an allowed form. In the first live run these were denied: Git with global options (`git --no-optional-locks …`, `git -c …`), compound lines containing any other command, `Get-FileHash`, `git ls-files` and `python`. The plan and code review prompts name the allowed standalone forms; the spec review uses read-only file and documentation tools and requires no Git metadata. If a prompt needs another Git form, add the matching rule in `global/opencode.json`.
- **Removing or renaming a command.** The installation receipt removes an unchanged retired command on the next install, with a backup; locally changed retired commands are kept and named. No `install.py` change is needed for commands tracked by a receipt.
- **Live check.** The unit tests cover delivery only. To check behavior without touching the global config:
  1. Create a scratch project with a small spec and plan. Run `git init` and commit before OpenCode first loads the directory. In the first run the planner described the fixture as a non-Git directory; the location had been queried before `git init`.
  2. Install into it with `install.ps1 -Destination <scratch>\.opencode` or `install.sh --destination <scratch>/.opencode`.
  3. Confirm registration with `opencode api get "/api/command?location[directory]=<URL-encoded path>"` and the same query on `/api/agent`. Initial reads for new or reloaded locations have returned incomplete command/agent lists; subsequent reads after loading settled were complete. The container rollout also used `/api/location/reload` while no sessions were active.
  4. Run the changed commands through the API sequence above and compare each assistant message's model with the pin. For spec review, use both an overbuilt example and a right-sized example; check that it makes justified cuts, accepts appropriate scope, and includes the user-choice handoff. This calls paid models.
     For document organization changes, cover new and legacy top-level discovery, ambiguity across both locations, archive/index exclusion, explicit missing paths, explicit archived reviews, selected legacy-plan revision, archived-plan follow-up into a new active plan, and denied edits outside active plan locations. Also exercise ordinary Superpowers spec and plan saving under the shared instructions, without an XM command.
  5. Preview and run the global installer, then repeat step 3 for a real project.

## Limits and open items

- **Review refinements:** code-review scope and verification are described [above](#code-review-verification-and-scope). The separate spec/plan reviewer refinements still have their own verification and rollout status under [reviewer perspectives and efficiency](#reviewer-perspectives-and-efficiency).
- **Guardrails, not a sandbox.** No rule denies Code Mode (`execute`) or MCP tools for `xm-planner` or `xm-reviewer`, and the allowed Git patterns also match forms that write, such as `git diff --no-ext-diff --no-textconv --output=<file>` and `git symbolic-ref <name> <ref>`. Reviewer prompts require read-only inspection; plan and code reviews also explicitly forbid Git output writes and external helpers. The spec review directs the agent to file and documentation tools. Tightening the permission rules was not part of this work; decide on it before using the commands on a repository you do not trust.
- **Not verified:** how the TUI behaves when the two background plan reviews report back at different times (the check used one parent session per command, through the API); a follow-up turn after `/xm-plan-write` (only the session's stored model was read); full command execution on Linux/Halo beyond the spec review installation and registration checks above; whether a `.env` read prompt inside a background reviewer reaches the user.
- **Model picks are dated.** They reflect the models and prices available on 2026-11-11. Revisit them when a provider ships a new model or the billing arrangement changes.

### Deferred work

These follow-ups are intentionally separate from the shared simulation guidance above and are not prerequisites for that refinement.

- [ ] **Boundary review:** examine simulated participant/evaluator information boundaries and development-reviewer read-only enforcement in a dedicated session. Distinguish the intended boundaries from implementation choices, and determine what must be enforced before relying on independent-performance claims. Keep later institutional deployment policies separate.
- [ ] **Optional workflow assistance:** examine handoff/reconciliation improvements and any opt-in runner in a separate session. Preserve explicit invocation and existing approval behavior, and assess integration costs before implementation.
