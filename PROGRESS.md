# Progress

One page that says exactly where this course is. `COURSE.md`, `hiver/ROADMAP.md`, and the
per-directory READMEs all use the same status language as this file. **The journey logs
(`hiver/journey/`) are the evidence for everything ticked here** — a checkbox without a
journal entry is a gap, not progress.

## One-line status

> Course shell complete. Agentic AI days -3 → 5 done, day 7+ partially pulled in. Lakehouse
> week 1 done (synthetic); weeks 2–5 happen inside the Hiver build. Hiver build: framing
> started, Phase 0 exit items still open.

## At a glance

| Area | Completed | In progress | Next |
|---|---|---|---|
| Agentic AI | Python basics, data structures, LLM terminology, prompting, tool calling (days -3 → 5) | RAG, async coding, data validation (days 7–9, pulled ahead) | LangGraph + agent loop (module 6) |
| Lakehouse | Week 1: RustFS + Spark + Iceberg medallion on synthetic trades | Weeks 2–5 (folded into Hiver Phases 2–5) | Week 2 → Phase 2 of the build |
| Hiver build | Problem framing drafted; project plan, decisions, learning log open | Phase 1 problem framing | Phase 0 exit items → Phase 2 lakehouse ingest |
| Concepts layer | 01–16 written | infra 26–30 + eval concepts 17–25 planned | write each when its phase starts |

---

## 1. Agentic AI course — `agentic-ai-40-days/`

| Module | Status |
|---|---|
| 0. Python basics | done |
| 1. Data structures | done |
| 2. Number guessing game | done |
| 3. LLM and terminology | done |
| 4. Prompt engineering | done |
| 5. Tool calling | done |
| 6. LangGraph / agent loop *(planned gap — see ROADMAP Phase 3)* | planned |
| 7. Simple RAG | pulled in ahead of schedule (needed for the build) |
| 8. Async coding | pulled in ahead of schedule |
| 9. Data validation | pulled in ahead of schedule |

Status language: `done` · `in progress` · `pulled in ahead of schedule` (synced during the
2026-09 restructure) · `planned`.

---

## 2. Lakehouse course — `lakehouse/`

| Week | Topic | Status | Proven by |
|---|---|---|---|
| 1 | Ingestion, storage, local env | done | `bronze_silver_gold.py` on RustFS + Spark + Iceberg |
| 2 | Parquet, Spark, tables, metadata | waits for Phase 2 | real-tweets Bronze→Silver→Gold |
| 3 | Streaming, partitioning, resilience | waits for Phase 5 | simulated file-source backlog |
| 4 | Orchestration, querying, ops | waits for Phase 5 | Airflow DAG + Trino queries |
| 5 | Data quality, catalog, governance | waits for Phase 4 | DQ checks + golden-set provenance |

The point of weeks 2–5 is completed *inside* the Hiver build, not as standalone exercises —
that is what `COURSE.md` calls "both skill sets, one problem".

---

## 3. Hiver build — `hiver/ROADMAP.md`

Do these in order; a phase's checkboxes are its definition of done.

- [x] Phase 0A/0B — orientation + foundations set up (Python, Groq, RustFS/Spark/Iceberg installed)
- [ ] **Phase 0 exit items** — 0B: re-run Week 1 pipeline · 0A: re-run `tool_calling.py` · then fill `journey/00-start-here.md` *(this gates Phase 1)*
- [ ] Phase 1 — problem framing (brand, intents, "good")
- [ ] Phase 2 — lakehouse ingest: Bronze → Silver → Gold + eval_pool holdout
- [ ] Phase 3 — baselines + agent v0
- [ ] Phase 4 — golden set + eval harness
- [ ] Phase 5 — harden: guardrails, memory, DAG, streaming
- [ ] Phase 6 — report + publish
- [ ] **Repro rule** — clean clone → headline numbers in < 15 min
- [ ] **Honesty rule** — every headline number carries a "what's misleading about this?" note

## 4. Concepts layer — `concepts/`

The authoritative index + status lives in `concepts/README.md`. Summary:

- **Done (01–16):** LLM → tokens → sampling → prompting → CoT → frameworks → agent loop →
  tool calling → medallion → append-only → parquet/iceberg → RAG → grounding → data leakage →
  baseline thinking → golden set.
- **Planned:** 17–25 (eval + hardening) and infra 26–30 (containers, object store, Spark vs
  pandas, embeddings, REST).

The rule (from `concepts/README.md`): a concept is written **when the phase that uses it
starts** — nothing goes stale, nothing is ghost-written ahead of the build.

---

## How to update this file

When any checkbox above flips, update it **here and in the place that owns the item**
(`hiver/ROADMAP.md` owns build phases; `concepts/README.md` owns concept status; each
module/week README owns its own status). If the lists above disagree with those owners, the
owners win — fix this file. The CI workflow in `.github/workflows/validate.yml` re-checks
the repo structure automatically.