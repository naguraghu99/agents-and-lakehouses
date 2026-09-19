# 05 — Chain-of-thought (CoT)

> Status: done · Phase: 0 · Prereqs: 01, 04

**One-liner:** Chain-of-thought is asking the model to show its intermediate reasoning steps
out loud *before* the final answer — which measurably improves correctness on tasks that need
more than one step.

## What it is

Without CoT, an LLM is asked a question and must jump straight to the answer in one move —
so the probability it picks the *final* response and gets the intermediate facts right is
lower. With CoT you prompt: *"Let's think step by step"* (or structure the answer with
explicit reasoning sections). The model now emits its working, and the mathematically
combined probability of "reach a plausible chain of short correct steps" is much higher than
"land directly on one correct final answer" — each small step is easy to get right, and the
chain is then used to derive the conclusion.

Two consequences the course makes you aware of:

1. **CoT costs tokens** — reasoning text occupies the context window and the output budget,
   and latency goes up. Trade-off, not free lunch.
2. **CoT is for tasks that *need* steps** — classifying a single tweet into one of eight
   intents is usually a one-step call; forcing a long CoT there wastes tokens and can add
   noise. Your classifier prompt should be *short*. Your evaluator (judge) call, where the
   rubric genuinely has several dimensions, benefits from CoT.

## Why it matters for this course

Two of the three agent components touch it:

- The **judge** (concept 18, Phase 4) scores replies on four dimensions (groundedness,
  tone-match, actionability, no-hallucination). Asking the judge to score dimension-by-dimension
  *before* aggregating is CoT and produces far more stable, explainable scores.
- The **router** must justify its auto-vs-escalate call with a reason — "with a stated reason"
  is literally in the problem statement. That reason is a mini-CoT: decide the angle, then the
  call, then the one-line justification.

The **classifier**, by contrast, should NOT chain-of-thought at length — see Where you'll use
it.

## Mental model

Two candidates: "solve 47 × 63 in your head and say the answer" vs "show and check your
multiplication." Same student, same arithmetic — but the second version has somewhere to check
its work. CoT opens that checking lane. Add it when the task has moving parts; drop it when
the task is a lookup.

## Where you'll use it

- `AgenticAI/40_day_of_agentic_ai/4.prompt_engineering/techniques/chain_of_thought.py`.
- `AgenticAI-Hiver/eval/judge.py` (planned) — dimension-by-dimension rubric scoring = CoT.
- Keep it OUT of `agent/prompts/classifier.txt` for the 8-intent classification.

## Check yourself

1. Why is "a chain of short easy steps" more likely to be right than "one big hard final step"?
2. Name the two costs CoT adds, and when you should skip it.
3. In this project, which component(s) should use CoT and which should not? Why?