---
name: data-preferences
description: Use when choosing analytical storage locations, file formats, query engines, or data pipeline tools for a new workflow. Existing project storage and architecture take precedence.
---

# Data Preferences

Apply these defaults when designing new data storage or analytical pipelines. Do not migrate an existing project's storage solely to match these preferences.

## Storage Location Priority
1. **Local filesystem / NAS first (default):** Prefer local workspace storage and NAS-backed paths by default.
2. **Cloud storage when needed — Google Drive:** cloud storage, off-site sync, or cloud object storage is needed, prefer **Google Cloud / Google Drive** (linked with `patrickreidy6@gmail.com`)

## Processing & Query Stack
Use **preserved raw CSVs, Parquet for processed data, Polars for transformations, and DuckDB for SQL analytics**. Add Pydantic for structured input/contract validation where helpful, and Delta Lake only when transactional table guarantees justify it.

```text
Incoming raw files (CSV / JSON)
    -> raw/ (preserved unmodified for traceability and reprocessing)
    -> Polars: validate, clean, and transform
    -> processed/: Parquet dataset (or Delta table when needed)
    -> DuckDB: SQL queries and analysis directly over files
```

## Core Choices
- **Raw layer:** Retain original incoming CSV/source files unmodified so pipelines can be re-run deterministically.
- **Parquet:** Default format for processed analytical datasets.
- **Polars over pandas:** Prefer Polars for ingestion, cleaning, and tabular transformations.
- **DuckDB:** Run analytical SQL directly over local/NAS Parquet and CSV files without standing up a separate database server; SQLite is fine for small transactional local ledgers.
- **Delta Lake (optional):** Start with plain Parquet for append-only or batch-replaced datasets. Add Python `deltalake` (no Spark/Databricks required) only when concurrent snapshot isolation, row-level updates/deletes, or table version history are genuinely needed—and query via DuckDB's `delta_scan` rather than globbing raw Parquet files.
