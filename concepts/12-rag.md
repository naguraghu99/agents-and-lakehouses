# 12 — RAG (retrieval-augmented generation)

> Status: done · Phase: 3 · Prereqs: 02, 04, 07

**One-liner:** RAG = before the LLM answers, *retrieve* the relevant facts from your own
corpus and stick them into the prompt — so the answer is grounded in your data instead of the
model's trained-in guesses.

## What it is

The retrieval-augmented generation recipe, step by step:

1. **Index** — your corpus (the brand's historic resolution threads from Gold) is cut into
   small chunks and stored in a vector/search index. Ideally each chunk is also embeddable, so
   it can be found by *meaning*, not just by word match.
2. **Retrieve** — given a new customer issue, find the top-k most relevant chunks (semantic
   search, or keyword BM25, or a hybrid). This is where the agent's
   `search_historic_resolutions(thread)` tool (concept 07/08) does its work.
3. **Augment** — stuff those chunks into the prompt as context ("Here is how this brand
   resolved similar issues: …").
4. **Generate** — the LLM drafts the reply using ONLY that supplied context (concept 13
   grounds it).

The key fact an agentic-AI beginner must internalize: **the LLM never searches anything
itself.** The retrieval is *your* code, running before/inside the generation. In the agent
loop (concept 07) the model can ask for retrieval mid-answer, but even then it's your tool
executing.

## Why it matters for this course

- The whole distinction between **Baseline B** (zero-shot Groq + prompt-only drafter, *no
  retrieval*) and **Agent v0** (RAG-grounded via the search tool) exists to isolate exactly
  this concept's contribution. Any score difference between those two systems is "what RAG
  buys."
- The Gold `threads` table was purpose-built as the retrieval source. The golden **holdout**
  (concept 14) is a RAG-specific integrity rule.
- RAG also guarantees cite-ability: because the reply's facts came from retrieved chunks, the
  evaluator can check groundedness (concept 13) — did the reply stick to the provided context
  or hallucinate?

## Mental model

The model is a journalist with a phenomenal memory for *style* and a terrible ability to know
current facts. RAG is the researcher who, before the journalist writes, drops a folder of
approved source clippings on the desk and says "your article may ONLY use these." Write from
the clippings → grounded. Write from what "everyone knows" → rumour. The journalist decides
words; the researcher decides facts. You are the researcher.

## Where you'll use it

- `hiver/agent/tools.py` — `search_historic_resolutions` (the retrieval tool).
- `hiver/agent/prompts/drafter.txt` — the "use ONLY the provided context" instruction.
- `hiver/ROADMAP.md` Phase 3 — "what RAG fixed vs didn't" is your journey-log deliverable.

## Check yourself

1. List the four RAG steps in order, and which one is *your* code vs the model.
2. In this project, what exactly is the retrieval corpus?
3. How would you design the Phase-3 comparison so the difference between B and v0 isolates RAG?