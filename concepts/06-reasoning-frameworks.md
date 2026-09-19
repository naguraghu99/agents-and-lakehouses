# 06 — Reasoning frameworks: ReAct, ToT, self-consistency

> Status: done · Phase: 0 · Prereqs: 05

**One-liner:** Three heavier prompting frameworks that extend chain-of-thought — ReAct lets the
model act and observe, Tree-of-Thoughts explores branches, and self-consistency samples many
answers and votes.

## What it is

- **ReAct (Reason + Act):** interleave *thinking* and *acting*. The model outputs a thought,
  then decides to call a tool, gets the tool's result back, thinks again, and continues until
  the answer. This is the ancestor of the modern *agent loop* (concept 07) — ReAct is the
  proto-agent. The course has a `react.py` and the Hiver agent's "retrieve → draft" step is
  literally a ReAct-shaped cycle.
- **Tree-of-Thoughts (ToT):** instead of one chain, the model generates *branches* of reasoning,
  evaluates them against each other, and explores the promising ones. Expensive; used for
  hard planning/search problems — deliberately out of scope for a support agent.
- **Self-consistency:** sample the *same* question N times (higher temperature), then pick the
  answer the majority agrees on. Kills random variance at N× the cost. Overkill for
  classification, useful for anything where the "answer" is easy to verify by agreement.

## Why it matters for this course

You need to *know* these to understand what your agent is and isn't doing:

- Your **Agent v0** (Phase 3) is ReAct-shaped — that is not an accident, and the roadmap's
  "prompts reuse your react techniques" line is literal.
- Your project **explicitly does not use** ToT or self-consistency for the live agent: they
  multiply latency and cost, and a support reply doesn't need branch-exploration or voting.
  That is a documented decision (`journey/decisions.md` already has the "what we chose NOT to
  build" slot for exactly this).
- Self-consistency's *idea* survives in evaluation: the judge can re-score a small random
  subset twice to check its own stability (that overlaps with concept 20's agreement theme).

## Mental model

- ReAct = *think-talk-do-look*. A handyman who states the problem out loud, picks a tool, sees
  it didn't fit, and changes tool.
- ToT = *same job, three handymen, keep the best plan*. Good when trapped in local dead-ends.
- Self-consistency = *ask the same person 5 times in different moods, take the majority*.

A support agent is a handyman with a toolbox; it is not three parallel handymen or a polling
booth — know the difference so you can defend why you skipped the fancier ones.

## Where you'll use it

- `AgenticAI/40_day_of_agentic_ai/4.prompt_engineering/techniques/react.py`,
  `tree_of_thought.py`, `self_consistency.py`.
- `AgenticAI-Hiver/agent/graph.py` (Phase 3) — the ReAct-shaped classify → retrieve → draft cycle.
- `AgenticAI-Hiver/journey/decisions.md` — record "no ToT/self-consistency in the live agent: cost".

## Check yourself

1. In one line each: what do ReAct, ToT, and self-consistency do?
2. Which framework is your Agent v0 most similar to, and which nodes map to which step?
3. Give a project-specific reason you skip ToT and self-consistency.