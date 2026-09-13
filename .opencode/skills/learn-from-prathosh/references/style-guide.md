---
name: style-guide
description: Phrase-level mechanics of Prathosh's teaching voice — stock phrases, analogy patterns, pacing, reassurance, and live Q&A handling. Evidence-backed from a full close-read of the 4 available lecture transcripts (2 Math-ML, 2 GenAI) plus the board notes; the one confirmed asymmetry is the "voice varies by course" note below.
metadata:
  type: reference
---

# Style guide

## Notation & formatting conventions — evidence-backed (from board notes)

These are safe to use now; see `board-notes-observations.md` for the full evidence.

- Type/annotate every symbol the moment it's introduced (domain, codomain, or dimension), never after.
- State the naive/ideal goal before the practical one, and say explicitly why the ideal one fails (`∵ ...`) rather than silently substituting the workable version.
- Pose the pivot of a derivation as an explicit `Question:` line before answering it.
- Reserve a boxed callout for the one result per section worth memorizing — not every equation.
- When two formulations are compared (true vs. empirical, original vs. modified), lay them out side by side with short inline labels rather than two separate paragraphs.
- Use color/visual channel consistently for one semantic distinction at a time (e.g. forward path vs. gradient path) if the medium supports it.
- Ground an abstract definition in one concrete instantiation immediately after stating it.

## Verbal phrasing, pacing, tone, humor, reassurance — evidence-backed (partial)

Sourced from `teaching-philosophy.md`'s quote bank (2 Math-ML + 2 GenAI transcripts). Full quotes and citations live there; this file distills them into reusable rules for lesson generation.

**Voice varies by course — do not flatten this.** Math-ML transcripts are humor-rich and analogy-rich; GenAI transcripts are dense, technical, and nearly humorless, leaning on recap/callback phrasing and dimensional grounding instead. Pick the register that matches the topic's home course, not a single averaged tone. A VAE/GAN/diffusion/attention/state-space/PPO lesson should read denser and more technical; a probability/ERM/SVM/regularization/PCA/RL lesson can carry more humor and story-analogy.

**Stock tics, roughly ranked by frequency:**
- `"right?"` — the single most frequent tic, a rhetorical check-in after nearly every clause, in both courses.
- `"Okay."` as a standalone paragraph-boundary marker — very high frequency, appears almost every few sentences.
- `"make sense?"` / `"got it?"` / `"do you see this?"` / `"do you see why?"` — comprehension-checkpoint tics threaded through derivations, several times per lecture.
- `"or rather"` — self-correcting hedge, used when restating something more precisely mid-sentence.
- Stutter-repeat: saying a word or short phrase twice before continuing — `"recall, recall that..."`, `"represent, represent..."` — observed specifically and repeatedly in the GenAI transcripts; not confirmed in Math-ML.
- Mild self-correction asides ("uh beg your pardon, there's no— it's not a network, it's a sampling operation") appear in GenAI material as texture — these read as corrections, not jokes; don't mistake them for humor.

**Transitioning into a hard derivation:** no single fixed warning phrase — the real move is posing a rhetorical question to the room and then answering it step by step ("How do you do that if you're totally blind? ... Anybody? ... that's a bad way to do it, right?"; "So what is a rollout? A rollout is..."). Occasionally names the size of an assumption directly ("You are making a big leap of faith that...").

**Transitioning out of one / payoff phrasing:** state the result as a flat, quotable line, sometimes explicitly flagged first ("So here is the statement. All models are wrong. Some are useful..."), then move directly to "we'll stop here and next class we'll..." — recap-then-forward-pointer, not a cliffhanger question.

**Recurring analogies and callbacks (Math-ML only, confirmed):** coin toss, radiologist/X-ray, typewriter-monkey problem, "all models are wrong, some are useful," flute/waveguide for phoneme modeling. Each is introduced once with narrative color, then referenced tersely later in a different lecture ("remember our example on the basian estimate...", "let's go back to our typewriter monkey problem"). **GenAI gap:** no equivalent story-analogies found yet — its grounding move is numeric/dimensional ("suppose your R is some 400 pixels...") or naming commercial products (ChatGPT, Gemini, Claude, Stable Diffusion), not storytelling. Don't invent a GenAI story-analogy to match the Math-ML pattern.

**Humor style:** dry, infrequent, concentrated in Math-ML material — a real anecdote (a colleague claiming "8 billion parameters" as if it were a personal achievement), a self-deprecating close ("why did I spend 90 minutes on this topic? Always happens that way"), historical trivia played for a light laugh (three names for one condition because "there are three different people, they did not collaborate"). GenAI transcripts mined so far show essentially none — don't inject jokes into a GenAI-topic lesson to force parity with the Math-ML voice.

**Sentence rhythm in speech vs. board writing:** confirmed different from the board notes. The board notes show terse declarative fragments; the spoken transcripts run long and clause-chained, larded with "uh," "right?," and the checkpoint tics above — closer to real spontaneous lecture speech than to the compressed board writing. When generating lesson prose meant to sound spoken (e.g. narration inside the "Make it precise" or "The math" steps), lean toward the clause-chained spoken rhythm with checkpoint tics; keep the boxed/typed notation itself terse per the board-notes conventions above. **Where this spoken-rhythm guidance and `interactive-html-spec.md`'s Conciseness rule pull in different directions, Conciseness wins.** Written prose a student reads alone is not speech a student hears in a room: the tics that give a lecture its pacing become padding on a page, because the reader sets their own pace. Use at most one checkpoint tic per sentence, never stack two or three, and prefer one clause-chained sentence to two separate ones — the rhythm is a texture applied inside the sentence budget, not a reason to exceed it.

**Pacing markers:** no numbered "let's make sure everyone's with me" ritual found — pacing is carried by the checkpoint tics threaded continuously through a derivation rather than one scheduled pause. He does periodically throw a wider comprehension check to the room mid-derivation — "any questions on the formulation, yeah", "any questions so far?", "Is there anybody who does not know what duality is?" — and will visibly change plan based on the answer, rather than a fixed scheduled pause.

**Live Q&A register (evidence-backed, Math-ML only — see `teaching-philosophy.md` §5 for full quotes):** a one- or two-word acknowledgment tic first ("Yeah.", "Correct.", "Exactly.", "that's a good question, right?"), then one of: a terse direct correction ("No it does not... Only policy depends on reward."), a named-and-scheduled deferral ("that's a question that we will answer... that is what we will see later"), or — for a plausible-but-wrong answer — a neutral restatement of the suggestion followed by the actual failure reason, sometimes redeemed later in the same lecture by naming the real concept it foreshadowed ("this is what is called as overfitting"). He also sometimes asks for the answer in English before in math ("Tell me in English what is the constraint?"), rewarding a conceptually-right answer before it's been formalized. Keep this register brisk and terse, not warm or Socratic — the evidence is short exchanges, not extended gentle dialogue.

**Course asymmetry on Q&A:** this live-correction pattern is confirmed only in the Math-ML transcripts, which capture an interactive classroom. No comparable exchange turned up anywhere in either GenAI transcript on a full pass — treat that as a real difference in register (GenAI reads as closer to monologue), not a mining gap. A GenAI-topic lesson's quick-check feedback should stay in the denser GenAI register rather than importing this back-and-forth wholesale.
