# Ops harness starting points

Updated 13 November 2026. These are interview starting briefs, not approved specifications or implementation plans.

The goal is a licensable operations application, potentially delivered entirely as a portable harness, that becomes the user's main middle- and back-office interface. Month 1 builds an autonomous institutional world that supplies its operational evidence. One command or schedule must start the necessary actions across all nine actors for a selected trade date, with zero manual intervention after setup. The principal harness build begins in month 2. Read [project direction](project-direction.md) for the governing decisions and visual roadmap.

## Start here

Continue the [ops-harness interview](ops-harness/starting-point.md) and its [shared terms](ops-harness/shared-terms.md), then follow the actor order below. The [decision-audit interview](interview-handoff.md#decision-audit-interview) records the 38 answers and latest correction: a separate [privates-agent](privates-agent.md) handles private loans and warrants, while [loan agents](loan-agents.md) handle syndicated loans only. Do not restart settled questions. This product planning does not move principal harness implementation into month 1.

**Actor runtime and hands-on work are distinct.** The nine simulated actor verticals act through schedules and agents without Patrick approving messages, resolving their breaks or overriding their decisions. Ops-harness, ops-infra and shared integration, replay and valuation work remain hands-on, with human-in-the-loop steps where appropriate. The simulated world does not depend on the harness being present.

Each brief distinguishes confirmed decisions, proposed scenarios and unresolved research. Open questions are intentional inputs to its cross-model interview, not permission to silently choose product scope.

## Interview order and month-1 effort

The percentages below preserve the **earlier proposal for eight verticals**, covering month-1 research, specification, implementation and verification. They are not a complete allocation for the new nine-vertical roster, elapsed-time estimates, model-token budgets or proof that the target fits one month. Patrick requested roughly 25% for funds and a reduced loan-agent share; the other exact percentages were planning judgments. A revised allocation, including the syndicated-loan/privates split, remains to be agreed.

| Earlier order / new entry | Starting brief / responsibility | Earlier effort proposal | Main result |
| --- | --- | ---: | --- |
| First, underway | [Ops-harness](ops-harness/starting-point.md) and [shared terms](ops-harness/shared-terms.md) | 0% implementation | Continue product/evidence framing and months 2–4; main build in month 2 |
| 1 | [Funds](funds.md) | 25% | Twelve strategy funds, portfolios, bookings, rule-based financing allocation and recipient files |
| 2 | [Prime brokers](prime-brokers.md) | 13% | Independent PB books, financing, settlement and reporting |
| 3 | [OTC counterparties](otc-counterparties.md) | 13% | Bilateral records, communications, calculations, collateral and calls |
| 4 | [FCMs](fcms.md) | 10% | Listed futures and cleared-CDS workflows, margin and reports |
| 5 | [Administrators](administrators.md) | 9% | Administrator records and distinct platform evidence |
| 6 | [Market-data providers](market-data.md) | 7% | Historical observations, reference coverage and reproducible deliveries |
| 7 | [Loan agents](loan-agents.md) | 3% before scope split; revise | Syndicated secondary-trade servicing only |
| Placement TBD | [Privates-agent](privates-agent.md) | TBD | Private-loan cash interest/simple PIK and private-warrant cash/cashless exercise |
| 8 | [Executing brokers](executing-brokers.md) | 4% | Independent execution evidence and corrections |
| Follow-through | [Shared world, replay and evaluation](shared-world.md) | 14% | Connected operations, evidence playback and independent evaluation |
| Follow-through | [Existing infrastructure](../../ops-infra/readme.md) via shared-world review | 2% | Necessary workspace, runtime and recovery integration |
| | **Earlier proposal subtotal** | **100%** | Excludes a separate privates-agent allocation; revised total TBD |

The numbered positions retain the earlier interview order. Privates-agent is shown beside loan agents for navigation, not as a newly approved interview position or build sequence. Private loans remain the last instrument to implement. Early product/vocabulary framing is included in planning effort across affected responsibilities; 0% means no principal ops-harness implementation in month 1.

Funds receive more effort because twelve distinct strategies and financing-aware allocations drive the world. Privates-agent has bounded private-loan servicing and warrant workflows. The historical less-than-5%-of-PB-effort cap concerns the original small private-agent role, not the entire new vertical; selected warrant functionality takes priority if that estimate must increase. Protect integration effort: isolated file generators do not establish that institutions exchange coherent evidence across days. Infrastructure assumes reuse; inspect the actual runtime before relying on that allowance.

## What is already decided

- Nine actor verticals, including separate privates-agent; no month-1 custodian or separate post-trade vertical. Administrators include platform-style matching, affirmation and reconciliation outputs.
- Twelve strategy funds, one per agreed type, all suffixed `-1`; one administrator per fund; multiple other relationships supported. Whole-trade allocations chosen by rules in the fund vertical.
- All agreed instruments at credible-workflow depth, including private loans last. See the [exact product list](project-direction.md#product-scope).
- Independent records and calculations, realistic risk/financing constraints and reports/calls. Choose strategy portfolios first, then size opening cash/collateral around them; routine calls and contractual flows remain active.
- All nine actors run unattended on schedules/agents once configured. Strongest-frontier institutional leaders use prescribed incentives and researched precedent; their choices are not overridden by a human during the run.
- Historical market baseline with fictional portfolios/trades. Start with evidence playback and decision/event logs; full processing reconstruction is deferred. Exact dates, durations, providers and first exceptions remain open.
- Shared terms owned by ops-harness, with no implied shared access to private books or hidden expected answers.
- OMS and instrument-master modules begin as shared foundations designed for later independent actor variants and selective updates. FINOS CDM remains the selected foundation; verify coverage, approve researched supplements and establish requirements product by product. Retain versioned agreed terms.
- The harness covers reconciliation, settlement, reference-data maintenance, financing and treasury. Readiness is a setup check using explicit assumptions, not an ongoing harness capability.
- Bilateral OTC options are now included in month 1. Existing listed-options research is not automatically a bilateral-OTC specification.
- The harness may autonomously correct authorized fund records only; other verticals correct their own records. External communications initially require approval of the exact message and recipients, renewed for material content/evidence changes; actor-to-actor messages do not.
- The 80% classify-and-prescribe target applies independently to each supported break family, not resolution. Other quality measures are initially reporting only; fresh held-out cases use familiar patterns/layouts. Failure/control checks are required at first integrated acceptance, and failures hold affected dependencies while independent work continues.
- Jev-style models assign typed characteristics/likelihoods; frontier agents investigate and exercise judgment. Priority weights and a few possible queue categories are deferred.
- New patterns are reported in a PDF for a separate investigation. Month 4 begins cheaper-worker and subsequent open-weight experiments, with strongest-frontier leadership retained.
- OpenCode-first development remains a preference with portable interfaces and skills. The form reviewer stays a later candidate; scheduled research–critic work is excluded from the current direction.

## How to use a brief

1. Read project direction, the chosen brief and shared terms. Inspect the current owning repository if one exists; these notes do not prove deployed behavior.
2. Start the brief's interview prompt. Ask one focused multiple-choice question at a time; distinguish researchable facts from Patrick's preferences. Do not repeat settled commercial, roster, autonomy or model-role questions, or force the deferred scoring choices now.
3. Read selected deeper sources. ZIP links open an archive; the named member is the specific file to inspect. Not all fields, examples or old proposals are adopted.
4. Resolve the first scenario and cross-actor agreements. Record decisions, proposals, unanswered questions and source limitations separately.
5. Write the maintained specification in the owning repository, then use the [current cross-model workflow](../README.md) to review it and develop/review its implementation plan. Use exact artifact paths.

The shared workflow normally keeps maintained specs in `docs/specs/`, active plans in `docs/plans/` and completed plans in `docs/plans/archive/`, subject to owning-repository instructions. Check the linked workflow before invoking commands. This task has not run cross-model reviews or approved implementation plans.

## Two focused follow-ups

**Strategy and portfolio pass.** During funds planning, research each strategy and build a compact strategy/instrument/relationship matrix. Identify plausible holdings and hedges, trading activity, financing needs, mandate and first operational scenario. Patrick can assess realism against his experience. A strategy name is not an investment algorithm or permission to add instruments without a decision.

**Joint instrument-workflow sessions.** Before finalizing dependent actor plans, walk one representative trade or existing position through the relevant institutions. Agree execution evidence, booking, allocation, reports, calculations, timing, one exception and observable completion. Prioritize gaps such as futures/FCMs, cleared CDS, private warrants and private loans. Existing research narrows the questions but does not replace them.

These follow-ups are agreed. Their detailed answers remain open; the starting briefs can be used immediately.

Use connected graphs throughout: [roadmap and autonomy boundary](project-direction.md), [actor relationships](vertical-map.md), and [harness case, scoring and learning flows](ops-harness/starting-point.md). Graphs express planned behavior, not evidence that the software has been built.

## Navigation and source authority

- [Vertical map](vertical-map.md): responsibilities, relationships and product/workflow boundaries.
- [Interview handoff](interview-handoff.md#decision-audit-interview): confirmed audit answers, where to resume and which questions remain open.
- [Decision audit](decision-audit.md): historical findings and source evidence, read with the subsequent interview decisions.
- [Source review](source-review.md): conflicts, superseded proposals and review limits.
- [Source catalog](source-catalog.md): all retained sources and archive members.
- [Interactive source map](index.html): browse the original collection by subject.

Current interview decisions govern intent; current owning repositories establish their documented implementation state. Original research remains reference material, not vendor certification or adopted schemas. The older `sim-funds` cash-equity demonstration is reusable but does not cap the new month-1 scope. No original personal source files were rewritten.

This is the user-selected preparation home inside `opencode-defaults`. It does not make financial simulation part of the shared coding harness. No new application repositories, deployments or dependencies are created by these briefs. The glossary lives in [the ops-harness subfolder](ops-harness/shared-terms.md); move the canonical file, rather than copying it, when the application repository is established.

## Source-map maintenance

The HTML source map is a standalone local file with no external libraries or network requests. It embeds the [JSON inventory](source-inventory.json); editing that JSON alone does not refresh the map. If the original source collection changes, update the catalog, JSON inventory and embedded snapshot together. New briefs are navigation links, not additions to the original-source inventory.

Links assume this package remains beside the sibling repositories and existing `pr1` collection. Copying it elsewhere requires repairing links or retaining the layout. The historical review covered 76 loose files and 431 file entries across 12 archives; [source review](source-review.md#coverage-and-limits) records what was and was not verified.
