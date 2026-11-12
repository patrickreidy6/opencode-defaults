# Cross-model workflow: design record

Design record for the opt-in `/xm-*` commands, verified 2026-11-11 on OpenCode 2.2.7 (Windows). Usage and the per-command model table are in the [README](../README.md#opt-in-cross-model-workflow). Implemented in [`global/commands/`](../global/commands/), the `xm-planner` and `xm-reviewer` agents in [`global/opencode.json`](../global/opencode.json), and the command copy step in [`install.py`](../install.py).

## Intent

Add review by a different model vendor at each stage of spec-driven work, for the few projects where the extra cost is justified: foundational specs and new codebases. Ordinary Plan and Superpowers sessions remain the default and are unaffected unless a command is typed.

## Decisions

- **Commands carry the models.** Plan writing and each review are slash commands with a pinned model. Authoring and execution are ordinary sessions on a model selected with `/models`. Nothing chains the stages; the user starts each one.
- **A different vendor reviews each artifact.**

  | Artifact | Written by | Reviewed by |
  |---|---|---|
  | Spec | Claude Fable 5.2 | GPT-6 Astra |
  | Plan | Claude Opus 5.5 | Gemini 4 Carbon (technical) and GPT-6 Astra (simplification) |
  | Code | GPT-6 Astra, including `general` workers | Claude Fable 5.2 |

- **Reviewers report and the author revises.** Review commands return findings and do not edit the artifact. The spec review ends with an explicit handoff requiring the authoring session to present scope recommendations and wait for the user's choices before editing.
- **Spec review judges the build's value and size.** Astra identifies the core payoff, challenges unnecessary features and data fields, and recommends what to remove, shrink or defer. Essential gaps matter when they threaten the intended outcome. The report recommends a build boundary rather than assigning a generic readiness verdict. Unlike plan simplification, it may challenge the proposed requirements themselves.
- **Planning preserves the approved scope.** Opus produces cohesive tasks, precise shared contracts and meaningful checks for a capable Astra executor. It carries forward exclusions and deferrals, justifies consequential implementation additions, and leaves routine coding choices open. The command overrides the generic `writing-plans` template's fixed review-case quota, exhaustive test-code prescriptions and execution-method menu.
- **When both plan reviews are requested, they run on one unchanged draft.** Each reports the plan and spec content hashes and tells the parent to wait if its companion is running, so both are reconciled in one revision. A single requested review does not create a wait for an unrequested companion.
- **High-volume work stays on OpenAI.** OpenAI usage draws on prepaid credits; Anthropic and Google are billed per call. Execution, `general` workers, `explore` and `title` run on OpenAI models, and Anthropic and Google handle the low-volume authoring and review stages.
- **An omitted path is never guessed.** The restricted agents have no reliable way to read modification times, so a command without a path proceeds only when the Superpowers directory holds exactly one candidate.

## OpenCode behavior the design depends on

From the V2 [agents](https://opencode.ai/docs/agents/), [commands](https://opencode.ai/docs/commands/), [models](https://opencode.ai/docs/models/) and [permissions](https://opencode.ai/docs/permissions/) documentation:

- A session stores its own model, and selecting a primary agent does not change it. A command's `model` overrides every other model for that command, and a subagent uses its configured model. This is why the stages are commands and not primary agents with models attached.
- The root `model` keeps no `#variant`. Agent and command model references do.
- Variants belong to each model. Gemini 4 Carbon offers `low`, `medium` and `high` only, so its review is pinned to `high`. An unknown variant fails model resolution.
- The built-in `plan` agent may edit only files under `~/.opencode/plan`, so it cannot save a plan in a repository. `xm-planner` may edit `docs/superpowers/plans/*.md` and nothing else, with shell and delegation denied.
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
  5. Preview and run the global installer, then repeat step 3 for a real project.

## Limits and open items

- **Guardrails, not a sandbox.** No rule denies Code Mode (`execute`) or MCP tools for `xm-planner` or `xm-reviewer`, and the allowed Git patterns also match forms that write, such as `git diff --no-ext-diff --no-textconv --output=<file>` and `git symbolic-ref <name> <ref>`. Reviewer prompts require read-only inspection; plan and code reviews also explicitly forbid Git output writes and external helpers. The spec review directs the agent to file and documentation tools. Tightening the permission rules was not part of this work; decide on it before using the commands on a repository you do not trust.
- **Not verified:** how the TUI behaves when the two background plan reviews report back at different times (the check used one parent session per command, through the API); a follow-up turn after `/xm-plan-write` (only the session's stored model was read); full command execution on Linux/Halo beyond the spec review installation and registration checks above; whether a `.env` read prompt inside a background reviewer reaches the user.
- **Model picks are dated.** They reflect the models and prices available on 2026-11-11. Revisit them when a provider ships a new model or the billing arrangement changes.
