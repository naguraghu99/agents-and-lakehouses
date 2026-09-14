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
