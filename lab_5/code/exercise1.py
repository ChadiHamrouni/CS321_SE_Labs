"""
Exercise 1: AI Pull Request Reviewer
"""

import ollama
import json
from pydantic import BaseModel
from typing import List

class Issue(BaseModel):
    line: int
    severity: str
    description: str


class PRReview(BaseModel):
    summary: str
    issues: List[Issue]
    approve: bool


def review_pr(code: str, model="gemma3:1b") -> PRReview:
    prompt = f"""
You are a strict senior software engineer reviewing a pull request.

Review the following Python code for:
- Bugs
- Bad practices
- Missing edge cases
- Performance issues

Code:
{code}

Return ONLY valid JSON with these exact fields:
- "summary": a short review summary string
- "issues": an array of objects, each with "line" (number), "severity" (one of: Critical, Major, Minor), and "description" (string)
- "approve": a boolean (true if no Critical or Major issues, false otherwise)

Example format:
{{
  "summary": "Code has division by zero bug",
  "issues": [
    {{"line": 1, "severity": "Critical", "description": "Division by zero possible"}}
  ],
  "approve": false
}}
"""

    response = ollama.chat(
        model=model,
        messages=[{"role": "user", "content": prompt}],
        format="json"
    )
    data = json.loads(response.message.content or "{}")
    return PRReview(**data)


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
    print(review.model_dump_json(indent=2))