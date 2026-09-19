# 04 — Prompting techniques (zero/few-shot, instruction, role, contextual)

> Status: done · Phase: 0 · Prereqs: 01, 02

**One-liner:** A prompt is how you tell an LLM what to do, and there are four basic levers —
give it an instruction, give it a role, give it examples, and give it context.

## What it is

Four baseline techniques (the course covers these as separate files in
`4.prompt_engineering/techniques/`):

- **Instruction-based** — just tell it what to do, explicitly and step by step. "Classify this
  customer tweet into exactly one of these intents: […]".
- **Role-based** — assign a persona to bias tone and knowledge. "You are a senior customer
  support agent for [brand], trained on our resolution playbooks."
- **Zero-shot** — no examples at all; the prompt is instruction + the input. Fast, no prep,
  but the model must already "know" the task pattern.
- **Few-shot** — you include 2–5 worked input→output examples before the real input. This is
  the single biggest correctness lever for boring, structured tasks (like intent
  classification) and costs almost nothing.

There's a fifth in the course — **contextual** (concept 02's sibling): wrapping the input in
surrounding facts/format so the model understands the situation, not just the sentence.

Each technique can be *combined*; real prompts in this repo stack role + instruction +
few-shot + contextual.

## Why it matters for this course

The whole agent's behavior is governed by prompts (there is no fine-tuning anywhere in this
project). Classification quality (Phase 3) comes mostly from a well-built few-shot prompt;
the drafter's groundedness comes from the contextual+instruction prompt plus retrieved
context (concept 12). The judge (concept 18) is itself just a prompt with a rubric. Prompting
is not a "soft skill" here — it is the primary tuning mechanism for a project with no finetuning budget.

## Mental model

The LLM is a brilliant but extremely literal intern with amnesia (no memory between calls).
- Instruction = the assignment. — Role = how to behave.
- Few-shot = three completed examples of the *exact* assignment. — Context = all the facts the
  intern is allowed to use.

Give the intern an assignment, a persona, worked examples, and the reference material, and
they stop improvising.

## Where you'll use it

- `agentic-ai-40-days/4.prompt_engineering/techniques/` — one runnable `.py` file
  per technique (zero_shot, few_shot, instruction_based, role_based, contextual_prompting).
- `hiver/agent/prompts/` — classifier, drafter, router, judge prompts (Phase 3-4).
- `hiver/journey/03-agent-v0.md` — you'll paste the final prompts there.

## Check yourself

1. What is the difference between zero-shot and few-shot?
2. Which one technique fixes most boring, structured-task errors cheaply?
3. Name the four base levers and the combinations you'd use for "classify this tweet".