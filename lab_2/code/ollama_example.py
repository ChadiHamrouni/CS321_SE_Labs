
import ollama

def generate_response(system_prompt: str, user_prompt: str) -> str:
    """Generate a response using system and user prompts with Ollama."""
    messages = [
        {'role': 'system', 'content': system_prompt},
        {'role': 'user', 'content': user_prompt}
    ]
    response = ollama.chat(model='functiongemma', messages=messages)
    return response['message']['content']


if __name__ == "__main__":
    # Example 1: Simple Q&A
    system_prompt1 = "You are a helpful assistant that answers questions clearly and concisely."
    user_prompt1 = "What is the capital of France?"
    response1 = generate_response(system_prompt1, user_prompt1)
    print(f"Response: {response1}\n")
