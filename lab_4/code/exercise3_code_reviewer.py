"""
Exercise 9: AI Code Reviewer.
Students submit Python code and Ollama acts as a code reviewer providing feedback.
"""

import ollama
import json
from models import CodeSubmission, CodeReview

def review_code(submission: CodeSubmission, model: str = 'gemma3:1b') -> CodeReview:
    """Review code and return structured feedback."""
    
    prompt = f"""Review this Python code and provide feedback.

    FILENAME: {submission.filename}
    CODE:
    {submission.code}

    Return JSON with:
    {{
        "rating": "Good/Fair/Poor",
        "issues": ["list of problems found"],
        "suggestions": ["list of improvements"],
        "refactored_code": "improved version of the code"
    }}

    Keep it concise (2-3 points each)."""

    response = ollama.chat(
        model=model,
        messages=[{'role': 'user', 'content': prompt}],
        format='json'
    )
    
    result = json.loads(response.message.content)
    
    # The ** operator is called "dictionary unpacking" - it takes a dictionary and unpacks it into keyword arguments.
    # For example, if result = {"rating": "Fair", "issues": ["bug 1"], "suggestions": ["fix 1"], "refactored_code": "..."}
    # Then CodeReview(**result) is equivalent to:
    # CodeReview(rating="Fair", issues=["bug 1"], suggestions=["fix 1"], refactored_code="...")
    return CodeReview(**result)


def run_exercise():
    """Run the AI code reviewer."""
    print("🔍 AI CODE REVIEWER\n")
    
    # Example: Calculate average of numbers (with bug)
    code = CodeSubmission(
        filename="calculate_average.py",
        code="""
def calculate_average(numbers):
    for num in numbers:
        total = total + num
    average = total / len(numbers)
    return average
        """
    )
    
    print(f"📄 {code.filename}")
    print(code.code)
    
    review = review_code(code)
    
    print(f"\n⭐ Rating: {review.rating}")
    print("\n⚠️  Issues:")
    for issue in review.issues:
        print(f"  • {issue}")
    print("\n💡 Suggestions:")
    for suggestion in review.suggestions:
        print(f"  • {suggestion}")
    print("\n🔧 Refactored Code:")
    print(review.refactored_code)


if __name__ == "__main__":
    run_exercise()