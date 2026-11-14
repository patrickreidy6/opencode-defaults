# FCMs: starting point

Interview brief, 13 November 2026. This is an input to a separate cross-model planning session, not an approved implementation specification or verified description of a particular firm's rules.

Read [project direction](project-direction.md), the [world and interview map](vertical-map.md), and [shared terms](ops-harness/shared-terms.md). The [overview](README.md) gives the sequence: FCMs follow OTC counterparties and precede administrators. The proposed allocation is **10% of month-1 effort**.

The [decision-audit interview](interview-handoff.md#decision-audit-interview) records the confirmed foundation, product, authority and evaluation choices that govern this brief's remaining questions.

## Purpose and confirmed scope

FCMs are a distinct month-1 actor vertical. They supply the independent account, position, financing/margin, and operational evidence needed for **listed futures, cleared single-name CDS, and cleared index CDS**. Patrick introduced this vertical because a PB-only world would not represent the required cleared-product relationships.

This is the intended product scope. It does not establish that every candidate contract is eligible for clearing, that every FCM supports it, or that one set of rules applies across these products. Contract selection, clearing venue, account setup, and the applicable rule versions must be verified during planning.

Each fund is one strategy instance and can have multiple FCM relationships. Each trade is assigned in full to one eligible relationship; splitting a trade across FCMs is outside the initial requirement. The **fund vertical** owns the initial rule-based financing/allocation choice needed to generate its files. The FCM independently applies its own supported-product, account, risk, and financing constraints.

Reports and calls must arise from independent calculations. Choose the strategy portfolios first, then size opening cash and collateral around them for several ordinary days. Routine margin calls and contractual cash flows remain active; headroom is not a suspension of those flows.

**Autonomous operation is confirmed:** after configuration, a single world-level “simulate trade-date” command triggers the FCM's scheduled work and institutional interactions. No human approval, intervention, or override is required for actor decisions, and the FCM does not wait for the future ops-harness. Senior FCM decision-makers use the strongest frontier models, researched precedent, their mandate, and institutional incentives. Their decisions may be poor; the observer inspects their consequences without correcting or overriding them. Future ops-harness approval rules apply only to that harness's actions.

## Responsibilities and private state

Candidate FCM-owned records include received instructions, processing outcomes, account relationships and constraints, accepted position records, applied market inputs, margin/financing calculations, cash and collateral records, calls, and issued reports. The interview should reduce this list to what the first workflows require.

The FCM must not obtain the fund's private book, another FCM's private capacities, or expected evaluation answers. It can consume explicitly delivered fund instructions, shared public contract definitions, and identified market observations. Accepted shared libraries do not substitute for independent state and recomputation.

The FCM maintains and corrects its own records. The harness may communicate discrepancies or requests, but its autonomous record-change access is limited to funds. Shared OMS and instrument-master foundations must support later independently maintained actor variants, with selective adoption of shared improvements.

Keep **execution, allocation, matching, clearing acceptance, positions, and settlement evidence** distinguishable. The exact transitions are not prescribed here. A submitted allocation alone must not be treated as proof of every later step succeeding.

No separate exchange or central-counterparty vertical has been approved for month 1. Planning must decide how their necessary evidence is represented, who produces it, and what the FCM knows. Do not silently create extra actors or let an FCM fabricate purportedly independent venue evidence without labeling the simulation arrangement.

## Interfaces to resolve together

| Partner | Evidence and boundary |
|---|---|
| Fund | Whole-trade allocation and account instructions; FCM processing outcomes, positions, cash/margin reporting, calls, and responses |
| Executing broker or OTC executing dealer | Independently recorded execution evidence and the references needed to associate it with the fund instruction; the exact cleared-CDS execution owner remains open |
| Administrator/platform functions | Matching/affirmation and reconciliation evidence; coordinate which function reports each status and avoid incompatible state descriptions |
| Market-data provider | Contract-specific observations, dates, corrections, and provenance; FCM retains the inputs actually used in calculations |
| Shared-world coordination | Timed deliveries, replay inputs, and selected clearing/venue evidence; operational facts remain separated from hidden scenario answers |

Recipient formats, batch times, and an on-demand reporting interface are planning choices. Patrick described both daily reports and access to current information; this does not yet require building a replica broker web portal. Agree the useful evidence first.

## Unattended day and interactions

Define a schedule that receives the day's allocation and permitted execution/clearing evidence, processes outcomes, updates positions, performs independent margin/cash calculations, and issues reports and calls. Incoming queries, rejected allocations, missing evidence, and disputed calls must reach the FCM's configured workflow and agents automatically. They determine the response and send it to the relevant fund or platform role.

The senior agents need researched precedents, visible relationship terms, and institutional incentives to make these decisions. Record the evidence available, decision, and communicated response. A rejection or unresolved dispute is a legitimate observable outcome; it must not be converted into a human approval prompt. The schedule continues according to the FCM's resulting state, and no human override is used to make the scenario reconcile. Specific cutoffs and autonomous escalation roles remain interview decisions.

## Proposed first scenario and acceptance examples

Use one fund with two eligible FCM relationships so its allocation rule has a meaningful choice. Begin with an opening futures position and one new futures execution. The fund sends a whole-trade allocation; the receiving FCM processes it, records the outcome, independently calculates its results, and produces the agreed daily evidence. The other FCM must not acquire that trade merely because it belongs to the same fund.

Then add one selected cleared single-name CDS and one selected cleared index CDS through a jointly agreed execution/matching/clearing path. Lead operational research with ICE/IceLink, checking exact contract, series and clearing-route terms. The archived maturity-date conflict must be resolved before activating the affected profile. Product eligibility and market-data availability should be checked before choosing the instruments. The aim is one credible workflow for each required product, not complete clearing-house functionality.

Proposed acceptance examples:

- A reviewer can associate independently recorded execution evidence, fund allocation, FCM processing outcome, position, and report without merging the actors' private records.
- An unsupported account/product combination or chosen rejection case does not become an accepted position merely because the fund sent it.
- Daily results trace to the FCM's own positions, applicable terms, and dated inputs. The model's stated limits are visible.
- Opening funding supports ordinary days while calculated calls and contractual cash flows continue. A later stress scenario can consume that headroom and produces a traceable response or unresolved status.
- A call, an instruction to move cash/collateral, and completed-movement evidence remain distinguishable.
- Initial replay is playback of delivered evidence with decision/event logs; full processing reconstruction is deferred. A fresh agent decision trial can differ from the recorded run.
- One date simulation completes scheduled FCM work and counterpart interactions without human approval or a dependency on ops-harness. Rejections and unresolved disputes retain autonomous outcomes without blocking for an observer's decision.

These are proposed tests. The precise break, autonomous response policies, replay duration, report set, and computation tolerances await interview decisions. Processing and resolving issues inside the FCM is the responsibility of its configured workflows and agents, without human intervention.

## Interview priorities and research

1. Select the first futures contract and CDS examples, the fictional FCM relationships, and the historical period. Verify product eligibility and usable reference/market data.
2. Walk execution through clearing and reporting. Who records the execution, who supplies venue/clearing evidence, and which statuses can arrive late or disagree?
3. Define each FCM's mandate and financing/risk constraints. Which terms must differ to make fund allocation meaningful, and what information is disclosed to the fund?
4. Choose the smallest defensible margin/cash methodology for each product, with explicit limitations. Which parts require independent calculations, and which external schedules or observations are received inputs?
5. Agree the unattended reporting schedule and first exception with funds and administrators. Which FCM agent decides the response, using which precedent and incentives, and how does processing continue when the issue remains unresolved? Keep the strongest-frontier institutional leadership and no-human-override requirement.
6. Size opening funding around the chosen portfolios and define a later stress scenario, while ordinary calls and contractual cash flows remain active.

Do not implement comprehensive clearing-house risk engines, default waterfalls, every futures delivery process, or all CDS lifecycle events by implication. Include only the behavior required by agreed month-1 examples, and record excluded behavior clearly in the resulting specification.

## Relevant detailed sources and gaps

- [CDS research packet](../../../pr1/business/ops-harness/research/credit/cds-research-packet.zip): begin with `packet/cds_research_report.md`; consult `packet/cds_ice_link_crosswalk.csv`, `packet/cds_product_profiles.csv`, and `packet/cds_source_register.csv`. The report separates contract economics, matching/clearing status, positions, and cash obligations. Its candidate fields and historical interface material are not certified current interfaces.
- Within that packet, `packet/cds_standards_notes.md` describes limits of earlier model/schema investigations. `packet/synthetic_cds_examples.json` and `packet/synthetic_cds_correction_branches.csv` are example inputs, not a ready FCM ledger or validated margin engine. Hidden expected-result files must remain outside participant access.
- [Earlier simulator architecture](../../../pr1/business/ops-harness/notes/architecture/2026-10-19_simulator-architecture-page-snapshot.md) and [shared-world brief](shared-world.md): use for evidence boundaries and cross-actor replay; the latest roster supersedes the older actor list.
- [Fund brief](funds.md), [OTC-counterparty brief](otc-counterparties.md), and [administrator brief](administrators.md): settle the allocation, executing-dealer, and platform responsibilities jointly.

The [catalog](source-catalog.md) contains no dedicated FCM or listed-futures research packet. A targeted primary-source research task is necessary before finalizing those workflows: applicable exchange/clearing product specifications, clearing eligibility, margin/reporting examples, and historical-data access. The [source review](source-review.md) explains why synthetic fixture passes do not establish runtime or production accuracy. Archive links open the ZIP; member paths identify the specific material inside it.

## Start the cross-model interview

> Read this brief, project-direction.md, ops-harness/shared-terms.md, and the relevant CDS packet sections. Interview me about one autonomous FCM day and a whole futures trade routed to one of two eligible FCM relationships, then the cleared-CDS differences. Preserve rule-based fund allocation, independent calculations, and opening funding sized around the chosen portfolio with routine flows active. One simulate-trade-date command must trigger scheduled work and interactions without human approvals, interventions, overrides, or ops-harness dependency. Strongest-frontier senior agents decide from precedent, mandate and incentives; their mistakes remain observable. Resolve execution, clearing, and platform evidence without inventing additional approved verticals. Ask one question at a time. Mark research gaps and proposals, then prepare a specification and plan after the necessary decisions; do not implement from this brief.
