# Week 2: Parquet, Spark & Table Metadata

## Goals

- Learn Parquet internals and Iceberg metadata
- Configure Spark with Iceberg catalog support
- Create and query Iceberg tables
- Inspect snapshots, history, and metadata tables

## Topics

- Parquet row groups, column chunks, and statistics
- Iceberg REST catalog and Spark integration
- CREATE TABLE, writeTo, and schema evolution
- Time travel and snapshot inspection

## Prerequisites

- Week 1 stack up (`podman-compose up -d` from `lakehouse/`), `concepts/09`–`11` read.
- Hiver Phase 2 context: you are replacing the synthetic trades with a 1-brand tweet subset.

## Expected artifact

- Iceberg tables in `s3a://warehouse/` (Bronze tweet subset, Silver threads, Gold
  threads + `eval_pool`), queried via Spark — **not** bare Parquet files in a bucket.

## How to run

```bash
podman-compose exec spark python /home/.../<your ingest script>
```

## Definition of done

- [ ] 1-brand subset landed in Iceberg `s3a://bronze/tweets/`
- [ ] Silver thread table queryable (dedup, language-filter, thread reconstruction)
- [ ] Gold `threads` / `intent_candidates` / `eval_pool` queryable
- [ ] `% dropped + why` documented in `journey/02-lakehouse-ingest.md`

## Common mistakes

- **Bare Parquet ≠ lakehouse.** Without the Iceberg catalog you have a data lake — the
  metadata catalog is the point of this week.
- **Keeping raw payload columns into Silver.** Silver drops the raw payload and keeps
  validated, deduped, typed columns.
