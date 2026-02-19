
# Lab 5: AI Pull Request Reviewer with Pydantic and JSON Mode

## Prerequisites
- Ollama installed and running (`ollama pull gemma3:1b`)
- Python libraries: `pip install ollama pydantic`

## Overview
This lab teaches you how to build a **reliable, structured AI code review system** using Pydantic models and JSON mode. You'll create a multi-step pipeline that reviews, fixes, and re-reviews code until it is approved.

## Exercise Files
All exercises are in `lab_5/code/`:

1. **exercise1.py** - PR reviewer with Pydantic models
2. **exercise2.py** - AI bug fix generator
3. **exercise3.py** - Self-rechecking PR loop

## Running Exercises

```bash
python exercise1.py      # PR reviewer
python exercise2.py      # Bug fix generator
python exercise3.py      # Self-rechecking PR loop
```

---

## Exercise 1: Define Structured Review Output

**File:** `exercise1.py`

**Concept:** Never trust free-text outputs. Use Pydantic models to define the structure of your review data.

### Pydantic Models (Already Defined)

**Issue:**
- `line`: int (line number where the issue occurs)
- `severity`: str ("Critical", "Major", or "Minor")
- `description`: str (short explanation of the issue)

**PRReview:**
- `summary`: str (short overall feedback)
- `issues`: List[Issue]
- `approve`: bool (should this PR be approved?)

### Function: `review_pr(code: str, model: str = "gemma3:1b") -> PRReview`
**Goal**: Send code to the LLM and receive structured JSON, validated by Pydantic.
- Use `format="json"` in the Ollama call
- Parse the output
- Validate using Pydantic
- If validation fails, raise the error

---

## Exercise 2: Generate a Fix from Review

**File:** `exercise2.py`

**Concept:** Use the review output to generate improved code, fixing only the issues found.

### Pydantic Model (Already Defined)

**Patch:**
- `fixed_code`: str (the corrected version of the code)
- `explanation`: str (what was fixed and why)

### Function: `generate_fix(original_code: str, review: PRReview, model: str = "gemma3:1b") -> Patch`
**Goal**: Use the review output to generate improved code.
- Fix all **Critical** and **Major** issues
- Do **not** add new features
- Do **not** change functionality unnecessarily
- Return **JSON only**
- Validate with your `Patch` model

---

## Exercise 3: Self-Rechecking PR Loop

**File:** `exercise3.py`

**Concept:** Real engineering teams review and fix code iteratively. Build a loop that keeps reviewing until the PR is approved or a maximum number of rounds is reached.

### Function: `review_until_fully_approved(code_str: str) -> str`
**Goal**: Review code iteratively until all major/critical issues are resolved.
- Start with the original code
- Run `review_pr`
- If `approve == True`, stop
- Otherwise, generate a fix and review again
- Repeat up to a maximum number of rounds

### Output
- Print each review round
- Print each patch explanation
- Print the final code

---

## Part 4: Testing the System

At the bottom of your file:
- Create a deliberately buggy function (e.g., division without zero check, averaging empty lists, mutating default arguments, inefficient loops, missing return statements)
- Run your `review_until_fully_approved` function

## Reflection Questions

After running your system, answer:
- Did the AI ever hallucinate issues?
- Did it miss obvious bugs?
- Did it solve the issue partially (fix one function while ignoring another one)
- Did it fix something incorrectly?
- Was severity classification consistent?
- How deterministic were the results?

---

## Bonus Challenge (Optional)
- Add automatic retry if JSON parsing fails
- Add severity scoring (`Critical = 3`, `Major = 2`, `Minor = 1`)
- Stop early if no Critical issues remain
- Compare performance between two models

---

## What This Lab Is Really About

This is **not** about reviewing Python code.  
This lab is about:
- Structured outputs
- Prompt contracts
- LLM reliability
- Multi-step pipelines
- Self-correction systems

You are designing an **AI system** — not just writing a prompt.

---

## Final Expected Architecture

By the end, your file should contain:
- Pydantic models
- `review_pr`
- `generate_fix`
- `review_until_fully_approved`
- A runnable main section

If your system works correctly, it should behave like a minimal AI GitHub reviewer.
