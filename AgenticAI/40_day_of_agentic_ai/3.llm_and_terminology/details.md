

You've probably typed something into ChatGPT or Claude and wondered — what's actually happening back there? Let's break it down, no jargon left unexplained.

## What is AI, really?

AI is just a computer program that's gotten good at spotting patterns and making decisions, instead of following one rigid set of rules a human wrote line by line.

**Example:** Your phone's camera automatically detecting a face and drawing a little box around it — that's AI. Nobody wrote "if nose is here and eyes are there, it's a face." It learned that from millions of photos.

## What is an LLM?

LLM stands for **Large Language Model**. It's a specific kind of AI trained on a massive pile of text — books, websites, articles — to learn how language works. Its whole job is simple to state: given some words, guess the next most likely word. Do that over and over, and you get sentences, paragraphs, even code.

**Example:** You type "The capital of France is" — the model has seen that phrase (or ones like it) so many times that "Paris" is the overwhelmingly likely next word. It's not "looking it up" — it's predicting.

## What is a Prompt?

A prompt is just what you type in. It's the instruction or question you give the model. The quality of your prompt massively changes the quality of the answer — this is why "prompt engineering" became a whole skill.

**Example:**
- Vague prompt: *"Write about dogs."* → generic, all-over-the-place answer.
- Sharp prompt: *"Write a 3-line, funny Instagram caption for a golden retriever who just got a bath and hates it."* → focused, usable answer.

## What are Parameters in a model?

Think of parameters as the "knobs" inside the model's brain — tiny numerical values that got adjusted during training to help it recognize patterns. More parameters generally (not always) means the model can capture more nuance — but it also needs more computing power to run.

**Example:** GPT-3 had about 175 billion parameters. A small local model like a 7B (7 billion parameter) model is much lighter — it'll run on your laptop, but it won't reason as deeply as a giant cloud model. It's like comparing a general practitioner (knows a lot, broadly) to a small-town doctor with fewer resources (still useful, faster, cheaper — but less depth).

## Temperature — how "creative" or "safe" the model gets

Temperature controls randomness. Low temperature = predictable, focused, plays it safe. High temperature = creative, surprising, sometimes weird.

**Example:** Ask "Suggest a name for my coffee shop":
- **Temperature 0.2:** "The Coffee Corner," "Bean & Brew" — safe, obvious picks.
- **Temperature 1.0:** "Roast Manifesto," "Grounds for Rebellion" — quirkier, less predictable.

Use low temperature for factual/coding tasks. Use high temperature for brainstorming or creative writing.

## Top K — limiting the model's word choices

When the model predicts the next word, it doesn't just pick one — it ranks *many* possible next words by probability. Top K says: "Only consider the top K most likely words, ignore the rest."

**Example:** If Top K = 3, and the model is predicting the word after "I love eating," it'll only choose among the 3 most probable next words (say: "pizza," "pasta," "mangoes") — even if "cardboard" was technically the 500th most likely option, it's not even in the running.

## Top P (nucleus sampling) — a smarter cutoff

Instead of a fixed number of words like Top K, Top P says: "Keep adding the most likely words until their combined probability crosses P (like 90%), then choose from that pool."

**Example:** Top P = 0.9 might mean just 2 words already cover 90% of the likely options in one sentence ("yes," "no"), but in a more open-ended sentence it might need 50 words to hit that same 90%. It adapts to context, unlike Top K which is a fixed number regardless of situation.

**Quick analogy for both:** Imagine ordering food from a menu.
- **Top K** = "Only look at the top 5 items on the menu."
- **Top P** = "Only look at as many items as needed to cover 90% of what people usually order."

## Local Models — running AI on your own machine

Local models are LLMs you download and run yourself (on your laptop or a home server) instead of calling them over the internet. No sending your data to a company's servers, no monthly subscription — but you need decent hardware.

**Popular examples:**
- **Llama (Meta)** — general-purpose, widely used as a base for other tools.
- **Mistral / Mixtral** — known for being small but surprisingly strong.
- **Gemma (Google)** — lightweight, good for laptops.
- **Phi (Microsoft)** — tiny but punches above its weight for its size.
- **DeepSeek** — strong at coding and reasoning, popular for local coding assistants.

People usually run these through tools like **Ollama** or **LM Studio**, which make downloading and chatting with a local model almost as easy as installing an app.

**Example use case:** A developer working with sensitive client code might run a local model like DeepSeek-Coder on their own machine instead of pasting code into a cloud AI — nothing ever leaves their laptop.

## Putting it all together

Say you're using a local model to write jokes

- The **LLM** is the model itself (say, Mistral 7B).
- The **prompt** is "Write a joke about Mondays."
- The **parameters** (7B) tell you how much "brainpower" it has.
- **Temperature** at 0.9 makes the joke a bit wild instead of safe.
- **Top P** at 0.9 keeps it from picking totally nonsensical words while still allowing creativity.

Tweak these dials, and the same model can go from a boring corporate email writer to a chaotic joke machine. That's really all prompting and tuning is — turning the right knobs for the right job.

[[2025-11-08-saving-and-reviving-a-basic-machine-learning-model]]
