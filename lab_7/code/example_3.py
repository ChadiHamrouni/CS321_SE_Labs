"""
Example 3 - Study Assistant (multi-turn, web + notes)
------------------------------------------------------
A full study assistant that combines:
  - web_search   : look up anything online
  - save_note    : persist a study note to notes.txt
  - list_notes   : read back saved notes
  - summarize_notes : ask the agent to turn your notes into a study sheet

The conversation loop runs until the user types 'exit'.

Install extra dep:
    pip install ddgs

Run:
    python example_3.py
"""

from pathlib import Path
from ddgs import DDGS
from agents import Agent, Runner, function_tool
from agents.tracing import set_tracing_disabled

from common import MODEL, print_tool_calls

set_tracing_disabled(True)

# Notes are stored in the same directory as this script
NOTES_FILE = Path(__file__).parent / "notes.txt"


# ── Tools ─────────────────────────────────────────────────────────────────────
@function_tool
def web_search(query: str, max_results: int = 3) -> str:
    """Search the web using DuckDuckGo and return the top results.

    Each result contains a title, URL, and a short snippet.
    Use this to answer questions that require up-to-date information.
    """
    results = DDGS().text(query, max_results=max_results)
    if not results:
        return "No results found."

    lines = []
    for i, r in enumerate(results, 1):
        lines.append(f"[{i}] {r['title']}")
        lines.append(f"    URL  : {r['href']}")
        lines.append(f"    Snippet: {r['body']}\n")

    return "\n".join(lines)


@function_tool
def save_note(topic: str, content: str, source_url: str = "") -> str:
    """Save a study note under a topic heading.

    Notes are appended to notes.txt so they persist between sessions.
    Use this whenever the user wants to remember something important.
    If the content came from a web search result, pass the source URL so it is saved as a reference.
    """
    with NOTES_FILE.open("a", encoding="utf-8") as f:
        f.write(f"\n## {topic}\n{content}\n")
        if source_url:
            f.write(f"Source: {source_url}\n")
    return f"Note saved under '{topic}'."


@function_tool
def list_notes() -> str:
    """Return all saved study notes from notes.txt.

    Call this when the user asks what they have saved or wants to review notes.
    """
    if not NOTES_FILE.exists() or NOTES_FILE.stat().st_size == 0:
        return "No notes saved yet."
    return NOTES_FILE.read_text(encoding="utf-8")


@function_tool
def clear_notes() -> str:
    """Delete all saved notes (irreversible). Ask the user to confirm first."""
    if NOTES_FILE.exists():
        NOTES_FILE.unlink()
    return "All notes have been cleared."


# ── Agent ─────────────────────────────────────────────────────────────────────
agent = Agent(
    name="Study Assistant",
    instructions=(
        "You are a personal study assistant helping a university student. "
        "You can search the web for information, save notes on topics the user "
        "wants to remember, and review their saved notes. "
        "\n\nGuidelines:\n"
        "- If the user asks you to research a topic, use web_search.\n"
        "- If the user says 'save this' or 'note that', call save_note with a "
        "  concise topic heading and the content to store.\n"
        "- If the user asks 'what have I saved' or 'show my notes', call list_notes.\n"
        "- Be concise and student-friendly. Explain jargon when you use it."
    ),
    tools=[web_search, save_note, list_notes, clear_notes],
    model=MODEL,
)


# ── Conversation loop ─────────────────────────────────────────────────────────
async def chat():
    print("\n" + "═" * 60)
    print("📚  Study Assistant")
    print("═" * 60)
    print("💬  Chat with your assistant. Type 'exit' to quit.")
    print("📌  Tips: ask it to search the web, save notes, or show your notes.")
    print("─" * 60 + "\n")

    history: list[dict] = []          # keep the full conversation in memory

    while True:
        user_input = input("🧑 You: ").strip()
        if user_input.lower() in ("exit", "quit"):
            print("\n" + "─" * 60)
            print("👋  Goodbye! Your notes are saved in notes.txt.")
            print("═" * 60 + "\n")
            break
        if not user_input:
            continue

        # Append the new message to history so the agent has context
        history.append({"role": "user", "content": user_input})

        result = await Runner.run(agent, input=history)
        print_tool_calls(result)

        reply = result.final_output
        print(f"\n🤖 Assistant:\n   {reply}\n")
        print("─" * 60)

        # Add assistant reply to history for the next turn
        history.append({"role": "assistant", "content": reply})


if __name__ == "__main__":
    import asyncio
    asyncio.run(chat())
