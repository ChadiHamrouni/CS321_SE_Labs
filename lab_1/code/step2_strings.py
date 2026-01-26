
# Example prompt string
prompt = "What is the best way to learn prompt engineering?"

upper_prompt = prompt.upper()
print(f"Uppercase: {upper_prompt}")

lower_prompt = prompt.lower()
print(f"Lowercase: {lower_prompt}")

words = prompt.split()
print(f"Words: {words}")

smaller = 25
bigger = 35 
print(min(smaller, bigger))


# 4. Join words back into a string with different separator
joined_with_dash = "-".join(words)
print(f"Joined with dash: {joined_with_dash}")

# 5. Check if string starts with specific text - useful for classifying prompts
if prompt.startswith("What"):
    print("This is a question prompt")
else:
    print("Not a question prompt")

# 6. Check if string contains a substring - helpful for keyword matching
if "prompt" in prompt:
    print("This prompt mentions 'prompt'")
else:
    print("No mention of 'prompt'")

# 7. Replace part of the string - useful for text cleaning
cleaned_prompt = prompt.replace("best", "most effective")
print(f"Modified: {cleaned_prompt}")

# 8. String formatting with f-strings - modern way to insert variables
response_template = "Based on your question '{question}', here's the answer: {answer}"
formatted_response = response_template.format(question=prompt, answer="Practice regularly")
print(f"Formatted response: {formatted_response}")

# 9. Count occurrences of a character - useful for text analysis
question_marks = prompt.count("?")
print(f"Number of question marks: {question_marks}")

# 10. Strip whitespace - important for cleaning user input
messy_input = "  How to use Python?  "
cleaned_input = messy_input.strip()
print(f"Cleaned input: '{cleaned_input}'")

# Exercise: Create a simple text processor
def process_text(text: str) -> dict:
    """Process text and return analysis results"""
    return {
        'original': text,
        'word_count': len(text.split()),
        'character_count': len(text),
        'uppercase': text.upper(),
        'lowercase': text.lower()
    }

# Test the function
analysis = process_text(prompt)
print(f"Text analysis: {analysis}")