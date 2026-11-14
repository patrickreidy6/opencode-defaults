# Executing brokers: starting brief

Updated 13 November 2026. Interview input for execution-side evidence, not an approved specification or implementation plan.

Read the [overview](README.md), [project direction](project-direction.md), [vertical map](vertical-map.md), [shared terms](ops-harness/shared-terms.md) and [shared world brief](shared-world.md). Interview this vertical after funds, financing, clearing and evidence providers. Executing brokers receive **4% of the proposed month-1 effort allocation**.

The [decision-audit interview](interview-handoff.md#decision-audit-interview) records the confirmed foundation, product, authority and evaluation choices that govern this brief's remaining questions.

## Purpose and confirmed direction

Executing brokers independently record and communicate supported executions. Their evidence lets the fund and operator distinguish intended activity from reported fills, identify corrections and investigate execution-side discrepancies.

**Confirmed:** executing brokers are one of the nine required month-1 role types. The world uses historical replay with fictional holdings and trades. Funds may have multiple institutional relationships, while the exact broker count and relationship map remain open. The fund owns the rule-based assignment of a whole trade to one PB or FCM when applicable.

The agreed breadth now includes bilateral OTC options. This does not establish that an executing broker handles every instrument: identify which products use this actor and which are agreed directly with a dealer. Executing-broker, PB, FCM and OTC-counterparty roles remain distinguishable even within one fictional institution.

## Autonomous daily operation

**Confirmed:** once configured, all nine actors run without human intervention, approvals or overrides of their decisions. One simulate-trade-date command schedules their work; neither ops-harness nor Patrick acting as a broker employee is required.

The strongest frontier agents make top-level broker decisions using its incentives, private state and limited available information. Decisions need not be wise or align with the fund's interests. Human setup establishes the scenario and permitted behavior; a human does not overrule runtime decisions to make the day succeed.

**Proposed daily flow:** review outstanding instructions and delivery issues; decide and execute supported responses; produce execution evidence; send corrections and answer counterparties' questions; pursue scheduled follow-ups; carry unresolved work forward. When delivery inventory is unavailable, a broker response or established explanation does not mean the security was delivered. A business fail can remain open. A failed tool/model call or job is an explicit technical failure, distinct from that business outcome.

## Proposed ownership and boundaries

The executing broker owns received instructions, supported execution facts, references, corrections, delivery history and responses. Copying a fund booking does not create independent execution evidence.

The broker corrects its own records through its own mechanism. The harness may communicate a discrepancy or correction request, but its autonomous business-record write access is limited to funds. Shared foundations must support later actor-owned OMS and instrument-master variants rather than force all actors to keep identical implementations.

Agree where the first execution fact is created. One option is a fund instruction followed by a broker-generated result; another is a deliberately supplied execution event that reaches each actor through appropriate evidence. This brief selects neither. The shared scenario can initiate a case, but actors must not receive future outcomes or hidden evaluator answers as operating inputs.

A trading instruction, fill, allocation, booking, acknowledgement and settlement are separate meanings. The broker may communicate the selected allocation or delivery details, but it does not own the fund's PB/FCM selection rule. It must not silently change that selection to make downstream processing succeed.

Execution does not itself prove PB acceptance, clearing acceptance, payment or securities delivery. Those facts require the agreed evidence from the appropriate role. Matching, affirmation and reconciliation-platform functions sit within the administrator vertical for this first world; coordinate the broker's participation without introducing another unapproved institutional vertical.

Do not make exchange order books, price discovery, market impact, investment signals or high-frequency realism implicit prerequisites. The existing fund baseline does not require an exchange simulator. If the selected broker workflow needs additional market mechanics, surface that as an explicit scope choice.

## Evidence to receive and send

**Proposed inputs:** fund instructions or agreed scenario execution inputs, relevant instrument/reference observations, relationship configuration and delivery/account instructions needed by the supported workflow. Identify what the broker actually knows; do not give it the entire fund portfolio merely because the simulator can access it.

**Proposed outputs:** fill/execution reports, supported confirmation details, correction or cancellation notices, and workflow responses. Determine recipients separately: the fund, its administrator/platform functions, and the relevant PB or FCM may receive different evidence and at different times.

Define each interface's purpose, parties, timing, identifier/units and revision behavior before choosing CSV layouts. Distinguish fills, aggregations and allocations. Whole-trade PB/FCM allocation does not itself decide whether partial fills or aggregated reports are supported.

## Proposed first scenario

Select one supported liquid instrument and one fund instruction or agreed supplied execution. Produce a broker-side execution report, let the fund book the activity and apply its allocation rule, then deliver the evidence required by the relevant PB/FCM and administrator/platform functions. Every participant retains its own state.

Add an execution-side exception such as a price correction arriving after an earlier file. The broker sends a linked revision; recipients interpret it without duplicating the trade. Select disagreement, rejection or late-delivery details during setup and require the agents to handle responses autonomously. Continuation cannot depend on any human response.

Document how historical observations support plausible synthetic execution facts and where they do not. Synthetic executions are not actual historical trades.

## Proposed acceptance examples

- A reviewer can trace a fund's booked activity to the broker evidence available at that time, including the distinction between original and amended facts.
- Broker references and fund references are linked through realistic exchanged information. No hidden universal key supplies the matching answer.
- The fund's PB/FCM allocation remains whole-trade and inspectable; the broker does not independently choose a contradictory destination.
- Duplicate delivery does not produce an extra economic fill. A supported correction changes the right record and retains history.
- At least one routine and one exception case reach the downstream actors and provide useful evidence for the harness.
- One configured simulate-trade-date command runs execution evidence, frontier decisions and scheduled communications without human prompts, approvals, overrides or ops-harness. Poor decisions are retained rather than manually repaired.
- An explanation of a delivery fail leaves the case open until appropriate completion evidence arrives. A technical failure is reported separately.
- Initial replay is evidence playback with decision/event logs; full processing reconstruction is deferred. Expected answers and future evidence stay hidden. A fresh frontier-agent run may choose a different trajectory.

## Focused interview and research agenda

First identify the funds and products that need executing-broker evidence. Walk through one trade from intention to execution, allocation and downstream acknowledgement; decide where the execution fact originates. Then settle the minimum broker population and whether distinct profiles materially improve the scenarios.

Ask which fill details are needed, whether partial fills or aggregation matter, what correction sequence is credible, and who receives each message. Define the broker's incentives and frontier-agent choices, together with the lower-level procedures that execute them. Settle delivery/inventory evidence and scheduled follow-ups without human runtime decisions. Preserve the fund's rule-based financing allocation; broker judgment does not replace it.

Research representative execution and correction interfaces for the selected products. Historical examples can guide the questions but do not establish current regulatory timing, venue rules or vendor compatibility. There has been no fresh verification of those matters in this brief.

## Relevant sources

- [Cash-equity packet](../../../pr1/business/ops-harness/research/equities/cash-equity-research-packet.zip): start with `cash_equity_oms_to_pb_research.md`, `broker_fills_synthetic.csv`, `broker_correction_synthetic.csv`, `correction_workflow_synthetic.csv` and `fill_allocation_links.csv`. These are selected research leads, not an adopted contract or executed implementation.
- [Current fund strategy and evidence baseline](../../sim-funds/docs/strategy-funds.md) and [fund scenario/acceptance](../../sim-funds/docs/scenario-and-acceptance.md): explain the old fictional execution and amendment example. The expanded world still needs an explicit decision about execution ownership and delivery.
- [Retained trade-file collection](../../../pr1/business/ops-harness/research/trade-file-sources/index.html), [source catalog](source-catalog.md) and [source review](source-review.md): additional interface evidence and its limitations. Fund upload formats must not automatically be treated as broker execution-report formats.

## Fresh-session prompt

> Continue the executing-broker interview in plan mode using this brief and its common links. Read the fund, PB, FCM and administrator interfaces; establish execution origin and the broker's role for the agreed products including bilateral OTC options. Strongest frontier agents make top-level choices from private state, incentives and available evidence. One configured simulate-trade-date command must run actors without ops-harness, human intervention, approvals or decision overrides. Walk a normal trade and an autonomously handled exception through scheduled communications; distinguish unresolved delivery from technical failure. Preserve fund-owned rule-based whole-trade allocation. Ask one question at a time and verify assumptions before specification/planning. Do not implement from this brief.
