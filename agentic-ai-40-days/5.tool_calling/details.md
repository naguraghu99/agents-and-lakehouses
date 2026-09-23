# Tool Calling — what it is and how the loop works

You've seen that an LLM is just a "next-word predictor" trained on text. That means it has exactly
one way to act in the world: produce words. It cannot check the weather, do exact arithmetic, query a
database, or hit an API — no matter how confidently it *talks* about doing them. **Tool calling**
(function calling) is the standard fix: instead of making the model smarter, we give it *hands*.

The script `tool_calling_homework.py` walks you through that fix step by step, with clean, annotated
output. (`tool_calling.py` is the upstream original — we leave it untouched and do the course homework
in the `_homework.py` copy.)

> Reading at your own pace: when homework 3 turned this script from a fixed pipeline into a real agent
> loop, we captured the whole transformation — the failing two-ticker question, the before/after code,
> and the deeper concepts (memory, termination, ReAct) — in
> [`agentic_loop.md`](agentic_loop.md).

---

## The core idea in one paragraph

The model doesn't run anything. It just decides **"I need some data to answer this — here's the
function name and the arguments;"** we run that function ourselves, hand the result back, and let the
model write the final answer using the fresh data.

```
You ask:   "What is the weather in Paris?"

Model:     "I need get_weather, with city='Paris'"  ← only *requests* this
We run:    1) geocode "Paris" -> lat=48.8566, lon=2.3522   (OpenWeather geocoding API)
           2) GET https://api.openweathermap.org/data/2.5/weather?lat=48.8566&lon=2.3522...
We send:   the real API's JSON back to the model as a tool result
Model:     "The weather in Paris is clear sky at 12.3°C."
```

---

## The four pieces in `tool_calling_homework.py`

### 1. Defining a tool — the `@tool` decorator

```python
@tool
def get_weather(city: str) -> str:
    """Get the current weather for a given city name.
    Args:
        city: name of the city, e.g. "Paris" or "Delhi".
    """
    # 1. geocode city -> lat/lon   (api.openweathermap.org/geo/1.0/direct)
    # 2. weather via lat/lon       (api.openweathermap.org/data/2.5/weather)
    # ... both keyed by OPENWEATHER_API_KEY
```

The decorator turns a plain function into a `StructuredTool`. Critically, the **name, the docstring
and the type hints become the tool's "user manual"** — that is what gets sent to the model so it knows
when and how to call it. The signature stays `city: str`: **the user always only says a city name**, and
geocoding (name → coordinates) is the tool's own first step — the model never needs to know a latitude.

### 2. The registry — mapping names back to functions

```python
tool_map = {t.name: t for t in tools}
```

The model only ever references tools **by name** (a string). `tool_map` lets us translate
`"get_weather"` back into the real Python function to execute it.

### 3. Binding tools to the model

```python
llm = ChatGroq(model="openai/gpt-oss-120b", temperature=0)
llm_with_tools = llm.bind_tools(tools)
```

Without this, the model is just a chatbot. `bind_tools` advertises the tool descriptions to the model,
so its reply can include a structured `tool_calls` request.

### 4. The message roles — how the conversation is recorded

The `messages` list is the model's working memory. Three roles matter here:

| Role | Who | Example |
|---|---|---|
| `human` | you | `HumanMessage("What is the weather in Paris?")` |
| `ai` | the model | may carry `tool_calls`, or a direct answer |
| `tool` | your code | the result of executing a tool, tagged with `tool_call_id` |

The `tool_call_id` is the glue: when the model requests 3 tools at once, each `tool` message must cite
the specific request it answers, or the model can't pair them up.

---

## Reading the script's output

Run `python tool_calling_homework.py`. Every question goes through the same loop, printed as numbered
banners. The loop is **agentic** — Step 2 repeats until the model stops asking for tools:

