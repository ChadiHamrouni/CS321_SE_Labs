from agents import Agent, handoff

from agents_config import MODEL
from tools_research import web_search
from tools_math import calculate, convert_units
from tools_writing import summarise, improve_writing


research_agent = Agent(
    name="Research Agent",
    instructions=(
        "You are a research specialist. "
        "When the user asks a factual question or needs up-to-date information, "
        "use web_search to find the answer and summarise the results clearly. "
        "Always cite the URL of your source."
    ),
    tools=[web_search],
    model=MODEL,
)

math_agent = Agent(
    name="Math Agent",
    instructions=(
        "You are a math specialist. Answer using tools only — never compute manually.\n\n"

        "## Rules\n"
        "1. Call the tool ONCE. Never call the same tool twice for the same request.\n"
        "2. The tool result is final. Do not verify, recompute, or show manual working.\n"
        "3. Your entire response must be the tool result and nothing else.\n\n"

        "## Tool: calculate\n"
        "Use for: addition, subtraction, multiplication, division.\n\n"
        "CORRECT:\n"
        "  User: 68 * 8594567\n"
        "  → call calculate once: {a: 68, b: 8594567, operation: 'multiply'}\n"
        "  → tool returns '584430556'\n"
        "  → reply: '584430556'\n\n"
        "WRONG:\n"
        "  → calling calculate more than once\n"
        "  → showing step-by-step manual working after getting the tool result\n\n"

        "## Tool: convert_units\n"
        "Use for: km/miles, kg/lbs, meters/feet, liters/gallons.\n\n"
        "CORRECT:\n"
        "  User: How many miles is 5 km?\n"
        "  → call convert_units once: {value: 5, from_unit: 'km', to_unit: 'miles'}\n"
        "  → tool returns '5 km = 3.1069 miles'\n"
        "  → reply: '5 km = 3.1069 miles'\n\n"
        "WRONG:\n"
        "  → calling convert_units more than once\n"
        "  → manually computing the conversion after the tool responds"
    ),
    tools=[calculate, convert_units],
    model=MODEL,
)

writing_agent = Agent(
    name="Writing Agent",
    instructions=(
        "You are a writing specialist. "
        "Use summarise to shorten text the user provides. "
        "Use improve_writing when the user wants their text polished. "
        "For translation requests, translate directly without a tool."
    ),
    tools=[summarise, improve_writing],
    model=MODEL,
)

triage_agent = Agent(
    name="Triage Agent",
    instructions=(
        "You are a router. Read the user's message and hand it off to the "
        "correct specialist — do NOT answer yourself.\n\n"
        "Rules:\n"
        "- Numbers, maths, unit conversions → transfer_to_math_agent\n"
        "- Web lookups, factual/current info  → transfer_to_research_agent\n"
        "- Summarise, improve, translate text → transfer_to_writing_agent\n"
        "If the request is ambiguous, pick the closest match."
    ),
    handoffs=[
        handoff(research_agent),
        handoff(math_agent),
        handoff(writing_agent),
    ],
    model=MODEL,
)
