# Prime brokers: starting brief

Updated 13 November 2026. Interview input for the PB vertical, not an approved specification or implementation plan.

Read the [overview](README.md), [project direction](project-direction.md), [vertical map](vertical-map.md), [shared terms](ops-harness/shared-terms.md) and [shared world brief](shared-world.md). Interview the harness and funds before this vertical so its evidence serves agreed operator workflows. PBs receive **13% of the proposed month-1 effort allocation**; feasibility remains unvalidated.

The [decision-audit interview](interview-handoff.md#decision-audit-interview) records the confirmed foundation, product, authority and evaluation choices that govern this brief's remaining questions.

## Purpose and confirmed direction

Prime brokers provide an independent institutional view of the fund relationships they service. The intended result is credible PB evidence an operations user can compare with fund records: accepted activity, positions, cash, financing information, reports, calls and discrepancies.

**Confirmed:** PBs are one of the nine month-1 institutional role types. Funds can have multiple PB relationships. The fund applies a rule to assign a whole trade to one PB when relevant; the PB does not choose allocations for the fund or silently distribute a trade across other PBs. PBs maintain their own state and perform their own applicable calculations. Choose strategy portfolios first, then size opening cash and collateral around them. Realistic reports, ordinary calls and contractual cash flows remain active during the opening days.

The institution count, account structure, serviced instruments, financing terms and minimum daily behavior are still open. No separate custodian vertical is selected. That decision does not automatically transfer every custodial function to the PB; identify the evidence needed for the chosen scenario and agree its source.

## Autonomous daily operation

**Confirmed:** after setup, PBs and the other eight actor types operate with zero human intervention, approvals or decision overrides. A single simulate-trade-date command schedules the necessary work. PB behavior cannot depend on ops-harness or Patrick responding as a simulated employee.

The strongest frontier agents make top-level PB judgments from its own incentives, limited information and private state. Supporting a client can conflict with protecting the PB's capital. Judgment may be unwise; retain its consequences instead of having a human correct the choice. Fund-owned rule-based financing allocation remains separate from the PB's own acceptance and financing decisions.

**Proposed daily flow:** process incoming activity and pending settlements; update independent positions and financing calculations; assess client requests and the PB's exposure; issue reports, calls and responses; follow up through actor channels; then carry unresolved matters forward. Define these policies and schedules during setup. A delivery fail or disputed call can remain open while daily processing continues. A failed model/tool invocation or job must be reported as a technical failure, not disguised as business disagreement or successful completion.

## Proposed ownership and role boundaries

A PB should own its received instructions, relationship/account configuration, local booking and acceptance history, positions, cash and obligations, financing state, calculations, notices and delivered reports. These are the PB's records as known at each point in the replay, not projections copied from the fund's answers.

Each relationship identifies the fund/account served and applicable terms. Shared reference data must not expose private fund records or hidden scenario answers. A shared legal group name must not blur executing-broker, FCM, OTC-counterparty and PB roles.

The executing broker supplies its own execution evidence. The FCM owns the selected clearing-account workflows. Bilateral derivatives, including the now-required bilateral OTC options, belong with the OTC-counterparty vertical unless a scenario gives a PB a separately identified role. Administrators/platform functions own their agreed independent records and matching, affirmation or reconciliation evidence.

Define the PB agent's correction/dispute actions and responses to other actors. Any operator approval for actions proposed by the separate ops-harness product must not become a dependency of the autonomous PB simulation.

The PB corrects its own records. The harness can communicate discrepancies or requests, but cannot directly edit the PB book. Shared OMS and instrument-master foundations are intended to support later independently maintained actor variants, with selective adoption of shared improvements and separate private data from the outset.

## Evidence to receive and send

**Proposed inputs:** fund trade instructions and amendments, recipient/account mappings, relevant broker or platform evidence, pinned instrument and market observations, opening relationship balances and agreed financing terms. Missing terms, unknown accounts or unsupported instruments should remain visible issues rather than be silently completed from another actor's private state.

**Proposed outputs:** delivery acknowledgements and business acceptances/rejections where needed, activity and position reports, cash/obligation evidence, financing statements, calls and responses, and correction/dispute status. Exact report types and intraday versus EOD timing remain interview choices.

For each report or call, identify its date, supporting information and response path. Preserve prior versions and enough detail to explain differing totals.

The initial shared OMS will use two differently shaped synthetic recipient profiles, tested to preserve equivalent quantities, cash and obligations. These are simulator-owned formats, not certified vendor interfaces. Coordinate the receiving PB interpretation with the [fund brief](funds.md).

Research must establish the selected meaning of financing and headroom for the relevant products. This brief selects no haircut, margin, stock-borrow, interest or fee formula. Do not substitute one generic account balance for every requirement or treat missing charges as confirmed zero.

## Proposed first scenario

Connect one fund to at least two PB relationships so its allocation rule has a visible consequence. Process representative activity independently, then deliver account and financing evidence. Each PB receives only activity and information supported by its relationship.

Start with a routine day that respects opening headroom. Add a revised trade, delayed acceptance or financing discrepancy that actors address autonomously and a later harness can investigate. Choose a plausible cause during interview and define agent-issued calls, queries or instructions. An unresolved business matter remains pending without waiting for a human to choose the PB's response.

The world-level product breadth does not imply that every PB supports every product. Confirm its service map against all twelve funds and coordinate gaps with the relevant actor brief. Use historical replay and fictional account activity consistently with the shared world.

## Proposed acceptance examples

- The fund's allocation is explainable and the chosen PB independently accepts or rejects the instruction. Re-delivery does not create another position.
- A reviewer can reconstruct the PB's reported position and financing result from its own opening state, received evidence, agreed terms and available observations.
- PB and fund disagreement has an inspectable cause and response history. Neither actor obtains the other's hidden calculations to make the test pass.
- A report, call and subsequent action retain distinct identities and states. Issuing a call is not proof that a payment happened.
- Corrections preserve the original report and show the changed result. The original as-known view remains available.
- At least one complete cross-actor case demonstrates useful evidence for the harness, beyond a syntactically valid PB file.
- One configured simulate-trade-date command runs PB calculations, frontier-agent decisions, reports and scheduled responses without human prompts, approvals, overrides or ops-harness. An unwise agent decision is retained for evaluation.
- A business fail can remain pending into another day; a technical execution failure is explicitly reported, holding affected work while independent processing continues. Initial replay is evidence playback with decision/event logs, not full processing reconstruction. Fresh frontier choices may differ.

## Focused interview and research agenda

Begin with one named fund relationship: what does its PB receive, calculate and send, and how does its frontier agent choose a response? Define the tension between client service and protecting its own capital. Then choose institution/account counts and differentiated terms.

Resolve the service map, opening balances, financing capacity, reports/calls, response mechanics and correction behavior. Identify which obligations require actual simulated movements and which are evidenced by explicit external notices. Agree one normal and one exception walkthrough before selecting field layouts or persistence technology.

Research representative interfaces and financing conventions using current primary sources. Distinguish synthetic conventions from verified vendor specifications. Inspect the actual PB implementation: the earlier review recorded a workspace but did not audit its financial behavior.

## Relevant sources

- [Current sim-funds baseline](../../sim-funds/readme.md): establishes the old outbound PB-file example, not an implemented receiving PB or the expanded financing scope.
- [Cash-equity packet](../../../pr1/business/ops-harness/research/equities/cash-equity-research-packet.zip): `cash_equity_oms_to_pb_research.md`, `recipient_field_matrix.csv`, `SIMFUNDS_20261014_fidelity_inspired.csv` and `SIMFUNDS_20261014_ibkr_inspired.csv`. These are research and synthetic profiles, not certified adapters.
- [Retained IBKR upload source](../../../pr1/business/ops-harness/research/trade-file-sources/ibkr-prime-trade-upload.html) and [retained Allvue/Goldman export source](../../../pr1/business/ops-harness/research/trade-file-sources/allvue-goldman-sachs-trade-export.html): concrete interface leads; reverify their applicability before adoption.
- [Historical verticals context](../../../pr1/business/ops-harness/notes/2026-10-30_hedge-fund-verticals-context.md), [source review](source-review.md) and [source catalog](source-catalog.md): actor-boundary history and research limits. Earlier setup alternatives and narrow demonstrations do not override this interview.

## Fresh-session prompt

> Continue the prime-broker interview in plan mode using this brief and its common links. Preserve independent PB records/calculations, fund-owned rule-based whole-trade allocation and realistic financing. Strongest frontier agents choose PB actions from its own incentives and available evidence. One configured simulate-trade-date command must run the world without ops-harness or human intervention, approvals or decision overrides. Walk through a normal day and a business exception carried forward autonomously; distinguish technical failures. Read the harness/fund decisions, including bilateral OTC-option scope, and ask one question at a time. Verify assumptions before a cross-model specification and plan. Do not implement from this brief.
