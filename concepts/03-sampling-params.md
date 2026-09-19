# 03 — Sampling parameters: temperature, top-k, top-p

> Status: done · Phase: 0 · Prereqs: 01, 02

**One-liner:** After the model computes probabilities for the next token, *sampling
parameters* decide how "greedy" or how "creative" its choice is — the three dials are
temperature, top-k, and top-p.

## What it is

From concept 01: the model scores every possible next token. Then it has to pick one.
**Sampling** is how it picks:

- **Temperature** — flattens or sharpens the probability curve. Low (near 0) → the most
  likely token nearly always wins (deterministic, dry, reliable). High (0.7–1.0) → lower-ranked
  tokens get a real chance (varied, sometimes surprising, sometimes wrong).
- **top-k** — *crop*: only consider the top *k* tokens by probability; the rest are set to zero.
- **top-p** — *crop-cumulative*: only consider the smallest set of tokens whose combined
  probability reaches *p* (e.g. 0.9). This adapts—when the model is confident, few tokens;
  when unsure, more.

The three compose: crop first, then sample.

## Why it matters for this course

The course's baseline rule is **temperature 0** for the classify/draft/route agent
(`ROADMAP.md` Phase 3). Reason: at temp 0 you get the same answer for the same input — you can
reproduce results, debug what changed between runs, and honestly report a number. Creativity
is a liability when drafting a support reply; you want the *most* likely wording, not a clever
one. When you later build the *judge* (concept 18), you may raise temperature slightly to *not*
collapse onto one score — but again, reproducibility in `run.py` argues for 0.

One subtlety worth knowing (a common interview gotcha): temperature 0 is not literally
"always same output" — there is still *batching/ordering* nondeterminism and token limits —
but for practical reproduction it suffices.

## Mental model

The model's probabilities are a roulette wheel with thousands of pockets. Temperature is how
smooth the wheel spins before the ball drops (cold → almost stops at the heaviest pocket).
top-k is "ignore every pocket except the k biggest"; top-p is "ignore everything outside the
biggest pockets that together cover p of the wheel."

## Where you'll use it

- `AgenticAI/40_day_of_agentic_ai/4.prompt_engineering/groq_client.py` — see the temperature
  parameter you are passing.
- `AgenticAI-Hiver/ROADMAP.md` Phase 0 exit: "explain temp 0 vs 1.0" — that is this concept.
- `AgenticAI-Hiver/agent/prompts/` — the classifier/drafter prompts are run at temp 0.

## Check yourself

1. What does temperature 0 do to the choice of next token?
2. What is the difference between top-k and top-p?
3. Why does the course mandate temp 0 for the agent (two reasons)?