```
Step 1 / 3 | The user asks a question
Step 2 / 3 | The model and tools go back and forth
Step 3 / 3 | Final answer
```

- **Step 1 — the user asks a question.** The question is wrapped in a `HumanMessage`.
- **Step 2 — an agentic round loop.** The model answers; you check `ai_msg.tool_calls`:
  - `[round 1] model requested 1 tool call(s): call #1: get_weather({'city': 'Paris'})` → execute the
    tool, append the result as a `tool` message, and **go around again** with the growing history.
  - `[round N] model: no more tools needed, composing the answer.` → the loop stops and moves to Step 3.
  - If a tool keeps failing (e.g. `401 Unauthorized` for a not-yet-activated weather key), the model
    may retry it — but `max_rounds=4` caps the loop so it can never spin forever.
- **Step 3 — the final answer.** Printed as `Assistant >>> ...`. If the model emits an empty reply on a
  tool-only round, the loop falls back to the collected tool results rather than printing nothing.
- **Conversation history panel.** At the end you see the exact message list the model acted on — all
  three roles, one readable line each. This is the payoff: it shows the message passing that powers
  the whole trick.

The `[INFO]` log lines (also on screen) are the *same* loop as a machine-readable trail — registered
tools, token usage per round, which tool returned what, and when the history was resent. Together the
banners and the log tell the same story twice: once pretty, once precise.

---

## When does the model NOT call a tool?

Run the third question — `"Convert 100 INR to USD."` The model answers directly. Why? Because the
only tools available are `get_weather` and `add_numbers`; neither can help with currency, so the model
knows it must answer from what it "knows" (an approximate rate). Same for `"What is 15 plus 27?"` — an
LLM can add small numbers in its head (less reliably for big ones, though — that's exactly when
`add_numbers` becomes worth binding).

This is the honest limit of tool calling: **the model chooses tools from the menu you gave it.** Give a
richer menu and it will reach for richer tools; give it nothing and it's just a chatbot again.

---

## Make it yours — try these

1. **Done in this step:** the weather tool is now a **real API call** to OpenWeatherMap. It takes just a
   city name (like the user gives), geocodes it via `geo/1.0/direct`, then asks `data/2.5/weather` with
   the resulting `lat`/`lon`. To run it for real, grab a free key from
   https://home.openweathermap.org/api_keys and put it in `.env`:
   `OPENWEATHER_API_KEY="..."` (see `.env.example`). Without the key the tool still returns a readable
   fallback message instead of crashing.
2. **Done in this step:** a `get_stock_price(ticker: str)` tool is added — ask "What's the price of
   RELIANCE?" and the model calls `get_stock_price('RELIANCE')`. It uses **Yahoo Finance's public chart
   endpoint** (`query1.finance.yahoo.com/v8/finance/chart/...`) so **no API key is needed** — nice
   contrast with the weather tool. It tries the NSE symbol first (`RELIANCE` → `RELIANCE.NS`) and
   falls back to the bare symbol for US tickers (`AAPL`). Same lesson as the docstring in homework 1:
   the examples in the docstring teach the model how to use the tool.
3. **Done in this step:** the multi-tool demo asks for **two stock prices at once** — "What are the
   current prices of RELIANCE and TCS?" The interesting discovery: this model (`gpt-oss-120b`) issues
   one tool call per reply, **not parallel calls**. That's exactly why `run_query` is now a real agentic
   loop — round 1 fetches RELIANCE, round 2 fetches TCS, round 3 composes the answer. The output shows
   all three rounds plus a final markdown table. Same lesson as a prompt: the model decides how to use
   the tool menu, and a robust agent must tolerate the model asking for tools one at a time.
4. Set `show_history=False` on a call and watch the loop without the history panel.
5. Change `logging.basicConfig(level=logging.DEBUG)` to expose the per-tool `DEBUG` lines too.

---

*Cursor at: the weather tool's docstring*. Write it well — it's the only "manual" the model gets.