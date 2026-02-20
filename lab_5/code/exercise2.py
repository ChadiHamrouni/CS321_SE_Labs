"""
Exercise 2: AI Bug Fix Generator
"""


from pydantic import BaseModel
from ollama import chat
import json

from exercise1 import PRReview, review_pr

class Patch(BaseModel):
    fixed_code: str
    explanation: str = ""

def generate_fix(original_code: str, review: PRReview, model="gemma3:1b") -> Patch:
    prompt = f"""
You are fixing a pull request based on the review.

Original code:
{original_code}

Review comments:
{review.model_dump_json(indent=2)}

You are fixing an existing code file.

Fix ALL critical and major issues.
Do NOT introduce new features.

STRICT RULES (DO NOT VIOLATE):
1. You MUST preserve ALL existing functions.
2. You MUST NOT delete, rename, or merge any function.
3. You MUST keep the same function signatures.
4. You MAY ONLY modify function bodies to fix issues.
5. You MUST fix only the issues listed in the review.
6. You MUST return the FULL updated code file.
7. If an issue is ambiguous, make the smallest possible change.

If you violate any rule, the output is considered incorrect.

Return ONLY valid JSON with these exact fields:
- "fixed_code": the complete fixed code as a string
- "explanation": a brief explanation of what you fixed (required, do not omit)

Example format:
{{
  "fixed_code": "def example(): pass",
  "explanation": "Fixed division by zero by adding check"
}}
"""

    response = chat(
        model=model,
        messages=[{"role": "user", "content": prompt}],
        format="json"
    )

    data = json.loads(response.message.content or "{}")
    return Patch(**data)


if __name__ == "__main__":
    buggy_code = """
            def divide_numbers(a, b):
                return a / b

            def average(nums):
                total = 0
                for n in nums:
                    total += n
                return total / len(nums)
            """
    review = review_pr(buggy_code)
    patch = generate_fix(buggy_code, review)
    print(patch.model_dump_json(indent=2))