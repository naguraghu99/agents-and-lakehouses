# 14 — Data leakage (and the golden holdout)

> Status: done · Phase: 3/4 · Prereqs: 09, 12, 13

**One-liner:** Data leakage is when the test set secretly feeds the system being tested, so
your evaluation number is a lie — and in a RAG project the classic leak is the golden
example's own thread sitting in the retrieval index.

## What it is

Leakage = *test-answer contamination of the pipeline*. Formally: information that is only
available in the ground-truth labels/answers flows into the predictions. Every metric it
touches then measures "how much of the answer the system was handed," not "how well it
works."

The classic leaks in a ML/data project:

1. **Train/test overlap** — the same row appears in training and in the eval set.
2. **Future-in-past** — a model trained on May data evaluates on April data (time travel).
3. **Duplicate-events** — near-identical rows split across splits, so "memorized" scores look
   like "learned" scores.
4. **RAG's own leak** — the *evaluation example* (the thread you will grade the reply on) also
   exists in the retrieval index. When the agent retrieves for that same example, it pulls the
   golden thread itself, drafts an instant perfect reply, and scores 5/5 groundedness. Trivial
   and fake.

This fourth leak is the one this repo guards explicitly.

## Why it matters for this course

The design that created the risk: `eval_pool` is *sampled from Gold threads*, and the agent
retrieves *from Gold threads* (concept 09). Same table, both sides of the test. Without a
guard, every groundedness/reply score is inflated and the Hiver "prove it's trustworthy"
requirement (problem_statement §3) is structurally unmeetable.

The fix, now enforced in the design:

- **Holdout at index build:** every `tweet_id` that lands in `eval_pool`/`golden.csv` is
  removed from `search_historic_resolutions`'s index (`agent/tools.py`). The agent can
  genuinely never retrieve a golden example's own thread.
- **Verify in the harness:** `eval/run.py` re-checks that no retrieved context contains a
  golden id. If some future change forgets the filter, eval fails loudly.
- **Record as a decision:** it's row #1 in `journey/decisions.md` — reviewers and interviewers
  ask exactly this question.

## Mental model

An open-book exam where the answer key is printed on the back of the question paper. Reading
the back isn't cheating if you're told it's allowed — but you can't claim the score proves
you know the subject. A holdout is *tearing the back pages off before you hand out the exam*,
so the only way to answer is to genuinely use the reference material provided. If your eval
number is a "proof-of-trust" (Hiver's exact words), never let the exam paper carry its own key.

## Where you'll use it

- `AgenticAI-Hiver/ROADMAP.md` Phase 2 — the holdout rule definition.
- `AgenticAI-Hiver/agent/tools.py` — the filter; `AgenticAI-Hiver/eval/run.py` — the verification.
- `AgenticAI-Hiver/journey/decisions.md` #1 — the recorded decision.
- `AgenticAI-Hiver/report/README.md` — the results line notes the holdout keeps retrieval honest.

## Check yourself

1. Define leakage in one sentence, then list the RAG-specific variant.
2. Why is the leak *structurally certain* here (which design choice creates it)?
3. Where is the holdout enforced, and how does the harness prevent regressions?