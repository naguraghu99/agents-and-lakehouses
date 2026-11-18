# 16 — Golden set and sampling

> Status: done · Phase: 2/4 · Prereqs: 14, 15

**One-liner:** A golden set is a small collection of cases *you* hand-labelled with the true
answer — the ground truth every metric and every system is scored against — and how you pick
those rows (sampling) decides whether your proof means anything.

## What it is

**The golden set** (`eval/golden.csv`, 150–250 rows) is human-labelled truth: for each chosen
tweet you record `true_intent, good_reply_traits, should_escalate, notes`. It is the fixed
ruler that all three systems (concept 15) are measured against. Everything reported as a
number in the report is "score against the golden set."

**Sampling** is *how you chose* those rows, and it is where the trust is won or lost:

- **Random sample** — easy, honest about "the average tweet," but you'll get few rare intents.
- **Stratified sample** — pick rows so every intent (including rare ones) appears in the set
  in known proportions. Results: your F1 per intent is statistically meaningful, and you can
  *prove* you didn't cherry-pick the easy rows.
- **Bias to avoid:** hands-on-you-only-pick-what-the-agent-gets-right rows. Stop. The
  checklist's "stratified by v0 intent + confidence" (ROADMAP Phase 4) exists precisely to
  forbid this.

The golden set has a second, quiet role: it's the **retrieval holdout list itself** (concept
14) — its `tweet_id`s are exactly the ones excluded from the agent's index.

## Why it matters for this course

- Hiver §3.2 requires 150–250 *self-labelled* examples with a note on **how you sampled and
  labelled**. That note (`eval/sampling.md`) is as graded as the numbers.
- Parallel-labelling is now built in (concept-09-era decision): the pool is exported as soon
  as Silver stabilizes (Phase 2 start), and you label "while you work," because hand-labelling
  150–250 rows at 1–2 h/day is the project's **long pole** — the task that would otherwise
  stall Phase 4.
- Small-n honesty: with n~200, intent accuracy's standard error is a few points. The
  mandatory "what's misleading about my headline number" section (Phase 6) is where you
  state exactly that.

## Mental model

The golden set is the **answer sheet** for a standardized test; the systems are the students.
Sampling is choosing *which questions* go on the test. If you weight the sheet toward the
questions one student is best at, every student looks better or worse than they are — a
stratified sheet shows the school the real distribution of difficulty. And the sheet is *held
outside* the students' textbook (concept 14's holdout) so nobody "studies the answer key."

## Where you'll use it

- `hiver/lakehouse/README.md` — the parallel-labelling rule (export early, label during Phase 3).
- `hiver/eval/sampling.md` and `eval/golden.csv` (planned) — the note + the truth.
- `hiver/ROADMAP.md` Phase 4 — the labelling spec + exit criteria.
- `Concept 14` — why the golden ids are also the holdout ids.

## Check yourself

1. What four columns does each golden row hold, and why is `good_reply_traits` a *label*, not a reply?
2. Why is a plain random sample weaker than a stratified one for reporting per-intent F1?
3. Name the two roles of the golden `tweet_id` list (evaluation truth + retrieval exclusion).