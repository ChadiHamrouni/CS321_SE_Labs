"""
Example 1 - Your First Agent: Unit Converter + Calculator
----------------------------------------------------------
Demonstrates the basics of the OpenAI Agents SDK wired to a local
Ollama model.  The agent has two simple tools (no external calls):
  - convert_units  : convert a value between common units
  - calculate      : add, subtract, multiply, or divide two integers

Run:
    python example_1.py
"""

from typing import Literal
from pydantic import BaseModel
from agents import Agent, Runner, function_tool
from agents.tracing import set_tracing_disabled
from common import MODEL, CONVERSION_TABLE, print_tool_calls

# Disable the SDK's built-in tracing (removes the OPENAI_API_KEY warning)
set_tracing_disabled(True)

@function_tool
def convert_units(value: float, from_unit: str, to_unit: str) -> str:
    """Convert a numeric value from one unit to another.

    Supported conversions: km↔miles, kg↔lbs, meters↔feet, liters↔gallons.
    """
    from_unit = from_unit.lower().strip()
    to_unit   = to_unit.lower().strip()

    factor = CONVERSION_TABLE.get(f"{from_unit}→{to_unit}")
    if factor is None:
        return f"Sorry, I don't know how to convert {from_unit} → {to_unit}."

    return f"{value} {from_unit} = {value * factor:.4f} {to_unit}"


# Pydantic model — the SDK reads Literal to restrict what the LLM can pass
class CalculateInput(BaseModel):
    a: int
    b: int
    operation: Literal["add", "subtract", "multiply", "divide"]


@function_tool
def calculate(params: CalculateInput) -> str:
    """Perform a basic arithmetic operation (add, subtract, multiply, divide) on two integers."""
    a, b, op = params.a, params.b, params.operation
    if op == "add":
        return f"{a} + {b} = {a + b}"
    if op == "subtract":
        return f"{a} - {b} = {a - b}"
    if op == "multiply":
        return f"{a} * {b} = {a * b}"
    if op == "divide":
        if b == 0:
            return "Cannot divide by zero."
        return f"{a} / {b} = {a / b}"


# ── Agent ─────────────────────────────────────────────────────────────────────
agent = Agent(
    name="Unit Converter Assistant",
    instructions=(
        "You are a helpful unit-conversion and calculation assistant. "
        "Use the provided tools to perform conversions and arithmetic. "
        "Always show the result clearly and explain any rounding."
    ),
    tools=[convert_units, calculate],
    model=MODEL,
)


# ── Main ──────────────────────────────────────────────────────────────────────
async def main():
    questions = [
        "How many miles is 100 km?",
        "How many feet is 5 meters?",
        "What is 1024 multiply by 3, and how many lbs is that in kg?",
    ]

    print("\n" + "═" * 60)
    print("🤖  Unit Converter + Calculator Agent")
    print("═" * 60)

    for i, question in enumerate(questions, 1):
        print(f"\n❓ Question {i}: {question}")
        print("─" * 60)
        result = await Runner.run(agent, input=question)
        print_tool_calls(result)
        print(f"💡 Answer:\n   {result.final_output}")
        print("─" * 60)

    print("\n✅ Done!\n")


if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
