---
name: board-notes-observations
description: Structural patterns observed directly in Prathosh's handwritten lecture notes (Math-ML.pdf, GenAI-IITM.pdf) — how he sequences a derivation, what he boxes, how he annotates. Evidence-backed from the notes themselves, not from speech.
metadata:
  type: reference
---

# Board-notes observations

Source: direct visual inspection of `Math-ML.pdf` (146 pages, NPTEL "Mathematical Foundations of Machine Learning") and `GenAI-IITM.pdf` (147 pages, IIT-M "Mathematical Foundations of Generative AI"), sampled across ~15 pages spread from page 1 to the final page of each. These are board/note-taking-app renders (ruled paper, handwriting, two ink colors), not slides. No audio — this file captures *sequencing and notation*, not *voice*. Voice comes from `teaching-philosophy.md` once transcripts are available.

## The recurring derivation arc

Every worked derivation sampled follows close to the same skeleton:

1. **Section header**, underlined, standalone line (e.g. "Machine Learning", "Neural Networks.", "The Policy Gradient Theorem").
2. **Set up notation and types before doing anything with them.** Every object introduced gets its domain/codomain or dimension annotated immediately and physically next to it: `X : domain set (Input)`, `Y : Range set (output)`, `W₁ ∈ R^(l₁×d)`. Nothing is left untyped for later.
3. **State the ideal/naive goal plainly**, often as a one-line "Assume" or "Given ... find ..." — frequently boxed: `Given D, find f`.
4. **Name the obstruction explicitly**, usually with a `∵` (because) or "can't be... since": *"True risk function can't be minimized ∵ Pxy is unknown."* He never silently swaps in the practical version — he states why the ideal one fails first.
5. **Pose it as an explicit `Question:`** at a heading-like line before deriving the fix — e.g. *"Question: What choice of q(z) would make the ELBO tight?"*, *"Question: How to modify a GAN such that the inversion is possible?"* This is a deliberate device: the question is written down, not just implied, before the derivation that answers it.
6. **Introduce the surrogate/fix and derive it inline**, with connective phrases doing the narration between equations ("Start with some initial guess on f. 'refine' the guess using D (data)").
7. **Name and box the payoff result**, usually with the acronym introduced right there: `Empirical Risk Minimization (ERM)`, `Evidence Lower Bound (ELBO)`. The box is reserved for the thing you're meant to remember, not every equation.
8. **Follow up with a concrete instantiation** of the abstract object where one is available — e.g. right after defining `X, Y, D, f` abstractly, he immediately grounds it: *"Consider Xᵢ to be x-ray images"* with a small hand-drawn diagram turning a P×Q image into an R^(PQ) vector.

## Other structural conventions

- **Two-column contrast for before/after.** When a problem is reformulated (e.g. true risk vs. empirical risk, original optimization vs. modified optimization), both versions are written side by side or stacked with inline labels (`: original`, `: modified optimization`), not narrated separately.
- **Color as a semantic channel, not decoration.** In the GAN/diffusion training notes, green consistently marks the forward/generative path (`g_θ(z)`, sampling), red consistently marks gradients and parameter updates (`∇_θ J`, `θ^(t+1) ← θ^t − α∇...`). The color tells you which "direction" of computation you're looking at.
- **Composite objects built up with braces/brackets showing nesting**, not flattened — e.g. the 3-layer MLP `h_θ(x) = W₃[σ(W₂[σ(W₁x)])]` is written with visible bracket nesting matching the composition order, and `Θ = [W₁, W₂, W₃]` is written immediately after to name the full parameter set.
- **Architecture diagrams sit next to their equations**, not before or after in a separate figure block — the U-net "bowtie" and the GAN generator/discriminator/encoder triangles are drawn inline, arrows labeled with the exact tensor/variable names used in the adjacent equations.
- **`∴` (therefore) marks the logical payoff line**, distinguishing "still deriving" from "here's the conclusion."
- **Terse, declarative sentence fragments carry the narration**, not full prose — "The underlying function 'f' is unknown." / "One NN which predicts μ_θ(x_t) for any x_t." Connective tissue is minimal; the math and the fragments alternate.

## Implication for lesson generation

When building the "the math" section of a generated lesson, follow this arc rather than a generic textbook derivation order:
`define & type everything → state the naive goal → name why it fails → ask the question the fix answers → derive the fix → name + box the result → ground it in a concrete instance`.

Use color deliberately in any generated diagram (e.g. forward pass vs. gradient path) rather than decoratively. Prefer a boxed "remember this" callout over highlighting every equation. When two formulations are being compared, lay them out side by side rather than describing the difference in prose alone.
