import logging
import os

import requests
from dotenv import load_dotenv
from langchain_core.messages import HumanMessage
from langchain_core.tools import tool
from langchain_groq import ChatGroq

load_dotenv()

# --- Logging: the technical event trail --------------------------------------
# INFO shows the tool-calling loop step by step; DEBUG adds tool internals.
# The library HTTP logs are silenced so they don't clutter the course trail.
for _noisy in ("httpx", "httpcore", "urllib3", "openai", "langsmith"):
    logging.getLogger(_noisy).setLevel(logging.WARNING)

logging.basicConfig(
    level=logging.INFO,
    format="[%(levelname)s] tool_calling | %(message)s",
)
log = logging.getLogger(__name__)

# --- Console formatting: the clean walkthrough --------------------------------
WIDTH = 74


def banner(step: str, title: str) -> None:
    """Print a section header so each phase of the loop is visually separated."""
    print(f"\n{'=' * WIDTH}")
    print(f"  {step}  |  {title}")
    print(f"{'=' * WIDTH}")


def summarize(message) -> str:
    """Collapse one message into a single readable line for the history panel."""
    if isinstance(message, dict):
        role = message.get("role", "?")
        content = str(message.get("content", ""))
    else:
        role = message.type
        content = str(message.content)
        calls = getattr(message, "tool_calls", None)
        if calls:
            content = content or ""
            content += (
                f" [tool calls: {', '.join(c['name'] + str(c['args']) for c in calls)}]"
            )
    one_line = content.replace("\n", " ").strip()
    if len(one_line) > 100:
        one_line = one_line[:100] + "..."
    return f"{role:12} | {one_line}"


def log_tokens(response) -> None:
    """Log how many tokens each model call consumed (hidden behind INFO)."""
    usage = getattr(response, "response_metadata", {}).get("token_usage", {})
    log.info(
        "tokens used: in=%s out=%s total=%s",
        usage.get("prompt_tokens"),
        usage.get("completion_tokens"),
        usage.get("total_tokens"),
    )


# --- 1. Define the tools the model is allowed to call --------------------------
# The @tool decorator turns a plain Python function into a tool whose name,
# description and argument schema (from the docstring + type hints) are sent
# to the model. The model never runs the function itself — it only *requests*
# a call, and we execute it locally below.


OPENWEATHER_WEATHER_URL = "https://api.openweathermap.org/data/2.5/weather"
OPENWEATHER_GEOCODE_URL = "http://api.openweathermap.org/geo/1.0/direct"


@tool
def get_weather(city: str) -> str:
    """Get the current weather for a given city name.

    Args:
        city: name of the city, e.g. "Paris" or "Delhi".
    """
    log.debug("get_weather(city=%r) executing", city)
    api_key = os.getenv("OPENWEATHER_API_KEY")
    if not api_key:
        return "Cannot fetch weather: OPENWEATHER_API_KEY is missing from .env"

    # 1. Geocode the city name into coordinates (the user only gives a name).
    try:
        geo_resp = requests.get(
            OPENWEATHER_GEOCODE_URL,
            params={"q": city, "limit": 1, "appid": api_key},
            timeout=10,
        )
        geo_resp.raise_for_status()
    except requests.RequestException as err:
        return f"Cannot find coordinates for {city!r}: {err}"

    matches = geo_resp.json()
    if not matches:
        return f"Cannot fetch weather: no city found matching {city!r}"

    lat, lon = matches[0]["lat"], matches[0]["lon"]
    log.debug("geocoded %r -> lat=%s lon=%s", city, lat, lon)

    # 2. Ask the weather API for that spot.
    try:
        weather_resp = requests.get(
            OPENWEATHER_WEATHER_URL,
            params={"lat": lat, "lon": lon, "appid": api_key, "units": "metric"},
            timeout=10,
        )
        weather_resp.raise_for_status()
    except requests.RequestException as err:
        return f"Cannot fetch weather for {city!r}: {err}"

    data = weather_resp.json()
    temp = data["main"]["temp"]
    feels_like = data["main"]["feels_like"]
    description = data["weather"][0]["description"]
    return (
        f"The weather in {data.get('name') or city} is {description} at {temp:.1f}°C "
        f"(feels like {feels_like:.1f}°C)."
    )


@tool
def add_numbers(a: int, b: int) -> int:
    """Add two integers together.

    Args:
        a: the first number.
        b: the second number.
    """
    log.debug("add_numbers(a=%r, b=%r) executing", a, b)
    return a + b


STOCK_QUOTE_URL = "https://query1.finance.yahoo.com/v8/finance/chart/{ticker}"


@tool
def get_stock_price(ticker: str) -> str:
    """Get the current price of a stock from Yahoo Finance (no API key needed).

    Args:
        ticker: the stock ticker, e.g. "RELIANCE" for Reliance Industries on NSE,
                or a fully-qualified symbol like "AAPL" for US markets.
                Indian tickers without an exchange suffix get ".NS" (NSE) appended.
    """
    log.debug("get_stock_price(ticker=%r) executing", ticker)

    # No exchange suffix? Try NSE first (e.g. RELIANCE -> RELIANCE.NS),
    # then fall back to the bare symbol (e.g. AAPL on US markets).
    symbol = ticker.upper()
    candidates = [symbol] if "." in symbol else [f"{symbol}.NS", symbol]

    last_error = None
    for candidate in candidates:
        try:
            resp = requests.get(
                STOCK_QUOTE_URL.format(ticker=candidate),
                headers={"User-Agent": "Mozilla/5.0"},
                timeout=10,
            )
            resp.raise_for_status()
            symbol = candidate
            break
        except requests.RequestException as err:
            last_error = err
    else:
        return f"Cannot fetch price for {ticker!r}: {last_error}"

    data = resp.json().get("chart", {})
    if data.get("error"):
        return f"Cannot fetch price for {ticker!r}: {data['error']}"

    meta = (data.get("result") or [{}])[0].get("meta", {})
    price = meta.get("regularMarketPrice")
    if price is None:
        return (
            f"Cannot fetch price for {ticker!r}: no price returned (check the ticker)"
        )

    name = meta.get("shortName") or symbol
    currency = meta.get("currency") or ""
    change = meta.get("regularMarketChange") or 0.0
    change_pct = meta.get("regularMarketChangePercent") or 0.0
    return (
        f"The current price of {name} ({symbol}) is {currency} {price:.2f} "
        f"({change:+.2f} / {change_pct:+.2f}% today)."
    )


