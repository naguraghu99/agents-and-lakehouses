---
name: transcript-request
description: Exact list/count of lecture transcripts still needed to fill teaching-philosophy.md and style-guide.md, and how to hand them over.
metadata:
  type: reference
---

# What transcripts are needed, and why this count

**Update: 4 real transcripts already supplied and fully mined** — `math ml lec transcription.docx`, `math ml lec transcription 2.0.docx` (Math-ML course) and `Gen AI transcription.docx`, `gen AI transcription 2.0.docx` (GenAI course), covering roughly 2 lectures' worth of material per course (several lecture transcripts are concatenated per file). They live in `source/transcripts/` on the maintainer's machine (not shipped in the packaged skill — see SKILL.md). `teaching-philosophy.md` and `style-guide.md` are now evidence-backed from a complete close-read of these — every one of the seven categories, including student-question handling, has direct quotes. This request is purely additive now: more transcripts would add range (more analogies, more topic areas, and would test whether the GenAI course really has no live Q&A or that's just these two lectures) rather than filling an empty category.

The board notes (`board-notes-observations.md`) already tell us *how Prathosh sequences a derivation*. They cannot tell us *how he talks* — phrasing, analogies, reassurance, humor, pacing — because they contain no speech, only what ended up on the board. That's the one thing only real lecture transcripts can supply, and it's the piece `teaching-philosophy.md` and `style-guide.md` draw from.

**Target: 24 transcripts total — 12 per course.** That's enough to see his range (early/mid/late in a course, easy vs. hard topics) without transcribing all 162 videos in the two playlists, which would be far more text than needed to extract a stable style (style saturates well before 162 lectures — most of the marginal value is in spreading across the course, not in raw volume).

Skip tutorial videos (`T1`, `T2`, ... in the GenAI playlist) — those are code walkthroughs (PyTorch mechanics), not conceptual teaching, and are a different register. Only lectures (`L` / `Lec`) count toward the 12+12.

## Course 1 — NPTEL "Mathematical Foundations of Machine Learning" (89 videos, IISc Bangalore)

Confirmed from the playlist so far:
1. Mathematical Foundations of Machine Learning (Intro) — 3:33
2. Lec 01 — Overview of Function Approximation — 47:50
3. Lec 02 — Recap of Probability Theory - 1, Part 1 — 32:13
4. Lec 03 — Recap of Probability Theory - 1, Part 2 — 14:30
5. Lec 04 — Recap of Probability Theory - 1, Part 3 — 29:06
6. Lec 05 — Recap of Probability Theory, Part 2 (title cut off in playlist view)

**Ask:** open the full 89-video playlist and pick 12 lecture transcripts spread across it — roughly one every 7-8 lectures — covering:
- The intro + Lec 01 (opening style, how he frames the course and first topic) — items 2-3 above
- 3-4 from the early/foundations third (probability recap, function approximation, ERM-era material — matches board-notes pages ~1-40)
- 3-4 from the middle third (neural networks, optimization — matches board-notes pages ~60-100)
- 3-4 from the late third (whatever the course closes on — matches board-notes pages ~110-146)

If you'd rather not hand-pick, just grab the NPTEL/SWAYAM transcript PDF for the whole course from the course's Downloads page if one exists — that's a single file and I can sample from it directly instead of you choosing 12.

## Course 2 — IIT Madras BS "Mathematical Foundations of Generative AI" (73 videos, Prof. Prathosh A P)

Confirmed from the playlist so far (Week 1):
1. W1_L1 — Course outline deep generative models — 9:33
2. W1_L2 — Introduction & problem setting: generative AI basics explained — 58:32
3. W1_L3 — F-divergence: variational divergence minimization in generative models — 28:44
4. W1_L4 — Variational divergence minimization — 26:09
(W1_T1-T3 are tutorials — skip per above)

**Ask:** all four Week 1 lectures above are a good start (covers his course-opening style). Then pick 8 more `L`-numbered lectures spread across weeks — e.g. one or two lectures each from roughly W3, W5, W7, W9, W11 (or whatever weeks exist up to the course's end) — to cover VAEs/ELBO territory, GAN territory, and diffusion/policy-gradient territory, which the board notes show all appear later in the course (pages ~35, ~90, ~130+).

## How to hand them over

Either:
- Paste/attach transcript text or PDF files directly in chat, or
- Drop them in a folder and tell me the path so I can read them with the Read tool, or
- If YouTube auto-captions are the only option, copy the caption text (Show transcript panel on the video → copy) even if messy — it's workable, just noisier than official transcripts.

## What happens once they arrive

I'll read across all 24 (or however many land), fill in the seven categories in `teaching-philosophy.md` with verbatim quotes and lecture citations, populate `style-guide.md`'s verbal-mechanics section, rewrite `EXAMPLE.md` with 1-2 more worked examples pulled from real topics, and regenerate a sample lesson so you can judge whether it actually sounds like him.
