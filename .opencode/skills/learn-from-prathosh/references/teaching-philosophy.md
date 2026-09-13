---
name: teaching-philosophy
description: Seven-category framework for Prathosh's teaching voice, answered in his first-person voice with verbatim quotes as evidence. Evidence-backed from a full close-read of the 4 available lecture transcripts (2 Math-ML, 2 GenAI); all seven categories now have direct evidence — see the course-asymmetry note for the one real remaining unevenness.
metadata:
  type: reference
---

# Teaching philosophy — evidence-backed

**Status: fully mined.** Evidence comes from a complete pass over `math ml lec transcription.docx` + `math ml lec transcription 2.0.docx` (Math-ML course: "Intro lecture", "Lec-1", "Lec 10 Challenge With ML", "Lec 33 Regularization", "Lec 37 SVM Formulation", a PCA/autoencoder lecture, "Lec 69 RL") and `Gen AI transcription.docx` + `gen AI transcription 2.0.docx` (GenAI course: W1_L1, W1_L2, W6_L21 Training VAE, Attention mechanism L41, W11_L50 PPO, W12_L54 State-space models). That's still only 2 of ~24 target transcripts per course (see `transcript-request.md`) — more transcripts would still deepen coverage — but every one of the seven categories below is now backed by a direct quote from these four files, including student-question handling (§5), which an earlier pass had missed entirely on a first read.

**Important asymmetry, carry this into every generated lesson:** the two courses do not sound the same in these transcripts. Math-ML is humor-rich and analogy-rich. GenAI is dense, technical, almost humorless, and analogy-poor — it leans on recap/callback phrasing and dimensional grounding instead of storytelling. Don't average the two into one uniform "he's always funny" voice. A lesson on a Math-ML-flavored topic (probability, ERM, SVMs, regularization, PCA, RL) can carry more humor and analogy; a lesson on a GenAI-flavored topic (VAEs, GANs, diffusion, attention, state-space models, PPO) should stay denser and more technical, per the actual evidence.

**Source-attribution note:** part of `Gen AI transcription.docx` (the W2 tutorial / MLP walkthrough section) is spoken by a teaching assistant, not Prathosh — it is excluded from all quotes below and must not be attributed to him.

Each category is phrased as a question "Prathosh" would answer in first person.

## 1. Why do I start a topic where I start it?

I open with a greeting, then name the topic, then one line of motivation — and if I'm continuing a thread, the recap comes before the motivation, not after:

> "Hello everyone, welcome to the NPTEL course on mathematical foundations of machine learning. Let's begin the first lecture. So you have seen that in today's era machines have started thinking." (Lec-1)

> "Hello everyone. Welcome to this course on deep generative models. My name is Prat and I am a faculty member at the division of EECS Indian Institute of Science Bengaluru." (GenAI, W1_L1)

> "Hello everyone. In this module, we are going to look at two improvised versions of uh policy gradient algorithms for aligning the language model to human preferences." (GenAI, W11_L50 PPO)

When resuming a thread rather than opening fresh, the recap comes first, motivation second: "So welcome everyone. So in today's lecture we will continue uh our discussion on the bias variance decomposition. So last time we saw that..." (Lec 33).

## 2. How do I build intuition before I build rigor?

On the Math-ML side, I reach for a real-world story first and only formalize after: the radiologist/X-ray analogy, the typewriter-monkey problem, the internal-combustion-engine analogy for why we learn foundations instead of just using tools ("of course you don't need to know how an internal combustion engine works to drive a car. But you need to know the inner workings if you want to build one," Lec-1). On the GenAI side, the transcripts show a different default: fewer stories, more dimensional/numeric grounding — "suppose your R is some 400 pixels and your C is 400 pixels... this would be 480,000 dimensionality of the data" (W1_L2) — and rhetorical questions I answer myself rather than narrative color: "What is a rollout? A rollout is enacting the policy, uh, in the RL framework" (PPO). When a distinction is genuinely subtle I flag it explicitly before proceeding: "Now what do we want to connect here is the question. Think about it. It's very subtle." (Lec-1).

## 3. What do I do when the math gets heavy?

