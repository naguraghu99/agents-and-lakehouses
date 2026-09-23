# One Problem, Two Skills, No Hand-Waving

**Learn Agentic AI and Data Lakehouses by building — and proving — a real AI support agent.**

This is a public, learn-by-building course. It is made of three things that live in this
repository:

1. **A 40-day Agentic AI course** — `agentic-ai-40-days/`
2. **A Lakehouse course** — `lakehouse/`
3. **A real problem to solve with both** — the OpenHiver SDE take-home — `hiver/`

Every small concept you meet along the way is explained in plain English in `concepts/`,
with no jargon left unexplained. If you are a beginner, that layer is for you.

---

## The story behind this repo

I was learning two things in parallel:

- **Agentic AI** — how LLMs work, prompting, tool calling, and (eventually) agents that take actions.
- **Data lakehouses** — how to turn messy raw data into clean, queryable, trustworthy data.

Both were my own self-made courses. Then I found the **OpenHiver** take-home problem:
take ~3 million real, messy Twitter customer-support conversations, pick one brand, and
build an AI support agent that (a) classifies each customer's intent, (b) drafts a reply
grounded in how the brand actually resolved similar issues before, and (c) decides whether
to auto-reply or escalate to a human — **and prove it is good enough to trust**.

It was the perfect intersection. To solve it I am forced to use almost everything from both
courses for real:

- Real data is messy → the lakehouse course's Bronze → Silver → Gold pattern stops being
  an exercise and becomes a necessity.
- An agent that drafts *grounded* replies → forces RAG, retrieval, and grounding — a module
  my agentic AI course didn't yet have.
- "Prove it's good enough to trust" → forces golden sets, LLM-as-judge, baselines, and
  honest failure analysis — the part everyone skips.

> **The dataset is not in this repo.** The Hiver problem uses the Kaggle dataset
> `thoughtvector/customer-support-on-twitter` (`twcs.csv`, ~3M rows, ~2017). Download it
> yourself and keep it outside the repo — it is large, historical, and can't be
> redistributed from here. See [`SETUP.md`](SETUP.md).

So this repo is three things at once: **my learning plan**, **the build**, and **the public
course that teaches everything used in the build** — as a course for others, one small
explained concept at a time.

---

## What you will build

A single system, end to end:

