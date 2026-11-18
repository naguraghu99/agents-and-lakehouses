# Agents and Lakehouses

A hands-on learning repository for building an AI support agent on top of a data lakehouse pipeline.

This project combines:

- an Agentic AI learning path
- a lakehouse/data engineering learning path
- a real-world end-to-end problem using OpenHiver-style customer support data

The repository is organized as a course and a build, with plain-English concept explainers alongside the code and project artifacts.

## What is in this repo?

- `AgenticAI/` — the Agentic AI curriculum and exercises
- `lakehouse-learning/` — lakehouse and data engineering lessons
- `concepts/` — short, beginner-friendly explanations of the core concepts used throughout the project
- `AgenticAI-Hiver/` — the applied project that ties the learning together
- `COURSE.md` — the main roadmap and course overview

## Learning goals

The main goal is to learn how to:

- reason about LLMs and agent behavior
- build tool-using AI workflows
- clean and structure messy real-world data
- design a lakehouse pipeline for customer conversation data
- retrieve grounded context for AI responses
- evaluate agent performance and trustworthiness
- route requests between automation and human escalation

## Project flavor

This repo focuses on a realistic support-agent workflow:

1. classify customer intent from support conversations
2. retrieve historical resolutions grounded in past cases
3. draft a useful response
4. decide whether to auto-reply or escalate to a human
5. measure success with evals, baselines, and honest failure analysis

## Repository structure

```text
.
├── COURSE.md
├── README.md
├── concepts/
├── AgenticAI/
├── AgenticAI-Hiver/
├── lakehouse-learning/
├── .gitignore
├── .github/
├── .opencode/
├── .vscode/
└── ...
```

## Start here

- Read `COURSE.md` for the overall course story and roadmap.
- Check the `concepts/` directory for the plain-English explanations.
- Follow the journey in `AgenticAI-Hiver/` to see the project progression.

## Recommended path

1. Begin with the basics in the Agentic AI curriculum.
2. Learn the lakehouse concepts and patterns.
3. Work through the project phases in `AgenticAI-Hiver/ROADMAP.md`.
4. Use the concept files as reference while building.

## Notes

This repository is intentionally structured as a learning-by-building project. It is designed to help you understand both the theory and the practical implementation behind AI agents and lakehouse-style data pipelines.

## License

No explicit license file is present in the repository root. If you plan to reuse or distribute materials, confirm whether a project license is intended before doing so.
