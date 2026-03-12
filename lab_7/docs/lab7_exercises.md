# Lab 7: AI Agents with the OpenAI Agents SDK

## What is an Agent?

An **agent** is an LLM that can decide *when* to call external tools, call them, observe the result, and keep reasoning until it has a final answer — all without you hard-coding the decision logic.

```
┌──────────────────────────────────────────────────────────────────────┐
│                          Agent Loop                                  │
│                                                                      │
│  User prompt ──► LLM ──► "I need to call tool X with args Y"        │
│                    ▲          │                                       │
│                    │          ▼                                       │
│                    └── Tool result ◄── Tool executes                 │
│                                                                      │
│  (loop repeats until LLM produces a final text answer)               │
└──────────────────────────────────────────────────────────────────────┘
```

The key insight: **you write the tools, the LLM decides when and how to use them**.

---

## How is this different from plain Ollama chat?

| Feature | Plain `ollama.chat()` | Agent |
|---|---|---|
| Can call functions | No | Yes |
| Knows the result of a tool | No | Yes |
| Can chain multiple steps | Only if you loop manually | Automatically |
| Needs an orchestration library | No | Yes (agents SDK) |

---

## Why the OpenAI Agents SDK?

The [OpenAI Agents SDK](https://openai.github.io/openai-agents-python/) is a lightweight, readable framework for building agents. Because Ollama exposes an **OpenAI-compatible REST API** at `http://localhost:11434/v1`, we can point the SDK there and use any local model — no OpenAI key, no cloud, no cost.

```python
from openai import AsyncOpenAI
from agents import OpenAIChatCompletionsModel

ollama_client = AsyncOpenAI(
    base_url="http://localhost:11434/v1",
    api_key="ollama",   # Ollama ignores this; the SDK requires a non-empty value
)

# Wrap the client so the SDK knows how to call it
model = OpenAIChatCompletionsModel(
    model="qwen3.5:4b",
    openai_client=ollama_client,
)
```

---

## Core Concepts

### `@function_tool`

Decorating a Python function with `@function_tool` registers it as a tool the agent can call. The SDK automatically reads the **function name**, **docstring**, and **type hints** to generate the tool description that the LLM sees.

```python
from agents import Agent, Runner, function_tool, OpenAIChatCompletionsModel
from openai import AsyncOpenAI

@function_tool
def add(a: float, b: float) -> str:
    """Add two numbers and return the result as a string."""
    return str(a + b)
```

> **Rule of thumb:** write a clear docstring — the LLM uses it to decide *when* to call your tool.

### `Agent`

An `Agent` bundles a model, a system prompt (`instructions`), and a list of tools.
Pass the `OpenAIChatCompletionsModel` object (not a plain string) so the agent uses your local Ollama instance.

```python
from agents import Agent, OpenAIChatCompletionsModel

agent = Agent(
    name="My Agent",
    instructions="You are a helpful assistant. Use tools when needed.",
    tools=[add],
    model=OpenAIChatCompletionsModel(
        model="qwen3.5:4b",
        openai_client=ollama_client,
    ),
)
```

### `Runner.run()`

`Runner.run()` starts the agent loop: send the prompt, receive a tool call (if any), execute the tool, send the result back, repeat until the model produces a final text answer.

```python
from agents import Runner

result = await Runner.run(agent, input="What is 42 + 58?")
print(result.final_output)   # "100"
```

### Multi-turn conversations

Pass the full message history as `input` instead of a single string to give the agent memory of previous turns.

```python
history = [
    {"role": "user",      "content": "My name is Sara."},
    {"role": "assistant", "content": "Nice to meet you, Sara!"},
    {"role": "user",      "content": "What is my name?"},
]
result = await Runner.run(agent, input=history)
```

---

### Pydantic models for tool inputs

The Agents SDK reads Python type hints to generate the JSON schema it sends to the LLM. Using a **Pydantic `BaseModel`** as the tool's input type lets you add constraints that plain type hints cannot express.

**When to use it:** only when you need to restrict a value beyond its basic type — for example, limiting a string to a fixed set of choices, or requiring a number to be positive.

**When NOT to use it:** for free-form strings (like a search query or a note) — plain `str` is fine and simpler.

```python
from typing import Literal
from pydantic import BaseModel

class CalculateInput(BaseModel):
    a: int
    b: int
    operation: Literal["add", "subtract", "multiply", "divide"]
    #           ^^^^^^^ the LLM sees this as an enum — it can only pick one of these
```

The SDK automatically converts the `Literal` annotation into a JSON Schema `enum`, which is included in the tool description sent to the model. If the model tries to pass a value outside the allowed set, Pydantic raises a validation error before your function even runs.

---

## Prerequisites

All Python dependencies are listed in `requirements.txt` inside `lab_7/code/`. Install them all at once:

```bash
pip install -r lab_7/code/requirements.txt
```

Pull the model you want to use:

```bash
ollama pull qwen3.5:4b
```

Make sure Ollama is running before you start:

```bash
ollama serve
```

---

## Code Examples

### Example 1 — Unit Converter + Calculator (`example_1.py`)

**What it shows:** the minimal agent pattern — define tools, create an agent, run it. Also introduces Pydantic models to constrain tool inputs.

Two tools, zero external calls:
- `convert_units` — converts between km/miles, kg/lbs, meters/feet, liters/gallons.
- `calculate` — adds, subtracts, multiplies, or divides two integers.

**Key point:** The agent decides *which* tool to use and *in which order* based on the user's question. You never write `if "convert" in question`.

The `calculate` tool uses a **Pydantic model** for its input. This locks `operation` to exactly four allowed values — the LLM cannot pass anything else:

```python
from typing import Literal
from pydantic import BaseModel

class CalculateInput(BaseModel):
    a: int
    b: int
    operation: Literal["add", "subtract", "multiply", "divide"]

@function_tool
def calculate(params: CalculateInput) -> str:
    """Perform a basic arithmetic operation (add, subtract, multiply, divide) on two integers."""
    ...
```

`Literal["add", "subtract", "multiply", "divide"]` is exposed in the tool schema sent to the LLM. The model sees it as an enum and will only pick one of those four values.

Run it:
```bash
python example_1.py
```

---

### Example 2 — Web Search Agent (`example_2.py`)

**What it shows:** tools that call external services — real web browsing, no API key.

Two tools:
- `web_search` — queries DuckDuckGo and returns titles + snippets.
- `fetch_page` — fetches the raw text of a URL for deeper reading.

The agent searches the web, picks the most relevant result, and optionally fetches the full page before answering.

```
User: "What are the latest features in Python 3.13?"

Agent loop:
  1. Calls web_search("Python 3.13 features")
  2. Reads the snippets
  3. Calls fetch_page(most relevant URL)
  4. Summarizes the page → final answer
```

Run it:
```bash
python example_2.py
```

---

### Example 3 — Study Assistant, Multi-turn (`example_3.py`)

**What it shows:** a stateful, multi-turn agent that persists data between turns.

Four tools:
- `web_search` — look things up online.
- `save_note(topic, content, source_url="")` — append a note to `notes.txt`, optionally with a source URL.
- `list_notes` — read all saved notes back.
- `clear_notes` — delete all notes.

The conversation history is accumulated in a Python list and passed to `Runner.run()` on every turn, giving the agent full context of what was said before.

```
You: Explain what an embedding is and save a note about it.

Agent loop:
  1. Calls web_search("what is an embedding in machine learning")
  2. Reads results
  3. Calls save_note("Embeddings", "An embedding is a dense vector ...")
  4. Confirms the note was saved → final answer
```

Run it:
```bash
python example_3.py
```

Sample session:
```
You: What is the transformer architecture?
Assistant: [searches web, summarizes]

You: Save a note about attention mechanisms.
Assistant: [calls save_note] Note saved under 'Attention Mechanisms'.

You: Show my notes.
Assistant: [calls list_notes] Here are your saved notes: ...

You: exit
Goodbye! Your notes are saved in notes.txt.
```

---

## How the Tool Loop Works Internally

When the LLM wants to call a tool, it responds with a special **tool-call message** instead of plain text. The SDK intercepts this, runs your Python function, and sends the result back as a **tool-result message**. The LLM then continues reasoning.

```
Message history grows with each step:

[user]         "How many miles is 5 km?"
[assistant]    tool_call: convert_units(value=5, from_unit="km", to_unit="miles")
[tool]         "5 km = 3.1069 miles"
[assistant]    "5 km is approximately 3.11 miles."   ← final_output
```

You can inspect this full trace via `result.new_items` after `Runner.run()`.

---

## Common Mistakes

| Mistake | Fix |
|---|---|
| Tool docstring is vague | Write a precise docstring — the model reads it |
| Tool returns a complex object | Return a plain `str`; the model can't read Python objects |
| Forgetting `await` | `Runner.run()` is async — always `await` it inside `async def` |
| Not passing history on turn 2+ | Accumulate messages in a list and pass the whole list each turn |
| Ollama not running | Run `ollama serve` in a separate terminal first |

---

## File Overview

| File | What it demonstrates |
|---|---|
| `example_1.py` | Basic agent, pure-Python tools, no external deps |
| `example_2.py` | Web search + page fetching, real external calls |
| `example_3.py` | Multi-turn chat, file persistence, 4 tools combined |
