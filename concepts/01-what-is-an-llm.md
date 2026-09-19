# 01 — What is an LLM?

> Status: done · Phase: 0 · Prereqs: none

**One-liner:** An LLM (large language model) is a program trained on enormous amounts of text
that predicts the next word — and doing that well, repeatedly, turns out to be enough to
write, summarize, classify, and reason.

## What it is

An LLM is not a database of facts and it is not a search engine. It is a *probability machine
over words*. Given a chunk of text (call it the context), it assigns a probability to every
word it knows, then picks the most likely next one. Then it adds that word, predicts the
next, and so on. That loop — *predict-one-word, feed it back, repeat* — is how it produces
answers. You can see the raw version of this in the course's early notebooks.

Two things make modern LLMs useful despite this simple idea:
- their *size* (billions of parameters trained on trillions of tokens), and
- *instruction tuning* (after pretraining, they are fine-tuned on "human asks / good answer"
  pairs), which is why asking in natural language works at all.

## Why it matters for this course

The Hiver build uses an LLM for all three sub-tasks — classifying intent, drafting the reply,
and (in the judge) scoring replies. When a reply "makes things up" (hallucination) or drifts
off-topic, the cause is usually visible at this level: it was the most *probable* sequence,
not the most *correct* one. You will fix that with better context (RAG, concept 12), better
prompts (concepts 04–06), and better evaluation (concept 18) — never by demanding the model
"be smarter".

## Mental model

Think of it as an extremely well-read autocomplete. Autocomplete on your phone suggests the
next word from your typing history; an LLM "types" like someone who has read more text than
you could in a thousand lifetimes. It doesn't *know* — it *sounds* like it knows. Your job as
an engineer is to give it enough surrounding context that its predictions are grounded in
reality, and enough structure that it can't confidently bluff.

## Where you'll use it

- `agentic-ai-40-days/3.llm_and_terminology/details.md` — the course's own notes.
- `agentic-ai-40-days/4.prompt_engineering/groq_client.py` — the client that talks
  to the LLM (Groq, very fast, free tier).
- `hiver/agent/README.md` — the LLM does classify → draft → route inside the agent.

## Check yourself

1. In one sentence, what does an LLM do "at the lowest level"?
2. Why does "it's the most probable next word" explain hallucinations?
3. What did instruction tuning add on top of raw next-word prediction?