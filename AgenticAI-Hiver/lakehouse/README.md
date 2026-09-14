# Lakehouse — Bronze → Silver → Gold for Twitter Data

> Phase 2 of `ROADMAP.md`. Turns messy `twcs.csv` (~3M tweets) into queryable Iceberg tables that feed the agent and eval.

## What this is for
- Ingest **1 brand subset only** (~20–50k tweets max, never full 3M) into a medallion lakehouse.
- Produces clean, threaded conversations the agent can retrieve from, and a stratified pool for golden labelling.
- Reuses the `bronze_silver_gold.py` pattern from `lakehouse-learning/week-1/` — but on real messy data, with Iceberg (not just Parquet).

## Layers
| Layer | Content | Properties |
|---|---|---|
| `bronze/` | Raw `twcs.csv` subset, 1 brand, immutable | Append-only, partitioned by `created_at` date → `s3a://bronze/tweets/` |
| `silver/` | Cleaned + thread-reconstructed | Joins `tweet_id` ↔ `response_tweet_id` / `in_response_to_tweet_id`, deduped, language-filtered |
| `gold/` | `threads`, `intent_candidates` (keyword weak labels), `eval_pool` (200–300 row stratified sample → `eval/`) | Retrieval source for agent + eval input |

## Planned structure
```
lakehouse/
├── README.md          ← you are here
├── ingest.py          ← bronze load (1 brand filter, date partition)
├── to_silver.py       ← clean + thread reconstruct + dedup
├── to_gold.py         ← threads + weak labels + eval_pool.csv export
└── checks.sql         ← row counts bronze→silver→gold, % dropped + why
```

## Exit criteria (Phase 2)
- [ ] 1-brand subset in `s3a://bronze/tweets/`; silver thread table queryable via Spark/Trino
- [ ] `gold/eval_pool.csv` (200–300 rows) exported for hand-labelling in `eval/`
- [ ] Journey log `journey/02-lakehouse-ingest.md` written: row counts, % dropped + why, partition choice

## Rules
- Subsample always. Never load full 3M rows locally — profile with `df.sample(frac=0.01)`.
- Bronze is append-only — fixes go in Silver (see `journey/00-start-here.md`).
- Stack: RustFS (S3) + Spark + Iceberg REST via `podman-compose` (same as `lakehouse-learning/`).
