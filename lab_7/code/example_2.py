"""
Example 2 - Agent with Web Search
----------------------------------
The agent can browse the web using DuckDuckGo (no API key needed).
It answers research questions by fetching real search results.

Install extra dep:
    pip install ddgs

Run:
    python example_2.py
"""

import httpx
from ddgs import DDGS
from agents import Agent, Runner, function_tool
from agents.tracing import set_tracing_disabled
from common import MODEL, print_tool_calls

set_tracing_disabled(True)

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
def fetch_page(url: str) -> str:
    """Fetch the plain-text content of a web page (first 3 000 characters).

    Use this after web_search when you need more detail from a specific result.
    """
    try:
        headers = {"User-Agent": "Mozilla/5.0 (research bot)"}
        response = httpx.get(url, headers=headers, timeout=10, follow_redirects=True)
        response.raise_for_status()

        # Strip HTML tags naively — good enough for snippets
        import re
        text = re.sub(r"<[^>]+>", " ", response.text)
        text = re.sub(r"\s+", " ", text).strip()
        return text[:3000]
    except Exception as e:
        return f"Could not fetch page: {e}"


# ── Agent ─────────────────────────────────────────────────────────────────────
agent = Agent(
    name="Web Research Assistant",
    instructions=(
        "You are a research assistant with access to the web. "
        "Call web_search ONCE with the best query you can form. "
        "Then immediately write your answer using the snippets returned — "
        "do NOT search again unless the results were completely empty. "
        "Cite the source URLs at the end of your answer."
    ),
    tools=[web_search, fetch_page],
    model=MODEL,
)

# ── Main ──────────────────────────────────────────────────────────────────────
async def main():
    questions = [
        "What are the latest features added to Python 3.13?",
        "What is retrieval-augmented generation and why is it useful?",
    ]

    print("\n" + "═" * 60)
    print("🌐  Web Research Agent")
    print("═" * 60)

    for i, question in enumerate(questions, 1):
        print(f"\n🔍 Question {i}: {question}")
        print("─" * 60)
        result = await Runner.run(agent, input=question)
        print_tool_calls(result)
        print(f"📝 Answer:\n")
        print(result.final_output)
        print("\n" + "─" * 60)

    print("\n✅ Done!\n")


if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