# Tool registry: a dict so the model's requested name maps to the real function.
tools = [get_weather, add_numbers, get_stock_price]
tool_map = {t.name: t for t in tools}
log.info("registered %d tool(s): %s", len(tools), ", ".join(tool_map))

llm = ChatGroq(model="openai/gpt-oss-120b", temperature=0)
llm_with_tools = llm.bind_tools(tools)


# --- 2. The tool-calling loop --------------------------------------------------
def run_query(question: str, show_history: bool = True, max_rounds: int = 4) -> str:
    """Send one question through the full tool-calling loop.

    This is an *agentic* loop, not a fixed two-step script: the model keeps
    getting the growing conversation back until it stops requesting tools and
    produces a final answer. One tool at a time is fine — the loop simply goes
    around again (see the two-stock demo).

    Returns the model's final answer as text. When *show_history* is True the
    conversation is printed at the end, so you can see exactly how each tool
    result gets plugged back into the message list.
    """
    messages = [HumanMessage(question)]

    # Phase 1: the user asks a question.
    banner("Step 1 / 3", "The user asks a question")
    print(f"\n  You       >>> {question}\n")

    # Phases 2 + 3: round-trip with the model until it stops calling tools.
    banner("Step 2 / 3", "The model and tools go back and forth")
    final_message = None
    for round_no in range(1, max_rounds + 1):
        log.info(
            "round %d: sending %d message(s) to the model", round_no, len(messages)
        )
        ai_msg = llm_with_tools.invoke(messages)
        messages.append(ai_msg)
        last_ai_message = ai_msg
        log_tokens(ai_msg)

        if not ai_msg.tool_calls:
            # No more tools wanted — this round's text is the final answer.
            log.info(
                "round %d: model made no tool call -> answering directly", round_no
            )
            final_message = ai_msg
            tool_msg = "no tools needed" if round_no == 1 else "no more tools needed"
            print(f"\n  [round {round_no}] model: {tool_msg}, composing the answer.\n")
            break

        print(
            f"\n  [round {round_no}] model requested {len(ai_msg.tool_calls)} tool call(s):"
        )
        for i, call in enumerate(ai_msg.tool_calls, start=1):
            print(f"    call #{i}: {call['name']}({call['args']})")

            selected_tool = tool_map[call["name"]]
            tool_result = selected_tool.invoke(call["args"])
            print(f"    result: {tool_result}")
            log.info(
                "round %d: tool %r returned %r", round_no, call["name"], tool_result
            )

            # Tool output is fed back as a 'tool' message, matched to the request
            # by its tool_call_id.
            messages.append(
                {
                    "role": "tool",
                    "content": str(tool_result),
                    "tool_call_id": call["id"],
                }
            )
            log.debug("appended tool message (tool_call_id=%r)", call["id"])
    else:
        log.warning("hit %d rounds without a final answer", max_rounds)
        # The last AI message is the best we have; try to answer from it anyway.
        final_message = last_ai_message

    # Phase 4: show the final answer.
    banner("Step 3 / 3", "Final answer")
    answer = final_message.content
    if not answer or not str(answer).strip():
        # Sometimes a reasoning model returns no visible text on a tool round.
        results = [
            m["content"]
            for m in messages
            if isinstance(m, dict) and m.get("role") == "tool"
        ]
        answer = (
            " ".join(results) if results else "The model did not produce a text answer."
        )
        log.info("empty model answer -> fell back to tool results")
    print(f"\n  Assistant  >>> {answer}\n")

    if show_history:
        show_conversation(messages)
    return str(answer)


def show_conversation(messages: list) -> None:
    """Print the message list the model acted on, one readable line per entry."""
    banner("Conversation history", "What the model actually saw")
    print()
    for msg in messages:
        print(f"  {summarize(msg)}")
    print()
    log.info("conversation shown: %d message(s)", len(messages))


# --- 3. Demo: run the same loop on five different questions -------------------
if __name__ == "__main__":
    print("#" * WIDTH)
    print("#  TOOL CALLING  -  the same loop, five questions")
    print("#")
    print(
        "#  1. weather needs a tool            -> get_weather      (real OpenWeather API)"
    )
    print(
        "#  2. stock price needs a tool        -> get_stock_price  (Yahoo Finance, no key)"
    )
    print("#  3. TWO stock prices -> TWO tool calls in ONE reply     (multi-tool demo)")
    print("#  4. arithmetic may need a tool      -> add_numbers")
    print("#  5. currency has no tool            -> model answers directly")
    print("#" * WIDTH)

    run_query("What is the weather in Paris?")
    run_query("What is the price of RELIANCE?")
    run_query("What are the current prices of RELIANCE and TCS?")
    run_query("What is 15 plus 27?")
    run_query("Convert 100 INR to USD.")
