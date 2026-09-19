# lakehouse/ — the Lakehouse course layer

A five-week, build-it-yourself course: turn a tiny local object store into a real lakehouse
(RustFS + Spark + Iceberg + Trino), explaining each layer as you stand it up. It is one of
the two course tracks (the other is `agentic-ai-40-days/`), and its official status lives
in [`PROGRESS.md`](../PROGRESS.md).

The deeper idea: **weeks 2–5 are not held as separate exercises.** They are completed inside
the Hiver build (`hiver/ROADMAP.md`) — weeks 2–3 inside Phase 2, weeks 3–4 inside Phase 5,
week 5 inside Phase 4. Only week 1 runs standalone, on synthetic data, to get the stack warm.

---

## How a week is written (the convention)

Every week follows the same shape, so you always know where to look:

```
# Week N — Topic

## Goals           — what you'll be able to do
## Prerequisites   — tooling/context needed before you start
## Topics          — the small concepts covered
## Expected artifact — the exact thing you should produce
## How to run      — the command(s)
## Definition of done — checkboxes
## Common mistakes — the traps you will hit, as the person who already hit them
```

`week-1/` is fully written this way (290 lines — it stands for the standard). Weeks 2–5
follow the same convention; their DoD checkboxes are what Phase 2 / 4 / 5 of the build are
measured against.

---

## The index

| Week | Topic | Status | Runs how | Proven by | DoD checkboxes |
|---|---|---|---|---|---|
| [Week 1](week-1/) | Ingestion, storage, local env | done | standalone (`podman-compose`, synthetic trades) | `bronze_silver_gold.py` → Parquet in bronze/silver/gold | `week-1/README.md` |
| [Week 2](week-2/) | Parquet, Spark, tables, metadata | waits for Hiver Phase 2 | inside the build (real tweets) | Iceberg tables, not just Parquet | below |
| [Week 3](week-3/) | Streaming, partitioning, resilience | waits for Hiver Phase 5 | simulated file-source backlog | MERGE INTO upserts, checkpoint recovery | below |
| [Week 4](week-4/) | Orchestration, querying, ops | waits for Hiver Phase 5 | Airflow DAG + Trino | DAG runs, Trino queries over Iceberg | below |
| [Week 5](week-5/) | Data quality, catalog, governance | waits for Hiver Phase 4 | golden-set provenance | DQ checks + lineage (silver → label → score) | below |

---

## Get started

- **Never touched a lakehouse?** Start at week 1 and run it end to end. [Setup](../SETUP.md)
  has the exact install + run + cleanup commands, including how to wipe the stack with
  `podman-compose down -v`.
- **Reading order:** week 1 → `concepts/09-medallion-architecture.md`, `10`,
  `11` → then the weeks as the build needs them.
- **On the 15-minute rule:** week 1 from a clean clone runs in under 15 minutes. If it takes
  longer on your machine, log it in `hiver/journey/learning-log.md`.

---

## Definitions of done for weeks 2–5

These are the exit checks each later week will be held to (the phases that own them live in
`hiver/ROADMAP.md`).

### Week 2 — Parquet, Spark, tables & metadata (Hiver Phase 2)

- [ ] 1-brand tweet subset landed in Iceberg `s3a://bronze/tweets/` (not bare Parquet)
- [ ] Silver thread table queryable (dedup, language-filter, thread reconstruction)
- [ ] Gold `threads` / `intent_candidates` / `eval_pool` tables queryable
- [ ] `% dropped + why` documented in `journey/02-lakehouse-ingest.md`

### Week 3 — Streaming, partitioning & resilience (Hiver Phase 5)

- [ ] File-source structured streaming empties a simulated backlog
- [ ] Partition transforms + MERGE INTO upserts work idempotently
- [ ] Checkpoint-restart proven (kill mid-stream, resume, no dupes)
- [ ] `journey/05-harden.md` records why "streaming a static csv" is a mechanism demo, not real insight

### Week 4 — Orchestration, querying & operations (Hiver Phase 5)

- [ ] Airflow DAG (or `make pipeline`) runs ingest → silver → gold → eval
- [ ] Trino ad-hoc queries over the Iceberg tables return correct results
- [ ] Compaction + snapshot expiry run safely
- [ ] DAG screenshot + Trino results pasted in `journey/05-harden.md`

### Week 5 — Data quality & governance (Hiver Phase 4)

- [ ] DQ assertions on gold (nulls, dupes, referential integrity)
- [ ] Lineage documented: which silver version → which golden label → which score
- [ ] Catalog discovery: Iceberg metadata history inspected for auditability

---

## Common mistakes (recorded, not hypotheticals)

- **Treating Iceberg like a folder of parquet.** Bare Parquet in a bucket is a data lake,
  not a lakehouse — the metadata catalog is the point. Weeks 2+ insist on Iceberg tables.
- **Deleting bronze rows to "fix" data.** Bronze is append-only source of truth; clean in
  silver, never edit bronze (`concepts/10`).
- **Letting `eval_pool` leak into retrieval.** The golden holdout `tweet_id`s must be
  excluded from the agent's index, or RAG becomes trivial and every score lies
  (`concepts/14`, `16`).
- **`podman-compose up -d` failing on ports.** Rootless podman: run with `sudo` or fix
  rootless networking (`week-1/README.md`).
- **The `Exited (0)` one-shot containers.** `rustfs-perms` and `rustfs-init` are *supposed*
  to exit 0. See `week-1/README.md` before "fixing" them.