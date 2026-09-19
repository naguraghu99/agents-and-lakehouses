# Decision Log (running — need 10-15 by submission)

Hiver requires this. Add 1-3 rows per phase. Non-obvious decisions only, with why + alternative rejected.

| # | Date | Decision | Why | Alternative rejected |
|---|------|----------|-----|----------------------|
| 1 | 2026-09-19 | Hold out every `eval_pool`/`golden.csv` `tweet_id` from the agent's retrieval index | A golden example retrieving its own thread makes RAG trivial and inflates reply scores (data leakage) | Keeping golden rows fully in-graph for simplicity |
| 2 | 2026-09-19 | Judge reply quality with a DIFFERENT model than the drafter | Same-model judge/drafter produces correlated, inflated agreement | Reusing the drafter's model for judge consistency |
| 3 | 2026-09-19 | Define "groundedness" as "follows the brand's documented historical pattern", not "correct policy today" | twcs.csv is ~2017; telecom/airline resolution policies have changed since | Judging against today's unknowable ground truth |
| 4 | 2026-09-19 | Deprioritize Banking77 (keep 3M-tweet twcs as the only build dataset) | Single-brand agent zero payoff from a lab-split intent corpus; v0 intents come from the brand's own data | Using Banking77 to pre-train intent classifier |
| 5 | 2026-09-19 | Start golden labelling in parallel with Phase 2/3 (export eval_pool early) | 150-250 hand labels at 1-2h/day is the project's long pole | Doing all labelling inside Phase 4 |
| 6 | 2026-09-19 | Add a retrieval-level metric (context hit-rate / recall@k) | A RAG failure at retrieval otherwise only surfaces indirectly in reply scores | Relying on reply BLEU/judge to catch retrieval misses |
| 7 | 2026-09-19 | Keep single-tweet threads in Silver instead of dropping reply-orphans | Many (likely most) inbound tweets have no reply chain; dropping them would gut the dataset | Dropping all threads without a `response_tweet_id` |
| 8 | 2026-09-19 | Mark Phase 5 streaming as a simulated backlog (static csv, file-source only) | Real streaming adds no insight on a static snapshot; the point is the mechanism (file-source → compact → snapshot expiry) | Building a live-ingestion demo against the public Twitter API |