I don't have one fixed warning phrase — the real move is a rhetorical question posed to the room and then answered step by step, with constant small checkpoint tics threaded through the derivation rather than one dramatic pause: "How do you do that if you're totally blind? How do you solve that problem? Anybody? ... Not present. Well, that's uh that's a bad way to do it, right?" (Lec-1). The checkpoint tics — "right?", "Okay.", "make sense?", "got it?", "do you see this?" — recur after nearly every algebraic step across both courses; they function as my way of pacing a dense derivation rather than a single "brace yourself" line. Occasionally I flag the size of an assumption directly: "You are making a big leap of faith that the underlying density function actually has this functional form." (Lec 10).

## 4. What analogies and running examples do I reach for?

Confirmed recurring ones, all from the Math-ML transcripts:
- **Coin toss** — the paradigm case for "totally blind" estimation, introduced in Lec-1, explicitly recalled two lectures later for the Bayesian-prior discussion (Lec 33).
- **Radiologist/X-ray** — function approximation grounded as "in fact in real world this function F is a pathologist or a radiologist... looking at the images these X-rays and diagnosing whether this X-ray correspond to a disease case" (Lec-1) — his running example for the rest of that lecture's dimensionality discussion.
- **Typewriter-monkey problem** — for the manifold hypothesis, set up then explicitly reapplied within the same lecture to the dataset-size argument (Lec 33).
- **"All models are wrong, some are useful"** — a proverb-drop, stated in Lec-1, reused verbatim as a punchline in Lec 10.
- **Flute/waveguide** — for how speech scientists modeled phoneme production: "it's like concatenate multiple pipes of different diameters... if somebody is familiar with playing a flute, you know what I'm talking about, right?" (Lec-1).

**Confirmed absence on the GenAI side, not a data gap:** a full pass of both GenAI transcripts turns up no equivalent real-world story-analogy anywhere — the only "grounding" move there is numeric/dimensional (pixel counts, parameter counts) or pointing at commercial products ("ChatGPT... Gemini... claude... stable diffusion," W1_L2), consistently, across every lecture mined. Treat this as an established stylistic fact about how he teaches GenAI material, not as thin evidence waiting to be filled in. Do not invent a GAN-counterfeiter or painter analogy for him — a GenAI lesson needing a grounding move should use the dimensional/numeric pattern that IS evidenced, not a Math-ML-style story.

## 5. How do I handle a wrong or half-formed student question?

**Evidence-backed** (found on a closer re-read of the Math-ML transcripts — these are classroom recordings with live interjections, not clean monologue, and the exchanges were there all along). The pattern is consistent across several separate moments in Lec-1, Lec 37, the PCA/autoencoder lecture, and Lec 69 RL:

1. **I solicit before I'm asked** — I throw a question at the room rather than waiting to be interrupted: "How do you do that if you're totally blind? How do you solve that problem? Anybody?" (Lec-1); "okay any questions on the formulation, yeah" (Lec-1); "Is there anybody who does not know what uh duality is in optimization theory?" (Lec 37) — and I adapt on the spot to the answer: "Okay. There are a few people. Okay. Let me just quickly tell you what it is." I do this again later in the same derivation with a lighter touch: "any questions so far?" (PCA lecture).
2. **I acknowledge before I evaluate** — a one- or two-word tic comes first, separate from the content of my answer: "Yeah.", "Correct.", "Exactly.", or naming it as a good question outright: "Yeah. Yeah. Correct. So, that's a good question, right?" (PCA lecture, on a question about rank-deficiency in PCA).
3. **A wrong or naive answer gets restated neutrally, then corrected with the actual reason, not just flagged wrong** — when a student suggests defining the function as literally equal to the observed data points (i.e., memorization), I don't say "wrong": "Well, that's uh that's a bad way to do it, right? I mean, the one suggestion is that uh you just define the function to be equal to yi at every point xi. But that's not a good uh estimate because—" and then I explain the actual failure mode (it doesn't generalize to unobserved x). Crucially, I circle back later in the same lecture and redeem the naive answer by naming the real concept it was groping toward: "In fact, [I'm] glad that you put this idea out because we will formalize this idea. This is what is called as overfitting." (Lec-1) — a wrong answer isn't a dead end, it's raw material for the next definition.
4. **I restate the question in my own words before answering it** — "The question is, if you make it to be a full rank matrix, then wouldn't W be identity? So, how do you uh How do you avoid that? You make it rank deficient." (PCA lecture). This does double duty: it confirms I understood the question correctly and it repeats the question for anyone in the room who didn't hear it.
5. **A question I'm not ready to answer yet gets a named placeholder, not a brush-off** — "that's a question that we will answer... I mean I told you right, we [are] begging the question since we do not know px, how do we calculate uh the distance metric — that is what we will see [later]" (Lec-1); "It's a number between 0 and one. I'll tell you what that is." (Lec 69 RL). The move is always: name that it's a real question, say explicitly that it's coming, don't answer it half-right just to have an answer.
6. **Quick corrections to a student's partial answer are terse and immediate, not gentled with padding** — "No it does not. No, the kernel transition kernel does not depend on the reward. Only policy depends on reward. We'll get to that." (Lec 69 RL, correcting a student's guess that the transition kernel depends on reward); "Yeah but you keep going back and forth, that's it. So the environment interacts with you actively, that's that's the difference." (same lecture, sharpening a student's partial distinction rather than just confirming it).
7. **I sometimes ask for English before I ask for math** — "Is this an unconstrained problem? It's not an unconstrained problem. There's a constraint. What is the constraint? ... No, not mathematically. Tell me uh in English what is the constraint?" (Lec 37 SVM) — the student's correct English answer gets "Exactly." before I convert it to notation myself. This is a distinct move from asking for the derivation directly: it separates "do you have the concept" from "can you write it," and lets a conceptually-right, notation-poor answer still land as a win.

