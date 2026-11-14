# Funds: starting brief

Updated 13 November 2026. Interview input for the fund-side vertical, not an approved specification or implementation plan.

Read the [overview](README.md), [project direction](project-direction.md), [vertical map](vertical-map.md), [shared terms](ops-harness/shared-terms.md) and [shared world brief](shared-world.md) first. The harness interview precedes this interview so that the evidence the product needs can inform the simulated funds. Funds receive **25% of the proposed month-1 effort allocation**; this is a planning weight, not a validated delivery estimate.

The [decision-audit interview](interview-handoff.md#decision-audit-interview) records the confirmed foundation, product, authority and evaluation choices that govern this brief's remaining questions.

## Purpose and confirmed direction

The funds supply credible fictional portfolios, activity, instructions and internal records for the simulated world. Their records let an operator explain what a fund intended, what actually happened, what it told each institution and why its own view may differ from received evidence. Investment profitability is not the acceptance measure.

**Confirmed in this interview:** there are twelve funds, one per strategy, each using the suffix `-1`. Each fund has one administrator and may have multiple other institutional relationships. Rule-based allocation belongs in the fund vertical. A whole trade is assigned to one PB or FCM when that relationship applies; splitting one trade across multiple PBs or FCMs is not the selected starting behavior. The allocation rule itself remains to be chosen.

| Fund | Question to settle in its mandate |
|---|---|
| `equity-arb-1` | Which arbitrage situations and hedge instruments generate its activity? |
| `convert-arb-1` | Which convertible profiles and related hedges must be present? |
| `equity-vol-dispersion-1` | Which index/constituent relationships and variance or volatility contracts are needed? |
| `credit-distressed-1` | Which securities, loans and distressed situations are represented initially? |
| `credit-vol-1` | What does credit volatility mean in the initial supported product set? |
| `credit-ig-1` | Which investment-grade exposures and hedges belong in the first portfolio? |
| `credit-hy-1` | Which high-yield exposures and hedges belong in the first portfolio? |
| `equity-activist-1` | What distinguishes its holdings and activity operationally? |
| `equity-longshort-1` | Which long, short and hedge exposures require financing evidence? |
| `equity-quant-1` | What turnover and trade pattern are credible without building a signal engine? |
| `equity-privates-1` | Which private holdings and warrants must the first portfolio contain? |
| `credit-privates-1` | Which existing private loans and servicing events are needed? |

These names do not automatically authorize every instrument suggested by the strategy label. The agreed world-level breadth includes cash equities, listed futures, corporate and convertible bonds, bilateral equity swaps, bilateral variance and volatility swaps, **bilateral OTC options**, cleared single-name and index CDS, private warrants, secondary syndicated-loan trading and simple servicing of existing private loans. The strategy-to-instrument map and exact variants are still open. Private-loan servicing remains in month 1 with lower priority.

Historical observations support replay; holdings and trades are fictional. Choose realistic strategy portfolios first, then size opening cash and collateral around them for the first few ordinary days. Routine margin calls and contractual cash flows remain active. Numerical terms, fund constraints and relationships still need interview decisions and research. Start with one fund per trade; cross-fund block allocation is a later candidate.

## Autonomous daily operation

**Confirmed:** once configured, all nine actors operate with zero human intervention, approvals or overrides of their decisions. One simulate-trade-date command schedules the necessary work across them. Funds must run without ops-harness or Patrick acting as their trader, operations staff or counterparty. Hands-on research and setup are separate from runtime.

The strongest frontier models make the fund's top-level judgments using its own incentives, state and available information. Poor decisions and their consequences can occur; a human does not overrule them to repair the scenario. This does not remove the required lower-level rule-based, whole-trade financing allocation.

**Proposed daily flow:** review opening state, available observations and pending matters; choose activity and responses; apply the fund's allocation rule; process received execution evidence, book and send recipient files; monitor reports, calls and replies; then carry positions, obligations and unresolved work forward. Agent-to-agent questions and follow-ups run through scheduled channels. A business issue may remain open without stopping the world for a human decision. An unavailable model/tool or failed job is an explicit technical failure, not a business break or a successful day.

## Proposed ownership and boundaries

The fund owns its mandate, opening positions and cash, intended activity, execution evidence it has received, allocation decisions, internal bookings, instructions, local calculations and history. Distinguish a generated trading intention from a broker-reported execution and distinguish an instruction from acknowledgement or settlement.

External institutions keep independent state and calculations. Sending a fund booking to the administrator does not make it the administrator's answer. The fund cannot inspect a PB's private book to resolve a disagreement. Shared instrument definitions and scenario references support exchange without becoming shared mutable books or universal matching answers.

Execution simulation belongs with the executing-broker discussion; PB financing belongs with PBs; cleared-product account evidence belongs with FCMs; bilateral contract evidence belongs with OTC counterparties. Syndicated-loan notices belong with [loan agents](loan-agents.md); private-loan servicing and warrant agency belong with the separate [privates-agent](privates-agent.md) vertical. Funds still need their own available evidence and expectations for each relationship. The administrator vertical includes the selected matching, affirmation and reconciliation-platform functions; their boundaries need agreement with that brief.

The harness may autonomously correct authorized fund-side OMS and instrument-master records, with an audit trail through legitimate fund interfaces. Every other vertical maintains and corrects its own records. This fund access does not grant the harness access to other actors' private books or turn the autonomous world into a harness-dependent system.

Use [shared terms](ops-harness/shared-terms.md) for common meanings; it does not establish a separate repository or runtime package.

## Confirmed foundation and product decisions

Initially develop shared OMS and instrument-master modules for reuse by funds, shared simulation support and ops-harness. Build a solid base across the supported instruments with independent actor variants as the intended future state. Each actor then maintains its own versions and selectively adopts shared improvements after compatibility checks. Private data is separate from the outset.

FINOS CDM remains the selected foundation for applicable instrument fields, price representation and verified calculations. Before implementing each product's dependent records and calculations, establish its applicable CDM requirements, calculation inputs, simulation additions and recipient needs. Research coverage gaps and obtain Patrick's approval for a proposed supplement. Select a release and binding during planning; adoption alone does not demonstrate valuation support.

The shared foundation preserves effective versions of master terms. A trade retains its agreed terms version; explicit amendments and reference-data corrections remain distinct. Setup readiness may use recorded assumptions about agreements and eligibility, without requiring supporting simulated executed documents. Detailed lifecycle milestones remain for product and actor interviews, while preserving history and evidence-backed outcomes.

| Product | Confirmed initial depth |
| --- | --- |
| Corporate bonds | Trade consideration, partial/failed settlement and a bounded coupon-entitlement case |
| Convertible bonds | Trading and valuation; conversion elections and delivery claims later |
| Equity swaps | Provider → underlying currency → settlement currency defaults; maturity, performance reset, financing reset, reference rate, signed spread, equity calendar, rate calendar and date adjustment |
| Variance and volatility swaps | A bounded expiry-settlement profile for each, including explicit units, observation handling and settlement corrections; valuation verified separately |
| CDS | ICE/IceLink-led operational research checked against exact contract and clearing-route terms; resolve conflicting historical dates before activating the affected profile |
| Syndicated loans | Fully funded positions and assignments first; unfunded commitments later |
| Private loans | Existing-loan servicing with cash interest and simple explicit PIK, through privates-agent; last in the instrument sequence |
| Private warrants | Cash and cashless exercise with rights and delivery evidence, through privates-agent |

Use two differently shaped synthetic recipient profiles early and verify that each preserves quantities, cash and obligations. Label them simulator-owned; verified vendor compatibility is separate. Select archived numerical examples that match approved profiles, independently verify expected results and reuse them as regression tests. Deferred lifecycle examples remain for later.

## Evidence to receive and send

**Proposed inputs:** pinned instrument and historical market data; opening-state inputs; mandate and relationship terms; broker fills and corrections; PB and FCM account reports and calls; bilateral confirmations and notices; administrator/platform statuses; syndicated-loan-agent and privates-agent notices and borrower communications delivered through the agreed route.

**Proposed outputs:** inspectable opening portfolios, trading instructions, fund allocation records, recipient-specific trade and amendment files, fund-side positions/cash/obligations, and responses to supported notices or discrepancies. The harness needs access to the evidence an operations user could obtain, not evaluator answers or future deliveries.

For each interface, the later interview must identify sender, recipient, business purpose, timing, field meanings, identifiers, units, correction behavior and acknowledgement. Decide formats only after these meanings are clear. Preserve original evidence and revisions; do not count an amendment or duplicate delivery as another trade.

## Proposed first scenario and acceptance examples

Start with an inspectable opening portfolio and a short historical replay for every fund. Select enough activity to establish each mandate and its required institutional relationships, then connect these cases into one complete operational day. The exact dates, number of days, trades per fund and required events remain open.

Use one simple cross-actor transaction first, followed by the remaining agreed product cases, including bilateral OTC options. Include a linked correction or genuine discrepancy that the actors address autonomously and a later harness can investigate from evidence. This sequencing does not replace the twelve-fund target with the old cash-equity demonstration.

**Proposed acceptance examples:**

- A reviewer can explain each opening portfolio, its financing headroom and the permitted activity without inferring missing terms from a strategy name.
- Every trade has one owning fund and an inspectable allocation decision. No balance from another fund hides a funding or position problem.
- A recipient can independently interpret its files. Different recipients receive information appropriate to their role, rather than renamed copies of one export.
- Fund and counterparty views evolve independently. A correction preserves the original evidence and explains its effect without duplicating the economic trade.
- One configured simulate-trade-date command runs the fund's scheduled decisions, allocations, communications and reports with no human prompt, approval or override and no ops-harness dependency. Outstanding business issues carry forward explicitly.
- A technical failure is reported separately from unresolved business work. Neither is silently converted into a clean completed day.
- Initial replay supports evidence playback with decision/event logs. Full processing reconstruction is deferred. A fresh frontier-agent run may choose differently; evaluator answers remain hidden.

## Focused interview and research agenda

Ask one question at a time. First complete a compact mandate matrix: instruments and variants, opening exposures, typical trades, counterparties, financing needs and the evidence each fund should produce. Then walk through the first complete day and one exception. Resolve the allocation rule using a concrete trade with more than one eligible relationship.

Next settle numerical funding buffers around the chosen portfolios, required calculations, missing-input behavior, fund incentives and which autonomous agent owns each response. Confirm whether funds originate instructions before execution or initially ingest generated execution evidence. Do not let both sides independently invent the same fill. Define the OTC-option profiles and evidence without importing listed-options scope. Runtime human approval is not an open choice; approval questions belong to the separate ops-harness support boundary.

Research must verify suitable historical data, instrument terms, applicable CDM support and representative recipient conventions. CDM is selected, but executable coverage for the expanded products still needs verification. Do not import entire field dictionaries, archived formulas or example engines as approved requirements.

## Relevant sources and existing baseline

- [Current sim-funds README](../../sim-funds/readme.md), [strategy definitions](../../sim-funds/docs/strategy-funds.md) and [scenario/acceptance document](../../sim-funds/docs/scenario-and-acceptance.md): inspected baseline is one long-only cash-equity fund, 20 opening holdings, two historical days, 10 new trades per day, two day-2 price amendments and PB/admin EOD files. It does not establish implementation of the expanded scope. Reconcile the owning documents during the later authorized planning session.
- [Cash-equity packet](../../../pr1/business/ops-harness/research/equities/cash-equity-research-packet.zip): `cash_equity_oms_to_pb_research.md`, `oms_bookings_synthetic.csv`, `fill_allocation_links.csv` and `recipient_field_matrix.csv` provide selective research leads.
- [Convertible-bond packet](../../../pr1/business/ops-harness/research/credit/convertible-bonds-research-packet.zip): `packet/convertible_bond_research_report.md` and `packet/operations_research.md` help frame a multi-instrument fund interview; their full lifecycle scope is not adopted.
- [Equity-swap packet](../../../pr1/business/ops-harness/research/equities/equity-swap-master-research-packet.zip): `equity_swap_master/equity_swap_master_research.md` and `equity_swap_master/example_fund_assignments.json` are term/relationship examples, not a selected allocation policy.
- Use the [source catalog](source-catalog.md#research) and [source review](source-review.md) for other instruments and known limitations. Existing research remains provisional.

## Fresh-session prompt

> Continue the fund-side interview in plan mode using this brief and its common links. Preserve twelve funds, fund-owned rule-based whole-trade allocation, historical replay, fictional activity, financing and all month-1 products including bilateral OTC options. Once configured, one simulate-trade-date command must run the actors without ops-harness, human intervention, approvals or overrides. Strongest frontier agents make top-level judgments from private state, incentives and available evidence; unresolved business issues and technical failures remain distinct. Read the owning sim-funds instructions, then interview the strategy/instrument/relationship matrix and an autonomous working day, one question at a time. Separate decisions, proposals and research gaps before a specification and plan. Do not implement from this brief.
