# OTC counterparties: starting point

Interview brief, 13 November 2026. This records agreed direction and proposes questions and examples for a later cross-model planning session. It is not an approved implementation specification.

Read [project direction](project-direction.md), the [world and interview map](vertical-map.md), and [shared terms](ops-harness/shared-terms.md) first. The [overview](README.md) gives the interview order and effort allocation: this vertical follows prime brokers, precedes FCMs, and has a proposed **13% of month-1 effort**. The commercial ops-harness remains the reason to build this world.

The [decision-audit interview](interview-handoff.md#decision-audit-interview) records the confirmed foundation, product, authority and evaluation choices that govern this brief's remaining questions.

## Purpose and confirmed scope

Represent the dealer side of bilateral relationships, with records, financing constraints, calculations, and communications that exist independently of the fund's book. The fund and dealer must be capable of recording different understandings of an executed transaction. Agreement should be demonstrated through exchanged evidence.

Month 1 requires credible workflows for **bilateral equity swaps, bilateral variance swaps, bilateral volatility swaps, and bilateral OTC options**. Include bounded observation-driven expiry settlement for variance and volatility swaps, with explicit units, observation handling and settlement corrections; valuation must be verified separately. Broad lifecycle coverage remains deferred. Funds may face multiple OTC counterparties with different terms and risk tolerances. The twelve strategy-fund instances are defined in the [fund brief](funds.md); their precise product assignments need the agreed strategy/portfolio follow-up.

Retain the equity-swap defaults hierarchy: provider → underlying currency → settlement currency. Required terms are maturity, performance reset, financing reset, reference rate, signed spread, equity calendar, rate calendar and date adjustment, subject to CDM alignment. Existing trades retain their agreed effective terms version; a changed default does not amend them. Verify detailed cash conventions before activating each profile.

Patrick expects high-touch execution evidence, with instrument-appropriate recaps, term sheets, and confirmations. The detailed documents and delivery sequence remain to be researched and selected. His examples establish the required kind of evidence, not a universal document checklist for every trade.

Financing is functional from the start: counterparties calculate independently, produce realistic reports, and can issue calls. Choose the strategy portfolios first, then size opening cash and collateral around them for several ordinary days. Routine margin calls and contractual cash flows remain active.

**Autonomous operation is confirmed:** once configured, the dealer participates in the world's single “simulate trade-date” command and performs its scheduled work and interactions without human prompts, approvals, interventions, or overrides. Its senior institutional decision-makers use the strongest frontier models, researched precedent, their mandate, and their own incentives. They may make poor decisions; the simulation records the consequences rather than having an observer correct those decisions. This month-1 actor behavior does not depend on the month-2 ops-harness. Any approval gates on future harness actions belong to that harness, not to the dealer's own decisions.

## Responsibilities and boundaries

The counterparty should own its transaction records and versions, relationship terms, applied pricing inputs, valuation and financing results, collateral/call records, and the evidence it has sent or received. This is a responsibility list for the interview, not a prescribed database schema.

The counterparty corrects its own records through its own mechanisms. The harness can communicate discrepancies or correction requests, but its autonomous business-record write access is limited to fund records. Setup may record assumptions that agreements and eligibility are in force; supporting simulated executed documents are not a readiness gate.

Shared public instrument identities or market observations may be reused. Undelivered private fund balances or valuation results, other dealers' private books, and hidden evaluator answers must not become dealer inputs. The dealer may receive a fund's stated valuation through a permitted dispute message and assess that claim; it still calculates its own value independently. Independent calculation means deriving results from its own records and documented methods, not requiring a different programming language or pricing library.

Keep these boundaries explicit:

- The **fund** chooses and records its relationship and manages its own portfolio. The dealer applies its own terms and constraints.
- The **administrator vertical** supplies the agreed matching, affirmation, and reconciliation-platform evidence. It must not silently replace the dealer's contract records or conclusions.
- The **FCM vertical** owns the clearing-account behavior selected for cleared products. Whether this OTC vertical also represents an executing dealer on a subsequently cleared CDS trade is an open cross-vertical decision.
- **Market data** provides identified observations. The dealer owns the calculation that applies them to its contracts.
- **Shared-world coordination** controls replay and evidence delivery. It must not overwrite participants' books to make them agree.

## Evidence to exchange

| Received evidence | Resulting dealer evidence to define |
|---|---|
| Execution understanding and fund booking/confirmation response | Dealer execution record, recap or term-sheet evidence, confirmation status, and a traceable discrepancy where terms differ |
| Relationship documents and selected trade terms | Explicit applied terms and effective versions; a clear distinction between defaults and transaction-specific elections |
| Market observations and correction notices | Reproducible valuations, financing/collateral calculations, and amended reporting where applicable |
| Payment/collateral instructions, responses, or settlement evidence | Calls and obligations distinguished from instructions, acknowledgments, and completed movements |
| Operational queries and agreed corrections | Responses and revised evidence retaining the earlier version and the reason for change |

Recipient layouts and transport remain open. A structured record can support a human-readable document, but the interview must decide what the future harness actually receives. Simulated communications do not imply sending messages to real firms.

## Unattended day and interactions

The detailed schedule remains for the interview. The required behavior is an unattended chain: receive the day's permitted evidence, process new executions and documentation, update the dealer's own records, perform scheduled valuation/financing work, issue reports or calls, and respond to counterparties' questions and disputes. Institutional agents handle decisions within that workflow and communicate their outcomes through the same simulated channels available to the other actors.

An unresolved discrepancy can remain disputed or pending under the dealer's autonomous decision; it must not stop the world waiting for Patrick to supply an answer. Record what the dealer knew, what it decided, and what it communicated. Scheduled routine work should continue as appropriate to the resulting state. The choice of model, instructions, evidence, and decision trace must be inspectable without granting another participant private access.

## Proposed first scenario and acceptance examples

Start with one fund, one dealer, an existing modest portfolio, and one new bilateral equity swap. Record the execution independently, exchange the chosen evidence, and calculate the dealer's ordinary valuation and financing output across the selected historical replay days. Add one variance-swap and one volatility-swap example using explicitly selected contract and observation conventions. They may share infrastructure without being treated as the same economic calculation. Include a bilateral OTC-option case with the exact contract variant selected through research.

For Patrick's put-versus-call example, distinguish the option term sheet from the dealer's valuation report. The case should allow evidence that the intended/documented option type and the dealer's booked or valued option type differ. The dealer and fund must investigate through their available records and autonomous exchanges. A mark alone does not establish that a put was booked as a call; preserve the term-sheet evidence, the relevant valuation assumptions or subsequent explanation, and any remaining uncertainty. The agents' conclusions and responses can themselves be wrong and remain observable.

These are proposed checks to refine in the interview:

- A reviewer can trace an execution through the dealer's booking, applied terms, calculation inputs, and outgoing report without consulting the fund's private book.
- A trade-term or observation correction produces an explained new version; earlier evidence remains available for replay and investigation.
- Initial replay retains delivered evidence and decision/event logs for playback. Full processing reconstruction is deferred; fresh frontier-agent decisions may differ.
- Opening funding supports ordinary processing while calls and contractual cash flows arise from actual calculations and terms. Later stress can exhaust that headroom.
- A reported obligation, a sent instruction, and evidence of completed payment can be inspected separately.
- A single date simulation completes scheduled dealer work and counterpart interactions without human approvals or dependency on ops-harness. A disputed item has an autonomous recorded status and response rather than a prompt to the observer.
- The option mismatch case preserves contract evidence separately from valuation evidence and does not assert put/call confusion solely from a price discrepancy.

The precise first break, contractual option variant, autonomous response policy, and replay period remain open. Responsibility for processing issues within the actor is settled: the dealer's configured workflow and agents handle them without a human decision or the harness. No lifecycle event should be added merely because an old research packet demonstrates it.

## Interview priorities and research

1. Select the smallest representative equity, variance, volatility swap, and bilateral option profiles. Which relationships, currencies, underlyings, valuation approaches, and contractual elections must differ?
2. Walk one trade through its communications. Which side originates each artifact, what constitutes agreement, and what remains pending at end of day?
3. Define the financing/collateral boundary. Which calculations and reports are required first, what creates a call, and how much opening cash and collateral supports the chosen portfolios while routine calls and contractual cash flows remain active?
4. Define the dealer agents' autonomous dispute and correction behavior. What precedent, incentives, and permitted evidence inform senior decisions, what does the dealer communicate, and how does routine processing continue while an issue remains unresolved? Use the put/call example to test evidence-based reasoning.
5. Agree the cleared-CDS execution boundary jointly with FCMs and administrators. Do not assume a bilateral trade becomes cleared just because an allocation was sent.
6. Identify unavailable historical inputs and minimum defensible modeling assumptions. Specify what needs current primary-source verification before implementation.

Full documentation negotiation, every corporate action, every exotic payoff, and comprehensive termination/default handling are not established month-1 requirements. The interview must choose any such behavior explicitly.

## Relevant detailed sources

- [Equity-swap master packet](../../../pr1/business/ops-harness/research/equities/equity-swap-master-research-packet.zip): read `equity_swap_master/README.md` and `equity_swap_master/equity_swap_master_research.md`; consult `example_master_profiles.json`, `example_resolved_trade.json`, and `example_cashflows.csv` within that same directory. These provide candidate relationship-term distinctions and synthetic calculations, not a completed dealer engine.
- [Variance/volatility packet](../../../pr1/business/ops-harness/research/volatility/variance-volatility-research-packet.zip): `packet/variance_volatility_research_report.md`, `packet/variance_volatility_contract_notes.md`, and `packet/variance_volatility_operations_notes.md`. Use the packet's consolidated `variance_volatility_source_register.csv`; some narrative references name intermediate files absent from the archive.
- [CDS packet](../../../pr1/business/ops-harness/research/credit/cds-research-packet.zip): `packet/cds_research_report.md` for the proposed distinction between execution, matching, clearing status, and obligations. Read jointly with the [FCM brief](fcms.md), rather than adopting a second competing CDS workflow here.
- [Listed-options packet](../../../pr1/business/ops-harness/research/options/listed-options-research-packet.zip): `listed_options/listed_options_research.md` supplies background comparison only. It does not establish the contract terms, documentation, valuation conventions, or lifecycle for the newly required bilateral OTC options; those need targeted research.
- [Earlier simulator architecture](../../../pr1/business/ops-harness/notes/architecture/2026-10-19_simulator-architecture-page-snapshot.md): background on independent state and evidence boundaries. Current interview decisions govern scope.

Archive links open the ZIP; the paths above identify members, not separately extracted files. The [source review](source-review.md) records evidence limits. Historical standards mappings, synthetic fixture passes, and old source URLs require appropriate rechecking before adoption.

## Start the cross-model interview

> Read this brief, project-direction.md, ops-harness/shared-terms.md, and the relevant source sections. Interview me about one autonomous dealer day, then the minimum equity/variance/volatility swap and bilateral OTC-option differences. Preserve independent state, functional financing, opening funding around the selected portfolios with routine flows active, and operation from one simulate-trade-date command without human approvals, interventions, overrides, or a harness dependency. Senior institutional agents use strongest-frontier models, precedent and incentives; their mistakes are observed, not corrected by a human. Use the put/call example to distinguish term-sheet evidence from valuation evidence. Ask one question at a time and resolve the FCM/administrator boundaries. Separate decisions, examples and research. Draft the specification and plan after the necessary choices; do not implement from this brief.