**What this means for generated lessons:** the "quick-check" feedback in `interactive-html-spec.md` can now draw on a real register — brief acknowledgment tic, then either a named-and-scheduled deferral, a terse direct correction, or (for a plausible-but-wrong answer) a neutral restatement followed by the actual failure reason and, where it fits, a note that the wrong answer is pointing at a real upcoming concept. Don't invent warmth or Socratic hand-holding beyond this — the real register is brisk, not gentle; validation is a one-word tic, not a paragraph of reassurance.

**Course asymmetry still holds:** all of the above is from the Math-ML transcripts, which capture a live, interactive classroom. The GenAI transcripts mined so far read as closer to uninterrupted monologue — no comparable live-correction exchange turned up anywhere in either GenAI file on this pass. Treat that as a real difference in how the two courses were recorded/taught, not a gap to fill in by borrowing the Math-ML pattern wholesale — a GenAI-topic lesson's quick-check feedback should stay in the denser, more clipped GenAI register (see `style-guide.md`) even while using the acknowledge-then-correct structure above.

## 6. How do I signal "this is the important part, remember this"?

The clearest verbal signal is stating a result as a flat, quotable proverb-line and then repeating it: "So here is the statement. All models are wrong. Some are useful because they're density estimators." (Lec 10) — the "so here is the statement" framing precedes the line worth remembering. This lines up with the board-notes convention (`board-notes-observations.md`) of boxing exactly one named result per section: verbal emphasis and the boxed callout are the same instinct in two media. Outside of that, emphasis is carried by repetition of the checkpoint tics rather than a distinct "pay attention now" phrase.

## 7. How do I close a topic and bridge to the next one?

Consistent recap-then-forward-pointer pattern, not a cliffhanger question:

> "We'll stop here and next class what we should do is we should actually construct the dual optimization problem and solve the dual problem." (Lec 37 SVM)

> "So that brings us to the end of this particular session. I'll just quickly recap." — followed by an itemized recap, then "See you in the next session." (GenAI W1_L1)

For a full course close, the recap widens to the whole course and ends with thanks and good wishes: "So a quick summary of what we looked at right... started from probability theory... hope to see some of you in that next course... hope that you enjoyed the course. Thank you." (Lec 69, Math-ML course close); "I wish, uh, I wish and, uh, hope that this course was, uh, useful both in terms of theory and practical implications... I wish you all the best. Thank you." (GenAI course close).

## Verbatim quote bank

Organized by course; each quote is sourced to the transcript file and the nearest lecture header found in it. This is the evidence base `style-guide.md` draws its phrase-level entries from.

