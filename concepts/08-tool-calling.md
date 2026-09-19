# 08 — Tool calling (function calling / bind_tools)

> Status: done · Phase: 0 · Prereqs: 01, 07

**One-liner:** Tool calling is how you hand the LLM a menu of functions it can *ask you to run*
— it returns a structured "call this function with these arguments" request instead of text,
and your code executes it.

## What it is

Models are trained to output *structured tool calls*, not just prose. When you **bind** tools,
you declare them in the request (name, description, JSON input schema). If the model decides a
tool would help, its response is not plain text but a structured object:

```json
{ "name": "search_historic_resolutions", "arguments": { "query": "delay + refund", "k": 3 } }
```

Your code then runs that function for real and appends the result to the conversation. The
model never executes anything — it *proposes*, you *execute*, then you feed back the outcome
(that last part is the agent loop of concept 07).

In the course's stack (Groq + LangChain) this looks like:

```python
@tool
def search_historic_resolutions(query: str, k: int = 3) -> str: ...
      # ← the definition the model sees

llm.bind_tools([search_historic_resolutions])
      # ← declares the tool in the request
      # then: response.tool_calls → run each → append result → call llm again
```

The full loop is: `bind_tools` → model returns `tool_calls` → execute → re-invoke the model
with the results → model can call again or finally answer.

## Why it matters for this course

- It is the Phase 0 exit item ("explain the `bind_tools` flow in your own words") — the course
  literally gates Phase 1 on you understanding this one loop.
- The agent's two tools (`search_historic_resolutions`, `escalate`) are function calls made
  through this mechanism — Agent v0 is just this loop with a graph around it.
- The *retrieval holdout* (concept 14) is enforced at the point where your code executes the
  tool: even if the model asks to search a golden thread, the execution layer filters it. The
  one piece of the loop *you* fully control.

## Mental model

You are a busy engineer. The model is a junior who can *describe* what they need but is not
allowed to touch anything. They write you a carefully formatted request slip ("get me file X"),
you go get it, you hand it back, and only you decide what you actually fetch. `bind_tools` is
you handing out the official request-slip forms; `tool_calls` is the filled-in slip coming
back.

## Where you'll use it

- `agentic-ai-40-days/5.tool_calling/tool_calling.py` — the working example (Groq
  + LangChain `@tool` + `bind_tools`).
- `hiver/agent/tools.py` — the project's real tools, same mechanism.
- `hiver/journey/00-start-here.md` — Phase 0 asks you to explain this loop in 3 sentences.

## Check yourself

1. In the response, how does a model express "run a tool" instead of answering?
2. Who executes the tool call, and what is the holdout's role at that exact point?
3. Reconstruct the 4 stages: bind → call → run → re-invoke. What could go wrong at each?