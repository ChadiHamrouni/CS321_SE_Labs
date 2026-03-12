from openai import AsyncOpenAI
from agents import OpenAIChatCompletionsModel

# ── Ollama client (OpenAI-compatible endpoint) ───────────────────────────────
ollama_client = AsyncOpenAI(
    base_url="http://localhost:11434/v1",
    api_key="ollama",          # Ollama ignores this but the SDK requires it
)

# Wrap the client in the SDK's model object so the agent knows how to call it
MODEL = OpenAIChatCompletionsModel(
    model="qwen3.5:4b",          # change to any tool-calling model you have pulled
    openai_client=ollama_client,
)


# ── Tools ─────────────────────────────────────────────────────────────────────
CONVERSION_TABLE: dict[str, float] = {
    "km→miles":       0.621371,
    "miles→km":       1.60934,
    "kg→lbs":         2.20462,
    "lbs→kg":         0.453592,
    "meters→feet":    3.28084,
    "feet→meters":    0.3048,
    "liters→gallons": 0.264172,
    "gallons→liters": 3.78541,
}

# ── Tool call printer ─────────────────────────────────────────────────────────
def print_tool_calls(result):
    """Print every tool the agent called during this run."""
    for item in result.new_items:
        if item.type == "tool_call_item":
            raw = item.raw_item
            print(f"   🔧 Tool called: {raw.name}({raw.arguments})")
