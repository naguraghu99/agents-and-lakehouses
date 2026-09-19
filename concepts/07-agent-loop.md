# 07 — The agent loop (model + tools + actions)

> Status: done · Phase: 3 · Prereqs: 06, 08

**One-liner:** An agent is an LLM inside a loop: *think → decide to call a tool → act → observe
the result → think again — until it has what it needs to answer.*

## What it is

A raw LLM answers with text only. An **agent** gives the LLM *tools* and lets it *use* them.
The loop (this is what frameworks like LangGraph orchestrate for you):

1. The model receives the user message + the list of available tools (their names, what they
   do, and their input schemas).
2. The model decides: either produce the final answer, or *request a tool call* (e.g.
   `search_historic_resolutions(thread="...")`).
3. Your code actually runs the tool and hands the result back to the model.
4. The model uses that result to decide again — call another tool or answer.
5. Repeat until it answers (or a safety cap stops the loop).

The crucial division of labor: **the model decides what to call; your code decides what runs.**
The model never touches your database or your API directly — it only proposes, you execute.
That separation is what makes agents safe and inspectable.

## Why it matters for this course

Agent v0 (Phase 3) is exactly this loop with two tools:

- `search_historic_resolutions(thread)` — go read how the brand handled similar threads (Gold
  table), so the reply is grounded (concept 12/13), and
- `escalate(reason)` — hand the case to a human with a justification.

Everything you learned in Phase 0/1 — prompt engineering (04), tool calling (08), ReAct (06) —
lands here as one loop. The "agent" was always a *loop around* the things you already know; it
is not a new magic model. Baselines A and B (concept 15) are deliberately *not* loops — that
contrast is what makes the agent's value measurable.

## Mental model

The LLM is the *brain* that cannot lift anything; tools are the *arms* that cannot think. The
agent loop is the conversation between them: brain says "I need the customer's thread history,
arm #1", the arm fetches it, the brain reads it and says "check similar past resolutions, arm
#2", until the brain says "I have enough — here's the drafted reply." The reason it feels
smarter than plain RAG: it can *decide to look things up mid-answer* instead of being handed
everything upfront.

## Where you'll use it

- `hiver/agent/graph.py` — LangGraph builds this loop as 3 named nodes that you can
  see, stop, and inspect individually.
- `hiver/agent/tools.py` — the two tools above (with the golden-holdout filter from
  concept 14).
- `hiver/ROADMAP.md` Phase 3 — the whole phase is "build the loop."

## Check yourself

1. Who decides *what to call*, and who decides *what actually runs*? Why the split?
2. Name the two tools in Agent v0 and what each gives the draft step.
3. Why is a single next-word predictor able to "decide" to use a tool?