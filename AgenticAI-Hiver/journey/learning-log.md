# Learning Log — assistant self-improvement

> Not a phase journal. The `0X-*.md` files are the *course content* (what you learned).
> This file is the *meta log* (how the assistant works): every correction, wrong guess,
> or preference discovered gets one row here so the same mistake is never repeated.

## Rules
- Log within the same turn a correction or preference surfaces — don't batch.
- One row per lesson. Small, specific, actionable. No essays.
- Each lesson ends with a **rule going forward**.
- Cap: if this file passes ~50 rows, condense stale rows into `Rules that stuck` below.

## Rules that stuck
- (none yet — promoted from the log when a lesson survives 3+ sessions)

## Log

| # | Date | Context | What happened | Rule going forward |
|---|------|---------|---------------|--------------------|
| 1 | 2026-09-14 | READMEs for lakehouse/agent/eval/report | Assumed folders at workspace root; they lived under `AgenticAI-Hiver/`. Had to search before writing. | Always locate real paths (`ls`/`glob`/`read`) before creating files — never assume layout. |
| 2 | 2026-09-14 | Roadmap architecture diagrams | First diagram was verbose; user asked twice to trim (number flow, then "a bit concise"). | Default to compact diagrams: short labels, fold details, numbered edges. Expand only on request. |
| 3 | 2026-09-14 | Diagram A vs B | User wanted phased numbered flow AND a phase-free system view as separate diagrams. | When mapping architecture, offer two views: build-order (phases) + running-system (components, no phases). |
| 4 | 2026-09-14 | Folder README format | Purpose + structure + exit criteria + rules mapped to ROADMAP phases, no extra tooling. | Match docs to existing repo vocabulary (phase numbers, Hiver § refs, infra names) — don't invent new terms. |
| 5 | 2026-09-19 | Roadmap architecture review | Found a correctness bug I'd have shipped: eval_pool rows are sampled from Gold threads, so a golden example's own thread would sit in the agent's retrieval index — RAG scores would be inflated. | Before writing a retrieval eval, ask "can the ground-truth row be retrieved by itself?" Enforce holdout at index build + re-verify in the harness. |
| 6 | 2026-09-19 | Review found scope creep + honesty gaps | Banking77 added nothing for a single-brand agent; "groundedness" over 2017 data can't mean "correct today"; streaming a static csv is checkbox engineering. | State dataset recency assumptions in framing; label "current-policy" vs "historical-pattern" claims explicitly; call out simulated demos in the log rather than implying real ones. |
| 7 | 2026-09-19 | Review found a blind metric | Reply BLEU/judge can be good even when retrieval returned the wrong thread — no metric measured retrieval itself. | Any RAG system needs a retrieval-level metric (hit-rate/@k) alongside downstream quality metrics. |
| 8 | 2026-09-19 | Review found progress-marker drift | ROADMAP said Phase 0 "~70% done" while its exit checkboxes were all unchecked and 00-start-here.md was blank. | Keep progress markers tied to checkboxes: a header % is only valid if the list it points at is green. |
| 9 | 2026-09-19 | Same-model judge bias | Using the drafter's model as judge inflates agreement via correlated reasoning; worse, submitting that as proof to Hiver. | Judge must be a different model (or at least a different prompt + temperature), and κ reported honestly. |
| 10 | 2026-09-19 | Course-shell convention | Repo is now a public course: `COURSE.md` homepage + `concepts/NN-*.md` teaching layer, one file per small concept, numbered by first-use order, prereqs in the header. | Write explainers at the START of the phase that uses them (never before, so prose can't go stale); no unexplained jargon — every term links to a concept or is glossed inline. |
