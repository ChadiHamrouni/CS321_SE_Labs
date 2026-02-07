from ollama import chat

MODEL = 'gemma3:1b' # MAKE SURE YOU HAVE THIS SPECIFIC MODEL INSTALLED USING 'ollma pull gemma3:1b'

def exercise_1_temperature():
    """Experiment with different temperature settings."""
    
    prompts = [
        "give me a random number",
        "What are three unusual uses for a paperclip?",
        "Complete this phrase in an unexpected way: 'The door opened and...'"
    ]
    
    temperatures = [0.0, 0.5, 1.9]
    
    print("\nEXERCISE 1: Temperature Exploration")
    
    for prompt in prompts:
        print(f"\n{'='*60}")
        print(f"Prompt: '{prompt}'")
        print('='*60)
        
        for temp in temperatures:
            print(f"\nTemperature = {temp}:")
            response = chat(
                model=MODEL,
                messages=[{'role': 'user', 'content': prompt}],
                options={'temperature': temp, 'num_predict': 200},
                stream=False
            )
            print(f"{response['message']['content']}")
        
        print()


if __name__ == "__main__":
    exercise_1_temperature()
