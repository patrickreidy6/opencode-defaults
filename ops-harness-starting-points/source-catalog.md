# Ops harness source catalog

Reviewed 2026-11-13. This catalog maps the retained [source directory](../../../pr1/business/ops-harness/) into eight digestible groups. It preserves the source filenames and archive membership. Grouping is navigation, not a decision about what to build or which requirements to adopt.

**Inventory:** 76 files on disk, including 12 ZIP archives. Those archives contain 431 additional file entries; archive directory entries are excluded. The [machine-readable inventory](source-inventory.json) contains the exact relative paths, byte sizes, file kinds and membership.

**Review coverage:** Narrative documents, retained source material, structured records and code were inspected. CSV and JSON records were parsed programmatically, code was inspected without executing archive programs, and stored validation receipts were treated as historical evidence. Some very small embedded screenshots could not be read reliably. This review does not independently certify every research claim, financial rule, screenshot detail, external interface or source URL. Research packets and their fields remain proposals unless a later decision explicitly adopts them.

**Duplicate material:** All 19 entries in the trade-file-sources ZIP match the corresponding loose files byte for byte. Both locations remain cataloged. Counts describe retained entries, not unique facts or independent evidence.

**Privacy:** Business administration entries contain only filenames and file metadata. No identification numbers, account values or private document contents are copied here.

