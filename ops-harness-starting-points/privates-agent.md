# Privates-agent vertical starting point

Status: interview starting brief, 13 November 2026, following the decision-audit interview and Patrick's subsequent role correction. These are confirmed direction and proposed design questions, not an approved implementation specification. No month-1 effort percentage has been assigned to this new vertical.

[Overview](README.md) · [Project direction](project-direction.md) · [Vertical map](vertical-map.md) · [Shared terms](ops-harness/shared-terms.md) · [Shared world](shared-world.md)

The [decision-audit interview](interview-handoff.md#decision-audit-interview) is the central record of the confirmed choices. The later correction establishes this ninth vertical: private loans and private warrants point here; [loan agents](loan-agents.md) handle syndicated loans only.

## Purpose and confirmed scope

Supply independent private-loan servicing and private-warrant agency records, notices and responses. The fund retains its own holdings and expectations; the privates agent supplies its own view of recognized interests, obligations, exercises and deliveries. Grouping the functions in one vertical does not make every loan-servicing and warrant-agency role the same institution.

- **Private loans:** simple servicing of an existing funded position, including cash interest and explicit payment-in-kind (PIK) capitalization. Private loans remain last in the month-1 instrument sequence. Broad origination, complex covenants and waterfalls are outside this narrow initial profile.
- **Private warrants:** bounded cash and cashless exercise workflows, with a register, exercise notices and evidence of pending or partial share delivery. Exact contract variants remain for the product interview.
- **Effort:** the historical less-than-5%-of-PB-effort limit concerned the original small private-agent role, not this entire new vertical. Selected cash and cashless warrant functionality takes priority if that limit conflicts with the required work; revise the estimate rather than silently dropping the functionality.

Choose terms and data requirements before implementing each profile, using CDM as the selected foundation where applicable. Research coverage gaps and obtain approval for proposed supplements. Setup readiness may rely on explicit recorded assumptions that agreements and eligibility are in force; supporting simulated executed documents are not a readiness gate.

## Independent state and authority

**Proposed owned records:** effective terms versions, recognized lender or warrant-holder interests, servicing and exercise notices, pending obligations, received movement evidence and correction history. Detailed lifecycle milestones belong to the product and actor interviews; preserve history and distinguish an obligation or notice from an evidenced outcome.

An interest-due event does not itself establish a cash payment. Explicit capitalization changes principal under the selected PIK terms. Warrant exercise, a claim for shares and delivery evidence must remain distinguishable for the chosen profile. Verify the exact contractual calculations rather than importing an entire archived dictionary.

The privates agent corrects its own records through its own mechanisms. The harness may communicate discrepancies or correction requests, but autonomous harness record changes are limited to fund records. Neither the agent nor its borrower/issuer representation may inspect another actor's private books or hidden evaluation answers.

OMS and instrument-master capabilities start as shared foundations, built to permit independently maintained actor variants. Each actor selectively adopts shared improvements after compatibility checks. Existing trades retain their agreed effective terms version; an amendment is distinct from a reference-data correction.

## Autonomous operation and evidence

After setup, this vertical runs with the other eight from one simulate-trade-date command or schedule, without the harness, human approvals, manual role-playing or decision overrides. Strongest-frontier institutional leaders use their own incentives, permitted evidence and private state. Humans configure and evaluate the world; they do not supply routine agent, borrower or issuer responses during a run.

Patrick expects borrower-facing loan reports and the ability for the borrower to ask questions. The minimal autonomous borrower and issuer representations remain design questions; this brief does not add further verticals.

| Evidence received | Evidence to define and produce |
| --- | --- |
| Selected loan terms and opening funded interests | Servicing statement, interest notice and explicit PIK capitalization record where applicable |
| Warrant terms, holder interests and exercise notices | Register changes, exercise responses and cash/share obligations under the selected contract |
| Cash or securities movement evidence | Payment or delivery status, including remaining obligations |
| Borrower, holder or fund query | Attributed response using the agent's available evidence |
| Corrected terms or prior notices | Linked corrections retaining earlier evidence and outcomes |

A blocked workflow and its dependants remain visibly incomplete or uncertain while independent work continues. Initial replay is evidence playback with decision/event logs; full processing reconstruction is deferred. A fresh probabilistic run may differ.

## Proposed first cases and checks

Use one existing funded private loan with simple cash-interest and explicit PIK terms, and a narrowly selected warrant profile or profiles covering both cash and cashless exercise. Exact instruments, dates, communications and exception cases remain open. Do not treat the same event or redelivered notice as a second payment, capitalization or exercise.

Check that the fund and agent views are separately inspectable, calculations trace to selected terms, and payment/delivery status traces to appropriate evidence. Preserve prior notices and correction lineage. The first integrated acceptance includes representative missing-input, duplicate-delivery and uncertain-outcome checks alongside the normal cases. Select relevant archived numerical examples, independently verify their expected results, then reuse them as regression tests.

## Questions for the vertical interview

1. Which existing private-loan terms provide the smallest credible cash-interest and PIK servicing case?
2. Which warrant contracts and units cover cash and cashless exercise, and what establishes pending, partial and completed delivery?
3. Which distinct servicing or agency identities and accounts are needed within this vertical?
4. What do the borrower and issuer receive and send, and what minimal autonomous representation supports those interactions?
5. Which reports and movement evidence reach the fund, administrator and harness, at what times?
6. What effort estimate supports the selected functionality, and which first exceptions best test the boundaries?

## Sources and limits

Use the [decision audit](decision-audit.md) findings A08, C12 and C15 and their exact source links, together with the [source catalog](source-catalog.md) and [source review](source-review.md). Private-loan and private-warrant research are separate from the syndicated-loan packet. Archived examples and stored test results remain research evidence until independently verified; they do not establish current contractual rules, executable CDM coverage or a complete agency platform.

## Fresh interview prompt

> Start the privates-agent interview from this brief, the decision-audit interview record and the shared-world direction. This ninth vertical owns private-loan servicing and private-warrant agency; syndicated loans remain with loan agents. Preserve existing-loan cash interest and simple PIK, cash and cashless warrant exercise, independently maintained records and autonomous borrower/issuer interactions. Private loans remain last in the instrument sequence. Define exact profiles, evidence and effort without inventing another vertical or expanding into a full transfer-agent platform. One simulate-trade-date command must operate without the harness, manual intervention, approvals or decision overrides. Ask one question at a time. Separate confirmed choices, proposed scenarios and research gaps; do not implement from this brief.
