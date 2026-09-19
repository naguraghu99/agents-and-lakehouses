# Agentic AI × Lakehouse Mastery — via the Hiver Problem

> Learn both worlds by solving **one real problem**: turn ~3M messy Twitter support tweets into a trustworthy AI support agent, built on a real lakehouse.

> This repo is part of a **public, learn-by-building course**. If you are a learner, start at
> [`COURSE.md`](../COURSE.md) (the course homepage) and read `concepts/` — every concept
> used in the roadmap is explained in plain English there. This folder is the course's *project
> and syllabus*; `concepts/` is the *teaching layer*.

This repo is **both**:
1. Your **self-learning course** (documented journey, step-by-step)
2. Your **Hiver submission repo** (runnable pipeline + eval + report)

## The Three Pieces (analyzed)

**1. Your AgenticAI course** (`/agentic-ai-40-days/`):
- Done: Python basics → data structures → LLM terminology (`details.md`) → prompt engineering (9 techniques: zero/few-shot, CoT, ReAct, ToT, self-consistency + CRISP/RICE frameworks via `groq_client.py`) → tool calling (`tool_calling.py` with LangChain `@tool` + `bind_tools` on Groq `openai/gpt-oss-120b`)
- Stack: Groq + LangChain + LangGraph (installed, not yet used)
- Missing for Hiver: agents/graphs, memory, RAG/grounding, eval/LLM-as-judge, guardrails/routing, tracing

**2. Your Lakehouse roadmap** (`/lakehouse/`):
- Week 1 DONE + working: RustFS (S3) + Spark + Iceberg REST via podman-compose, medallion `bronze_silver_gold.py` on synthetic trades
- Week 2-5 planned but empty (README-only): W2 Parquet/Iceberg/time-travel → W3 streaming/partitioning/MERGE → W4 Airflow/Trino/maintenance → W5 DQ/governance/lineage
- Gap: never used on *real messy data* yet

**3. Hiver problem** (`problem_statement.md`):
- Pick 1 brand → **Classify** (your intents) + **Draft grounded reply** + **Route** (auto vs escalate with reason)
- Prove trust: 150-250 golden labels, eval harness (metrics + LLM-judge + human agreement), baselines (trivial + simple), failure analysis, "what's misleading", decision log
- Repro <15 min, subsample encouraged

**The insight:** Hiver *is* the missing Week 2-5 project + the missing AgenticAI modules 6-12. Twitter data forces you to do Bronze→Silver→Gold for real. The agent forces you to go beyond prompting into RAG + eval.

## How This Course Works

Follow `ROADMAP.md` in order. Each step has:
- `concepts/` — what you learn (AgenticAI + Lakehouse)
- `build/` — what you ship in this repo
- `prove/` — how you verify (checklist + commands)
- `journal/` — what you write (your learning log — this is the course content)

Do not skip the journal. That *is* the GitHub course.

```
hiver/
├── README.md               ← you are here
├── ROADMAP.md              ← full 7-phase plan
├── problem_statement.md    ← original brief
├── journey/                ← your dated learning logs
│   ├── 00-start-here.md
│   ├── 01-problem-framing.md       ← STEP 1 (start here)
│   └── decisions.md                ← running 10-15 decision log
│   └── learning-log.md             ← assistant self-improvement log (corrections go here)
├── lakehouse/              ← Bronze→Silver→Gold for Twitter data
├── agent/                  ← classify / draft / route agent
├── eval/                   ← golden set + harness + judge
└── report/                 ← final 6-page report
```

## Start Now

1. Read `ROADMAP.md`
2. Open `journey/01-problem-framing.md` — that's Step 1. Complete it before writing any pipeline code.
3. Work step-by-step. Ask your AI assistant for the next step only when the checklist is green.

## Rules for this repo (from Hiver, enforced on yourself)

- Reproducible in <15 min — keep `README` run instructions current every step
- Cite what you borrowed
- Subsample: never process 3M rows locally. Target: 1 brand, ~20-50k tweets max, golden 150-250.
- Every headline number gets a "what's misleading" note.
