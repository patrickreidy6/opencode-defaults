# Loan-agent vertical starting point

Status: interview starting brief, 13 November 2026, updated after the decision-audit interview. Confirmed decisions below come from Patrick's interview. Proposed behavior remains subject to the vertical's planning session. The earlier **3%** allocation predates the separate privates-agent vertical; a revised allocation has not been agreed.

[Overview](README.md) · [Project direction](project-direction.md) · [Vertical map](vertical-map.md) · [Shared terms](ops-harness/shared-terms.md) · [Shared world](shared-world.md)

The [decision-audit interview](interview-handoff.md#decision-audit-interview) records the confirmed foundation, product, authority and evaluation choices that govern this brief's remaining questions.

## Purpose and confirmed direction

The loan-agent vertical supplies servicing records and communications for syndicated-loan positions only. The future harness will compare fund records, traded interests, expected cash, notices, and servicing events. Private loans and private warrants belong to the separate [privates-agent](privates-agent.md) vertical.

**Confirmed:** start with secondary trading of fully funded syndicated-loan positions and assignments. Unfunded commitments belong to a later profile. Participation, elevation, broad origination and comprehensive lifecycle behavior are not established initial requirements. Exact settlement and delayed-compensation conventions still require the product interview and source verification.

**Confirmed:** Patrick expects direct borrower communications: the agent reports details to the borrower, and the borrower can ask questions. The implementation of that borrower role remains unresolved. Decide its representation during planning without automatically adding a vertical. Whatever arrangement is chosen must operate autonomously; Patrick does not roleplay the borrower.

Initial loan holdings belong in the fund/strategy interview. Historical replay is the market baseline; portfolios, trades, and scenario communications are fictional. Select real versus fictional underlying loan identities and reference terms during research; that choice is not yet settled.

**Confirmed operating model:** after configuration, one simulate-trade-date command coordinates all nine actor verticals. Loan agents perform scheduled work and institutional responses without the harness, manual intervention, approval gates, or runtime user overrides. The strongest available frontier models provide judgment under each agent institution's own goals, incentives, mandate, and private state. Probabilistic behavior is permitted. Humans handle setup and evaluation, not servicing actions during the run.

## Owned state and boundaries

**Proposed:** maintain the servicing view, relevant terms, recognized lender interests, notices, and selected servicing events. Choose only the terms needed to explain the first position, interest amount, or payment notice.

The [fund](funds.md) owns its internal book and trade instructions. An independently recorded secondary trade is not automatically the same thing as the agent's recognized servicing position. The [administrator vertical](administrators.md) supplies the platform-style matching/reconciliation evidence grouped there by Patrick. Agent servicing evidence and platform workflow evidence must retain distinct origins even where both concern one transaction.

Reported expected cash, an agent's statement about payment, and evidence of a completed simulated cash movement must be distinguishable. The [shared world](shared-world.md) interview must settle how cash evidence is generated without silently adding the excluded custodian vertical.

Neither agent nor borrower may read another participant's private records or hidden answers. Shared identifiers connect evidence without sharing private financial books.

The loan agent maintains and corrects its own records; the harness may send queries or correction requests but cannot directly edit them. Shared OMS and instrument-master capabilities begin as common foundations and must allow independently maintained actor variants with selective updates. Setup readiness can use explicit recorded assumptions about agreements and eligibility.

## Evidence received and produced

These are **proposed evidence families**, not a selected vendor protocol or contractual rule set.

| Received evidence | Output to consider |
| --- | --- |
| Agreed loan terms and opening lender interests | Opening servicing statement and relevant terms |
| Secondary-trade or transfer-related instructions/status | Agent response and updated servicing position when the chosen conditions are met |
| Rate or other servicing inputs | Interest calculation/notice under explicitly selected terms |
| Scheduled servicing event | Expected payment or principal information for the appropriate recipients |
| Borrower question or response | Agent correspondence linked to the relevant loan or notice |
| Corrected information or payment evidence | Revised notice, updated status, and retained earlier evidence |

Lender reports and borrower messages are separate views. Determine their content, timing, and direction without automatically adding a credit model or autonomous borrower balance sheet.

## Autonomous operating loop

At its configured servicing times, the agent processes received trade/transfer evidence, updates the selected servicing records, calculates due items, and issues recipient-specific statements or notices. Its institutional agent handles lender and borrower queries, requests missing evidence from other actors, and decides the appropriate follow-up using its own permitted information. Subsequent corrections and payment evidence update its records and responses autonomously.

The borrower representation produces any selected questions or replies through the agreed autonomous mechanism. Unresolved servicing matters can remain explicitly pending with a next action; they cannot require Patrick to supply a message, approve an action, or override a runtime decision. The shared coordinator provides time and delivery, not the agent's financial conclusions.

## Proposed first scenarios and acceptance examples

**Funded assignment first:** use one secondary purchase or sale and follow the evidence from the fund's booked trade through the selected platform and agent steps to a servicing position and relevant cash evidence. Select the exact assignment and settlement terms during the product interview; do not silently adopt the packet's wider participation, elevation, delayed-compensation or distressed procedures.

Acceptance examples to refine:

- A fund trade and agent-recognized position are separately inspectable and connected by delivered evidence.
- A notice's amount can be recomputed from the selected terms and servicing inputs.
- The same servicing event does not create duplicate principal or cash postings when a notice is repeated.
- A corrected notice preserves the earlier version and explains the changed current result.
- Borrower and lender recipients receive the selected views without access to one another's private records.
- Replay retains the servicing chronology and agent decisions without exposing future notices early; fresh probabilistic runs preserve evidence explaining any different actions.
- The servicing and borrower-response sequence runs from the common simulate-trade-date command with the harness absent and no manual actions, approvals, or runtime overrides.

First exceptions and the responsible institutional responses remain open; their execution must be autonomous. These checks do not establish vendor compatibility or universal conventions.

## Questions for the vertical interview

1. What exact secondary syndicated-loan case should be first, and which messages would Patrick use to judge it complete?
2. Which transfer and servicing steps belong to the agent, and which platform-style outputs belong to the administrator build?
3. Which funded-assignment settlement conventions and supporting evidence are needed first, including any applicable delayed compensation?
4. What does the borrower receive and ask about? Which autonomous representation is sufficient: independent state or a bounded response mechanism within the chosen arrangement?
5. What independently generated evidence establishes payment in the simulated world?
6. Which mismatch or late/corrected notice is useful first, and which autonomous agent actions and inter-actor responses address it?

## Targeted source map

The [syndicated-loan research packet](../../../pr1/business/ops-harness/research/loans/loans-research-packet.zip) is the principal retained source. Read selectively:

- `clearpar_loans/README.md` and `clearpar_loans/clearpar_loan_research_report.md`: intended product scope and limits.
- `clearpar_loans/loan_model_design.md`: proposed distinctions among terms, trades, servicing positions, notices, obligations, and observed cash.
- `clearpar_loans/loan_settlement_conventions.md` and `clearpar_loans/loan_lifecycle_notes.md`: candidate cases and research questions; select only those needed.
- `clearpar_loans/clearpar_platform_notes.md`: coordinate with the administrator interview rather than duplicating platform ownership.
- `clearpar_loans/loan_example_trades.csv`, `clearpar_loans/loan_example_settlements.csv`, and `clearpar_loans/loan_example_events.csv`: separate synthetic examples, not an integrated live portfolio.

The packet explicitly excludes private/direct loans and does not validate a universal settlement clock or current contractual rules. [Source review](source-review.md) records those limitations. The decision audit records a crosswalk defect: quantity basis, price-basis enumeration and numeric price must be separated and the mapping checked before reuse. Existing numeric examples must be independently verified before becoming regression tests. Private-loan research and servicing are owned by [privates-agent](privates-agent.md).

## Fresh interview prompt

> Start the loan-agent vertical's cross-model planning interview. Read this brief, project-direction.md, shared-world.md, and ops-harness/shared-terms.md. This vertical owns syndicated loans only; private loans and warrants have a separate privates-agent vertical. Start with fully funded secondary assignments, leaving unfunded commitments for later. Keep agent and platform evidence distinct. Design scheduled servicing and autonomous institutional responses using frontier-model judgment, goals/incentives, and private state. The borrower arrangement must also run autonomously. One simulate-trade-date command must operate without the harness, manual intervention, approvals, or user runtime overrides. Ask one design question at a time and define no-prompt acceptance checks. Do not implement during the interview.
