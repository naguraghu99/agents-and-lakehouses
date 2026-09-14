# Eval — Golden Set + Harness + Judge

> Phase 4 of `ROADMAP.md` (the hard part — "the proof is worth more than the system"). Proves the agent is good enough to trust.

## What this is for
- Holds the **hand-labelled truth** (150–250 examples), the **automated harness** that scores all systems, and the **LLM-as-judge** rubric for reply quality + human-agreement evidence.
- Every headline number reported in `report/` must be reproducible from here in **<15 min**.

## Contents
| Path | What |
|---|---|
| `golden.csv` | 150–250 hand labels, stratified by v0 intent + confidence. Columns: `text, true_intent, good_reply_traits, should_escalate, notes` |
| `run.py` | Harness: runs baselines + Agent v0 over `golden.csv`, outputs metrics |
| `judge.py` | LLM-as-judge: 1–5 rubric on `groundedness, tone-match, actionability, no-hallucination` |
| `agreement.md` | Human re-scores 30–50 judge outputs → Cohen's κ or % agreement |
| `sampling.md` | Short note: how you sampled + labelled (required by Hiver §3.2) |

## Metrics
- Intent: accuracy / F1
- Escalation: precision / recall (recall matters most on angry/safety cases)
- Reply: BLEU/ROUGE (auto, weak signal) + judge 1–5 (primary) + human agreement (κ)

## Planned structure
```
eval/
├── README.md          ← you are here
├── golden.csv         ← hand-labelled truth
├── eval_pool.csv      ← (copy/symlink from lakehouse/gold/) labelling source
├── run.py             ← reproduce headline numbers
├── judge.py           ← reply-quality rubric
├── agreement.md       ← judge-vs-human evidence
└── sampling.md        ← sampling + labelling note
```

## Exit criteria (Phase 4)
- [ ] `golden.csv` ≥150 rows, stratified, with sampling note
- [ ] `run.py` reproduces headline numbers in <15 min from clean clone
- [ ] Journey log `journey/04-evaluation.md` + draft of mandatory "what's misleading about my headline number" section

## Rules
- Source pool comes from `lakehouse/` Gold `eval_pool` — record which silver version → which label → which score (lineage, Week 5 DQ practice).
- Headline numbers without a "what's misleading" note don't count.
