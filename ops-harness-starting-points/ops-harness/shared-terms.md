# Shared terms

Owner: ops-harness. Updated working vocabulary, 13 November 2026, incorporating the [decision-audit interview](../interview-handoff.md#decision-audit-interview) and subsequent privates-agent correction. Continue the [ops-harness interview](starting-point.md) from the remaining questions; do not reopen the confirmed boundaries below.

These definitions establish how this project uses words. They are not a substitute for product contracts, legal definitions, a wire schema or current market rules. **Confirmed** entries express interview choices. **Working** entries are proposed language for the next interview. Record product-specific meanings where a generic definition would hide an important distinction.

This is the canonical glossary within the preparation package. No local application repository exists yet, so it lives in this ops-harness subfolder. When that repository is created, move the canonical file and update links; do not maintain a separate glossary in every simulator.

## Institutions and boundaries

| Term | Project meaning | Status |
| --- | --- | --- |
| Ops-harness | The licensable operations application, potentially entirely a portable harness, intended as the main middle-/back-office interface. | Confirmed |
| Simulation world | Institutions, market evidence and interactions used to develop and evaluate that application. | Confirmed |
| Vertical | An independently planned responsibility. One actor vertical may support many institution instances; a support responsibility need not be a separate service/repository. | Working |
| Actor / institution instance | A participant with its own records, mandate and permitted evidence. Shared implementation code does not imply shared private state. | Working |
| Actor autonomy | After configuration, all nine actors run from schedules and agents with zero manual intervention, human approvals, role-playing, or runtime overrides of institutional decisions. The world works without ops-harness. | Confirmed |
| Institutional decision-maker | The strongest frontier-model agent at the top of a vertical, applying its institution's goals, incentives, mandate and permitted information. It can make probabilistic choices and need not cooperate perfectly with other institutions. | Confirmed direction; exact implementation open |
| Human-in-the-loop work | Hands-on work in ops-harness, ops-infra, setup, and shared integration/replay/valuation. It does not make actor runtime actions depend on Patrick. | Confirmed |
| Harness communication approval | Communications to other institutions initially require approval of the exact message and recipients. Material changes to content or supporting evidence require fresh approval. Selected communication types may later enter an established auto-approval route. This does not gate autonomous actor-to-actor messages. | Confirmed boundary; later auto-approval criteria open |
| Harness record-change authority | Ops-harness may autonomously correct fund-side records within authorized access, with an audit trail and legitimate operator/action interface. Other verticals correct their own records through their own mechanisms; the harness can communicate discrepancies or requests. | Confirmed boundary; exact interfaces and access to specify |
| Fund / strategy instance | One simulated fund corresponds to one strategy instance. Initially there are twelve, each named with `-1`. | Confirmed |
| Strategy type | A portfolio/trading style such as equity-arb. Several fund instances could use the same type later; only one per type is initially required. | Confirmed |
| Executing broker | The role supplying independent broker-side execution records and communications. Distinguish it from carrying/financing the resulting position. | Working |
| PB | Prime-broker role responsible for its own account records, financing and reporting in the selected scenario. Define supported products and services per relationship. | Working |
| OTC counterparty | Bilateral dealer/counterparty role for selected contracts, with its own records, contractual calculations and evidence. | Working |
| FCM | Futures commission merchant role for listed-futures and applicable cleared-OTC account workflows. It is not automatically the executing party or clearinghouse. | Working |
| Administrator vertical | Build boundary containing fund-administrator evidence plus matching, affirmation and reconciliation-platform evidence. | Confirmed |
| Fund administrator | The fund's single assigned administrator relationship; distinguish it from platform roles implemented in the same vertical. | Confirmed |
| Loan agent | The vertical handling syndicated loans only. Exact settlement, lender and borrower communications need the instrument interview. | Confirmed scope; details open |
| Privates-agent | Separate ninth vertical handling private-loan servicing and private-warrant agency, including relevant registers, exercise notices and delivery evidence. Initial private-loan scope includes cash interest and simple PIK; initial warrant scope includes cash and cashless exercise. | Confirmed scope; profiles and interfaces to specify |
| Borrower | Identify the party owing under the loan; distinguish it from a fund receiving PB financing. | Working |
| Shared world / ops-lab | Coordination of scenarios, time, deliveries, replay and evaluation; not an economic participant. | Working |
| Ops-infra | Trusted workspace/runtime infrastructure, governed by its owning repository; not a financial actor. | Confirmed |

## Execution and processing

| Term | Working definition or confirmed rule |
| --- | --- |
| Instrument | Product/contract and terms needed for the selected workflow. Its type alone does not settle route, eligibility or account treatment. |
| Bilateral OTC option | An explicitly included month-1 product family. Exact variants and workflows remain to select; this addition does not automatically include listed options or FX. |
| Execution / fill | Evidence that a trade was agreed/executed. Preserve origin and party perspective; a synthetic fill is not an actual historical exchange print. |
| Trade capture | Recording and validating executed trade details, including comparison with independent evidence. Patrick emphasized matching the two sides as a central T+0 task. |
| Booking | A participant's representation of the trade in its own records. Distinguish it from execution and another participant's acceptance. |
| OMS | Order management system. Initially develop a shared reusable foundation for trade-processing capabilities, including booking and recipient exports. Once established, independent actors maintain their own variants and selectively adopt shared improvements after compatibility checks. A complete trading application is not specified. |
| Instrument master / security master | Initially a shared reusable foundation for instrument definitions and terms, designed for independently maintained actor variants after the base is established. Shared implementation does not share private records. Preserve effective terms versions so a trade keeps its agreed version unless explicitly amended; distinguish contractual amendments from reference-data corrections. |
| FINOS CDM | Selected foundation and authority for applicable instrument fields, price representation and relevant verified calculations. Verify coverage rather than assume a complete valuation engine. Research gaps and obtain Patrick's approval before adopting a supplement. Release and binding remain to select. |
| Product definition gate | Before implementing each product's dependent records and calculations, establish applicable CDM requirements, calculation inputs, simulation additions and recipient needs. Apply the gate product by product. |
| Readiness | Setup assessment of whether the selected arrangement can be supported. Explicit recorded assumptions that agreements and eligibility are in place suffice; supporting simulated executed documents are not a readiness gate. This is not an ongoing harness capability. |
| Allocation | Assignment to the relevant fund/account/relationship. **Confirmed simplification:** 100% allocation to one applicable financing relationship, without PB/FCM splitting. One fund per trade initially; cross-fund block allocation is a later candidate. |
| Financing allocation decision | The fund's rule-based choice of eligible financing/carrying relationship, inside the fund vertical before export. Counterparty acceptance is a separate result. |
| Matching | Comparing relevant submitted details and recording agreement/differences. Fields and tolerances depend on the workflow. |
| Affirmation / confirmation | Distinct workflow terms whose meaning, actor and evidence must be specified per product/platform. An acknowledgment is not automatically a final contractual confirmation. |
| Acknowledgment | Evidence of receipt or processing, with its actual status. Receipt alone does not imply matching, acceptance or settlement. |
| Settlement | Completion of the relevant cash/security delivery obligations. A projected obligation or instruction is not proof of completion. |
| Lifecycle event | Contractual or position-related event after execution. Month 1 selects events needed for credible workflows, not broad coverage. |
| Break / discrepancy | Difference, missing item or status conflict requiring interpretation. Timing/perspective differences are not automatically errors. |
| Correction | A change linked to earlier evidence and its effective meaning. Preserve prior deliveries, as-known history and correction lineage; a corrected report must not erase what was previously available. Detailed lifecycle milestones are deferred to product and actor interviews. |
| T+0 / subsequent day | Time relative to a trade date in the agreed calendar. This project does not assume one settlement cycle for all instruments. |

## Financing, data and evaluation

| Term | Working definition or confirmed rule |
| --- | --- |
| Mandate / constraint | Rules governing permissible holdings, activity, risk or financing. Measures, limits and consequences remain scenario decisions. |
| Headroom | Remaining capacity under a constraint. Choose realistic strategy portfolios first, then size opening cash/collateral around them for the initial ordinary days. Routine margin calls and contractual cash flows remain active. |
| Financing / margin / collateral | Related but distinct contractual/operational concepts. Each actor names its calculation, obligation and evidence; no universal formula is prescribed here. |
| Call | Communicated request or obligation from a financing/collateral process, with a status. Distinguish routine requirements from shortfalls or disputed calls. |
| Independent calculation | An actor derives its own result from permitted inputs and terms. Copying another actor's final answer does not demonstrate independence. Shared published observations do not invalidate it. |
| Shared valuation work | Human-led development, inspection and evaluation of valuation capabilities in shared support. Once configured, the capability required by an actor must be callable automatically during a run. |
| Historical baseline | Observations from a selected historical period. Portfolio holdings and executions remain fictional unless explicitly identified otherwise. |
| Reference data / market data | Reference data identifies/describes instruments, parties and terms; market data supplies observations. The instrument-master foundation begins shared and is built for later independent actor variants; exact initial component ownership and interfaces remain to specify. |
| As-of / available-at | What time a value describes versus when a participant could obtain it. Replay must not reveal information early merely because it describes an earlier date. |
| Replay | The umbrella for reconstructing or re-running a scenario. Specify whether the operation is recorded playback or a fresh trial; these have different reproducibility expectations. |
| Recorded playback | Initial scope is inspection of delivered evidence and decision/event logs, preserving what participants could know at each point. The fuller package needed to reconstruct processing is deferred; evidence playback does not establish complete reproducibility. |
| Fresh stochastic trial | A new run in which probabilistic agents can make different choices, even from the same starting conditions. Record the resulting history rather than requiring it to match a prior trial. |
| Counterfactual investigation | Exploring an alternative after inspecting a prior failure or outcome. Keep changed assumptions and the resulting new history distinct from the original observed run. |
| Scenario | Opening conditions and scheduled activity, including controlled exceptions. Identify historical, fictional, injected and expected elements. |
| Evidence | Delivered file, message, report or response available at that point, with a source, time and meaning; not necessarily ground truth. Use authority rules by fact and workflow where possible, investigate provenance/timing and allow unresolved conclusions. A majority of matching sources or the fund's own record is not automatically authoritative. |
| Hidden expected result | Evaluation material kept separate from actors and the harness so their work can be checked without supplying answers. |
| Live, for month 1 | **Confirmed:** one simulate-trade-date command or schedule coordinates all nine actors, producing independent activity and evidence without the harness, user prompts, human approval gates or manual completion. Exact command syntax remains open. |
| Business pending versus run failure | A dispute or unsettled obligation can remain pending. If a workflow cannot proceed safely, mark it incomplete or uncertain and hold dependent work while independent actors/workflows continue. Do not treat missing input as a clean result or wait silently for a human to perform an actor's work. |
| First integrated control checks | Required representative checks for missing input, duplicate delivery, uncertain submission outcomes, provider/quota failures, stale approvals and instructions embedded in untrusted documents. Check visible uncertainty and protection against duplicate business effects. This describes required testing, not completed validation. |
| Starting brief / specification / plan | Interview context and questions; agreed intended behavior; implementation approach and checks. Creating a brief does not approve the latter two. |

## Harness cases and decision models

The role distinctions and goals below are confirmed. Detailed taxonomies, algorithms, score weights, queue categories and calibration methods have not been selected.

| Term | Project meaning |
| --- | --- |
| Operational case | The maintained record of an issue: evidence, chronology, findings, completed actions, outstanding work, current priority and outcome. Exact case/status fields remain a design choice. |
| Task / investigation step | A concrete action within a case, such as examining a term sheet, preparing a query or reviewing a reply. Completing a task does not by itself resolve the case. |
| Pending resolution | Available work may have been performed while an external response, delivery, payment or other outcome is still outstanding. Keep the case and next steps current as evidence arrives. |
| Classification plus prescribed investigation | Identify the kind of break and a useful path for investigating its cause. **The 80% target applies independently to each supported break family**, not final resolution or financial-risk reduction. Exact family definitions, cases and review rubric remain to specify. |
| Initial evaluation | Fresh held-out cases use familiar scenario patterns and document layouts; broader generalization testing comes later. Report false-clean conclusions, unsupported certainty, abstention and unnecessary escalation without separate initial acceptance gates. The per-family 80% target is the performance gate; required failure/control checks still apply. |
| Verified resolution | Evidence supports closing the particular issue. Sending a message, completing a control, proposing a cause or exhausting currently available tasks is not enough by itself. Exact closure rules remain open. |
| Operational frontier agent | Performs open-ended investigation, evidence synthesis and appropriate work under harness authority. Distinguish this role from bounded decision models and from autonomous institutional agents. |
| Jev-style decision model | A non-generative model answering defined typed questions against supplied state, with structured results such as choices, scores or probabilities. This is not shorthand for a cheaper LLM agent. [TypeSafe's introduction](https://docs.typesafe.ai/introduction) describes this interface; project-specific quality has not been validated. |
| Tag / characteristic | A named property used to describe and prioritize a case. Candidate characteristics include product family, trade net money, assigned broker risk, recent volatility and matching status. Values can be recorded, calculated or inferred; a complete taxonomy is deferred. |
| Recorded characteristic | A value taken from identified evidence or an explicitly assigned configuration. Its source, time and meaning matter; a reported value is not automatically a verified fact. |
| Calculated characteristic | A value derived through an explicit computation using identified inputs, such as an amount or selected volatility measure. Retain the calculation and input provenance; no particular formula is chosen here. |
| Inferred characteristic | A judgment or estimate derived from available evidence, including a decision-model output. Preserve its inferential status rather than presenting it as a directly reported fact. |
| Priority score | A value used to order attention in the work queue: higher means earlier attention. It is not automatically a probability of loss, model confidence or expected financial loss. Evidence changes can change priority. |
| Priority weights / queue categories | The coefficients or rules combining characteristics, and any small set of presentation groups. Their values, construction method and category choices are explicitly deferred. The example ordering of three cases is not a universal hierarchy. |
| Model probability / confidence | Output whose meaning depends on the defined model question. Do not substitute it for a queue score or assume it provides validated risk probabilities. Calibration and decision thresholds remain to be investigated on the relevant population. |
| Finding | An observed pattern, prediction or possible missed risk arising from case histories or accelerated trials. Keep those evidential statuses distinct; association does not establish cause. |
| PDF finding and separate investigation | The agreed route for discoveries: expose the finding in a PDF, then Patrick launches a separate investigation until a clearer process exists. Findings do not automatically change policies or promote a model. |
| Cheaper worker model | A later candidate for a defined subordinate task, investigated from month 4. The strongest frontier decision-makers remain at the top of the verticals; this is not their blanket replacement. |
| Open-weight post-training | Changing an open model's learned weights for selected tasks. It is distinct from editing prompts/skills, adding tags, changing priority-score weights, or using a Jev-style decision model. Data, evaluation and promotion choices remain open. |

## Remaining terminology work

1. Define product-specific meanings and evidence for captured, matched, confirmed and settled in each first workflow.
2. Specify opening funding amounts for the selected strategy portfolios while keeping ordinary scheduled cash/margin flows active.
3. Identify which administrator outputs represent the fund administrator versus platform roles, and each recipient's evidence access.
4. Specify case completion, closure, escalation and pending-action meanings, plus interfaces/access for autonomous fund-record corrections within the confirmed boundary.
5. Define supported break families, cases and the review rubric for the per-family classification/investigation target, separately from eventual resolution.

Do not restart decisions on actor autonomy, the initial harness external-message approval boundary, the PDF investigation route or what post-training means. Keep the full tag taxonomy, scoring weights, queue categories and calibration design for the later stage Patrick requested.

Record changes here with the affected workflow/source and update linked examples. Do not rename business concepts merely to match implementation variables.

## References

- [Project direction](../project-direction.md): explicit scope and interview choices.
- [Ops-harness starting point](starting-point.md): morning cases, approval boundaries, decision-model roles and remaining interview work.
- [Vertical map](../vertical-map.md): actor and support boundaries.
- [Existing fund definitions](../../../sim-funds/docs/shared-definitions.md): earlier vocabulary and mapping questions; reconcile the old baseline with the selected CDM foundation and verify applicable coverage before reuse.
- [Retained architecture](../../../../pr1/business/ops-harness/notes/architecture/2026-10-19_simulator-architecture-page-snapshot.md): evidence/evaluation concepts; old role and repository proposals are not current scope.
- [TypeSafe introduction](https://docs.typesafe.ai/introduction): official description of Jev's typed, non-generative decision interface. It does not establish accuracy, calibration or suitability for the selected financial tasks.
