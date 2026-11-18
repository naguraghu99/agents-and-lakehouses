# Agents and Lakehouses

**Learn Agentic AI and data lakehouses by building — and proving — a real AI support agent.**

One problem (the OpenHiver take-home: classify, draft grounded replies, and route a real
support inbox) forces you to use both skill sets for real. No hand-waving — every headline
number comes with a "what's misleading about this?" note.

**Start here:** [`hiver/weekly-plan.html`](hiver/weekly-plan.html) (the week-by-week front door) · **Why & rules:** [`COURSE.md`](COURSE.md) · **Setup:** [`SETUP.md`](SETUP.md) ·
**Status:** [`PROGRESS.md`](PROGRESS.md)

- **Orientation (how the course works, the sacred rules):** [`COURSE.md`](COURSE.md)
- **The teaching layer (explained from zero):** [`concepts/`](concepts/)
- **40-day agentic AI course (separate fork):** [naguraghu99/40_day_of_agentic_ai](https://github.com/naguraghu99/40_day_of_agentic_ai)
- **Lakehouse course:** [`lakehouse/`](lakehouse/)
- **The build — the Hiver project + its plan:** [`hiver/`](hiver/) · [`ROADMAP.md`](hiver/ROADMAP.md)
- **Capstone rubric and failure scenarios:** [`hiver/ROADMAP.md`](hiver/ROADMAP.md)

## Learning goals

The main goal is to learn how to:

- reason about LLMs and agent behaviour
- build tool-using AI workflows
- clean and structure messy real-world data
- design a lakehouse pipeline for customer conversation data
- retrieve grounded context for AI responses
- evaluate agent performance and trustworthiness
- route requests between automation and human escalation

## Project flavour

This repo focuses on a realistic support-agent workflow:

1. classify customer intent from support conversations
2. retrieve historical resolutions grounded in past cases
3. draft a useful response
4. decide whether to auto-reply or escalate to a human
5. measure success with evals, baselines, and honest failure analysis

## Repository structure

```text
.
├── COURSE.md          ← orientation, sequence, teaching standard
├── SETUP.md           ← tested dependencies, containers, keys
├── PROGRESS.md        ← honest status
├── concepts/          ← plain-English explainers, numbered
├── lakehouse/         ← the lakehouse course (week-1 … week-5)
├── hiver/             ← the build: ROADMAP.md, weekly-plan.html, journey/
├── risk_tracker.html
├── TODO.md
├── .github/  .opencode/  .vscode/
└── ../40_day_of_agentic_ai/   ← separate fork, cloned beside this repo
```

## Recommended path

1. Set up both tracks with [`SETUP.md`](SETUP.md).
2. Follow the sequence in [`COURSE.md`](COURSE.md) → "Course index"; it lists prerequisites,
   timing, status and the exact fork modules / lakehouse weeks each phase needs.
3. Use `concepts/` as the plain-English reference while building.
4. Work through the phases in [`hiver/ROADMAP.md`](hiver/ROADMAP.md); its capstone rubric is
   how you score the finished system.

## Notes

This repository is intentionally structured as a learning-by-building project. It is designed
to help you understand both the theory and the practical implementation behind AI agents and
lakehouse-style data pipelines. Depth over breadth: fewer technologies, understood well enough
to troubleshoot independently.

## License

No explicit license file is present in the repository root. If you plan to reuse or distribute
materials, confirm whether a project license is intended before doing so.
