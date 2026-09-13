# 01 — Problem Framing (STEP 1, do this now)

Goal: answer "what is good for this brand?" before writing pipeline code.
Concepts: intent taxonomy, task decomposition, scoping (what NOT to build).

## Tasks
1. Download Kaggle `thoughtvector/customer-support-on-twitter` → `twcs.csv`. Do NOT load full file into memory. Profile a 1% sample with pandas:
   `df.sample(frac=0.01)`, check `author_id`, `inbound`, `text`, `response_tweet_id`, `in_response_to_tweet_id`, brand handle column.
2. Count top 10 brands by inbound volume. Pick ONE. Recommended: high-volume airline/telco (e.g. AmericanAir) — rich complaints + clear escalation signal.
3. Draft v0 intent set (6-9): keep `praise`, `other`, rest from data (e.g. delay, baggage, refund, booking_change, connectivity, billing).
4. Define "good": e.g. intent accuracy ≥ X, escalation recall ≥ Y on angry/safety cases, reply groundedness ≥ 4/5, p95 latency < Zs, cost < $C/1k msgs.
5. List out-of-scope (e.g. images, DMs, multilingual, live Twitter API, full 3M scale).

## Write your answers here

**Brand chosen + why (volume + pain + data richness):**

**Top-10 brand counts (paste table):**

**v0 intents (name — 1-line definition — 1 example tweet each):**
1.
2.
3.

**What GOOD means (metric + threshold + why):**

**Explicitly NOT building (3-5 items):**

## Exit checklist
- [ ] Brand fixed; sample profiled, never full 3M
- [ ] v0 intents written with examples
- [ ] "Good" thresholds written
- [ ] Out-of-scope written
- [ ] Append row(s) to `decisions.md`

Next: Phase 2 — lakehouse ingest (only after this is filled).
