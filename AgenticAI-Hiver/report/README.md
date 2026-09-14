# Report — Final 6-Page Hiver Report

> Phase 6 of `ROADMAP.md`. The submission artifact sent to `anurag@hiverhq.com` with the repo link.

## What this is for
- Convinces Hiver the agent is **good enough to trust** — results vs baselines, failure analysis, and honest caveats.
- Max 6 pages (or a README section). Covers Hiver §3.4, sections 1–6 below. No new experiments here — synthesis of `lakehouse/` + `agent/` + `eval/` + `journey/`.

## Required sections (Hiver §3.4)
1. **Problem framing** — what "good" means for this brand (from `journey/01-problem-framing.md`), and what you chose NOT to build.
2. **Results vs ≥2 baselines** — Agent v0 vs trivial (keyword/template) vs simple (zero-shot, no RAG): intent accuracy/F1, escalation P/R, reply judge scores + cost/latency.
3. **Failure analysis** — top 5 failure modes with real examples + hypotheses.
4. **"What is misleading about my headline number?"** — mandatory. Sampling bias, judge bias, metric gaming, small-n, etc.
5. **What you'd do next** — with one more week.
6. **Decision log** — 10–15 non-obvious decisions + why (condensed from `journey/decisions.md`).

## Planned structure
```
report/
├── README.md          ← you are here
├── report.md          ← the 6-page report (source of truth)
└── assets/            ← figures: confusion matrix, score distributions, latency/cost table, failure examples
```

## Exit criteria (Phase 6)
- [ ] `report.md` complete — all 6 sections, real examples, every headline number has a "misleading" caveat
- [ ] Root `README.md` run instructions reproduce eval headline numbers in <15 min
- [ ] Submission sent; retro written to `journey/06-retro.md`

## Rules
- Cite anything borrowed. Bullet points fine for decision log.
- Keep it honest: a weaker number with good failure analysis beats an inflated number.
