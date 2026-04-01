from openai import AsyncOpenAI
from agents import OpenAIChatCompletionsModel

# ── Ollama client (OpenAI-compatible endpoint) ───────────────────────────────
ollama_client = AsyncOpenAI(
    base_url="http://localhost:11434/v1",
    api_key="ollama",          # Ollama ignores this but the SDK requires it
)

# Shared model for all agents
MODEL = OpenAIChatCompletionsModel(
    model="qwen3.5:4b",        # change to any tool-calling model you have pulled
    openai_client=ollama_client,
)


# ── Result printer ───────────────────────────────────────────────────────────
def print_tool_calls(result):
    """Print every handoff and tool call made during this run."""
    for item in result.new_items:
        if item.type == "handoff_output_item":
            print(f"   ➡️  Handoff → {item.target_agent.name}")
        elif item.type == "tool_call_item":
            raw = item.raw_item
            print(f"   🔧 Tool called: {raw.name}({raw.arguments})")
