# 15 — Baseline thinking (trivial vs simple)

> Status: done · Phase: 3 · Prereqs: 04, 12

**One-liner:** A baseline is a deliberately dumb-but-runnable system you compare your agent
against, so a headline number means *"the agent beats X"* — not just "the agent scored Y."
Hiver requires two: a *trivial* one and a *simple* one.

## What it is

Two required baselines in this project, and the point of each:

- **Trivial (Baseline A):** keyword/regex classifier + template reply + always-escalate
  router. Zero machine learning. It answers: "how much of this task is just pattern matching?"
  If a competent regex already gets 40% intent accuracy, your agent's agent-ness had better
  visibly clear that bar, or you're adding complexity for nothing.
- **Simple (Baseline B):** zero-shot Groq classifier + prompt-only drafter, no retrieval. One
  LLM call, no tools, no graph. It answers: "how much does the *agent machinery* — retrieval,
  the loop — add over a plain LLM call?" (This is exactly the RAG contribution of concept 12.)

Both run over the same `eval_pool`/`golden.csv`, so every score in the report is a
three-column table: A/B/v0.

## Why it matters for this course

- Hiver §3.4 section 2 requires "results vs at least two baselines." The phrase "at least"
  is deliberate — baselines are how you *structure the argument*, not just a compliance box.
- Baselines give you **failure analysis material** (Phase 6 section 3): the failure modes B
  reveals that A didn't (e.g. "regex never caught sarcasm; zero-shot caught it but drafted a
  useless generic reply") are *hypotheses with alternatives* — which is literally what the
  report asks for.
- They protect you from your own demo-bias: excited after building the agent, everyone wants
  to report absolute numbers. A baseline row is the sobering mirror.

## Mental model

Medicine's trial logic. A new drug's effect is meaningless against "we tried it and patients
seemed better." You need a **placebo** (the trivial baseline — no active ingredient, but
follows the same ritual) and a **standard treatment** (the simple baseline — the incumbent
simple approach). The new treatment's *incremental* effect over both is the only honest
headline. Nobody publishes "patients improved 70%"; they publish "new drug beats placebo by 55
points and standard care by 12."

## Where you'll use it

- `hiver/agent/README.md` — the Systems table (Baseline A / B / Agent v0).
- `hiver/agent/run.py` — runs all three over the same eval pool; logs accuracy,
  cost/latency, retrieval hit-rate.
- `hiver/report/report.md` (planned) — the three-column results table.

## Check yourself

1. In one sentence each, what are the trivial and the simple baselines here?
2. What exact question does the simple-baseline comparison answer (which concept does it isolate)?
3. Why does "the agent scored 68% intent accuracy" mean nothing on its own?