from ollama import chat

MODEL = 'gemma3:1b' # MAKE SURE YOU HAVE THIS SPECIFIC MODEL INSTALLED USING 'ollma pull gemma3:1b'
TEMPERATURE = 0.3

def exercise_4_prompt_structure():
    """Compare different prompt structures for the same task."""
    
    print("\nEXERCISE 5: Prompt Structure Impact\n")
    
    prompts = {
        "Vague": "Tell me about Python",
        
        "Specific": "Explain what Python programming language is used for, in 2-3 sentences.",
        
        "Structured": """Task: Explain Python programming language
        Format: 
        - One sentence on what it is
        - One sentence on main uses
        - One sentence on why it's popular

        Keep it concise.""",
        
       "With Context": """You are a teaching assistant helping CS students.
        A student asks: "What is Python and why should I learn it?"
        Provide a clear, beginner-friendly answer in 3 sentences."""
    }
    
    for prompt_type, prompt_text in prompts.items():
        print(f"[{prompt_type}]")
        print(f"Prompt: {prompt_text}\n")
        response = chat(
            model = MODEL,
            messages=[{'role': 'user', 'content': prompt_text}],
            options={'temperature': TEMPERATURE}
        )
        print(f"Response: {response.message.content}\n")


if __name__ == "__main__":
    try:
        exercise_4_prompt_structure()
    except Exception as e:
        print(f"Error: {e}")
