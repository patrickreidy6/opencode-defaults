# Interview handoff

Updated 13 November 2026 after the 38-question decision-audit interview and the subsequent privates-agent correction. These are confirmed planning directions, not a complete implementation specification; no simulator, harness, integrations or model experiments were implemented.

## Resume without reopening settled choices

Continue the [ops-harness interview](ops-harness/starting-point.md), [shared terms](ops-harness/shared-terms.md) and [project direction](project-direction.md), carrying forward the confirmed [decision-audit choices](#decision-audit-interview) below. The audit interview is complete at direction level; the detailed actor and product interviews remain. Keep the entire month 1–4 map visible using roadmap, actor and workflow graphs. Ask one question at a time.

After the harness framing, follow the [overview order](README.md#interview-order-and-month-1-effort): funds, PBs, OTC counterparties, FCMs, administrators, market-data providers, loan agents, executing brokers, then shared-world/infrastructure review, also covering the new [privates-agent](privates-agent.md) brief. Placing privates-agent beside loan agents is an editorial convenience, not a newly agreed implementation sequence. This is interview order, not a serial implementation schedule. Shared dependencies need agreement before dependent plans finalize.

## Decision-audit interview

The choices below record Patrick's answers to Q1–Q38 and his subsequent correction separating private instruments from syndicated loans. They govern current direction where the earlier [decision audit](decision-audit.md) or starting briefs differ. The audit's evidence and proposed actions remain historical review material; not every recommendation was adopted.

### Shared foundations, ownership and controls

| Questions | Confirmed direction |
| --- | --- |
| Q1–Q2: shared modules and variants | Initially build and mature reusable OMS and instrument-master modules for funds, shared simulation support and ops-harness across the intended instruments. Design for the later state in which each independent actor maintains its own version of both, with private records separate from the outset. Actors selectively adopt shared fixes and features after compatibility checks; permanent uniformity is not the goal. |
| Q3–Q4: FINOS CDM | Retain CDM as the selected foundation and authority where applicable for instrument fields, price representation and verified calculations. Identify actual coverage gaps, research a recommended supplement, and obtain Patrick's approval before adopting it. No release, binding, fallback library or complete valuation capability has been selected or established here. |
| Q5–Q6: definitions and terms | Apply the definition-before-build gate per product: establish applicable CDM requirements, calculation inputs, simulation additions and recipient needs before dependent implementation. Keep effective versions of master terms; trades retain the agreed version, with explicit amendments and separate reference-data corrections. |
| Q7–Q8: readiness | Instrument/documentation readiness checks belong in setup, not as an ongoing harness capability. Explicit recorded assumptions that agreements and eligibility are in place suffice; supporting simulated executed documents are not a setup gate. Assumptions are not verified documentary coverage. |
| Q9: operating scope | Retain all five harness domains: reconciliation, settlement, reference-data maintenance, financing and treasury, developed incrementally. Investment performance, full accounting and regulatory reporting are not added as initial harness objectives. |
| Q10–Q11: fund-record authority | The harness may autonomously correct fund OMS/instrument-master records within its authorized access, retaining an audit trail. It may change fund-side business records only. Other verticals must have mechanisms to correct their own records; the harness can communicate discrepancies or correction requests. This is not unrestricted access to actor-private state. |
| Q12: communications | Initial external-message approval covers the exact prepared content and recipients. Material changes to the message or its supporting evidence require renewed approval. This does not gate autonomous actor-to-actor communications. |
| Q13–Q14: history and failures | Preserve prior history and deliveries and require evidence-backed outcomes; define detailed lifecycle milestones during product/actor interviews. Incomplete or uncertain outcomes hold the affected work and its dependencies while independent work continues. Missing input is not a successful empty result. |
| Q29: conflicting evidence | Define authority by fact and workflow where possible; investigate conflicts using provenance and timing and allow an unresolved conclusion. Matching feeds or the fund's own record are not automatically correct. |
| Q37: first integrated checks | Require a bounded set of representative failure/control checks at first integrated acceptance: missing inputs, duplicate delivery, uncertain submissions, provider/quota failures, stale approvals and untrusted document instructions. Preserve visible uncertainty and protection against duplicate business effects. |

### Actor map, product depth and opening conditions

| Questions | Confirmed direction |
| --- | --- |
| Q15 and later correction: private instruments | Create a separate **privates-agent** vertical for private-loan servicing and private-warrant agency, including the relevant register, exercise notices and delivery evidence. **Loan agents handle syndicated loans only.** This replaces the earlier placement of private instruments in loan agents and expands the roster to nine verticals. |
| Q16 and Q38: limited agency effort | The historical less-than-5%-of-PB-effort target concerns the original small private-agent role, not the entire new privates-agent vertical. If the selected cash and cashless warrant functionality cannot fit, functionality takes priority and the effort allowance may be revised. No new nine-vertical percentage allocation was chosen. |
| Q17: recipient formats | Establish two differently shaped synthetic recipient profiles early and test that they preserve quantities, cash and obligations. They are simulator-owned formats, not certified vendor interfaces; verified vendor compatibility is separate work. |
| Q18: equity swaps | Retain the default hierarchy of provider → underlying currency → settlement currency and eight terms: maturity, performance reset, financing reset, reference rate, signed spread, equity calendar, rate calendar and date adjustment. Align with CDM and verify detailed cash conventions before activating each profile. |
| Q19: CDS | Lead operational research with ICE/IceLink, checking the exact contract, series and clearing route against applicable authoritative terms. CDM remains the model foundation. The old maturity-date conflict requires source verification, not a chosen date from this interview. |
| Q20–Q22: bonds and volatility | Corporate bonds include a bounded coupon-entitlement case alongside trade consideration and partial/failed settlement. Convertibles start with trading and valuation; conversion elections, calculations and delivery lifecycle remain later work. Variance and volatility swaps include bounded observation-driven expiry settlement and corrections, with explicit units and observation handling; verify valuation separately. |
| Q23–Q25: loans and warrants | Private loans include cash interest and simple explicit PIK capitalization, without complex covenants or waterfalls, and remain last in the instrument sequence. Syndicated loans start with fully funded positions and assignments; unfunded-commitment economics are later work. Private warrants include cash and cashless exercise with relevant pending/partial delivery. |
| Q26: archived examples | Select examples matching approved profiles, independently verify expected results, and reuse them as regression tests. Keep examples of deferred workflows for later. No archived calculation or engine was newly certified in this interview. |
| Q27: opening headroom | Choose realistic strategy portfolios first, then size opening cash and collateral around them. Keep routine margin calls and contractual cash flows active; do not reduce exposures simply to ease funding or suppress flows to create a quiet period. |
| Q28: allocation | Keep one fund per trade initially; cross-fund block allocation is a later candidate. A whole trade routes to one applicable PB or FCM, with no splitting across those relationships. Correct the FCM prompt accordingly. |

### Replay, evaluation and development workflow

| Questions | Confirmed direction |
| --- | --- |
| Q30: replay depth | Start with evidence playback and decision/event logs for inspection. The fuller input/version package needed to reconstruct processing is deferred. Do not describe initial playback as complete reproducibility or assume a fresh model run repeats past decisions. |
| Q31: 80% population | Require each supported **break family** to meet the 80% classify-and-prescribe target independently. This is not a case-resolution target or a separate quota for every instrument. Exact family definitions, test cases and delivery milestone still need design. |
| Q32–Q33: quality and holdouts | Initially report false-clean conclusions, unsupported certainty, abstention and escalation without separate acceptance gates. Use fresh held-out cases with familiar scenario patterns and document layouts. Broader generalization testing comes later; hidden evaluation answers remain separate from operating agents. |
| Q34–Q35: older workflow ideas | Exclude scheduled research–critic–human-review work from the current direction. Retain only the form reviewer as a later specialist-tool candidate; other exploratory specialist-tool ideas remain in the historical archive. This does not remove the existing PDF-finding/separate-investigation workflow. |
| Q36: development preference | Retain OpenCode-first development with portable shared interfaces and skills. Infrastructure remains owned by ops-infra. This does not select a mandatory financial application runtime, storage stack or multi-agent pipeline. |

Detailed contract variants, calculation conventions, data providers and operating interfaces still require research and the relevant interviews. In particular, do not directly import the defective syndicated-loan dictionary mapping before correction and verification. These decisions authorize retaining direction in the briefs, not editing original research, implementing the system or treating all audit recommendations as approved requirements.

## Most important correction: autonomous reality

**All nine actor verticals must run on schedules and agents with zero manual intervention after setup.** One command or schedule such as “simulate trade date November 14” starts the necessary activity across the configured world. The example establishes a date-triggered interface, not a chosen year, trading calendar or implemented command syntax.

Patrick does not approve actor messages, role-play responses, resolve their exceptions or override their decisions. Strongest-frontier leaders make institutional judgments from researched examples, incentives and their own available information. Randomness and poor decisions can be part of the observed outcome. Preserve private state and hidden-evaluation boundaries.

Ops-harness, ops-infra and shared integration/replay/valuation work remain hands-on areas where human-in-the-loop steps can exist. The nine actor verticals must run without the harness. Runtime valuation capabilities support them automatically even when their development is hands-on. Business issues may remain unresolved; technical failures must be reported explicitly, holding affected work and dependencies while independent work continues rather than waiting silently for a manual step.

Earlier suggestions that Patrick might manually work an actor's break are superseded. Do not ask that question again.

## Other confirmed world choices

- Commercial licensable product first, professional development second; preserve the one-year ambition.
- Nine actor verticals, including the separate privates-agent. No custodian in month 1. Administrator build includes matching/affirmation/reconciliation-platform evidence with distinct roles.
- Twelve strategy funds, one per type, all suffixed `-1`. The earlier request for multiple initial instances was corrected. Exactly one administrator per fund; multiple other relationships supported.
- Whole-trade allocation without PB/FCM splitting; initial financing allocation is rule based in the fund vertical. Keep one fund per trade initially; cross-fund block allocation is a later candidate.
- Full [month-1 product list](project-direction.md#product-scope), now including **bilateral OTC options**. Private loans are separate from syndicated loans, simple existing-loan servicing and last in instrument implementation.
- Independent records and financing calculations with realistic mandates. Select strategy portfolios first and size opening funding around them; routine margin/cash flows remain active. Exact numerical terms still need product-specific definition.
- Historical market baseline and fictional portfolios/trades. Start with evidence playback and decision/event logs; fuller processing reconstruction is deferred and a fresh stochastic run can differ.
- Loan agents service syndicated loans; privates-agent services private loans and private warrants. Borrower representation is still a design choice but must be autonomous; Patrick is not a runtime borrower.
- Funds receive roughly 25% of month-1 effort. The [effort table](README.md#interview-order-and-month-1-effort) is a planning reference, not measured effort; a revised allocation across the nine-vertical roster remains unchosen.

## Month 2: operating work and authority

The morning outcome is a prioritized actionable list with evidence, investigation and prepared next steps. The [harness brief](ops-harness/starting-point.md) contains the funding, OTC put/call discrepancy and failed-HY-bond examples.

The **80% target means classifying breaks and prescribing investigation steps in each supported break family**, not closing 80% of cases. A fully investigated fail can remain pending; Patrick gave a continuing fail two days after settlement as an example for a phone call, not a universal escalation deadline. A firm delivery milestone, exact family definitions and case sets remain open; initial quality reporting and holdout depth are settled above.

Harness external messages initially require human approval of exact content and recipients, renewed after material message/evidence changes. Specific communication types may later qualify for an auto-approval list with demonstrated reliability. This does not constrain actor-to-actor communications. The harness can autonomously correct fund OMS/instrument-master records within authorized access, with an audit trail; other verticals correct their own records. The exact operating interfaces still need specification.

## Months 3–4: decision models and model economics

“Decision model” means a **non-generative typed model such as Jev**, scoring predefined options/questions. It does not mean a small LLM investigator. It can help tag cases; direct facts and calculated values should retain their sources.

Example tags: product family, trade net money, assigned executing-broker risk, recent bond volatility, affirmation/matching status. Combine characteristics into a priority score, where higher means earlier attention. Put/call discrepancy, funding and HY fail were ranked in that order in the example, but news/volatility and funding size can change it.

**Deliberately deferred:** exact score weights, methods to establish them, complete taxonomy and a small number of possible queue categories. Do not insist on resolving these in the next round.

Months 2–3 build agents and decision-based characterization. Across accelerated runs, tags and outcomes may expose predictive patterns or hidden operational risks. Findings go into a **PDF report**, then Patrick launches a separate investigation until a clearer process can be developed. No automatic live-policy rewrite or automatic promotion is approved.

Month 4 begins cheaper, less reasoning-intensive model experiments for defined subordinate tasks, then open-model weight changes to approach frontier task performance. Top-level institutional decision-makers remain the strongest frontier models. “Post-training” means changing open-model weights; do not conflate it with tagging, priority-weight adjustment or prompt editing. Month-3 UI and conditional fundraising remain in the direction.

The 1,000-simulated-days-per-day ambition and the rough 3x volume / 10–20x breaks example are unvalidated goals/hypotheses. Separate imposed stress assumptions from emergent effects. No formal randomness distribution or game-theory implementation is selected.

## Agreed focused follow-ups and remaining decisions

1. Strategy/portfolio research and interview before finalizing the fund plan: plausible holdings, hedges, trading behavior, financing and constraints, informed by real strategies and Patrick's experience.
2. Joint instrument-workflow sessions before finalizing interdependent actor plans: evidence, calculations, timing, autonomous responses and observable completion.

Other open items to carry to the appropriate interview:

- Exact historical period, data coverage, evidence-playback duration, schedules, run controls and detailed technical failure reporting.
- Execution origin, venue/clearinghouse evidence, product variants and administrator-versus-platform responsibility.
- Autonomous institution context and permitted evidence; numerical funding buffers and product-specific routine flows.
- Detailed control coverage and fund-record action interfaces, later communication auto-approval evidence and closure rules; preserve the confirmed authority boundary and first integrated failure checks.
- CDM release/binding and verified capability coverage; researched supplements for approval; product definitions, contract variants and settlement conventions, including correction of the loan dictionary mapping before reuse.
- Break-family definitions and reviewed evaluation cases; retain per-family 80%, reporting-only additional metrics and familiar-pattern holdouts initially.
- Revised effort allocation for the nine verticals and the eventual transition from mature shared modules to actor-maintained variants.
- Data and task-level evaluations for lower-cost/open-weight models; detailed PDF investigation and UI workflows.
- Calendar kickoff, human development/review capacity, commercial deployment and licensing.

## Sources and state

Use [source review](source-review.md) and the [catalog](source-catalog.md) selectively. The briefs include links to retained material; the harness/shared-world briefs also link the official Jev documentation and the Archegos investigation consulted during this session. Sources are not adopted schemas or demonstrated model performance.

The original personal collection and application-owning repositories remain unchanged. This add-notes pass updates the preparation package only. These local files are not approved build specifications. No deployment, commit or publication was performed.

## Fresh-session prompt

> Continue the ops-harness and month 1–4 interview from this handoff, including its Decision-audit interview section, project-direction.md, ops-harness/starting-point.md and ops-harness/shared-terms.md. Ask one question at a time and do not restart settled scope. All nine actor verticals run unattended from one trade-date command or schedule; privates-agent owns private-loan/warrant agency and loan agents handle syndicated loans only. Patrick does not intervene in or override actor decisions. Preserve initially shared OMS/master modules designed for later independent actor variants, selected CDM authority, per-product definition gates and versioned terms. The harness may autonomously correct authorized fund records only; other actors correct their own records, and harness external messages initially require exact-message approval. Readiness is setup-only with explicit assumptions sufficient. Initial replay is evidence playback/logs, not full processing reconstruction. Evaluate 80% classify-and-prescribe per supported break family using fresh familiar-pattern cases; other quality metrics are reporting-only initially. Preserve PDF findings followed by investigation and later cheaper/open-weight worker experiments with frontier leaders retained. Carry forward the selected product depths and active routine cash flows. Bilateral OTC options are in month 1. Scoring weights and a few queue categories are deferred. Use graphs when useful and follow the actor interview order. Do not implement from these starting briefs.