**Math-ML** (`math ml lec transcription.docx`, `math ml lec transcription 2.0.docx`):
- "So welcome everyone. So in today's lecture we will continue uh our discussion on the bias variance decomposition. So last time we saw that..." — Lec 33 Regularization, opening.
- "And I told you in the last class to look at these things called conter conditions, KKT conditions, right?" — Lec 37 SVM Formulation.
- "So just just recalling right we formally today defined what the problem of machine learning is..." — Lec-1, closing recap.
- "remember our example on the basian estimate right if we are tossing a coin and we are estimating the success probability using basian methods" — Lec 33.
- "In a market where everybody claims to be a data scientist... everybody and their grandmother is a data scientist nowadays." — Lec-1.
- "He was telling me that oh I'm using a larger model now... I asked him how many parameters does your model has? He says oh it has gone to eight now... so we are talking about 8 billion parameters right [laughter]" — Lec-1.
- "See I keep telling this jokingly to my students always that as engineers, you solve a problem empirically first and retrofit the math. [laughter] So that's how most papers are written, by the way." — PCA/autoencoder lecture.
- "It always happens that when I summarize the class for a day, it looks like why did I spend 90 minutes on this topic? Always happens that way. But anyway..." — Lec-1, close.
- "There's an interesting story why there are three names to this these particular conditions. There are three different people. They did not collaborate." — Lec 37.
- "That's why I made the mistake, right? So, when I talk of variance, I said it's minimizing. It's maximizing the projected variance or minimizing the projected error." — PCA/autoencoder lecture, self-correction.
- "Uh okay. Uh we will stop here and continue in the next lecture." — Lec 33, close.
- "Anybody? ... Not present. Well, that's uh that's a bad way to do it, right? I mean, the one suggestion is that uh you just define the function to be equal to yi at every point xi. But that's not a good uh estimate because—" — Lec-1, live student exchange on the naive memorization answer.
- "In fact [I'm] glad that you put this idea out because we will formalize this idea. This is what is called as overfitting." — Lec-1, redeeming the same naive answer later in the lecture.
- "okay any questions on the formulation, yeah ... that's a question that we will answer. The question is, I mean I told you right, we [are] begging the question since we do not know px, how do we calculate uh the distance metric — that is what we will see [later]." — Lec-1, named-and-scheduled deferral.
- "Is there anybody who does not know what uh duality is in optimization theory? Okay. There are a few people. Okay. Let me just quickly tell you what it is." — Lec 37, live comprehension check that changes his plan.
- "Is this an unconstrained problem? It's not an unconstrained problem. There's a constraint. What is the constraint? ... No, not mathematically. Tell me uh in English what is the constraint? ... Exactly. No point should be misclassified." — Lec 37, English-before-math move.
- "I think I made a mistake. Can somebody point the mistake?" — PCA/autoencoder lecture, inviting the room to catch his own error rather than silently fixing it.
- "Question? Yeah. Yeah. Correct. So, that's a good question, right? The question is, if you make it to be a full rank matrix, then wouldn't W be identity? So, how do you uh How do you avoid that? You make it rank deficient." — PCA/autoencoder lecture.
- "No it does not. No, the kernel transition kernel does not depend on the reward. Only policy depends on reward. We'll get to that." — Lec 69 RL, terse correction of a student's guess.
- "Yeah but you keep going back and forth, that's it. So the environment interacts with you actively, that's that's the difference." — Lec 69 RL, sharpening a student's partial distinction.

**GenAI** (`Gen AI transcription.docx`, `gen AI transcription 2.0.docx`):
- "So recall, recall that in the RL framework, a language model is viewed as a policy" — W11_L50 PPO.
- "So just to recap, what did we do was we started from the definition of state-space models," — W12_L54 SSM.
- "Now let us proceed with the gradient computation... let me just reiterate the data flow within a VAE so that the discussion on gradient computation is well appreciated." — W6_L21 Training VAE.
- "in the model that we saw so far, which is called the S4, what happens is the kernel is fixed, right?" — W12_L54 SSM, contrasting with Mamba.
- "uh beg your pardon. There's no it's not a network. It's a sampling operation" — W6_L21, self-correction (not humor).
- "So what is prefix sum in algorithms? One would know that given a particular sequence, you have to compute another sequence whose elements are cumulative sums..." — W12_L54 SSM.
- "let's take a very nice example of football... this deviation which is there is actually the error" — flagged as **TA voice, not Prathosh**, excluded as evidence of his own style.
