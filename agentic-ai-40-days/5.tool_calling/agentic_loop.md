# From Tool Calling to an Agentic Loop

*A worked transformation — the one change that turned a two-step script into a mini-agent.
Everything here is from `tool_calling_homework.py` in this module; it happened because a single
question ("What are the current prices of RELIANCE and TCS?") broke the original design.*

Related concepts: [`concepts/08-tool-calling`](../../concepts/08-tool-calling.md) ·
[`concepts/07-agent-loop`](../../concepts/07-agent-loop.md) ·
[`concepts/06-reasoning-frameworks`](../../concepts/06-reasoning-frameworks.md)

---

## 1. Stage zero: tool calling is a *feature*, not a system

Tool calling (concept 08) is the primitive: the model, given a menu of `@tool` functions, may reply
with a structured *request* instead of text. `bind_tools` advertises the menu; `ai_msg.tool_calls`
comes back filled in; your code runs the function and appends the outcome.

The original script treated that as a **fixed two-stage pipeline**:

```python
ai_msg = llm_with_tools.invoke(messages)          # call #1 — might request tools
messages.append(ai_msg)

if ai_msg.tool_calls:
    for call in ai_msg.tool_calls:                # run tools ONCE
        result = tool_map[call["name"]].invoke(call["args"])
        messages.append({"role": "tool", "content": str(result), "tool_call_id": call["id"]})

    final_response = llm_with_tools.invoke(messages)   # call #2 — "the last one"
    return final_response.content
else:
    return ai_msg.content                         # answered on the first try
```

Two assumptions hide in there:

1. **One invocation gives you every tool call you'll ever need** (both tickers in a single reply).
2. **One follow-up call is enough to write the final answer.**

Both are assumptions about *the model*, and the model didn't cooperate.

---

## 2. The trigger: a two-ticker question

Running `"What are the current prices of RELIANCE and TCS?"`:

```
Model      >>> call tool #1: get_stock_price({'ticker': 'RELIANCE'})
Tool       <<< The current price of RELIANCE INDUSTRIES LTD (RELIANCE.NS) is INR 1233.40 ...
Assistant  >>>           ← empty! TCS was never fetched.
```

What happened: `gpt-oss-120b` returned **one** tool call, not two. The script ran RELIANCE, made its
one "final" call — and the model, still missing TCS's price, produced nothing. Two defects surfaced:

- **Incomplete planning:** the model asked for things across multiple turns, but the script only
  allowed one turn of tool use.
- **No re-asking:** there was no way to say *"you asked for RELIANCE — here it is. Do you want
  anything else?"*

The lesson: **`tool_calls` arriving at once is an optimization, not a guarantee.** Real agents must
tolerate their model requesting tools *gradually*.

---

## 3. The transformation: a fixed pipeline → a round loop

The minimal change is to make the "invoke → run tools → append results" block a **loop** whose exit
condition is **the model asking for nothing**:

```python
for round_no in range(1, max_rounds + 1):          # keep going until…
    ai_msg = llm_with_tools.invoke(messages)        # re-invoke with the FULL history
    messages.append(ai_msg)

    if not ai_msg.tool_calls:                       # …the model stops requesting tools
        final_message = ai_msg
        break

    for call in ai_msg.tool_calls:                  # run whatever it asked for this round
        result = tool_map[call["name"]].invoke(call["args"])
        messages.append({"role": "tool", "content": str(result),
                         "tool_call_id": call["id"]})
```

The control-flow picture:

```
BEFORE (linear):                              AFTER (a loop):
  invoke ──► tools? ──no──► answer              invoke ──► tools? ──no──► answer
     │         │                                  ▲           │
     │         yes                                │           yes (run tools,
     ▼                                            │            append results)
  run tools                                      │            │
     │                                            │            ▼
     ▼                                            └── re-invoke with growing history
  invoke once more ──► answer                    (capped by max_rounds)
```

What actually changed in the code is small (the `for` + `break` + `max_rounds`). What changed in
*meaning* is large — see the next section.

---

## 4. The concepts that make this loop a *real* pattern

### 4a. Messages are the agent's memory

Nothing is stored in variables between rounds. The agent's entire state is the **`messages` list** —
every human question, every AI request, every tool result, in order. Each round the model reads the
whole transcript, which is exactly how it "remembers" that RELIANCE was fetched and TCS wasn't.

