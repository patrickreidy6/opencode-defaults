# Administrator vertical starting point

Status: interview starting brief, 13 November 2026. Confirmed decisions below come from Patrick's interview. Proposed examples are discussion material, not approved specifications. Month-1 effort allocation: **9%**, a planning allocation rather than a delivery estimate.

[Overview](README.md) · [Project direction](project-direction.md) · [Vertical map](vertical-map.md) · [Shared terms](ops-harness/shared-terms.md) · [Shared world](shared-world.md)

The [decision-audit interview](interview-handoff.md#decision-audit-interview) records the confirmed foundation, product, authority and evaluation choices that govern this brief's remaining questions.

## Purpose and confirmed direction

This vertical provides independent administrator evidence and the matching, affirmation, and reconciliation-platform evidence that Patrick wants grouped under the administrator build. Its purpose is to give the future operations harness realistic external records against which to understand a fund's trades, balances, and outstanding work.

**Confirmed:** every fund has exactly one administrator relationship. The initial population is one fund for each of the 12 strategy types, with names ending in `-1`. Funds can have multiple PBs, FCMs, OTC counterparties, and executing brokers. The number of administrator institutions serving those funds has not been decided.

**Confirmed:** matching, affirmation, and reconciliation services belong in this vertical for month 1. This is a build boundary; it does not make all those roles the same institution or the same kind of evidence. Custodians are outside month 1. The target is credible workflows across the agreed instruments, with limited lifecycle coverage. Private loans come last in the instrument sequence.

The world supports historical replay with fictional portfolios and trades. Reports may evolve during development. The principal harness build remains in month 2.

**Confirmed operating model:** after configuration, all nine actor verticals run autonomously from one simulate-trade-date command. The administrator must operate without the ops-harness, user intervention, approval gates, or runtime overrides. Humans configure and evaluate the world; they do not perform administrator actions during a run. The strongest available frontier models supply institutional judgment, applying the administrator's own goals, incentives, mandate, and private state. Probabilistic behavior is permitted.

## Owned state and institutional boundaries

**Proposed:** maintain the administrator's received trade records, its own resulting position/cash views where required, source arrival history, comparison results, outstanding differences, and report versions. For platform-style functions, preserve submitted details, each party's responses, and the resulting workflow status. The precise calculations and status meanings are interview decisions.

Independent state means this vertical derives its view from evidence delivered to it. It must not read another participant's private ledger or the evaluator's expected answer. A matching result should explain the comparison performed; it should not silently establish that settlement happened. Grouping several functions in one build must preserve which role issued each record.

The [fund](funds.md) owns its internal book. [PBs](prime-brokers.md), [FCMs](fcms.md), and [OTC counterparties](otc-counterparties.md) own their respective account, financing, and obligation records. The administrator may compare those records, but it does not take over their calculations. The [shared world](shared-world.md) owns coordination and replay responsibilities, not institutional conclusions.

[Loan agents](loan-agents.md) handle syndicated loans only; the separate [privates-agent](privates-agent.md) handles private-loan servicing and warrant agency. Those roles do not transfer to the administrator merely because it compares their evidence. The administrator corrects its own records; the harness's autonomous business-record write access is limited to funds.

**Open:** how much administrator accounting is necessary in month 1? Full NAV, fee allocation, investor accounting, and a complete fund-accounting engine have not been requested. The interview must choose the smallest independent calculations that make the selected reports credible.

## Evidence received and produced

The following are **proposed evidence families**, not adopted file formats or vendor interfaces.

| Received evidence | Resulting evidence to consider |
| --- | --- |
| Fund trade files and amendments | Receipt/validation responses and administrator trade views |
| Broker or counterparty trade details | Matching results, affirmation/workflow status, unresolved differences |
| PB/FCM account and financing reports | Position/cash comparisons and identified differences |
| Counterparty obligations, syndicated-loan-agent and privates-agent notices | Relevant accrued or expected amounts and reconciliation evidence |
| Market observations and instrument terms | Valuation inputs or administrator calculations where explicitly in scope |
| Corrected or late source records | Revised reports with an explanation of what changed |

Delivery permissions and formats need agreement per workflow. A report available to one fund is not automatically available to every institution.

## Autonomous operating loop

The detailed schedule is a planning decision; the required behavior is autonomous. On its scheduled work or incoming evidence, the administrator processes new records, updates its own views, performs the selected comparisons/calculations, and determines what institutional action is appropriate. Its agent sends queries or responses, requests missing evidence from the relevant actor, publishes reports, and processes subsequent corrections without prompting Patrick.

Platform-style functions follow their own defined submission and response behavior within this vertical. Unresolved differences can remain open with an explanation and a next scheduled action; they must not become requests for a human to complete the simulation. The shared coordinator schedules and delivers work without deciding the administrator's financial conclusions.

## Proposed first scenario and acceptance examples

Start with one fund's trade file and the corresponding independently produced broker evidence. The administrator receives both, records the arrival sequence, and produces a comparison report. In a replay variation, one source arrives late or contains a changed economic detail. The first exception and the responsible institutional actors remain interview questions; all responses and follow-ups occur autonomously.

Acceptance examples to refine with Patrick:

- Agreeing source records produce an explainable match and the chosen administrator view.
- A missing source remains visibly missing; it is not filled from another actor's private book.
- A discrepancy points to the relevant source versions and compared values.
- A later correction changes the current result while retaining the earlier reported result.
- Initial replay supports playback of the delivered evidence and decision/event logs; full processing reconstruction is deferred. A fresh probabilistic run may differ.
- Adding a second fund does not expose the first fund's reports through that fund's relationship.
- One simulate-trade-date command completes the administrator's scheduled activity and inter-actor responses with the harness absent and zero user prompts, approvals, or overrides.

These examples validate evidence behavior, not comprehensive accounting or vendor compatibility.

## Questions for the vertical interview

1. Which reports would Patrick actually use first: trade matching, positions, cash, settlement status, valuation differences, or something else?
2. Which platform roles need distinct identities and messages within this vertical? Which source records establish each status?
3. What calculations must be independent, and what can simply report a received amount with its source?
4. What daily and on-demand outputs matter? What late-report and correction behavior should the first replay show?
5. Which administrator and counterparty actions address each difference, and what autonomous follow-up occurs if it remains unresolved?
6. Which common administrator profile can serve the first funds, and where are materially different profiles required?

## Targeted source map

Read [source review](source-review.md) before adopting older requirements. The [catalog](source-catalog.md#interfaces) records the retained interface examples and their limitations.

- [Allvue/BNY trade acknowledgments](../../../pr1/business/ops-harness/research/trade-file-sources/allvue-bny-trade-acknowledgements.html) and [trade reconciliation](../../../pr1/business/ops-harness/research/trade-file-sources/allvue-bny-trade-reconciliation.html): candidate acknowledgment and comparison evidence. They are historical examples, not a current administrator specification.
- [Simulator architecture](../../../pr1/business/ops-harness/notes/architecture/2026-10-19_simulator-architecture-page-snapshot.md): participant boundaries and exchanged evidence. Older proposals require reconciliation with this interview.
- [CDS packet](../../../pr1/business/ops-harness/research/credit/cds-research-packet.zip): `packet/cds_research_report.md` and `packet/cds_ice_link_crosswalk.csv` are starting references for the relevant workflow vocabulary; select and verify the actual month-1 coverage.
- [Loan packet](../../../pr1/business/ops-harness/research/loans/loans-research-packet.zip): `clearpar_loans/clearpar_platform_notes.md` covers platform concepts; loan-agent servicing belongs in [loan agents](loan-agents.md). The packet excludes private/direct loans.

## Fresh interview prompt

> Start the administrator vertical's cross-model planning interview. Read this brief, project-direction.md, shared-world.md, and ops-harness/shared-terms.md. Preserve the agreed grouping of functions and one-administrator-per-fund relationship. Design autonomous scheduled work and inter-actor responses using frontier-model institutional judgment, private state, and distinct goals/incentives. One simulate-trade-date command must run the world without the harness or any user intervention, approvals, or runtime overrides. Ask one setup/design question at a time; do not introduce human runtime tasks. Define reports, calculations, and no-prompt acceptance checks before choosing software. Do not implement during the interview.
