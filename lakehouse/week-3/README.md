# Week 3: Streaming, Partitioning & Resilience

## Goals

- Build streaming ingestion with Spark
- Learn partitioning and hidden partition specs
- Implement MERGE INTO upserts for lakehouse tables
- Test pipeline recovery and checkpoint resilience

## Topics

- Spark Structured Streaming and file source backlogs
- Iceberg partition transforms and spec evolution
- Micro-batch upserts and idempotency
- Checkpointing and failure recovery

## Prerequisites

- Week 2 done (you have an Iceberg Silver/Gold to stream into).
- Honesty required: streaming a *static* `twcs.csv` is a **simulated backlog** — the point is
  the mechanism (file-source → compact → snapshot expiry), not the data flow.

## Expected artifact

- A file-source structured-streaming job with checkpointing that upserts into an Iceberg table
  and survives a mid-stream kill without duplicating rows.

## How to run

```bash
podman-compose exec spark spark-submit ...   # path under week-3 when built
```

## Definition of done

- [ ] File-source streaming empties a simulated backlog
- [ ] Partition transforms + MERGE INTO upserts run idempotently
- [ ] Checkpoint-restart proven (kill mid-stream, resume, no dupes)
- [ ] `journey/05-harden.md` records why this is a mechanism demo, not real insight

## Common mistakes

- **No checkpoint location / shared checkpoint.** You lose exactly-once and restart safety.
- **Not asserting idempotency.** Re-running the backlog should produce the same Silver/Gold
  state, not duplicates.
