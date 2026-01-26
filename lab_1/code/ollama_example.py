# Ollama Python Example - Introducing Prompting
# This file demonstrates prompting with Ollama: using system prompts to set behavior and user prompts for queries.
# Prerequisites: Install Ollama, pull a model (e.g., ollama pull gemma3), install library (pip install ollama)

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
    
    print(f"Example 1 - System: {system_prompt1}")
    print(f"User: {user_prompt1}")
    print(f"Response: {response1}\n")

    # Example 2: RAG-style with context
    system_prompt2 = "You are an expert in Python programming. Answer based on the provided context."
    user_prompt2 = "What are the main features of Python?"
    context = "Python is a high-level, interpreted programming language known for its simplicity, readability, and extensive libraries for data science, web development, and AI."
    full_user_prompt = f"Context: {context}\n\nQuestion: {user_prompt2}"
    
    response2 = generate_response(system_prompt2, full_user_prompt)
    
    print(f"Example 2 - System: {system_prompt2}")
    print(f"User: {user_prompt2}")
    print(f"Context: {context}")
    print(f"Response: {response2}")