| Group | Files on disk | ZIP file entries |
| --- | ---: | ---: |
| [Project direction and product ideas](#direction) | 14 | 0 |
| [World architecture and interfaces](#architecture) | 3 | 0 |
| [Simulated funds handoff](#funds) | 9 | 0 |
| [Product and lifecycle research](#research) | 9 | 246 |
| [Trade-file evidence and source copies](#interfaces) | 20 | 19 |
| [Infrastructure and workspaces](#infrastructure) | 4 | 0 |
| [Earlier designs and archived context](#history) | 12 | 166 |
| [Business administration](#administration) | 5 | 0 |

<a id="direction"></a>

## Project direction and product ideas

Independent build proposals, service positioning, workflow ideas and names. These record intentions and alternatives, not automatically adopted requirements.

| Source file | Kind | Bytes | ZIP file entries |
| --- | --- | ---: | ---: |
| [notes/2026-10-30_company-name-ideas.md](../../../pr1/business/ops-harness/notes/2026-10-30_company-name-ideas.md) | md | 892 |  |
| [notes/2026-10-30_distressed-forms-reviewer.md](../../../pr1/business/ops-harness/notes/2026-10-30_distressed-forms-reviewer.md) | md | 1,352 |  |
| [notes/2026-10-30_forensic-accountant-agent-idea.md](../../../pr1/business/ops-harness/notes/2026-10-30_forensic-accountant-agent-idea.md) | md | 570 |  |
| [notes/2026-10-30_hedge-fund-verticals-context.md](../../../pr1/business/ops-harness/notes/2026-10-30_hedge-fund-verticals-context.md) | md | 2,020 |  |
| [notes/2026-10-30_otc-settlement-agent-idea.md](../../../pr1/business/ops-harness/notes/2026-10-30_otc-settlement-agent-idea.md) | md | 1,056 |  |
| [notes/2026-10-30_research-agent-plan.md](../../../pr1/business/ops-harness/notes/2026-10-30_research-agent-plan.md) | md | 1,435 |  |
| [notes/2026-10-30_si-domain-idea.md](../../../pr1/business/ops-harness/notes/2026-10-30_si-domain-idea.md) | md | 970 |  |
| [notes/naming/2026-10-03_opsiv-trademark-research.md](../../../pr1/business/ops-harness/notes/naming/2026-10-03_opsiv-trademark-research.md) | md | 13,407 |  |
| [notes/naming/2026-10-03_opstone-trademark-research.md](../../../pr1/business/ops-harness/notes/naming/2026-10-03_opstone-trademark-research.md) | md | 24,954 |  |
| [notes/naming/2026-10-03_opziv-trademark-research.md](../../../pr1/business/ops-harness/notes/naming/2026-10-03_opziv-trademark-research.md) | md | 16,986 |  |
| [notes/planning/2026-10-11_independent-build-plan.md](../../../pr1/business/ops-harness/notes/planning/2026-10-11_independent-build-plan.md) | md | 34,909 |  |
| [ops-harness-independent-build-plan-id-cb53eed6.md](../../../pr1/business/ops-harness/ops-harness-independent-build-plan-id-cb53eed6.md) | md | 26,586 |  |
| [positioning-deck-custom-agents-vs-network-fintechs-id-46789ecd.md](../../../pr1/business/ops-harness/positioning-deck-custom-agents-vs-network-fintechs-id-46789ecd.md) | md | 16,329 |  |
| [service-offering-equity-swap-lifecycle-agents-id-4296741d.md](../../../pr1/business/ops-harness/service-offering-equity-swap-lifecycle-agents-id-4296741d.md) | md | 21,337 |  |

<a id="architecture"></a>

## World architecture and interfaces

Simulator architecture and trade-simulation planning, including boundaries between participants, evidence and interfaces.

| Source file | Kind | Bytes | ZIP file entries |
| --- | --- | ---: | ---: |
| [notes/architecture/2026-10-19_simulator-architecture-page-snapshot.md](../../../pr1/business/ops-harness/notes/architecture/2026-10-19_simulator-architecture-page-snapshot.md) | md | 38,338 |  |
| [notes/trade-simulation/2026-10-19_trade-interface-evidence-wiki-page-snapshot.md](../../../pr1/business/ops-harness/notes/trade-simulation/2026-10-19_trade-interface-evidence-wiki-page-snapshot.md) | md | 32,093 |  |
| [notes/trade-simulation/2026-10-19_trade-simulator-research-plan-page-snapshot.md](../../../pr1/business/ops-harness/notes/trade-simulation/2026-10-19_trade-simulator-research-plan-page-snapshot.md) | md | 38,609 |  |

<a id="funds"></a>

## Simulated funds handoff

Copied sim-funds planning and handoff documents. Compare with the owning repository before treating a copied status or instruction as current.

| Source file | Kind | Bytes | ZIP file entries |
| --- | --- | ---: | ---: |
| [notes/sim-funds/AGENTS.md](../../../pr1/business/ops-harness/notes/sim-funds/AGENTS.md) | md | 11,128 |  |
| [notes/sim-funds/docs/decisions-and-open-questions.md](../../../pr1/business/ops-harness/notes/sim-funds/docs/decisions-and-open-questions.md) | md | 16,557 |  |
| [notes/sim-funds/docs/first-session-prompt.md](../../../pr1/business/ops-harness/notes/sim-funds/docs/first-session-prompt.md) | md | 1,464 |  |
| [notes/sim-funds/docs/implementation-plan.md](../../../pr1/business/ops-harness/notes/sim-funds/docs/implementation-plan.md) | md | 18,219 |  |
| [notes/sim-funds/docs/shared-definitions.md](../../../pr1/business/ops-harness/notes/sim-funds/docs/shared-definitions.md) | md | 10,270 |  |
| [notes/sim-funds/docs/sim-funds-handover.md](../../../pr1/business/ops-harness/notes/sim-funds/docs/sim-funds-handover.md) | md | 40,439 |  |
| [notes/sim-funds/docs/source-map.md](../../../pr1/business/ops-harness/notes/sim-funds/docs/source-map.md) | md | 16,293 |  |
| [notes/sim-funds/docs/strategy-funds.md](../../../pr1/business/ops-harness/notes/sim-funds/docs/strategy-funds.md) | md | 6,910 |  |
| [notes/sim-funds/readme.md](../../../pr1/business/ops-harness/notes/sim-funds/readme.md) | md | 3,222 |  |

<a id="research"></a>

## Product and lifecycle research

Nine research packets with proposed field dictionaries, source registers, synthetic examples and code. They are reference material for selecting each build scope.

| Source file | Kind | Bytes | ZIP file entries |
| --- | --- | ---: | ---: |
| [research/credit/cds-research-packet.zip](../../../pr1/business/ops-harness/research/credit/cds-research-packet.zip) | zip | 127,000 | 31 |
| [research/credit/convertible-bonds-research-packet.zip](../../../pr1/business/ops-harness/research/credit/convertible-bonds-research-packet.zip) | zip | 215,391 | 37 |
| [research/credit/corporate-bonds-research-packet.zip](../../../pr1/business/ops-harness/research/credit/corporate-bonds-research-packet.zip) | zip | 182,635 | 37 |
| [research/equities/cash-equity-research-packet.zip](../../../pr1/business/ops-harness/research/equities/cash-equity-research-packet.zip) | zip | 31,540 | 16 |
| [research/equities/equity-swap-master-research-packet.zip](../../../pr1/business/ops-harness/research/equities/equity-swap-master-research-packet.zip) | zip | 64,274 | 17 |
| [research/foreign-exchange/fx-spot-forward-swap-research-packet.zip](../../../pr1/business/ops-harness/research/foreign-exchange/fx-spot-forward-swap-research-packet.zip) | zip | 90,268 | 24 |
| [research/loans/loans-research-packet.zip](../../../pr1/business/ops-harness/research/loans/loans-research-packet.zip) | zip | 212,462 | 33 |
| [research/options/listed-options-research-packet.zip](../../../pr1/business/ops-harness/research/options/listed-options-research-packet.zip) | zip | 74,729 | 21 |
| [research/volatility/variance-volatility-research-packet.zip](../../../pr1/business/ops-harness/research/volatility/variance-volatility-research-packet.zip) | zip | 108,541 | 30 |

<details>
<summary>research/credit/cds-research-packet.zip ? 31 file entries</summary>

Archive: [research/credit/cds-research-packet.zip](../../../pr1/business/ops-harness/research/credit/cds-research-packet.zip). Member sizes below are uncompressed bytes. Members inherit this archive's thematic group.

| Archive member | Bytes |
| --- | ---: |
| `packet/cds_csv_column_mapping.csv` | 8,143 |
| `packet/cds_example_engine.py` | 11,469 |
| `packet/cds_example_validation_results.json` | 4,363 |
| `packet/cds_field_dictionary.csv` | 138,496 |
| `packet/cds_field_dictionary.json` | 215,017 |
| `packet/cds_ice_link_crosswalk.csv` | 8,309 |
| `packet/cds_ice_link_crosswalk.json` | 13,871 |
| `packet/cds_model_mapping.csv` | 7,535 |
| `packet/cds_model_mapping.json` | 11,772 |
| `packet/cds_product_profiles.csv` | 1,179 |
| `packet/cds_research_report.md` | 24,658 |
| `packet/cds_source_register.csv` | 37,042 |
| `packet/cds_source_register.json` | 54,243 |
| `packet/cds_standards_notes.md` | 4,405 |
| `packet/file_manifest.json` | 4,750 |
| `packet/independent_fixture_review_results.json` | 20,308 |
| `packet/independent_review.md` | 9,085 |
| `packet/models_code_manifest.json` | 15,138 |
| `packet/models_fixture_assertions.json` | 7,905 |
| `packet/packet_summary.json` | 437 |
| `packet/README.md` | 1,305 |
| `packet/README_examples.md` | 13,884 |
| `packet/sim_funds_cds_trade_export.csv` | 10,075 |
| `packet/synthetic_cds_cash_instructions.csv` | 10,144 |
| `packet/synthetic_cds_correction_branches.csv` | 302 |
| `packet/synthetic_cds_credit_events.csv` | 1,927 |
| `packet/synthetic_cds_examples.json` | 81,859 |
| `packet/synthetic_cds_expected_results.json` | 1,601 |
| `packet/validate_cds_examples.py` | 12,038 |
| `working/build_examples.py` | 12,477 |
| `working/independent_fixture_review.py` | 17,275 |

</details>

<details>
<summary>research/credit/convertible-bonds-research-packet.zip ? 37 file entries</summary>

Archive: [research/credit/convertible-bonds-research-packet.zip](../../../pr1/business/ops-harness/research/credit/convertible-bonds-research-packet.zip). Member sizes below are uncompressed bytes. Members inherit this archive's thematic group.

| Archive member | Bytes |
| --- | ---: |
| `packet/build_examples.py` | 39,450 |
| `packet/contract_terms_research.md` | 13,595 |
| `packet/convention_review.md` | 8,853 |
| `packet/convertible_bond_conversions.csv` | 6,507 |
| `packet/convertible_bond_csv_column_mapping.csv` | 46,003 |
| `packet/convertible_bond_csv_column_mapping.json` | 76,008 |
| `packet/convertible_bond_csv_field_mapping.csv` | 26,056 |
| `packet/convertible_bond_csv_field_mapping.json` | 48,897 |
| `packet/convertible_bond_events.csv` | 801 |
| `packet/convertible_bond_example_sources.json` | 1,793 |
| `packet/convertible_bond_examples.json` | 91,263 |
| `packet/convertible_bond_field_dictionary.csv` | 128,271 |
| `packet/convertible_bond_field_dictionary.json` | 215,241 |
| `packet/convertible_bond_movements.csv` | 1,273 |
| `packet/convertible_bond_obligations.csv` | 3,866 |
| `packet/convertible_bond_rejected_records.csv` | 769 |
| `packet/convertible_bond_research_report.md` | 21,598 |
| `packet/convertible_bond_scenario_manifest.json` | 5,370 |
| `packet/convertible_bond_source_register.csv` | 33,149 |
| `packet/convertible_bond_source_register.json` | 45,131 |
| `packet/convertible_bond_standards_crosswalk.csv` | 9,749 |
| `packet/convertible_bond_standards_crosswalk.json` | 17,402 |
| `packet/convertible_bond_validation_results.json` | 9,432 |
| `packet/example_engine.py` | 14,189 |
| `packet/file_manifest.json` | 5,871 |
| `packet/independent_review.md` | 7,227 |
| `packet/independent_review.py` | 23,607 |
| `packet/independent_review_results.json` | 243,287 |
| `packet/operations_research.md` | 13,220 |
| `packet/packet_summary.json` | 263,868 |
| `packet/README.md` | 1,020 |
| `packet/README_examples.md` | 9,150 |
| `packet/review_dictionary_crosswalk.py` | 9,050 |
| `packet/sim_funds_convertible_bond_trade_export.csv` | 1,398 |
| `packet/source_code_manifest.json` | 6,695 |
| `packet/standards_implementation_notes.md` | 9,116 |
| `packet/validate_examples.py` | 9,080 |

</details>

<details>
<summary>research/credit/corporate-bonds-research-packet.zip ? 37 file entries</summary>

Archive: [research/credit/corporate-bonds-research-packet.zip](../../../pr1/business/ops-harness/research/credit/corporate-bonds-research-packet.zip). Member sizes below are uncompressed bytes. Members inherit this archive's thematic group.

| Archive member | Bytes |
| --- | ---: |
| `packet/build_examples.py` | 31,387 |
| `packet/cdm_fixture_inspection.json` | 1,325 |
| `packet/cdm_source_manifest.json` | 10,196 |
| `packet/convention_review.md` | 9,540 |
| `packet/corporate_bond_cash_obligations.csv` | 4,401 |
| `packet/corporate_bond_csv_column_mapping.csv` | 46,382 |
| `packet/corporate_bond_csv_column_mapping.json` | 78,905 |
| `packet/corporate_bond_csv_field_mapping.csv` | 27,460 |
| `packet/corporate_bond_csv_field_mapping.json` | 49,015 |
| `packet/corporate_bond_events.csv` | 1,803 |
| `packet/corporate_bond_example_sources.json` | 5,723 |
| `packet/corporate_bond_examples.json` | 62,375 |
| `packet/corporate_bond_field_dictionary.csv` | 69,629 |
| `packet/corporate_bond_field_dictionary.json` | 127,968 |
| `packet/corporate_bond_product_profiles.csv` | 1,331 |
| `packet/corporate_bond_rejected_bookings.csv` | 1,514 |
| `packet/corporate_bond_research_report.md` | 22,810 |
| `packet/corporate_bond_scenario_manifest.json` | 7,242 |
| `packet/corporate_bond_settlements.csv` | 892 |
| `packet/corporate_bond_source_register.csv` | 44,158 |
| `packet/corporate_bond_source_register.json` | 64,458 |
| `packet/corporate_bond_standards_crosswalk.csv` | 8,549 |
| `packet/corporate_bond_standards_crosswalk.json` | 15,056 |
| `packet/corporate_bond_validation_results.json` | 9,953 |
| `packet/example_engine.py` | 9,506 |
| `packet/file_manifest.json` | 5,845 |
| `packet/independent_review.md` | 6,954 |
| `packet/independent_review.py` | 16,250 |
| `packet/independent_review_results.json` | 271,050 |
| `packet/packet_summary.json` | 4,368 |
| `packet/quantlib_source_manifest.json` | 1,035 |
| `packet/README.md` | 952 |
| `packet/README_examples.md` | 8,371 |
| `packet/review_dictionary_crosswalk.py` | 7,792 |
| `packet/sim_funds_corporate_bond_trade_export.csv` | 6,548 |
| `packet/standards_implementation_notes.md` | 8,394 |
| `packet/validate_examples.py` | 10,899 |

</details>

<details>
<summary>research/equities/cash-equity-research-packet.zip ? 16 file entries</summary>

Archive: [research/equities/cash-equity-research-packet.zip](../../../pr1/business/ops-harness/research/equities/cash-equity-research-packet.zip). Member sizes below are uncompressed bytes. Members inherit this archive's thematic group.

| Archive member | Bytes |
| --- | ---: |
| `broker_correction_synthetic.csv` | 377 |
| `broker_fills_synthetic.csv` | 519 |
| `cash_equity_oms_to_pb_research.md` | 28,971 |
| `correction_workflow_synthetic.csv` | 552 |
| `exception_fidelity_underallocation.csv` | 298 |
| `fill_allocation_links.csv` | 253 |
| `oms_bookings_synthetic.csv` | 645 |
| `README.md` | 3,391 |
| `recipient_field_matrix.csv` | 13,798 |
| `recipient_field_matrix.json` | 25,361 |
| `reference_data_synthetic.json` | 1,398 |
| `SIMFUNDS_20261014_fidelity_inspired.csv` | 646 |
| `SIMFUNDS_20261014_ibkr_inspired.csv` | 483 |
| `source_register.csv` | 6,613 |
| `validate_packet.py` | 6,335 |
| `validation_results.json` | 2,085 |

</details>

<details>
<summary>research/equities/equity-swap-master-research-packet.zip ? 17 file entries</summary>

Archive: [research/equities/equity-swap-master-research-packet.zip](../../../pr1/business/ops-harness/research/equities/equity-swap-master-research-packet.zip). Member sizes below are uncompressed bytes. Members inherit this archive's thematic group.

| Archive member | Bytes |
| --- | ---: |
| `equity_swap_master/equity_swap_master_research.md` | 25,148 |
| `equity_swap_master/example_calendar_and_observations.json` | 1,343 |
| `equity_swap_master/example_cashflows.csv` | 561 |
| `equity_swap_master/example_cashflows.json` | 1,202 |
| `equity_swap_master/example_fund_assignments.json` | 885 |
| `equity_swap_master/example_master_profiles.json` | 17,208 |
| `equity_swap_master/example_resolved_trade.json` | 11,684 |
| `equity_swap_master/example_wrapper_instances.json` | 12,389 |
| `equity_swap_master/field_dictionary.csv` | 22,191 |
| `equity_swap_master/field_dictionary.json` | 38,952 |
| `equity_swap_master/model_mapping.csv` | 21,854 |
| `equity_swap_master/model_mapping.json` | 30,153 |
| `equity_swap_master/README.md` | 3,001 |
| `equity_swap_master/source_register.csv` | 22,091 |
| `equity_swap_master/source_register.json` | 30,480 |
| `equity_swap_master/validate_examples.py` | 21,565 |
| `equity_swap_master/validation_results.json` | 10,265 |

</details>

<details>
<summary>research/foreign-exchange/fx-spot-forward-swap-research-packet.zip ? 24 file entries</summary>

Archive: [research/foreign-exchange/fx-spot-forward-swap-research-packet.zip](../../../pr1/business/ops-harness/research/foreign-exchange/fx-spot-forward-swap-research-packet.zip). Member sizes below are uncompressed bytes. Members inherit this archive's thematic group.

| Archive member | Bytes |
| --- | ---: |
| `fx_research/artifact_manifest.json` | 3,436 |
| `fx_research/fx_example_engine.py` | 13,466 |
| `fx_research/fx_field_dictionary.csv` | 85,571 |
| `fx_research/fx_field_dictionary.json` | 132,610 |
| `fx_research/fx_model_code_manifest.json` | 4,428 |
| `fx_research/fx_model_mapping.csv` | 5,500 |
| `fx_research/fx_model_mapping.json` | 8,048 |
| `fx_research/fx_model_source_urls.json` | 5,160 |
| `fx_research/fx_product_matrix.csv` | 1,864 |
| `fx_research/fx_recipient_column_mapping.csv` | 3,193 |
| `fx_research/fx_source_register.csv` | 23,822 |
| `fx_research/fx_source_register.json` | 36,490 |
| `fx_research/fx_spot_forward_swap_research.md` | 27,197 |
| `fx_research/fx_standards_notes.md` | 4,262 |
| `fx_research/packet_summary.json` | 8,264 |
| `fx_research/README.md` | 1,062 |
| `fx_research/README_examples.md` | 9,729 |
| `fx_research/sim_funds_fx_trade_export.csv` | 3,559 |
| `fx_research/synthetic_fx_examples.json` | 48,134 |
| `fx_research/synthetic_fx_expected_results.json` | 1,500 |
| `fx_research/synthetic_fx_lifecycle_events.csv` | 1,030 |
| `fx_research/synthetic_fx_obligations.csv` | 5,860 |
| `fx_research/validate_examples.py` | 17,204 |
| `fx_research/validation_results.json` | 7,517 |

</details>

<details>
<summary>research/loans/loans-research-packet.zip ? 33 file entries</summary>

Archive: [research/loans/loans-research-packet.zip](../../../pr1/business/ops-harness/research/loans/loans-research-packet.zip). Member sizes below are uncompressed bytes. Members inherit this archive's thematic group.

| Archive member | Bytes |
| --- | ---: |
| `clearpar_loans/build_csvs.mjs` | 3,055 |
| `clearpar_loans/build_loan_examples.py` | 36,279 |
| `clearpar_loans/clearpar_loan_csv_column_mapping.csv` | 30,752 |
| `clearpar_loans/clearpar_loan_csv_column_mapping.json` | 50,099 |
| `clearpar_loans/clearpar_loan_field_dictionary.csv` | 75,013 |
| `clearpar_loans/clearpar_loan_field_dictionary.json` | 134,741 |
| `clearpar_loans/clearpar_loan_research_report.md` | 26,418 |
| `clearpar_loans/clearpar_loan_source_register.csv` | 27,744 |
| `clearpar_loans/clearpar_loan_source_register.json` | 38,264 |
| `clearpar_loans/clearpar_loan_standards_crosswalk.csv` | 10,305 |
| `clearpar_loans/clearpar_loan_standards_crosswalk.json` | 15,714 |
| `clearpar_loans/clearpar_platform_notes.md` | 11,995 |
| `clearpar_loans/csv_authoring_input.json` | 373,963 |
| `clearpar_loans/csv_authoring_verification.json` | 1,623 |
| `clearpar_loans/file_manifest.json` | 5,310 |
| `clearpar_loans/independent_review.py` | 21,124 |
| `clearpar_loans/loan_example_cash_components.csv` | 4,223 |
| `clearpar_loans/loan_example_cash_movements.csv` | 2,220 |
| `clearpar_loans/loan_example_contracts.csv` | 3,210 |
| `clearpar_loans/loan_example_events.csv` | 2,428 |
| `clearpar_loans/loan_example_rejections.csv` | 1,566 |
| `clearpar_loans/loan_example_settlements.csv` | 3,702 |
| `clearpar_loans/loan_example_trades.csv` | 6,887 |
| `clearpar_loans/loan_example_verification.json` | 8,922 |
| `clearpar_loans/loan_examples.json` | 95,325 |
| `clearpar_loans/loan_independent_review.json` | 394,447 |
| `clearpar_loans/loan_lifecycle_notes.md` | 15,584 |
| `clearpar_loans/loan_model_design.md` | 8,947 |
| `clearpar_loans/loan_settlement_conventions.md` | 13,633 |
| `clearpar_loans/README.md` | 7,498 |
| `clearpar_loans/README_examples.md` | 10,854 |
| `clearpar_loans/scenario_manifest.json` | 35,877 |
| `clearpar_loans/validation_summary.json` | 7,075 |

</details>

<details>
<summary>research/options/listed-options-research-packet.zip ? 21 file entries</summary>

Archive: [research/options/listed-options-research-packet.zip](../../../pr1/business/ops-harness/research/options/listed-options-research-packet.zip). Member sizes below are uncompressed bytes. Members inherit this archive's thematic group.

| Archive member | Bytes |
| --- | ---: |
| `listed_options/example_allocation_export.csv` | 1,255 |
| `listed_options/example_allocation_export.json` | 3,290 |
| `listed_options/example_instruments.json` | 6,840 |
| `listed_options/example_lifecycle_events.json` | 2,162 |
| `listed_options/example_rules_observations.json` | 2,678 |
| `listed_options/example_settlement_obligations.csv` | 1,607 |
| `listed_options/example_settlement_obligations.json` | 5,410 |
| `listed_options/example_trades.json` | 3,126 |
| `listed_options/listed_options_field_dictionary.csv` | 19,869 |
| `listed_options/listed_options_field_dictionary.json` | 34,052 |
| `listed_options/listed_options_model_mapping.csv` | 9,823 |
| `listed_options/listed_options_model_mapping.json` | 15,549 |
| `listed_options/listed_options_product_matrix.csv` | 5,856 |
| `listed_options/listed_options_product_matrix.json` | 9,888 |
| `listed_options/listed_options_research.md` | 26,728 |
| `listed_options/listed_options_sources.csv` | 36,990 |
| `listed_options/listed_options_sources.json` | 51,741 |
| `listed_options/README.md` | 3,279 |
| `listed_options/scenario_expectations.json` | 856 |
| `listed_options/validate_examples.py` | 18,798 |
| `listed_options/validation_results.json` | 3,133 |

</details>

<details>
<summary>research/volatility/variance-volatility-research-packet.zip ? 30 file entries</summary>

Archive: [research/volatility/variance-volatility-research-packet.zip](../../../pr1/business/ops-harness/research/volatility/variance-volatility-research-packet.zip). Member sizes below are uncompressed bytes. Members inherit this archive's thematic group.

| Archive member | Bytes |
| --- | ---: |
| `packet/file_manifest.json` | 4,846 |
| `packet/independent_fixture_review_results.json` | 3,724 |
| `packet/independent_review.md` | 6,450 |
| `packet/models_code_manifest.json` | 25,632 |
| `packet/models_fixture_assertions.json` | 3,327 |
| `packet/packet_summary.json` | 298 |
| `packet/README.md` | 1,054 |
| `packet/README_examples.md` | 7,240 |
| `packet/sim_funds_variance_volatility_trade_export.csv` | 7,076 |
| `packet/synthetic_variance_volatility_cash_instructions.csv` | 1,799 |
| `packet/synthetic_variance_volatility_examples.json` | 59,912 |
| `packet/synthetic_variance_volatility_expected_results.json` | 677 |
| `packet/synthetic_variance_volatility_lifecycle_events.csv` | 508 |
| `packet/synthetic_variance_volatility_observations.csv` | 5,978 |
| `packet/validate_examples.py` | 8,211 |
| `packet/validation_results.json` | 5,964 |
| `packet/variance_volatility_contract_notes.md` | 13,275 |
| `packet/variance_volatility_csv_column_mapping.csv` | 5,078 |
| `packet/variance_volatility_example_engine.py` | 7,672 |
| `packet/variance_volatility_field_dictionary.csv` | 89,690 |
| `packet/variance_volatility_field_dictionary.json` | 144,887 |
| `packet/variance_volatility_model_mapping.csv` | 12,584 |
| `packet/variance_volatility_model_mapping.json` | 18,757 |
| `packet/variance_volatility_operations_notes.md` | 14,966 |
| `packet/variance_volatility_research_report.md` | 23,888 |
| `packet/variance_volatility_source_register.csv` | 26,399 |
| `packet/variance_volatility_source_register.json` | 37,778 |
| `packet/variance_volatility_standards_notes.md` | 10,388 |
| `working/build_examples.py` | 9,384 |
| `working/independent_fixture_review.py` | 7,192 |

</details>

<a id="interfaces"></a>

## Trade-file evidence and source copies

Published interface examples, retained source pages and PDFs, provenance records, and a duplicate ZIP snapshot. Examples are not proof of live recipient compatibility.

| Source file | Kind | Bytes | ZIP file entries |
| --- | --- | ---: | ---: |
| [research/2026-11-11_trade-file-sources.zip](../../../pr1/business/ops-harness/research/2026-11-11_trade-file-sources.zip) | zip | 15,149,881 | 19 |
| [research/trade-file-sources/allvue-bny-trade-acknowledgements.html](../../../pr1/business/ops-harness/research/trade-file-sources/allvue-bny-trade-acknowledgements.html) | html | 8,569 |  |
| [research/trade-file-sources/allvue-bny-trade-acknowledgements.pdf](../../../pr1/business/ops-harness/research/trade-file-sources/allvue-bny-trade-acknowledgements.pdf) | pdf | 68,616 |  |
| [research/trade-file-sources/allvue-bny-trade-reconciliation.html](../../../pr1/business/ops-harness/research/trade-file-sources/allvue-bny-trade-reconciliation.html) | html | 15,910 |  |
| [research/trade-file-sources/allvue-bny-trade-reconciliation.pdf](../../../pr1/business/ops-harness/research/trade-file-sources/allvue-bny-trade-reconciliation.pdf) | pdf | 71,174 |  |
| [research/trade-file-sources/allvue-goldman-sachs-trade-export.html](../../../pr1/business/ops-harness/research/trade-file-sources/allvue-goldman-sachs-trade-export.html) | html | 41,829 |  |
| [research/trade-file-sources/allvue-goldman-sachs-trade-export.pdf](../../../pr1/business/ops-harness/research/trade-file-sources/allvue-goldman-sachs-trade-export.pdf) | pdf | 133,473 |  |
| [research/trade-file-sources/checksums.sha256](../../../pr1/business/ops-harness/research/trade-file-sources/checksums.sha256) | sha256 | 1,848 |  |
| [research/trade-file-sources/ibkr-prime-trade-upload.html](../../../pr1/business/ops-harness/research/trade-file-sources/ibkr-prime-trade-upload.html) | html | 351,433 |  |
| [research/trade-file-sources/ibkr-prime-trade-upload.pdf](../../../pr1/business/ops-harness/research/trade-file-sources/ibkr-prime-trade-upload.pdf) | pdf | 323,183 |  |
| [research/trade-file-sources/index.html](../../../pr1/business/ops-harness/research/trade-file-sources/index.html) | html | 4,473 |  |
| [research/trade-file-sources/originals/allvue-bny-trade-acknowledgements.html](../../../pr1/business/ops-harness/research/trade-file-sources/originals/allvue-bny-trade-acknowledgements.html) | html | 1,698,416 |  |
| [research/trade-file-sources/originals/allvue-bny-trade-reconciliation.html](../../../pr1/business/ops-harness/research/trade-file-sources/originals/allvue-bny-trade-reconciliation.html) | html | 1,733,730 |  |
| [research/trade-file-sources/originals/allvue-goldman-sachs-trade-export.html](../../../pr1/business/ops-harness/research/trade-file-sources/originals/allvue-goldman-sachs-trade-export.html) | html | 1,788,346 |  |
| [research/trade-file-sources/originals/anson-funds-court-filing-t14.pdf](../../../pr1/business/ops-harness/research/trade-file-sources/originals/anson-funds-court-filing-t14.pdf) | pdf | 13,644,560 |  |
| [research/trade-file-sources/originals/greenlight-capital-v-fishback.pdf](../../../pr1/business/ops-harness/research/trade-file-sources/originals/greenlight-capital-v-fishback.pdf) | pdf | 361,912 |  |
| [research/trade-file-sources/originals/ibkr-prime-trade-upload.html](../../../pr1/business/ops-harness/research/trade-file-sources/originals/ibkr-prime-trade-upload.html) | html | 49,043 |  |
| [research/trade-file-sources/originals/ibkr-sample-trade-file.csv](../../../pr1/business/ops-harness/research/trade-file-sources/originals/ibkr-sample-trade-file.csv) | csv | 1,659 |  |
| [research/trade-file-sources/source-manifest.json](../../../pr1/business/ops-harness/research/trade-file-sources/source-manifest.json) | json | 7,435 |  |
| [research/trade-file-sources/verification.json](../../../pr1/business/ops-harness/research/trade-file-sources/verification.json) | json | 762 |  |

<details>
<summary>research/2026-11-11_trade-file-sources.zip ? 19 file entries</summary>

Archive: [research/2026-11-11_trade-file-sources.zip](../../../pr1/business/ops-harness/research/2026-11-11_trade-file-sources.zip). Member sizes below are uncompressed bytes. Members inherit this archive's thematic group.

| Archive member | Bytes |
| --- | ---: |
| `trade-file-sources/allvue-bny-trade-acknowledgements.html` | 8,569 |
| `trade-file-sources/allvue-bny-trade-acknowledgements.pdf` | 68,616 |
| `trade-file-sources/allvue-bny-trade-reconciliation.html` | 15,910 |
| `trade-file-sources/allvue-bny-trade-reconciliation.pdf` | 71,174 |
| `trade-file-sources/allvue-goldman-sachs-trade-export.html` | 41,829 |
| `trade-file-sources/allvue-goldman-sachs-trade-export.pdf` | 133,473 |
| `trade-file-sources/checksums.sha256` | 1,848 |
| `trade-file-sources/ibkr-prime-trade-upload.html` | 351,433 |
| `trade-file-sources/ibkr-prime-trade-upload.pdf` | 323,183 |
| `trade-file-sources/index.html` | 4,473 |
| `trade-file-sources/originals/allvue-bny-trade-acknowledgements.html` | 1,698,416 |
| `trade-file-sources/originals/allvue-bny-trade-reconciliation.html` | 1,733,730 |
| `trade-file-sources/originals/allvue-goldman-sachs-trade-export.html` | 1,788,346 |
| `trade-file-sources/originals/anson-funds-court-filing-t14.pdf` | 13,644,560 |
| `trade-file-sources/originals/greenlight-capital-v-fishback.pdf` | 361,912 |
| `trade-file-sources/originals/ibkr-prime-trade-upload.html` | 49,043 |
| `trade-file-sources/originals/ibkr-sample-trade-file.csv` | 1,659 |
| `trade-file-sources/source-manifest.json` | 7,435 |
| `trade-file-sources/verification.json` | 762 |

</details>

<a id="infrastructure"></a>

## Infrastructure and workspaces

Workstation, hosting and workspace plans and a preview. Dated plans must be reconciled with current infrastructure before implementation.

| Source file | Kind | Bytes | ZIP file entries |
| --- | --- | ---: | ---: |
| [notes/infrastructure/2026-10-19_infrastructure-implementation-plan-page-snapshot.md](../../../pr1/business/ops-harness/notes/infrastructure/2026-10-19_infrastructure-implementation-plan-page-snapshot.md) | md | 41,756 |  |
| [notes/infrastructure/assets/ops-workspace-preview.html](../../../pr1/business/ops-harness/notes/infrastructure/assets/ops-workspace-preview.html) | html | 9,239 |  |
| [Ops harness infrastructure setup and implementation plan.md](../../../pr1/business/ops-harness/Ops%20harness%20infrastructure%20setup%20and%20implementation%20plan.md) | md | 46,102 |  |
| [spec-linux-workstation_v02.md](../../../pr1/business/ops-harness/spec-linux-workstation_v02.md) | md | 12,860 |  |

<a id="history"></a>

## Earlier designs and archived context

The legacy research wiki, September workplace harness scaffold, early structure and AI notes, competitive background and explicitly archived ideas.

| Source file | Kind | Bytes | ZIP file entries |
| --- | --- | ---: | ---: |
| [2026-09-29_ops-harness-source-index.html](../../../pr1/business/ops-harness/2026-09-29_ops-harness-source-index.html) | html | 5,975 |  |
| [archive-ops-harness-research-1-id-582126d6.zip](../../../pr1/business/ops-harness/archive-ops-harness-research-1-id-582126d6.zip) | zip | 43,093 | 33 |
| [hedge-fund-operations-wiki-repository.png](../../../pr1/business/ops-harness/hedge-fund-operations-wiki-repository.png) | png | 106,616 |  |
| [notes/2023_financial-software-competitive-landscape_last-modified.docx](../../../pr1/business/ops-harness/notes/2023_financial-software-competitive-landscape_last-modified.docx) | docx | 16,701 |  |
| [notes/2026_ai-notes_last-modified.txt](../../../pr1/business/ops-harness/notes/2026_ai-notes_last-modified.txt) | txt | 1,877 |  |
| [notes/2026_archived-skill-lines-1-id-f2f7d4b9_last-modified.md](../../../pr1/business/ops-harness/notes/2026_archived-skill-lines-1-id-f2f7d4b9_last-modified.md) | md | 633 |  |
| [notes/2026_ops-harness-high-level-structure_last-modified.docx](../../../pr1/business/ops-harness/notes/2026_ops-harness-high-level-structure_last-modified.docx) | docx | 13,000 |  |
| [notes/archived/2026-10-30_agent-consulting-business.md](../../../pr1/business/ops-harness/notes/archived/2026-10-30_agent-consulting-business.md) | md | 1,325 |  |
| [notes/archived/2026-10-30_agent-product-ideas.md](../../../pr1/business/ops-harness/notes/archived/2026-10-30_agent-product-ideas.md) | md | 977 |  |
| [notes/archived/2026-10-30_agent-team-design.md](../../../pr1/business/ops-harness/notes/archived/2026-10-30_agent-team-design.md) | md | 2,293 |  |
| [notes/archived/2026-10-30_reidy-systems-ideas.md](../../../pr1/business/ops-harness/notes/archived/2026-10-30_reidy-systems-ideas.md) | md | 1,297 |  |
| [ops-harness-v2-id-d574f41c.zip](../../../pr1/business/ops-harness/ops-harness-v2-id-d574f41c.zip) | zip | 146,328 | 133 |

<details>
<summary>archive-ops-harness-research-1-id-582126d6.zip ? 33 file entries</summary>

Archive: [archive-ops-harness-research-1-id-582126d6.zip](../../../pr1/business/ops-harness/archive-ops-harness-research-1-id-582126d6.zip). Member sizes below are uncompressed bytes. Members inherit this archive's thematic group.

| Archive member | Bytes |
| --- | ---: |
| `wiki/analyses/platform-comparison.md` | 3,592 |
| `wiki/analyses/t1-impact-analysis.md` | 3,380 |
| `wiki/concepts/ai-post-trade.md` | 2,057 |
| `wiki/concepts/form-pf-reporting.md` | 2,469 |
| `wiki/concepts/hedge-fund-coo-role.md` | 2,635 |
| `wiki/concepts/isda-master-agreement.md` | 3,180 |
| `wiki/concepts/nav-calculation.md` | 2,986 |
| `wiki/concepts/oms-ems-landscape.md` | 3,270 |
| `wiki/concepts/prime-brokerage.md` | 3,505 |
| `wiki/concepts/reconciliation.md` | 2,643 |
| `wiki/concepts/shadow-accounting.md` | 2,431 |
| `wiki/concepts/straight-through-processing.md` | 2,054 |
| `wiki/concepts/t-plus-1-settlement.md` | 2,934 |
| `wiki/concepts/trade-lifecycle.md` | 2,975 |
| `wiki/entities/arcesium.md` | 3,588 |
| `wiki/entities/bloomberg-aim.md` | 1,322 |
| `wiki/entities/charles-river-ims.md` | 1,981 |
| `wiki/entities/dtcc.md` | 2,653 |
| `wiki/entities/enfusion.md` | 2,550 |
| `wiki/entities/flextrade.md` | 1,274 |
| `wiki/entities/isda.md` | 1,620 |
| `wiki/entities/orchestrade.md` | 1,281 |
| `wiki/entities/sec.md` | 1,288 |
| `wiki/entities/ssc-technologies.md` | 2,496 |
| `wiki/index.md` | 7,757 |
| `wiki/log.md` | 3,041 |
| `wiki/sources/arcesium-post-trade-ai.md` | 1,328 |
| `wiki/sources/bis-prime-broker-nexus.md` | 1,281 |
| `wiki/sources/dtcc-t1-functional-changes.md` | 1,119 |
| `wiki/sources/investopedia-isda.md` | 1,102 |
| `wiki/sources/investopedia-prime-broker.md` | 1,318 |
| `wiki/sources/limina-nav-reconciliation.md` | 1,264 |
| `wiki/sources/sec-form-pf-amendments.md` | 1,193 |

</details>

<details>
<summary>ops-harness-v2-id-d574f41c.zip ? 133 file entries</summary>

Archive: [ops-harness-v2-id-d574f41c.zip](../../../pr1/business/ops-harness/ops-harness-v2-id-d574f41c.zip). Member sizes below are uncompressed bytes. Members inherit this archive's thematic group.

| Archive member | Bytes |
| --- | ---: |
| `ops-harness-v2/.gitignore` | 572 |
| `ops-harness-v2/adapters/hermes/README.md` | 1,301 |
| `ops-harness-v2/adapters/hermes/restricted-memory.fragment.yaml` | 167 |
| `ops-harness-v2/adapters/opencode/opencode.project.example.json` | 2,830 |
| `ops-harness-v2/adapters/opencode/README.md` | 1,614 |
| `ops-harness-v2/adapters/README.md` | 592 |
| `ops-harness-v2/AGENTS.md` | 3,243 |
| `ops-harness-v2/agents/business-action-executor.md` | 1,657 |
| `ops-harness-v2/agents/code-analyzer.md` | 1,524 |
| `ops-harness-v2/agents/code-executor.md` | 1,564 |
| `ops-harness-v2/agents/code-locator.md` | 1,443 |
| `ops-harness-v2/agents/data-explorer.md` | 1,616 |
| `ops-harness-v2/agents/executor.md` | 442 |
| `ops-harness-v2/agents/investigator.md` | 1,572 |
| `ops-harness-v2/agents/orchestrator.md` | 1,565 |
| `ops-harness-v2/agents/README.md` | 486 |
| `ops-harness-v2/agents/reviewer.md` | 1,559 |
| `ops-harness-v2/CHANGELOG.md` | 2,129 |
| `ops-harness-v2/config/context-routing.yaml` | 940 |
| `ops-harness-v2/config/model-routing.yaml` | 522 |
| `ops-harness-v2/config/README.md` | 296 |
| `ops-harness-v2/data/catalog/corporate_action_entitlements.yaml` | 842 |
| `ops-harness-v2/data/catalog/corporate_actions.yaml` | 792 |
| `ops-harness-v2/data/catalog/instrument_mappings.yaml` | 795 |
| `ops-harness-v2/data/catalog/operational_state.yaml` | 761 |
| `ops-harness-v2/data/catalog/positions.yaml` | 809 |
| `ops-harness-v2/data/catalog/README.md` | 463 |
| `ops-harness-v2/data/catalog/reconciliation_results.yaml` | 775 |
| `ops-harness-v2/data/catalog/reference_overrides.yaml` | 796 |
| `ops-harness-v2/data/catalog/security_master.yaml` | 779 |
| `ops-harness-v2/data/catalog/trades.yaml` | 782 |
| `ops-harness-v2/data/curated/README.md` | 288 |
| `ops-harness-v2/data/normalized/README.md` | 302 |
| `ops-harness-v2/data/raw/README.md` | 287 |
| `ops-harness-v2/data/README.md` | 741 |
| `ops-harness-v2/docs/AGENT_DESIGN.md` | 4,166 |
| `ops-harness-v2/docs/ARCHITECTURE.md` | 6,557 |
| `ops-harness-v2/docs/BUILD_PLAN.md` | 7,480 |
| `ops-harness-v2/docs/CONTEXT_PRINCIPLES.md` | 6,227 |
| `ops-harness-v2/docs/CORRECTIONS_AND_CAVEATS.md` | 5,588 |
| `ops-harness-v2/docs/DATA_ARCHITECTURE.md` | 10,482 |
| `ops-harness-v2/docs/DECISIONS.md` | 2,573 |
| `ops-harness-v2/docs/EVAL_STRATEGY.md` | 5,590 |
| `ops-harness-v2/docs/EXECUTIVE_SUMMARY.md` | 7,396 |
| `ops-harness-v2/docs/EXTERNAL_SOURCES.md` | 3,771 |
| `ops-harness-v2/docs/FIRST_BUILD_BRIEF.md` | 1,996 |
| `ops-harness-v2/docs/IMPLEMENTATION_STATUS.md` | 2,104 |
| `ops-harness-v2/docs/MASTER_CONTEXT.md` | 19,879 |
| `ops-harness-v2/docs/MODEL_STRATEGY.md` | 2,921 |
| `ops-harness-v2/docs/OPEN_QUESTIONS.md` | 2,001 |
| `ops-harness-v2/docs/OPENCODE_HERMES_STRATEGY.md` | 4,530 |
| `ops-harness-v2/docs/PROJECT_TREE.md` | 6,274 |
| `ops-harness-v2/docs/provenance/original-archive-manifest.json` | 8,889 |
| `ops-harness-v2/docs/SESSION_CONTEXT.md` | 642 |
| `ops-harness-v2/docs/SOURCE_COVERAGE.md` | 6,603 |
| `ops-harness-v2/docs/TOOL_CONTRACTS.md` | 3,996 |
| `ops-harness-v2/docs/VALIDATION_REPORT.md` | 3,369 |
| `ops-harness-v2/docs/WORKFLOW_RELIABILITY.md` | 5,856 |
| `ops-harness-v2/evals/break-investigation/README.md` | 249 |
| `ops-harness-v2/evals/cases/e001.yaml` | 756 |
| `ops-harness-v2/evals/cases/e002.yaml` | 619 |
| `ops-harness-v2/evals/cases/e003.yaml` | 618 |
| `ops-harness-v2/evals/cases/e004.yaml` | 631 |
| `ops-harness-v2/evals/cases/e005.yaml` | 666 |
| `ops-harness-v2/evals/cases/e006.yaml` | 702 |
| `ops-harness-v2/evals/cases/e007.yaml` | 685 |
| `ops-harness-v2/evals/cases/e008.yaml` | 712 |
| `ops-harness-v2/evals/cases/e009.yaml` | 624 |
| `ops-harness-v2/evals/cases/e010.yaml` | 724 |
| `ops-harness-v2/evals/cases/e011.yaml` | 636 |
| `ops-harness-v2/evals/cases/e012.yaml` | 697 |
| `ops-harness-v2/evals/README.md` | 658 |
| `ops-harness-v2/evals/reconciliation/README.md` | 239 |
| `ops-harness-v2/evals/settlements/README.md` | 243 |
| `ops-harness-v2/fixtures/README.md` | 674 |
| `ops-harness-v2/fixtures/synthetic/agent-result.json` | 558 |
| `ops-harness-v2/fixtures/synthetic/context-packet.json` | 1,657 |
| `ops-harness-v2/fixtures/synthetic/position-comparison.json` | 353 |
| `ops-harness-v2/fixtures/synthetic/reference-change-proposal.json` | 605 |
| `ops-harness-v2/knowledge/corporate_actions/README.md` | 503 |
| `ops-harness-v2/knowledge/instruments/README.md` | 549 |
| `ops-harness-v2/knowledge/prime_brokers/README.md` | 493 |
| `ops-harness-v2/knowledge/README.md` | 447 |
| `ops-harness-v2/knowledge/reconciliations/README.md` | 487 |
| `ops-harness-v2/knowledge/settlement/README.md` | 488 |
| `ops-harness-v2/MANIFEST.json` | 21,665 |
| `ops-harness-v2/policies/approvals.md` | 1,366 |
| `ops-harness-v2/policies/context-governance.md` | 978 |
| `ops-harness-v2/policies/data-access.md` | 1,025 |
| `ops-harness-v2/policies/escalation.md` | 1,051 |
| `ops-harness-v2/policies/README.md` | 349 |
| `ops-harness-v2/policies/reference-data.md` | 1,012 |
| `ops-harness-v2/policies/release-control.md` | 858 |
| `ops-harness-v2/policies/settlement-risk.md` | 1,123 |
| `ops-harness-v2/policies/trade-booking.md` | 1,063 |
| `ops-harness-v2/README.md` | 5,131 |
| `ops-harness-v2/requirements-dev.txt` | 145 |
| `ops-harness-v2/runbooks/auth-and-quota.md` | 1,649 |
| `ops-harness-v2/runbooks/connector-onboarding.md` | 1,333 |
| `ops-harness-v2/runbooks/incident-recovery.md` | 1,568 |
| `ops-harness-v2/runbooks/README.md` | 239 |
| `ops-harness-v2/runbooks/reference-data-maintenance.md` | 1,243 |
| `ops-harness-v2/schemas/agent-result.schema.json` | 1,865 |
| `ops-harness-v2/schemas/context-packet.schema.json` | 3,511 |
| `ops-harness-v2/schemas/dataset-catalog.schema.json` | 2,395 |
| `ops-harness-v2/schemas/eval-case.schema.json` | 1,464 |
| `ops-harness-v2/schemas/evidence.schema.json` | 1,071 |
| `ops-harness-v2/schemas/README.md` | 842 |
| `ops-harness-v2/schemas/reference-change-proposal.schema.json` | 1,673 |
| `ops-harness-v2/skills/build-reconciliation/SKILL.md` | 1,974 |
| `ops-harness-v2/skills/capture-operational-knowledge/SKILL.md` | 1,874 |
| `ops-harness-v2/skills/draft-ops-email/SKILL.md` | 1,834 |
| `ops-harness-v2/skills/investigate-break/SKILL.md` | 2,072 |
| `ops-harness-v2/skills/maintain-reference-data/SKILL.md` | 1,877 |
| `ops-harness-v2/skills/normalize-pb-data/SKILL.md` | 2,021 |
| `ops-harness-v2/skills/README.md` | 696 |
| `ops-harness-v2/skills/scrub-corporate-actions/SKILL.md` | 1,863 |
| `ops-harness-v2/skills/settle-equity-swap/SKILL.md` | 1,987 |
| `ops-harness-v2/skills/validate-pnl/SKILL.md` | 1,820 |
| `ops-harness-v2/src/README.md` | 1,340 |
| `ops-harness-v2/templates/asset-inventory.yaml` | 407 |
| `ops-harness-v2/templates/decision-record.md` | 624 |
| `ops-harness-v2/templates/knowledge-item.md` | 899 |
| `ops-harness-v2/templates/README.md` | 280 |
| `ops-harness-v2/templates/run-manifest.yaml` | 506 |
| `ops-harness-v2/tests/README.md` | 993 |
| `ops-harness-v2/tests/test_project.py` | 5,614 |
| `ops-harness-v2/tools/README.md` | 1,385 |
| `ops-harness-v2/tools/validate_project.py` | 10,374 |
| `ops-harness-v2/workflows/broker-reconciliation.yaml` | 1,346 |
| `ops-harness-v2/workflows/corporate-action-scrub.yaml` | 476 |
| `ops-harness-v2/workflows/README.md` | 491 |
| `ops-harness-v2/workflows/reference-data-change.yaml` | 459 |

</details>

<a id="administration"></a>

## Business administration

Formation, identification and recordkeeping files. The catalog lists filenames and metadata only; private values and document contents are not reproduced.

| Source file | Kind | Bytes | ZIP file entries |
| --- | --- | ---: | ---: |
| [ein.txt](../../../pr1/business/ops-harness/ein.txt) | txt | 16 |  |
| [notes/administration/2026-10-05_sole-proprietorship-business-plan.docx](../../../pr1/business/ops-harness/notes/administration/2026-10-05_sole-proprietorship-business-plan.docx) | docx | 38,289 |  |
| [notes/administration/2026-10-05_sole-proprietorship-setup-checklist.docx](../../../pr1/business/ops-harness/notes/administration/2026-10-05_sole-proprietorship-setup-checklist.docx) | docx | 43,051 |  |
| [notes/administration/2026-10-16_sole-proprietor-records.xlsx](../../../pr1/business/ops-harness/notes/administration/2026-10-16_sole-proprietor-records.xlsx) | xlsx | 95,404 |  |
| [ny-llc-2026-action-playbook.docx](../../../pr1/business/ops-harness/ny-llc-2026-action-playbook.docx) | docx | 67,167 |  |

## Using this catalog

Begin with project direction and architecture, then the copied funds handoff. Open product research only for the selected workflow. Use interface evidence to establish what a source actually documents, and keep historical designs and business administration separate from the current build instructions.

A timestamp, a detailed field dictionary, a passing fixture receipt or placement outside an archive does not by itself make a document current. Record adopted decisions in the starting-point notes and link back to these sources. Source files were not moved, rewritten or deleted.
