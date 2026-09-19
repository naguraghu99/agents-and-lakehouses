# 02 — Tokens and the context window

> Status: done · Phase: 0 · Prereqs: 01

**One-liner:** LLMs don't read letters or words — they read *tokens* — and everything you
send or receive must fit inside the model's context window, which is a hard size limit.

## What it is

Before an LLM can predict, the text you give it is chopped into **tokens**. A token is a
small chunk of text — roughly ¾ of an English word, so about 4 characters. Common words are
often one token; "supercalifragilistic" might be four or five. The model prices and counts
everything in tokens, not words.

The **context window** is how many tokens the model can hold in mind at once: your prompt +
the conversation history + any retrieved documents + the answer it is generating. They all
share one bucket. Run over the limit and the oldest parts get dropped (truncation) or the
request fails.

## Why it matters for this course

Three practical consequences you will hit every day of the build:

1. **Cost and latency scale with tokens** — a longer prompt costs more and answers slower.
   This is why cost/latency is one of the metrics logged for every system in Phase 3.
2. **RAG is a context-window strategy.** The repo can't stuff 50k tweets into the prompt, so
   it *retrieves the relevant ones* and only sends a small slice (concept 12).
3. **Thread context is finite.** A long support thread + history + instructions can blow the
   window; the agent must decide what to include.

## Mental model

The context window is a workbench. It has a fixed surface area. Your instructions, the
customer's thread, the brand's past similar resolutions, and the reply-in-progress all have
to fit on the bench at once — and you, the engineer, decide in advance what earns a spot.
RAG is the trick of "fetch from the warehouse only the parts you put on the bench."

## Where you'll use it

- `agentic-ai-40-days/4.prompt_engineering/contextual_prompting.py` — a technique
  built entirely around what context, and how much, to include.
- `hiver/agent/tools.py` — `search_historic_resolutions` returns a *small* number of
  threads precisely because the window is finite.
- `hiver/ROADMAP.md` Phase 3 — "accuracy + cost/latency logged" per system.

## Check yourself

1. Roughly how many English words is 1,000 tokens?
2. What actually happens when your prompt plus history exceeds the context window?
3. Why does RAG "look like" a context-window hedge? (two reasons)