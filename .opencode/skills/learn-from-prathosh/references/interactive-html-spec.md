---
name: interactive-html-spec
description: Technical rules for the interactive HTML lessons this skill produces — MathJax, widgets, layout, accessibility.
metadata:
  type: reference
---

# Interactive HTML spec

## Output format

- Single self-contained `.html` file. Inline `<style>` and `<script>`; MathJax loaded via its public CDN `<script>` tag is fine since these are local files the user opens directly, not claude.ai Artifacts (Artifacts disallow external requests — this skill's output is not published as an Artifact by default).
- No build step. Plain HTML/CSS/JS, MathJax 3 (`tex-mml-chtml.js`) for math rendering with `$...$` / `$$...$$` delimiters.
- Works standalone when opened from disk (`file://`) — no server assumed.

## Required structural blocks (from `assets/lesson-template.html`)

These blocks are the *internal* arc you write to — they are scaffolding names for you, the author, not copy. Never let "Hook", "Intuition", "Make it precise", "The math", "Why it matters", or "Edges & what's next" appear verbatim as a heading in the output. Every `<h2>` must be a topic-specific phrase a reader would actually want to read, so the lesson reads as one continuous lecture, not a labeled rubric. See "Headings" below for how to derive them.

1. **Header + progress bar** — topic title, short subtitle, a thin progress bar that fills as the reader scrolls through named sections.
2. **Hook** — a short, concrete opening (question, surprising fact, or minimal example) before any formalism. No equations in this block.
3. **Intuition** — picture/analogy-first explanation, ideally with one lightweight interactive element (slider, toggle) that lets the reader feel the concept before seeing its equation.
4. **Make it precise** — the informal intuition restated with correct notation, typed immediately per `board-notes-observations.md` conventions.
5. **The math** — the derivation itself, following the arc in `board-notes-observations.md`: define & type → naive goal → why it fails → explicit `Question:` → derive the fix → boxed named result → concrete instantiation. Use a step-through control (next/prev buttons or numbered reveal) rather than dumping the whole derivation at once. **Every step that performs an algebraic or logical manipulation must show the result of that manipulation as a displayed equation (`$$...$$`), not just describe it in prose.** "Add and subtract the mean and expand" is not a derivation step on its own — follow it with the actual expanded expression. A reader should be able to follow the derivation by reading only the equations, with the prose as narration alongside them, the way it would appear on his board.
6. **Why it matters** — connects the boxed result back to a real use case or to where it reappears later in a course.
7. **Edges / next** — caveats, failure modes, and a pointer to the natural next topic (mirrors "close a topic and bridge to the next" in `teaching-philosophy.md`).
8. **Quick-check** — 2-4 short self-check questions (multiple choice or numeric input) with immediate inline feedback, no server round-trip. **Every question carries a `data-why` attribute: one sentence saying why the correct answer is correct**, shown when the reader answers wrong. A wrong answer is the single highest-value learning moment on the page — the student has just discovered a gap and is motivated to close it. "Not quite — correct answer highlighted" wastes that moment entirely; it tells them *what* without *why*, so they memorize the option letter instead of the reason.
9. **Doubt callouts** — 2-3 collapsed `<details class="doubt">` boxes, placed inline at the derivation's `Question:` step and at the boxed result (the two points where readers actually get stuck). Each anticipates one specific plausible confusion for *this* topic and answers it in the register documented in `teaching-philosophy.md` §5: a one-word acknowledgment tic first ("Yeah — common one."), then a terse direct answer, or a named forward-pointer if a later topic covers it. Collapsed by default, so they add zero visible length for a reader who doesn't need them — this is what lets doubt-clearing coexist with the Conciseness rules below. A doubt callout answers a *side-question*; it never re-derives the main line, and it is not a place to park content that was cut for length.

## Conciseness (hard limit — this is the #1 failure mode)

Generated lessons have consistently come out too verbose. Enforce this strictly:

- **One short paragraph per prose block**, 2-3 sentences max, outside "the math." If you're about to write a second paragraph in hook/intuition/precise/why/edges, cut instead — pick the one sentence that's doing the real work and delete the rest.
- **Don't say the same thing twice in different words.** Each section advances the lesson one step; it does not restate what the previous section already established. If intuition already showed *why* something's needed, precise does not re-justify it — it just types it.
- **In "the math," the equations carry the argument.** Each derivation step gets at most one sentence of narration next to its equation(s) — never a paragraph explaining what the equation "really means" after already showing it. If the equation is clear, don't caption it.
- **"Why it matters" makes exactly one connection, in one or two sentences** — not a list of use cases. **"Edges" names at most two caveats**, one to two sentences each. Capping sentences-per-point isn't enough: four one-sentence caveats is still a mini-lecture, and a student remembers one caveat named sharply where they forget four named briskly. Three or more worth naming is a signal to pick the most consequential and cut the rest. Don't re-derive the mechanism — it was already derived in "the math."
- **Cut throat-clearing.** No "Let's take a moment to understand..." / "Now, it's important to note that..." — start the sentence at the content.
- **Spoken rhythm is a texture inside this budget, not a licence to exceed it.** `style-guide.md` documents his clause-chained lecture speech and checkpoint tics — apply that *within* the sentence caps above. One tic per sentence; never stack two or three ("right? — got it? — make sense?"). Where the two rules pull apart, conciseness wins.
- If a section still feels long after a pass, the fix is deletion, not tighter wording — cut the sentence, don't just compress it.

## Headings

- Write every `<h2>` as a topic-specific phrase, not the scaffold name. Think of it as the caption you'd actually put on that part of the board for *this* topic — e.g. for bias-variance: "Where does the error actually come from?" (hook), "Watch the tradeoff happen" (intuition), "Setting up the objects" (precise), "Cracking the error apart" (math), "Why this is the reason regularization exists" (why it matters), "What this doesn't cover" (edges). For MLE: "Guessing the coin's bias", "Watch the likelihood peak", "Typing the problem", "From product to sum", "Where this shows up again", "What MLE can't tell you".
- Section `id` attributes (`hook`, `intuition`, `precise`, `math`, `why`, `edges`, `check`) stay as-is internally for the progress bar and any anchor logic — only the visible `<h2>` text changes.
- Don't announce the section's function in its own heading ("Intuition:", "The Math:") — the content and the reader's momentum should make the function obvious without a label prefix.

## Running example / callback thread

Evidence-backed pattern (`teaching-philosophy.md` §4, `style-guide.md` "Recurring analogies and callbacks"): he doesn't reach for a fresh example in every section — he picks **one concrete running example for the whole lesson**, gives it narrative color once, then calls back to the same example tersely at later points instead of re-explaining it ("remember our example on the Bayesian estimate...", "let's go back to our typewriter-monkey problem").

Apply this to every generated lesson:
- Choose one concrete running example before writing any section. If the topic naturally fits one of the confirmed Math-ML story-analogies (coin toss, radiologist/X-ray, typewriter-monkey, flute/waveguide), reuse it rather than inventing a new one. If it doesn't fit and the topic is GenAI-flavored, use a concrete numeric/model instantiation instead (per the dimensional-grounding move in `style-guide.md`) — don't force a real-world story onto GenAI material or invent a new Math-ML-style analogy not in evidence.
- Introduce it with full narrative color exactly once — typically in the Hook or Intuition section.
- Callback to the *same* example, briefly, at natural later points: grounding the boxed result in "the math," and optionally in "why it matters." A callback should be short — a clause or a sentence — not a re-explanation from scratch.
- Don't introduce a second unrelated example partway through; if the intuition section needs a live widget, wire it to the same running example rather than a different one.

## Widget guidance

- A widget earns its place only if it changes what the reader *understands*, not decoration. A slider on a variance parameter that redraws a live plot is good; a slider that just replays a static GIF is not.
- Prefer `<canvas>` or inline SVG redrawn via JS for live plots over embedding external chart libraries (keeps it dependency-free besides MathJax).
- Every interactive control needs a visible current-value readout next to it (not just the slider handle position).
- **Every control also gets a short always-visible hint caption** (`<span class="hint">`) saying what to do with it — "drag to see the weights redistribute" beside a slider, "use ← → or Prev/Next" beside the step counter. A reader who doesn't realize the slider moves gets nothing from the widget, and a reader who doesn't realize the derivation is step-through thinks the lesson is missing five steps. This is a caption, not a doubt callout: one short phrase, always visible, no expand/collapse, and it does not count against the prose sentence budget.
- Keyboard-operable: sliders/buttons must be reachable and usable via Tab + arrow keys, not mouse-only. If the step-nav hint promises ← →, wire an actual `keydown` handler for it — a hint that lies is worse than no hint.

## Accessibility & responsiveness

- Semantic headings (`h1`/`h2`/`h3`) matching the structural blocks above, so the page has a real outline.
- `alt` text or an adjacent text description for any hand-drawn-style diagram, since these lessons are meant to also work for a screen-reader user.
- Relative units, `max-width` on the content column (~720-840px) for readability, responsive down to mobile width.
- Respect `prefers-color-scheme` — the page should not be unreadable in a user's dark-mode browser.
- Any color used semantically (e.g. forward-path vs. gradient-path per the board-notes color convention) must also be distinguishable without color alone (label, dash pattern, or icon) for colorblind readers.

## What NOT to do

- Don't fabricate a Prathosh quote or verbal tic not present in `teaching-philosophy.md`/`style-guide.md` — if those are still placeholders, write in a neutral precise voice instead of guessing at his phrasing.
- Don't box more than one or two results per lesson — over-boxing defeats the "this is the important part" signal observed in the notes.
- Don't add a widget just to prove the page is interactive; every element in the required blocks above should survive being asked "does this help intuition or is it noise?"
