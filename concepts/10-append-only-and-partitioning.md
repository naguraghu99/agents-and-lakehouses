# 10 — Append-only and partitioning

> Status: done · Phase: 2 · Prereqs: 09

**One-liner:** Bronze is stored append-only (you can add, never edit or delete) and is cut into
partitions by date — two cheap properties that make immutable raw data simultaneously safe
and fast.

## What it is

**Append-only** means the only write operation allowed is "add new rows at the end." No UPDATE,
no DELETE. If the source data was wrong, you don't repair Bronze — you record a fix downstream
(in Silver) and let Bronze keep its original evidence. Consequences:

- Bronze can be re-derived/replayed exactly — it's a permanent audit trail of "what actually
  arrived."
- If a downstream bug is found, you re-run from Bronze, you don't scramble to patch corrupted
  history.

**Partitioning** means rows are physically grouped by a column — here, the `created_at` date —
so each day's tweets live in their own folder/file set. Consequences:

- Queries can skip whole partitions. "How many tweets in May?" touches only May files, not the
  entire table.
- Ingestion is trickle-friendly: each day's batch lands as one partition and stays isolated.

Together: an immutable log, split by time, that only grows.

## Why it matters for this course

- The lakehouse spec says Bronze is "raw, immutable, partitioned by `created_at` date" — this
  concept *is* those words. The exit criteria even asks you to explain why Bronze is
  append-only.
- The Twitter data lands as one giant historical csv, but partitioning it by date as you
  ingest makes the whole pipeline's later queries (checks.sql, Gold sampling, "this month's
  complaints") cheap and is a direct answer to interview questions about Bronze design.
- Silver keeps only the *clean* subset, but Bronze keeps every original row — so if the thread
  reconstruction logic (concept 09's Silver step) improves, nothing is lost; you just re-run
  the re-construction from the same Bronze.

## Mental model

A banker's ledger vs. a whiteboard. A ledger is **append-only**: entries get written, never
erased, and a mistaken entry is corrected with a *new* entry pointing at the old one (that's
your Silver fix). A whiteboard is **ephemeral and editable** — great for scratch, terrible as
evidence. Partitions are a filing system *within* the ledger: one cabinet drawer per month, so
you open the one drawer you need instead of reading every page.

## Where you'll use it

- `AgenticAI-Hiver/lakehouse/README.md` — "Bronze is append-only" is a stated rule; fixes go in Silver.
- `AgenticAI-Hiver/lakehouse/ingest.py` — the date-partitioned Bronze load.
- `AgenticAI-Hiver/journey/00-start-here.md` — asks you to explain why Bronze is append-only.

## Check yourself

1. What two operations are banned on an append-only table, and why is that a feature?
2. If your cleanup logic improves, where do you make the change — Bronze or Silver? Why?
3. What query gets faster because Bronze is partitioned by date?