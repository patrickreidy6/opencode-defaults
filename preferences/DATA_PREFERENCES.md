# Preferred Data Structure and Tools

## Default approach

Use **S3 for storage, Parquet for processed data, Polars for processing, and DuckDB for analytical queries**. Add Delta Lake when table management and transactional guarantees are needed.

```text
Incoming CSV files
    -> S3 raw storage
    -> Polars: validate, clean, and transform
    -> S3 processed storage: Parquet or Delta tables
    -> DuckDB: SQL queries and analysis
```

## Preferences

- **S3:** Store original files and processed datasets in the data lake.
- **CSV:** Keep received files in a raw area for traceability and reprocessing.
- **Parquet:** Prefer this format for processed analytical data.
- **Polars over pandas:** Prefer Polars for ingestion, cleaning, and transformations.
- **DuckDB:** Use for SQL analysis directly over files or Delta tables in S3.
- **Delta Lake:** Use when updates/deletes, consistent table snapshots during writes, or version history justify the additional management.

## Suggested layout

```text
s3://my-data-lake/
    raw/
        sales/                  # Original CSV files
    processed/
        sales/                  # Plain Parquet dataset OR a Delta table
            part-001.parquet
            part-002.parquet
            _delta_log/         # Present only for a Delta table
```

## When to use Delta Lake

Start with plain Parquet for simple append-only analytical datasets. DuckDB can query CSV and Parquet directly; Delta Lake is optional.

A Delta table consists of Parquet data files plus a transaction log maintained by Delta-compatible software. Create and update it with a library such as Python's `deltalake`; Spark or Databricks is not required for a basic pipeline.

Query Delta tables through DuckDB's `delta_scan`, rather than reading all their Parquet files directly. The transaction log identifies the current table contents; older files may still exist.

Delta Lake handles table transactions, not data cleaning or automatic deduplication. The ingestion pipeline still needs to track processed files, handle retries without duplicate ingestion, and manage schema changes. Version history is available only while the required logs and data files are retained.
