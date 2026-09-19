# 11 — Parquet and Iceberg (columnar, time travel)

> Status: done · Phase: 2 · Prereqs: 09, 10

**One-liner:** Parquet is a compact, column-oriented file format for many rows; Iceberg is a
table layer on top of Parquet that adds schema, snapshots (time travel), and proper
ACID-ish updates — the "real" upgrade over the synthetic course.

## What it is

**Parquet** — a file format that stores data *column by column* instead of row by row (like a
CSV). Reading a Parquet file can fetch only the columns you actually want and is heavily
compressed, so analytics queries over millions of rows get dramatically cheaper. But Parquet
alone is just files: no schema enforcement across files, no transaction-consistent view, no
history.

**Iceberg** — an open table format that *wraps* a directory of Parquet files and gives the
collection table-level superpowers:

- **Snapshots / time travel** — every commit creates an immutable snapshot. You can query the
  table *as of last Tuesday* by pointing at that snapshot. "What did this table say before I
  ran the dedup job?" becomes a one-liner.
- **Safe MERGE / dedup** — rows can be atomically up/corated (added, updated, deleted under one
  transaction) via MERGE, so "reconstruct threads, dedupe tweets, filter language" happens
  without readers seeing half-state.
- **Compaction & snapshot expiry** — small files get merged into few large ones, and old
  snapshots get pruned (the sleep-away of maintenance in Phase 5).

RustFS (their local S3 stand-in) + Spark + an Iceberg REST catalog is the exact stack running
in this repo.

## Why it matters for this course

- Phase 2 explicitly says: "Use Iceberg tables (not just Parquet) — this completes your Week 2."
  The synthetic course's `bronze_silver_gold.py` could get away with plain Parquet; real messy
  tweets need the *transactional* Silver step. Thread reconstruction + dedup + language filter
  is a series of MERGE operations that MUST be atomic — that's what Iceberg buys directly.
- `journey/02-lakehouse-ingest.md` documents partition choice and drop rates; Iceberg's
  snapshots let you *prove* lineage later (concept 25): which silver snapshot produced which
  gold export.
- Time travel is also the honest answer to the classic eviction question: "I changed the dedup
  rule — what subset did the golden labels come from?" (concept 14/16).

## Mental model

CSV is a phonebook (many pages, flip to a page). Parquet is a phonebook where all first names
live in one volume and all numbers in another — if you only need the numbers, you carry one
volume. Iceberg is then the *librarian + journal* on top: snapshots are "the catalogue as it
looked on Tuesday," MERGE is "a stamp-approval process before edits go in," and compaction is
the weekly re-bound of the whole thing. You (the analyst) always ask the librarian for the
catalogue; you never dig through volumes blind.

## Where you'll use it

- `lakehouse-learning/week-1/` — the synthetic start (Parquet; Iceberg catalog in compose).
- `AgenticAI-Hiver/lakehouse/to_silver.py` / `to_gold.py` — MERGE-based thread reconstruction on
  Iceberg.
- `AgenticAI-Hiver/ROADMAP.md` Phase 2 & 5 — the Iceberg upgrade and later compaction/snapshot expiry.

## Check yourself

1. Why is "fetch only the columns you need" the reason Parquet beats CSV for analytics?
2. What three table-level powers does Iceberg add over plain Parquet files?
3. Which Silver operation would be dangerous without transactions, and which snapshot-vs-version
   question does time travel answer?