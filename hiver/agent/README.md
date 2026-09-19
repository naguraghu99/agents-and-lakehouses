# Agent — Classify / Draft / Route

> Phase 3 of `ROADMAP.md`. LangGraph agent that classifies intent, drafts a grounded reply, and routes auto vs escalate.

## What this is for
- Implements the 3 Hiver sub-tasks as 3 graph nodes: **classify → retrieve → draft+route**.
- Grounds replies in how the brand historically resolved similar issues (RAG over `lakehouse/` Gold `threads` table).
- **Retrieval leakage guard:** every `tweet_id` in `eval/golden.csv` (and its `eval_pool` source rows) is excluded from the retrieval index in `tools.py` — the agent must never retrieve a golden example's own thread. Enforced at index build, verified in `run.py`.
- **Grounding scope:** retrieved resolutions are historical *patterns* (twcs.csv ~2017), not current policy. Groundedness measures "follows the brand's documented historical pattern".
- Compares 3 systems: 2 required baselines + Agent v0 (Hiver report §4.2).

## Systems
| System | Classifier | Drafter | Router |
|---|---|---|---|
| Baseline A (trivial) | keyword / regex | template reply | always-escalate |
| Baseline B (simple) | zero-shot Groq, no retrieval | prompt-only (no RAG) | prompt-decided |
| Agent v0 | few-shot + instruction prompt (temp 0) | RAG-grounded via `search_historic_resolutions(thread)` tool | confidence-threshold + `escalate(reason)` tool |

## Planned structure
```
agent/
├── README.md          ← you are here
├── graph.py           ← LangGraph: 3 nodes + edge logic
├── tools.py           ← search_historic_resolutions (golden-holdout filtered), escalate (+ PII redaction in Phase 5)
├── prompts/           ← classifier, drafter, router, judge prompts (reuse techniques from agentic-ai-40-days/4.prompt_engineering/)
└── run.py             ← run all 3 systems over gold/eval_pool, log accuracy + cost/latency + retrieval hit-rate
```

## Stack
- Groq (`openai/gpt-oss-120b`) + LangChain `@tool` / `bind_tools` + LangGraph (see `agentic-ai-40-days/5.tool_calling/tool_calling.py`).
- Phase 5 additions (not yet): thread-state memory, guardrails (PII/tone/refusal), tracing, cost control.

## Exit criteria (Phase 3)
- [ ] All 3 systems run on `eval_pool`; accuracy + cost/latency logged; golden holdout verified (no golden thread retrieved)
- [ ] Journey log `journey/03-agent-v0.md`: prompts pasted, 5 errors pasted, what RAG fixed vs didn't

## Inputs / Outputs
- In: raw customer tweet (+ thread context from Silver) → Out: `{ intent, draft_reply, route: auto|escalate, route_reason }`
