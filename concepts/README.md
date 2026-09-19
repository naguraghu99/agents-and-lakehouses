# concepts/ — the teaching layer

Every small concept used in this course has one file here, explained in plain English,
in the order you meet it (numbered). This is the layer that turns the repo into a course
*for others*, not just a personal build.

---

## How an explainer is written (the convention)

Every file follows the same shape so readers always know where to look:

```
# NN — Concept name

> Status: `done` | `planned` ·
> Phase: which ROADMAP phase needs it ·
> Prereqs: concept numbers to read first

**One-liner:** one plain sentence — what this thing is.

## What it is         — the definition, no jargon, short paragraphs
## Why it matters here — why the Hiver build forces you to understand it
## Mental model        — the analogy / picture that makes it stick
## Where you'll use it — concrete file paths in this repo that exercise it
## Check yourself      — 2–3 questions you should be able to answer in your own words
```

Rules the writer follows (self-enforced, logged in `AgenticAI-Hiver/journey/learning-log.md`):

1. **No unexplained jargon.** Every technical term is either the file's main subject, or is
   linked to another concept file, or is glossed in parentheses on first use.
2. **Concrete, not abstract.** Every concept must point at a real file/step in this repo
   where it shows up ("Where you'll use it" is mandatory).
3. **One concept per file.** If it's a different idea, it's a new file.
4. **Written when the phase that uses it starts** — that keeps docs honest and avoids stale prose.
5. **Beginner-first.** If a concept has a prerequisite, say so in the header — no shame in
   reading them in order.

---

## The index

| # | Concept | Phase | Status |
|---|---------|-------|--------|
| 01 | What is an LLM? | 0 | done |
| 02 | Tokens and the context window | 0 | done |
| 03 | Sampling parameters: temperature, top-k, top-p | 0 | done |
| 04 | Prompting techniques (zero/few-shot, instruction, role, contextual) | 0 | done |
| 05 | Chain-of-thought (CoT) | 0 | done |
| 06 | Reasoning frameworks: ReAct, ToT, self-consistency | 0 | done |
| 07 | The agent loop (model + tools + actions) | 3 | done |
| 08 | Tool calling (function calling / bind_tools) | 0 | done |
| 09 | Medallion architecture (Bronze → Silver → Gold) | 2 | done |
| 10 | Append-only and partitioning | 2 | done |
| 11 | Parquet and Iceberg (columnar, time travel) | 2 | done |
| 12 | RAG — retrieval-augmented generation | 3 | done |
| 13 | Grounding (and why "2017 data" changes its meaning) | 3 | done |
| 14 | Data leakage (and the golden holdout) | 3/4 | done |
| 15 | Baseline thinking (trivial vs simple) | 3 | done |
| 16 | Golden set and sampling | 2/4 | done |
| 17 | Precision, recall, F1 | 4 | planned |
| 18 | LLM-as-judge | 4 | planned |
| 19 | BLEU and ROUGE | 4 | planned |
| 20 | Cohen's kappa (judge-vs-human agreement) | 4 | planned |
| 21 | Confidence thresholds and routing | 5 | planned |
| 22 | Guardrails: PII, tone, refusal | 5 | planned |
| 23 | Memory and thread state | 5 | planned |
| 24 | DAG orchestration (Airflow) | 5 | planned |
| 25 | Lineage and data quality (DQ) checks | 4/5 | planned |

Status definitions:

- `done` — fully written and linked; if you spot a gap in one, log it in
  `AgenticAI-Hiver/journey/learning-log.md`.
- `planned` — on the syllabus, will be written when its phase starts (rule 4 above).

---

## Reading order

- **Never used an LLM before?** Start at 01 and go up — they build on each other.
- **Data person here?** Jump to 09, then 10–11, then back to 12–14 (RAG sits on both worlds).
- **Building already?** The ROADMAP phase tells you which numbers to read before you build
  that phase's deliverable.