from agents import function_tool


@function_tool
def summarise(text: str, max_sentences: int = 3) -> str:
    """Summarise a block of text in a given number of sentences.

    Use this when the user wants a shorter version of something they pasted.
    """
    sentences = [s.strip() for s in text.replace("\n", " ").split(".") if s.strip()]
    chosen = sentences[:max_sentences]
    return ". ".join(chosen) + ("." if chosen else "")


@function_tool
def improve_writing(text: str) -> str:
    """Return a prompt asking the LLM to improve the clarity and grammar of text.

    The tool itself just structures the request — the LLM does the rewriting.
    """
    return f"Please rewrite the following for clarity and grammar:\n\n{text}"
