# Market-data vertical starting point

Status: interview starting brief, 13 November 2026. Confirmed decisions are separated from proposed design and research questions. Month-1 effort allocation: **7%**, a planning allocation rather than a delivery estimate.

[Overview](README.md) · [Project direction](project-direction.md) · [Vertical map](vertical-map.md) · [Shared terms](ops-harness/shared-terms.md) · [Shared world](shared-world.md)

The [decision-audit interview](interview-handoff.md#decision-audit-interview) records the confirmed foundation, product, authority and evaluation choices that govern this brief's remaining questions.

## Purpose and confirmed direction

The market-data vertical supplies observations for fictional funds and counterparties: inputs to trading, independent valuation and financing calculations, and credible reports. Its success depends on whether the agreed workflows can run and be inspected.

**Confirmed:** market-data providers are a month-1 actor vertical. Patrick selected a historical market baseline for replay, with fictional portfolios and trades. One fund will initially represent each of the 12 strategy types. The agreed product scope spans cash equities, listed futures, corporate and convertible bonds, bilateral equity and variance/volatility swaps, bilateral OTC options, cleared single-name and index CDS, private warrants, syndicated loans, and simple private loans. Private loans are the last instrument to cover.

The historical period, provider population, selected instruments, observation frequency, and acquisition route remain open. Selecting historical replay does not establish that all required history is obtainable. Nor does it make the synthetic prices inside earlier research packets historical observations.

The principal harness build remains in month 2. Month 1 supplies retained evidence and decision/event logs for playback. Provider imperfections are candidate scenarios for the interview; no specific delay, correction or other fault has been selected yet.

**Confirmed operating model:** one simulate-trade-date command coordinates all nine actor verticals after configuration. Providers operate on their schedules and respond autonomously, without the harness, manual intervention, approval gates, or user runtime overrides. The strongest available frontier models provide institutional judgment under each provider's own mandate, goals, incentives, and private state. Probabilistic decisions are permitted; historical observations retain their provenance.

## Owned state and boundaries

**Proposed:** the provider owns its available observation history, source/provenance records, publication or delivery history, and corrections to its own delivered data. Recipients preserve what they received and when. The provider should not infer a recipient's private positions or reveal hidden scenario outcomes.

[Funds](funds.md), [PBs](prime-brokers.md), [FCMs](fcms.md), and [OTC counterparties](otc-counterparties.md) remain responsible for their own calculations under their own terms and mandates. Sharing an observed price does not require sharing private valuations, risk decisions, or ledgers. Conversely, different provider records can be a deliberate source of operational disagreement, if the selected scenario needs it.

**Open:** ownership of instrument identities, reference terms, calendars, rates, and corporate-action or lifecycle notices. Some may belong with this vertical; others may be shared reference resources or evidence issued by another actor. Resolve those responsibilities in [shared world](shared-world.md) rather than automatically placing every reusable value in a central market-data database.

**Confirmed foundation:** initially shared instrument-master and OMS modules mature into a base for independently maintained actor variants, with selective adoption of improvements. The master supports effective terms versions; existing trades retain their agreed terms, and reference-data corrections do not silently amend contracts. CDM is the selected model foundation where applicable. This reuse does not decide which actor supplies each reference fact or grant shared access to private records.

The provider corrects its own delivered data. The harness may request correction but cannot directly edit provider records; its autonomous record-change access is limited to funds.

A provider's stated value, an institution's calculated mark, and an execution price must remain distinguishable. The brief does not select valuation models or decide that every instrument has a readily observable traded price.

Market-data and news context may also support the harness's issuer-risk research. The exact provider, research interface, and division between provider evidence and harness analysis remain open. No specific vendor, news service, or additional service has been selected.

## Evidence received and produced

These are **proposed input/output families** for the interview, not an adopted universal feed.

| Input or configuration | Output to consider |
| --- | --- |
| Selected historical period and instrument universe | Reproducible observations for the approved scenario |
| Retained source data with provenance | Deliveries identifying source, instrument, observation time, and availability time |
| Provider subscription or request | A bounded response appropriate to the recipient's requested coverage |
| Source correction or delayed publication | Corrected or late delivery retaining the prior version |
| Unsupported instrument or missing period | Explicit coverage/missing-data evidence for the recipient |

Select necessary observation types per product. Rates, prices, credit measures, volatility inputs, and instrument terms are candidates to investigate.

During setup, resolve sparse history through an agreed instrument/period, calculation scope, or explicitly labeled synthetic input. During a run, handle missing coverage autonomously under the configured mandate and disclose the resulting limitation. Do not prompt Patrick, invent a historical observation, or silently switch the world to synthetic market paths.

## Autonomous operating loop

At configured publication times, the provider prepares the observations available for the simulated date, checks source/coverage status, and delivers the appropriate recipient views. Incoming requests trigger autonomous responses using the provider's available evidence and institutional judgment. The provider handles late data, corrections, conflicting sources, and unavailable coverage according to its configured responsibilities, recording what it did and why.

Where issuer/news context is selected during planning, its availability and source boundaries enter the same loop. The provider supplies evidence; recipient institutions and the harness retain their own analytical judgments. Human work belongs in source selection, configuration, integration, and evaluation, not routine provider actions during a run.

## Proposed first scenario and acceptance examples

Choose a small historical universe jointly with the fund and PB briefs. Replay a sequence of observations while the fund and PB consume them independently. Compare what each institution received without inspecting its private calculation state. Extend the same evidence discipline to less readily sourced products after selecting their required inputs.

Acceptance examples to refine:

- Initial evidence playback retains deliveries and decision/event logs; full processing reconstruction is deferred. Fresh probabilistic runs can differ while preserving an explainable delivery history.
- The recipient cannot consume an observation before its chosen availability time.
- A missing value remains explicit instead of being silently copied forward or replaced.
- An introduced correction preserves both the originally delivered value and its successor.
- Units, currency, instrument identity, and date interpretation are unambiguous for the chosen outputs.
- Independent institutional calculations can be traced to delivered observations and their own assumptions.
- One simulate-trade-date command produces scheduled deliveries and request responses without the harness, user prompts, approvals, or overrides, including a selected missing-data case.

These are proposed checks; no delayed-feed or correction scenario is selected yet.

## Questions and research before implementation

1. What historical period and universe can cover the first portfolios while supplying useful financing and risk inputs?
2. Which workflows require intraday observations, and which can run on daily observations? Is “on demand” a new source observation or retrieval of the latest available one?
3. How many distinct provider behaviors are necessary initially? Which intentional differences would create useful operational work?
4. What evidence is available for bonds, CDS, loans, private warrants, and private loans? Where is an independent model mark needed instead of a quoted observation?
5. Which terms and calendars belong here, and which actor or shared resource owns the authoritative version for the scenario?
6. What acquisition, retention, and reuse permissions apply to the selected sources? Verify them when the actual data route is selected.
7. What provider goals and incentives govern autonomous publication, correction, and query handling? What issuer/news evidence is needed, if any, without prescribing a vendor?

The catalog has no dedicated market-data-provider packet. Establish data feasibility early; instrument field dictionaries do not settle it.

## Targeted source map

- [Current fund baseline](../../sim-funds/readme.md): the earlier, narrow historical-equity demonstration. Reuse its relevant evidence discipline; its small universe does not cap the new scope.
- [Cash-equity packet](../../../pr1/business/ops-harness/research/equities/cash-equity-research-packet.zip): `README.md` and `reference_data_synthetic.json`. The README explicitly identifies invented prices; use it to avoid mistaking fixtures for acquired history.
- [Variance/volatility packet](../../../pr1/business/ops-harness/research/volatility/variance-volatility-research-packet.zip): `packet/variance_volatility_research_report.md`, `packet/synthetic_variance_volatility_observations.csv`, and `packet/variance_volatility_source_register.csv`. These identify candidate observation needs and source leads.
- [Equity-swap packet](../../../pr1/business/ops-harness/research/equities/equity-swap-master-research-packet.zip): `equity_swap_master/equity_swap_master_research.md` and `equity_swap_master/example_calendar_and_observations.json` provide another proposed terms/observations boundary.
- [Source review](source-review.md) and [product catalog](source-catalog.md#research): retained research is provisional; no comprehensive historical feed or current provider compatibility was validated.

## Fresh interview prompt

> Start the market-data vertical's cross-model planning interview. Read this brief, project-direction.md, shared-world.md, and ops-harness/shared-terms.md. Preserve historical replay with fictional funds/trades, including the agreed bilateral OTC-options scope. Establish required observations and source coverage during setup. Design autonomous scheduled publication and query handling with frontier-model judgment, provider goals/incentives, and private state. One simulate-trade-date command must work without the harness, manual intervention, approvals, or runtime overrides. Discuss issuer/news context without assuming a vendor. Ask one design question at a time. Retain provenance and no-prompt acceptance checks. Do not implement or acquire paid data during the interview.
