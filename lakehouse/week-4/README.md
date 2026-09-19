# Week 4: Orchestration, Querying & Operations

## Goals

- Orchestrate lakehouse workflows with Airflow
- Query Iceberg tables with Trino
- Build maintenance and compaction pipelines
- Monitor DAGs and data pipeline health

## Topics

- Airflow DAG design and scheduling
- Task retries, alerts, and SLA checks
- Trino catalog setup for Iceberg
- Compaction, snapshot expiration, and orphan file cleanup

## Prerequisites

- Week 3 done (a stable, streaming-ready Iceberg table to orchestrate).
- No Airflow experience needed — the DAG is small (ingest → silver → gold → eval).

## Expected artifact

- An Airflow DAG (or `make pipeline`) that runs the ingest→silver→gold→eval chain on demand,
  plus Trino queries over the Iceberg tables and a maintenance job.

## How to run

```bash
# after the orchestrator is up (see SETUP.md / week-1 stack)
make pipeline       # or the Airflow DAG triggered via its web UI
trino --execute "SELECT count(*) FROM iceberg.gold.threads"
```

## Definition of done

- [ ] Pipeline runs ingest → silver → gold → eval by one trigger
- [ ] Trino ad-hoc queries over the Iceberg tables return correct results
- [ ] Compaction + snapshot expiry run safely
- [ ] DAG screenshot + Trino results pasted in `journey/05-harden.md`

## Common mistakes

- **Orchestrator owning business logic.** The DAG should orchestrate, not transform — heavy
  transforms belong in the pipeline steps, not the scheduler.
- **No cleanup path.** Compaction run without snapshot expiry just grows metadata forever.
