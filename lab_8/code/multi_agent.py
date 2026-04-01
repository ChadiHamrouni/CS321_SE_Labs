"""
Lab 8 - Multi-Agent System (Triage + 3 Specialists)
-----------------------------------------------------
Entry point. Runs the conversation loop.

Three specialist agents:
  - Research Agent  : searches the web for information
  - Math Agent      : solves arithmetic and unit conversions
  - Writing Agent   : improves, summarises, or translates text

The triage agent never answers itself — it only routes.

Install deps:
    pip install -r lab_8/code/requirements.txt

Run:
    python multi_agent.py
"""

import asyncio
from agents import Runner
from agents.tracing import set_tracing_disabled

from agents_config import print_tool_calls
from specialist_agents import triage_agent

set_tracing_disabled(True)


async def chat():
    print("\n" + "═" * 60)
    print("🤖  Multi-Agent System  (Triage + Research / Math / Writing)")
    print("═" * 60)
    print("💬  Type your message. The triage agent routes it automatically.")
    print("🔍  Research  |  🔢  Math  |  ✍️   Writing")
    print("─" * 60 + "\n")

    while True:
        user_input = input("🧑 You: ").strip()
        if user_input.lower() in ("exit", "quit"):
            print("\n👋  Goodbye!")
            break
        if not user_input:
            continue

        result = await Runner.run(triage_agent, input=user_input)
        print_tool_calls(result)

        print(f"\n🤖 Agent:\n   {result.final_output}\n")
        print("─" * 60)


if __name__ == "__main__":
    asyncio.run(chat())
