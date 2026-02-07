from ollama import chat

MODEL = 'qwen3-coder:30b'
TEMPERATURE = 0.0

def exercise_5_tokenization_limits():
    """Test the model's ability to handle character-level operations."""
        
    test_cases = [
        ("How many letter 'm' are in the word 'gemma3'?", "2"),
        ("Reverse the letters in the word 'HELLO'", "OLLEH"),
        ("What is the 3rd letter in 'PYTHON'?", "T"),
        ("Count the number of 'e' letters in 'Tennessee'", "4")
    ]
    
    for question, correct in test_cases:
        print(f"Q: {question}")
        response = chat(
            model=MODEL,
            messages=[{'role': 'user', 'content': question}],
            options={'temperature': TEMPERATURE}
        )
        print(f"Model: {response.message.content}")
        print(f"Correct: {correct}\n")


if __name__ == "__main__":
    try:
        exercise_5_tokenization_limits()
    except Exception as e:
        print(f"Error: {e}")
