"""
Lab 8 - Multi-Agent Examples
------------------------------
Three hardcoded prompts — one per specialist agent — so you can see
exactly which agent the triage routes to and what tools it calls.

Run:
    python examples.py
"""

import asyncio
from agents import Runner
from agents.tracing import set_tracing_disabled

from agents_config import print_tool_calls
from specialist_agents import triage_agent

set_tracing_disabled(True)

EXAMPLES = [
    ("Math Agent",     "What is 128 * 4096?"),
    ("Research Agent", "What is the latest version of Python?"),
    ("Writing Agent",  "Summarise this: Artificial intelligence is the simulation of human intelligence by machines. It includes learning, reasoning, and self-correction. AI is used in healthcare, finance, and transportation."),
]


async def run_examples():
    print("\n" + "═" * 60)
    print("🤖  Multi-Agent Examples  (3 prompts, 3 specialists)")
    print("═" * 60 + "\n")

    for i, (expected_agent, prompt) in enumerate(EXAMPLES, 1):
        print(f"── Example {i}: {expected_agent} {'─' * (40 - len(expected_agent))}")
        print(f"🧑 Prompt: {prompt}")
        print()

        result = await Runner.run(triage_agent, input=prompt)
        print_tool_calls(result)

        print(f"\n🤖 Answer:\n   {result.final_output}\n")
        print("═" * 60 + "\n")


if __name__ == "__main__":
    asyncio.run(run_examples())
