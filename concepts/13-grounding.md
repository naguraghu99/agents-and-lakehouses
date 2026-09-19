# 13 — Grounding (and why "2017 data" changes its meaning)

> Status: done · Phase: 3 · Prereqs: 12

**One-liner:** A reply is *grounded* if its claims come from the context you supplied — not
from the model's training data — and for this project "grounded" specifically means "follows
the brand's documented *historical pattern*," not "is correct policy today."

## What it is

Every RAG answer can fail in two opposite ways:

- **Hallucination** — the model invents a policy, an offer, or a process that appears in no
  retrieved chunk. ("Carry-on is free up to 25kg." was never in the data.)
- **Un-grounded-but-true-drifting** — the model gives a plausible generic answer ("we take
  feedback seriously") that is technically true and completely useless because it ignores what
  the brand actually did for this exact situation.

**Groundedness** is the measure of "the answer's specifics came from the supplied context."
A rubric that scores it asks: could every concrete claim be traced to one of the retrieved
chunks? That's the same test a human does in a live interview: "show me where in the data you
got that."

## Why it matters for this course

Two workshop questions, both with sharp answers:

1. **Where is grounding scored?** The judge rubric (concept 18) has `groundedness` as one of
   its four 1–5 dimensions. Low groundedness → the drafter is hallucinating → fix prompts or
   retrieval, never "try again."
2. **What does "history" mean when the data is ~9 years old?** twcs.csv is from ~2017. The
   brand's 2017 resolutions are a *pattern of how they used to handle things*, not a current
   SLA, fare rule, or policy. The repo makes this explicit (ROADMAP Phase 3 + the framing docs):
   **groundedness = "does the reply follow the brand's documented historical pattern?"** — and
   the reply should be worded to sound historical, not authoritative-on-policy. The report's
   "what's misleading" section (Phase 6) must own this limitation, and a stale-policy
   disclaimer is a legitimate part of the drafter prompt.

## Mental model

Grounding is *citation discipline*, the way a student is "grounded in the readings": every
paragraph traces to a source. Hallucination is citing a paper that doesn't exist. But note the
twist in this project: your readings are a *history textbook*, not this week's news. A reply
grounded in it is accurate about *what the brand did then* — truthful about the source, even
as policy evolves. Cite honestly, and say plainly that it's historical.

## Where you'll use it

- `AgenticAI-Hiver/ROADMAP.md` Phase 3 — the grounding caveat (2017 data), wording for the framing doc.
- `AgenticAI-Hiver/eval/judge.py` (planned) — `groundedness` rubric dimension.
- `AgenticAI-Hiver/agent/prompts/drafter.txt` — "only use the provided context; this is the
  brand's historical pattern."
- `concepts/14` — the leakage rule that keeps grounding scores honest.

## Check yourself

1. Define grounding in one sentence, and give the two ways an answer can violate it.
2. Why can't "grounded" mean "correct today" with this dataset?
3. Which rubric dimension, and which report section, are responsible for owning this?