| Step | What | Teaches |
|---|---|---|
| Classify | What is this customer asking? (6–9 intents from the brand's own data) | LLMs, prompting, classification |
| Draft | A reply grounded in how the brand historically resolved this issue | RAG, retrieval, grounding |
| Route | Auto-reply or escalate to a human, with a reason | Confidence thresholds, routing |
| Prove | Show it's trustworthy: golden labels, metrics, judge, failure analysis | Eval, baselines, honesty about numbers |

Underneath it all: a real lakehouse pipeline that turns raw tweets into clean, threaded,
queryable tables the agent retrieves from.

---

## Audience and prerequisites

- **You.** If you are doing this course, you are learning both skill sets from scratch.
- **Target reader of this course:** someone who knows *basic* Python (variables, loops,
  functions, dicts/lists) and nothing else about AI or data engineering. If you don't have
  that yet, do `agentic-ai-40-days/0.python_basics/` first.
- **No GPU, no big infra.** Everything runs on a laptop with free/cheap APIs and containers.

---

## The four layers of this repo

```
# Agents and Lakehouses (repo root)
├── COURSE.md                        ← this file: orientation (why, rules, how the course works)
│                                    ← daily front door: hiver/weekly-plan.html
├── concepts/                        ← the teaching layer: one file per small concept
│   ├── README.md                    ← how explainers are written + full index
│   └── NN-name.md                   ← plain-English explainers, numbered in order of use
│
├── agentic-ai-40-days/               ← the 40-day agentic AI course (synced from syedjaferk)
│   ├── 0.python_basics/  …  5.tool_calling/   (days -3 → 5)
│   └── 7.simple_rag/ … 9.data_validation/     (latest sync, 2026-09)
│
├── lakehouse/              ← your lakehouse course
│   └── week-1/  …  week-5/         (week 1 done, rest planned)
│
└── hiver/                 ← the build = the course's project
    ├── weekly-plan.html                   ← course front door (week-by-week schedule, concepts linked)
    ├── ROADMAP.md                    ← the 7-phase plan (this is the course's syllabus)
    ├── problem_statement.md          ← the OpenHiver assignment
    ├── journey/                      ← learning journals (the evidence trail)
    ├── lakehouse/  agent/  eval/  report/
```

The relationship: **`concepts/` explains *every* small concept a phase needs.** The ROADMAP
tells you *what* to build and *why*. The `journey/` logs are the proof that it actually
happened. Nothing is assumed — if a term appears, it either has its own concept file or is
glossed inline.

**Where `concepts/` ends and the course modules begin:** `concepts/` is the *why* —
one page each, plain English, for a reader who has never met the idea. The modules in
`agentic-ai-40-days/` are the *how* — follow-along code, runnable exercises, real output
(`concepts/` tells you what you're doing, the module shows you running it). If a concept
confuses you, read it, then run the module it points at in "Where you'll use it".

Setup (Python, Groq key, lakehouse containers) is in [`SETUP.md`](SETUP.md); the single
status page is [`PROGRESS.md`](PROGRESS.md).

---

## How the course works (the loop)

For each phase in `hiver/ROADMAP.md`:

1. **Read the concepts** linked for that phase (`concepts/` — plain English, a few minutes each).
2. **Build the thing** the phase describes (small, runnable, subsampled).
3. **Keep the journal** — write what you learned in `journey/0X-*.md`. This is honestly where
   the real learning gets locked in.
4. **Tick the exit checkboxes** — they are the definition of "done."
5. **Log one decision** in `journey/decisions.md` when you make a non-obvious call.

Order matters. Do not skip phases — later work hands you the failure analysis material.

---

## The learning path (Roadmap → Concepts → Artifact)

| Phase | Quick summary | Concepts you'll meet | Artifact you ship |
|---|---|---|---|
| 0 | Orientation + two parallel tracks: 0A agentic (tool-calling), 0B lakehouse (medallion) | 0A: 01–08 (+ infra 26) · 0B: 09–11 | filled `journey/00-start-here.md` |
| 1 | Pick a brand, define intents + "good" | 01–07, 15, 16 | `journey/01-problem-framing.md` |
| 2 | Real tweets → Bronze → Silver → Gold (label in parallel) | 09–16 (+ infra 27, 28) | `lakehouse/` pipeline + `eval/golden.csv` |
| 3 | Agent v0: classify → retrieve → draft/route + baselines | 07, 08, 12–16 (+ infra 29, 30) | `agent/graph.py`, baselines |
| 4 | Golden set + eval harness + judge | 16–21 (planned) | `eval/run.py` + reproducible numbers |
| 5 | Harden: guardrails, memory, DAG, streaming | 22–25 (planned) | hardened agent + `journey/05-harden.md` |
| 6 | Report + publish | — | `report/report.md` + public repo |

> Concepts marked *(planned)* are written when the project reaches that phase — the course
> grows with the build, so nothing goes stale. See the index in `concepts/README.md` for status.

## T-shaped learning — the sequencing rule

**Learn concepts separately, practice them together, deepen them only when the project
demands it.** Phase 0 is two parallel foundation tracks, not a sequence: Phase 0A gives you a
runnable tool-calling agent, Phase 0B a runnable Bronze → Silver → Gold pipeline — a shallow,
provable slice of each, nothing more. Then the Hiver build integrates them and supplies depth
on demand: the lakehouse weeks 2–5 happen *inside* Phases 2–5, and LangGraph, memory, and
streaming are learned when the agent phases require them. Do **not** complete either subject
in isolation before joining the build, and do **not** reach for advanced tooling early —
everything is a dead end until the project asks for it.

---

## Two rules this course treats as sacred (they come from OpenHiver)

1. **Reproduce in <15 minutes.** Anyone (including an interviewer) can clone this repo and
   regenerate the headline numbers. That forces tiny datasets in — which is also what makes
   the whole thing learnable on a laptop.
2. **Every headline number gets a "what's misleading about this?" note.** The first time
   they ask you to defend the number, you'll be glad it's there.

---

## Status (honest, current)

- **Course shell:** this file + the `concepts/` layer.
- **40-day Agentic AI course:** days -3 → 5 done (basics → tool calling); rests on the roadmap.
- **Lakehouse course:** week 1 done (synthetic); weeks 2–5 are completed *inside* the Hiver
  build (this is the point).
- **The build:** Phase 0 exit items pending (journey templates empty). See `hiver/ROADMAP.md`.

Corrections, wrong guesses, and preferences are logged in `hiver/journey/learning-log.md`
the moment they surface — the assistant reads that file first every session.

---

## Start here

1. Set up your machine — [`SETUP.md`](SETUP.md): Python + one free Groq key (Track A) and
   the lakehouse containers (Track B).
2. Open `hiver/weekly-plan.html` — **the course's front door**: a week-by-week schedule
   (phase → weeks → concepts with links → files to run → exit checkboxes) that tells you what
   to complete each day on a ~1 hour/day pace, from both agentic AI and lakehouse, all the way
   to the Hiver submission.
3. Read `hiver/ROADMAP.md` (the syllabus the schedule follows).
4. Read `concepts/01-what-is-an-llm.md` and `concepts/09-medallion-architecture.md` (the two
   worlds in one page each).
5. Complete Phase 0 — **both parallel tracks** 0A (tool-calling agent) and 0B (medallion
   pipeline) — then Phase 1. No pipeline code before the framing doc is filled.

Track live status at any time in [`PROGRESS.md`](PROGRESS.md).