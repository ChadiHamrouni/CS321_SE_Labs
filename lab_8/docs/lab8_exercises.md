# Lab 8: Multi-Agent Systems

## What is a Multi-Agent System?

A **multi-agent system** is a group of specialised agents coordinated by a **triage (router) agent**. Instead of one agent that does everything, each agent is an expert at a narrow task.

```
┌─────────────────────────────────────────────────────────────────┐
│                     Multi-Agent Flow                            │
│                                                                 │
│  User message                                                   │
│       │                                                         │
│       ▼                                                         │
│  ┌──────────────┐                                               │
│  │ Triage Agent │  ← reads message, picks a specialist         │
│  └──────┬───────┘                                               │
│         │  handoff                                              │
│    ┌────┴────────────────────┐                                  │
│    ▼            ▼            ▼                                  │
│ Research      Math        Writing                               │
│  Agent        Agent        Agent                                │
│    │            │            │                                  │
│    └────────────┴────────────┘                                  │
│                 │                                               │
│            Final answer                                         │
└─────────────────────────────────────────────────────────────────┘
```

The key insight: **the triage agent never answers — it only routes**. Each specialist owns its own tools and system prompt.

---

## Why Multiple Agents?

| Single Agent | Multi-Agent |
|---|---|
| One system prompt for everything | Each agent has a focused role |
| Tools pile up and confuse the LLM | Only relevant tools per agent |
| Hard to maintain | Swap/add specialists independently |

---

## How Handoffs Work

The agents SDK `handoff()` primitive lets an agent transfer control to another agent mid-conversation. The triage agent has no tools — it only has handoffs.

```python
from agents import handoff

triage_agent = Agent(
    name="Triage Agent",
    instructions="Route to the right specialist. Do not answer yourself.",
    handoffs=[
        handoff(research_agent),
        handoff(math_agent),
        handoff(writing_agent),
    ],
    model=MODEL,
)
```

When the triage agent decides to route, the SDK:
1. Calls the handoff (looks like a tool call internally)
2. Passes the conversation to the specialist
3. The specialist runs its own agent loop with its own tools
4. Returns the final answer to the user

---

## Agents in This Lab

### Triage Agent (router)
- **Tools:** none
- **Handoffs:** research, math, writing
- **Role:** read the user's intent and pick a specialist

### Research Agent
- **Tools:** `web_search`
- **Role:** answer factual/current questions by searching DuckDuckGo

### Math Agent
- **Tools:** `calculate`, `convert_units`
- **Role:** arithmetic and unit conversions

### Writing Agent
- **Tools:** `summarise`, `improve_writing`
- **Role:** shorten, polish, or translate text

---

## Prerequisites

```bash
pip install -r lab_8/code/requirements.txt
ollama pull qwen3.5:4b
ollama serve
```

---

## Running the System

```bash
cd lab_8/code
python multi_agent.py
```

---

## Sample Session

```
🧑 You: What is 250 miles in km?
   🔧 Tool called: transfer_to_math_agent(...)
   🔧 Tool called: convert_units({"value": 250, "from_unit": "miles", "to_unit": "km"})
🤖 Agent: 250 miles = 402.335 km

🧑 You: What are the key features of Python 3.13?
   🔧 Tool called: transfer_to_research_agent(...)
   🔧 Tool called: web_search({"query": "Python 3.13 key features"})
🤖 Agent: Python 3.13 introduces... [summarised from web]

🧑 You: Summarise this: "Large language models are neural networks trained on..."
   🔧 Tool called: transfer_to_writing_agent(...)
   🔧 Tool called: summarise({"text": "..."})
🤖 Agent: Large language models are neural networks trained on vast text data.
```

---

## Exercises

### Exercise 1 — Add a Fourth Agent

Add a **Code Agent** that can:
- `run_python(code: str)` — execute a small Python snippet and return its output
- Route to it when the user asks to write or run code

Steps:
1. Define the tool `run_python` (use `subprocess` or `exec`)
2. Create `code_agent` with that tool
3. Add it to the triage agent's `handoffs` list
4. Update the triage instructions to include the routing rule

### Exercise 2 — Stateful Research

Modify the Research Agent to also have `save_note` and `list_notes` tools from Lab 7, so users can save what they find across turns.

Pass a `history` list to `Runner.run()` (like in Lab 7 Example 3) to enable multi-turn memory.

### Exercise 3 — Trace the Handoff

After `Runner.run()`, inspect `result.new_items` and print:
- Which agent handled the request (look for `handoff_output_item`)
- All tool calls made by the specialist

This gives you full visibility into the routing decision.

---

## Common Mistakes

| Mistake | Fix |
|---|---|
| Triage agent answers instead of routing | Its instructions must say "do not answer, only route" |
| Specialist can't find its tool | Make sure tools are in the specialist's `tools=[]`, not the triage's |
| Vague triage instructions | Give clear per-agent routing rules in the triage system prompt |
| Forgetting `await` | `Runner.run()` is async — always `await` inside `async def` |

---

## File Overview

| File | What it demonstrates |
|---|---|
| `agents_config.py` | Shared Ollama client and MODEL (same pattern as Lab 7 `common.py`) |
| `multi_agent.py` | Triage agent + 3 specialists with handoffs |
