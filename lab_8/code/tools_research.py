from ddgs import DDGS
from agents import function_tool


@function_tool
def web_search(query: str, max_results: int = 3) -> str:
    """Search the web using DuckDuckGo and return the top results.

    Each result includes a title, URL, and a short snippet.
    Use this for questions that need up-to-date or factual information.
    """
    results = DDGS().text(query, max_results=max_results)
    if not results:
        return "No results found."
    lines = []
    for i, r in enumerate(results, 1):
        lines.append(f"[{i}] {r['title']}")
        lines.append(f"    URL    : {r['href']}")
        lines.append(f"    Snippet: {r['body']}\n")
    return "\n".join(lines)