That is the working-memory model of an LLM conversation: *the context window is memory, and
appending is how you write to it.* The `tool_call_id` on each `tool` message is the write-protocol —
it associates a result with the specific request that asked for it, so multi-call rounds stay
unambiguous.

### 4b. Separation of powers: the model proposes, your code disposes

Throughout the loop the model never executes anything — it only emits structured requests. *Your*
code decides which function really runs (`tool_map[call["name"]]`). This split (concept 07) is what
makes agents safe: the model could ask for anything, but the execution layer is where you enforce
policy (rate limits, allowed tickers, a golden holdout — anything).

### 4c. Termination: every loop needs a dead-man's switch

An unguarded `while model wants tools:` is an infinite source of LLM calls — and every call is
**money**. A tool that keeps failing (we hit this: the weather key returned `401` for two hours) makes
the model retry the same tool forever. `max_rounds=4` is the cap that converts "might loop forever"
into "can loop for at most 4 rounds." Termination conditions belong in agent design from day one, not
as an afterthought.

### 4d. "One at a time" is a fact, not a bug — plan for it

Some models batch several tool calls into one reply; `gpt-oss-120b` emits one. The loop makes both
work: a batched reply runs several tools in one round; a one-at-a-time model simply takes several
rounds. Treat *parallel tool calls as a performance optimization*, never as a requirement.

### 4e. This *is* ReAct

The loop is reason → act → observe, repeated (concept 06). Round 1: "I need RELIANCE's price" →
act → observe. Round 2: "…and TCS's" → act → observe. Round 3: "no more tools, composing the table."
The reasoning does not happen in one giant generation — it **emerges across turns**, each turn
grounded in real observations. That emergent look-it-up-mid-answer behavior is the entire pay-off
of an agent over a one-shot LLM call.

### 4f. Graceful degradation is part of the contract

The loop must also survive *bad outcomes*, because models and tools fail:

- **Empty final answers.** A reasoning model sometimes ends a tool round having produced no visible
  text (it "answered" with an empty string). The fallback in the homework file rebuilds an answer
  from the collected tool results rather than printing nothing.
- **Failing tools.** A failed tool returns a readable error string (not an exception), so the model
  can either retry or answer honestly — the choice stays with the model.
- **Round exhaustion.** If `max_rounds` runs out, the loop must still hand the caller *something*
  sensible (in our code, the last AI message), never crash on a type mismatch — which is exactly the
  `last_ai_message` fix we made when the naive fallback grabbed the last `tool` dict and blew up on
  `.content`.

---

## 5. What you've built (and what big frameworks call it)

The loop you now have is a *hand-rolled* ReAct agent: tools, a message-history buffer, an invoke-run-
append cycle, a termination cap, and an error path. LangChain calls it
`create_react_agent` / AgentExecutor; LangGraph models it as three named nodes (`agent` → `tools` →
`agent`); many newer tools call it *function-calling agents*. Your version is ~30 lines and fully
visible — which is exactly why building it by hand teaches more than importing the framework. You now
know what the frameworks are wrapping.

---

## 6. The invariant checklist for any agentic loop

Tape this to your monitor. Any loop that misses one of these will bite you:

- [ ] **Start condition:** wrap the user message in `HumanMessage`.
- [ ] **Exit condition:** the model returns no `tool_calls` → its text is the answer.
- [ ] **Result hydration:** every tool result is appended as a `tool` message with a `tool_call_id`.
- [ ] **Memory:** the full `messages` list is re-sent every round (never a trimmed summary — yet).
- [ ] **Safety cap:** `max_rounds` bounds the loop; log when it fires.
- [ ] **Error path:** tools return readable strings on failure; loop survives empty model text.
- [ ] **Observability:** print/log each round, call, and token count (that's the `[INFO]` trail).

---

## 7. Check yourself

1. What exactly broke when the model returned one tool call for a two-ticker question — and which
   part of the code fixed it?
2. Where does the model "store" its memory between rounds? What role does `tool_call_id` play?
3. Why must an agentic loop always have a step cap, and what happens without one?
4. In `tool_calling_homework.py`, trace the rounds for "RELIANCE and TCS" — which messages are `human`,
   which are `ai`, which are `tool`, and in what order?
5. Spot the failure-handling points in the loop: what happens if a tool errors, if the model emits an
   empty answer, and if rounds run out?

---

*Next stop: frameworks (LangGraph `create_react_agent`) automate this exact loop — read concepts 07
and 06 first so it reads as "the same thing, wrapped," not new magic.*