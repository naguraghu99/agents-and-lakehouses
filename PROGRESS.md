# Progress

One page that says exactly where this course is. `COURSE.md`, `hiver/ROADMAP.md`, and the
per-directory READMEs all use the same status language as this file. **The journey logs
(`hiver/journey/`) are the evidence for everything ticked here** — a checkbox without a
journal entry is a gap, not progress.

## One-line status

> Course shell complete. Agentic AI days -3 → 18 synced (12–18 added in the 2026-10 pull).
> Lakehouse week 1 done (synthetic); weeks 2–5 happen inside the Hiver build. Hiver build:
> framing started, Phase 0 exit items still open.

## At a glance

| Area | Completed | In progress | Next |
|---|---|---|---|
| Agentic AI | Python basics → custom tools, i.e. modules -3 → 18 synced | Stage 6 advanced material (LCEL, HIL, context, personalisation, RAG) synced but not yet run | LangGraph + agent loop (module 6) |
| Lakehouse | Week 1: RustFS + Spark + Iceberg medallion on synthetic trades | Weeks 2–5 (folded into Hiver Phases 2–5) | Week 2 → Phase 2 of the build |
| Hiver build | Problem framing drafted; project plan, decisions, learning log open | Phase 1 problem framing | Phase 0 exit items → Phase 2 lakehouse ingest |
| Concepts layer | 01–16 written | infra 26–30 + eval concepts 17–25 planned | write each when its phase starts |

---

## 1. Agentic AI course — [separate fork](https://github.com/naguraghu99/40_day_of_agentic_ai)

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
| 10. Memory management | done (synced 2026-10) — [module folder](https://github.com/naguraghu99/40_day_of_agentic_ai/tree/main/10.memory_management) |
| 11. Custom tools (+ MCP intro) | done (synced 2026-10) — [module folder](https://github.com/naguraghu99/40_day_of_agentic_ai/tree/main/11.tools-custom) |
| 12. LCEL (chains, parallel, passthrough) | synced (2026-10) — code only, no `details.md` yet |
| 13. HIL (human-in-the-loop) | synced (2026-10) — code only, no `details.md` yet |
| 14. Context management | synced (2026-10) — code only, no `details.md` yet |
| 15. Personalised AI | synced (2026-10) — code only, no `details.md` yet |
| 16. RAG as agent (minimal) | synced (2026-10) — code only, no `details.md` yet |
| 17. RAG embeddings (dense + sparse) | synced (2026-10) — code only, no `details.md` yet |
| 18. RAG as agent (advanced: 7 techniques) | synced (2026-10) — code only, no `details.md` yet |

Status language: `done` · `in progress` · `pulled in ahead of schedule` / `synced (2026-10)`
(course content pulled from upstream; not yet run end-to-end here) · `planned`.

> **Naming note:** modules `16.rag_as_agent` and `18.rag_as_agent` share the same folder name.
> `16` is the minimal "RAG wrapped as an agent tool" demo; `18` is the advanced suite
> (metadata filtering, re-ranking, semantic caching, query expansion, context compression,
> parent retriever, multi-vector retrieval). Read `16` first, then `18`.

Modules 10 and 11 are `done` as **synced course content**, not as course homework: the upstream
code is in place and `details.md` explains it, but nothing here has been run end-to-end against Groq
yet, so there is no journey entry for them. Module 10's `6.semantic_memory.py` additionally needs
`langchain-huggingface` + `sentence-transformers`, which are deliberately **not** in the pinned set
(see [`SETUP.md`](SETUP.md)) — so it is "done" only once that extra install is verified.

Modules 12–18 are `synced` but **weaker**: they ship runnable code with **no `details.md`/README**,
so there is written guidance for modules 0–5, 10 and 11 only. Until those docs exist, treat the
code as the source of truth and read it top-to-bottom before running. Writing the missing
`details.md` files is tracked as an open gap (see the course review).

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