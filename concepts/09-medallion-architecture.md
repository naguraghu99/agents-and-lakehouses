# 09 — Medallion architecture (Bronze → Silver → Gold)

> Status: done · Phase: 2 · Prereqs: none

**One-liner:** A medallion architecture moves data through three labeled layers of increasing
trust — Bronze (raw, keep everything), Silver (clean and joined), Gold (ready for specific
uses) — so that trust is built *step by step*, not in one lucky script.

## What it is

| Layer | What lives there | Properties |
|---|---|---|
| **Bronze** | Raw data, exactly as it arrived (the whole csv subset, no fixes) | Append-only, immutable, partitioned. Fixes NEVER edit Bronze. |
| **Silver** | Cleaned, de-duplicated, joined into usable records (real conversations) | Needs the messy joins (thread reconstruction) to happen here |
| **Gold** | Prepared *for a specific consumer*: the agent's retrieval table, the eval pool, a report | Small, curated, task-shaped |

The point of separation: Bronze is the *frozen evidence*, Silver is the *one truth the whole
company can trust*, Gold is *whatever one team needs today*. If a new consumer arrives with a
new need, they derive a new Gold table from Silver — they never re-clean raw data, and they
never touch Bronze.

## Why it matters for this course

- Phase 2 is this pattern built for real: 1 brand (~20–50k tweets) → `s3a://bronze/tweets/`
  → Silver threads → Gold `threads` + `intent_candidates` + `eval_pool`.
- It **forces honest auditing**: the `checks.sql` row counts (bronze→silver→gold, % dropped +
  why) are only meaningful because the layers are separated — you can see exactly where rows
  vanish.
- It makes the earlier synthetic exercise real: `lakehouse/week-1/bronze_silver_gold.py`
  ran on clean fake trades; Phase 2 runs the same shape on messy tweets where most of the
  work is *surviving the Silver step* (see concept 10 for why).

## Mental model

A crime scene, an evidence locker, and a courtroom exhibit. Bronze is the **garbage bag full
of whatever you found** — untouched, sealed, timestamped. Silver is the **evidence locker**
where items are logged, cross-referenced and duplicates thrown out. Gold is the **exhibit the
prosecutor actually shows** — a clean single slide for one purpose. You never put the original
garbage bag directly in front of the judge; you show them the Gold exhibit and can *prove*
(because of the chain) exactly how it was derived.

## Where you'll use it

- `lakehouse/week-1/` — the working synthetic example (RustFS + Spark + Iceberg).
- `hiver/lakehouse/README.md` — this project's bronze/silver/gold spec.
- `hiver/ROADMAP.md` Phase 2 — the build, with row-count proof in `journey/02-lakehouse-ingest.md`.
- `concepts/10` (append-only), `concepts/11` (Parquet/Iceberg) — the mechanics inside each layer.

## Check yourself

1. What is stored in each layer, and which layer is forbidden to edit?
2. Why does separation into layers make "where did my rows go?" trivially answerable?
3. Where do the *agent* and *eval* consumers read from, and why not directly from Bronze?