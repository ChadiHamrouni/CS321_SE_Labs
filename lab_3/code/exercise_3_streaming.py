from ollama import chat
import time

MODEL = 'gemma3:1b' # MAKE SURE YOU HAVE THIS SPECIFIC MODEL INSTALLED USING 'ollma pull gemma3:1b'

def exercise_3_streaming():
    """Observe token-by-token generation in real-time."""
    
    print("\nEXERCISE 4: Token-by-Token Generation (Streaming)\n")
    
    prompt = "Explain how a toaster works in exactly 3 steps."
    print(f"Prompt: {prompt}\n")
    
    stream = chat(
        model = MODEL,
        messages=[{'role': 'user', 'content': prompt}],
        stream=True
    )
    
    for chunk in stream:
        print(chunk.message.content, end='', flush=True)
        time.sleep(0.05)
    
    print("\n")


if __name__ == "__main__":
    try:
        exercise_3_streaming()
    except Exception as e:
        print(f"Error: {e}")
