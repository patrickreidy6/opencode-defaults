# Source review and reconciliation

Review date: 13 November 2026. Original collection: `C:/Users/preid/pr1/business/ops-harness`.

Updated after the continued interview on the same date. The original full-collection review described below is historical review evidence; preparation of the new briefs involved selective source checks, not a second full audit or fresh external verification.

## Latest interview reconciliation

The [decision-audit interview](interview-handoff.md#decision-audit-interview) records the subsequent 38-question review and separate privates-agent correction. Its outcomes govern over conflicting historical audit recommendations; the original audit evidence remains intact. No new external verification or archived-engine execution was performed while saving these decisions.

The [direction document](project-direction.md) now records the nine actor types, twelve named strategy funds, full month-1 instrument list, realistic financing and historical replay. These replace the earlier open roster questions. [The overview](README.md) links the nine actor briefs, ops-harness/shared terms and shared-world brief, and records the revised effort proposal.

- FCMs, executing brokers, market-data providers, syndicated-loan agents and the separate privates-agent are explicit actor verticals. Custodians are excluded from month 1.
- Administrator and platform roles remain conceptually distinct but their evidence is grouped into one administrator build vertical. The old administrator-versus-post-trade choice is superseded.
- The fund's old narrow cash-equity demonstration is a reusable example, not the current total world scope. No owning repository was rewritten by this preparation task.
- Fully funded syndicated-loan assignments belong to loan agents; private-loan cash interest/simple PIK and private-warrant cash/cashless exercise belong to privates-agent. Private loans are last in the month-1 instrument sequence.
- The catalog has no dedicated listed-futures/FCM, private-warrant or private-loan research packet. These are targeted research gaps, not permission to omit the products. Market-history coverage also needs verification.
- Bilateral OTC options were explicitly added during the continued interview. Existing FX/listed-options research does not automatically add those products or establish bilateral OTC conventions. Strategy research may expose further gaps; bring proposed changes back explicitly.
- Common vocabulary belongs in [ops-harness/shared-terms.md](ops-harness/shared-terms.md). CDM remains the selected model foundation for applicable definitions/calculations; reconcile verified capabilities with the shared vocabulary rather than treating CDM as an optional survey.
- Initial exceptions, autonomous response details, borrower representation, portfolios, dates and run acceptance remain open. Manual pre-harness resolution is no longer a choice: all nine actors must run unattended from a single date trigger, without runtime human approvals or overrides, even when the harness is absent.

## Continued interview: autonomy and model roles

- Ops-harness, ops-infra and shared integration/replay/valuation work are hands-on. Their possible human-in-the-loop steps must not leak into the autonomous actors' scheduled work. Top institutional judgment uses the strongest frontier models and prescribed incentives, informed by real cases.
- The 80% goal concerns classification and prescribed investigation paths across breaks, not case closure. Harness external messages initially need approval; actor-to-actor communications do not. The harness may autonomously correct fund records within authorized access; other verticals correct their own. Exact external-message approval, per-family 80% evaluation and other confirmed limits are in the [harness brief](ops-harness/starting-point.md).
- “Decision model” means typed non-generative decisions such as Jev, not cheaper LLM investigators. The [official TypeSafe introduction](https://docs.typesafe.ai/introduction), checked during this session, documents defined questions with structured outputs/probabilities. It does not establish quality on this project's cases.
- Priority derives from case characteristics. Weights and a small number of possible categories are deferred. Findings become PDF reports and separate investigations; automatic live-policy changes are not approved.
- Month 4 begins cheaper-worker experiments and subsequent open-weight post-training, while strongest-frontier leadership remains. No successful replacement or training result is claimed.
- The [Archegos investigation](https://www.sec.gov/Archives/edgar/data/1159510/000137036821000064/a210729-ex992.htm), checked selectively during the discussion, is a primary example of warnings, client accommodations and delayed risk action. It motivates research into institutional behavior, not a universal causal model.
- Randomness, accelerated runs and disproportionate break growth are design interests. The stated throughput and stress multipliers remain ambitions/hypotheses; record them separately from validated evidence. Recorded playback is distinct from fresh stochastic decision-making.

These new web references supplement the original collection; they have not been added as purported local files to the historical source inventory.

## How to use the source layers

| Layer | Use | Do not infer |
|---|---|---|
| Current interview decisions | Product purpose, relative priorities and requested sequence; see `project-direction.md`. | Complete specifications or feasible delivery estimates. |
| Current owning repositories | Already settled requirements and recorded implementation state. | That recorded state proves the present deployed runtime without inspection. |
| Earlier architecture and handovers | Actor boundaries, temporal evidence, proposed designs and decision history. | Every old proposal remains current. |
| Product research packets | Domain distinctions, candidate fields, worked examples and source leads. | Full schemas are adopted; passing fixtures prove production readiness. |
| External interface examples | Concrete examples of how sources differ. | Current vendor compatibility or a universal industry format. |
| Marketing, naming and administration | Business history and supporting records. | Product requirements, validated demand, legal clearance or commitments to customers. |

## Reconciliation register

| Finding | Evidence in the collection | Current treatment / next action |
|---|---|---|
| Workplace hardening versus independent build | `ops-harness-v2-id-d574f41c.zip` assumes existing employer scripts, skills and Delta Lake; root independent-build addendum explicitly supersedes reuse. | Historical implementation baseline. Retain portable contracts and evidence principles, not inherited code/data assumptions. |
| Product purpose was ambiguous | Toolkit, professional preparation, consulting and simulated-world narratives coexist. | Resolved at intent level by 13 November answer: licensable product first, professional positioning second; simulation supports the product. |
| Deadlines conflict | September/October plans describe January 2027 preparation and two demonstrations. | New one-year product horizon and relative month-1–4 sequence govern current intent. Calendar dates and scope remain open. |
| First examples differ | Earlier variance-swap and loan flagships; copied fund docs variously say two PB formats or PB plus admin. | Current `sim-funds` repo resolves its earlier baseline to cash equities and PB/admin outputs. The continued interview establishes broader month-1 intent; reconcile the owning repo during its own planning session. |
| Administrator versus post-trade | Infrastructure/architecture offers either as initial fourth workstream. | Superseded: administrator, matching, affirmation and reconciliation-platform evidence is grouped in one administrator vertical, with distinct roles and outputs. |
| Monolithic project versus independent actors | Independent-build plan starts one modular Python project; later architecture separates institutional workstreams. | Clarify scope of each statement: modular harness internals can coexist with separate simulators. Do not assume one project for the entire world. |
| Infrastructure is stale in PR1 | Root setup document retains VM/container options, Tailscale pause and pending first boot; workstation spec names older hardware candidates. | Current `ops-infra` source settles containers and Tailscale and records workspace rollout. No need to re-interview those historical choices. |
| Hindsight requirement is stale | `notes/planning/2026-10-11_independent-build-plan.md` selects Hindsight. | Current `ops-infra` guidance explicitly supersedes it as a prerequisite and keeps durable decisions in repository files. |
| Agent authority conflicts | Equity-swap service pitch proposes automatic resolution below dollar thresholds; later plans disable/simulate actions and require accountable decisions. | Clarified: all nine simulated actors run without human approvals or decision overrides. Harness external messages initially need approval, with later evidence-based auto-approval types. Fund-only autonomous correction authority is now confirmed; exact interfaces and customer-deployment permissions remain open. Pitch thresholds are not adopted. |
| Commercial ownership conflicts | Service/positioning documents promise 100% client ownership; independent plan proposes reusable licensed core. | New licensable-product goal is confirmed. Exact ownership, customization and licensing model remain open. |
| Extensive research can look like a required schema | Nine packets contain 1,543 field entries/families, including overlaps and inherited concepts. | Candidate inventory for later reduction. Adopt only what the selected scenario and actor need. |
| Loans are not one interchangeable module | Original flagship emphasizes private debt; ClearPar packet explicitly covers syndicated loans and excludes private/direct lending. | Preserve separate scope. Do not claim that the packet implements the private-loan flagship. |
| Fixture results can look like system validation | Stored passes for arithmetic, projections, corrections and validation. | Not proof of persistent ingestion, full ledgers, live agent behavior, current legal conventions or vendor acceptance. |
| Legacy wiki has broken/ambiguous evidence | 23 linked source pages absent; conflicting 9 p.m. / 10:45 p.m. affirmation wording. | Research repair, not a question for Patrick to resolve from memory. Verify precise processes before operational adoption. |
| Research subnotes retain intermediate paths | FX references unbundled `../working/build_examples.py`; loan notes name absent `clearpar_sources.json` and `lifecycle_sources.json`; volatility notes name absent intermediate registers/model paths. | Use final consolidated registers, retain source IDs and repair links when the relevant packet is adopted. |
| Vendor examples are historical | Allvue/BNY/Goldman pages include older formats and sample dates; IBKR examples have their own scope and ambiguities. | Useful interface evidence, not current certified adapters. Download date is not specification date. |
| Court sources do not supply the sought trade records | Anson PDF is volume 1 of 3; indexed trading-record exhibits W–BB are in volume 3 at printed pp945–981. Greenlight PDF is a fee opinion describing sheets, not containing them. | Explicit source gaps. Do not count either as an acquired trade-file dataset or import allegations as facts. |
| Administration and unrelated content are mixed in | Earlier LLC template versus later sole-proprietor memo; old vendor landscape includes an unrelated family-event paragraph. | Preserve originals. These are peripheral/history, not blockers to simulation planning; do not copy private values into build briefs. |

## Current repository pointers

- [sim-funds requirements](../../sim-funds/readme.md): authoritative local fund baseline as inspected.
- [ops-infra direction](../../ops-infra/readme.md): workspace responsibilities and supersession of old setup choices.
- [ops-infra working rules](../../ops-infra/AGENTS.md): trusted management, workspace isolation and scope.
- [OpenCode defaults](../README.md): coding environment defaults, not the financial application.

## Coverage and limits

The team reviewed all 76 loose files and 431 file entries across 12 archives. Byte-identical duplicate payloads were not treated as new evidence. All 113 archive JSON files were parsed recursively (8,832 objects and 70,810 scalar values), and all 80 CSVs were parsed (3,461 data rows, no variable-width rows). All 27 Python files parsed and were inspected for structure and bounded business behavior; code was not executed. All 318 available self-manifest hash records matched. Thirty-two same-name CSV/JSON list pairs had matching record counts; that is shape evidence, not complete semantic validation.

All five loose DOCX files, five workbook tabs, the PNG and six PDFs were reviewed. Anson's 418 pages were divided across readers; narrative was read, structured disclosure listings parsed, and scanned material rendered/OCR processed. The disclosure catalogs are document metadata, not the underlying emails or trade records. Tiny screenshot text remains imperfectly legible, especially pp136,140,195–196,276,293,296; one original linked image at p92 is already broken. This is not a character-perfect transcription claim.

External URLs were treated as references unless their content was included locally. This review did not newly verify every current vendor, market, regulatory, legal, model or library claim. No source files were reorganized, edited or deleted. Do not let preservation/integrity checks turn into claims that the material is accurate or adopted.
