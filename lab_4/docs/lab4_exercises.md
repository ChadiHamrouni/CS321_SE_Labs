# Lab 4: Structured Output with Pydantic and JSON Mode

## Prerequisites
- Ollama installed and running (`ollama pull gemma3:1b`)
- Python libraries: `pip install ollama pydantic`

## Overview
This lab teaches you how to get **structured, reliable output** from LLMs using Pydantic models and JSON mode. You'll build three practical applications that demonstrate real-world LLM usage patterns.

## Exercise Files
All exercises are in `lab_4/code/`:

1. **exercise1_pydantic.py** - RAG system with Pydantic models for type-safe data
2. **eexercise2_sentiment_analyzer.py** - Extract sentiment from reviews using JSON mode
3. **exercise3_code_reviewer.py** - Automated code review with structured feedback

## Running Exercises

```bash
python exercise1_pydantic.py      # RAG with Pydantic
python eexercise2_sentiment_analyzer.py  # Sentiment analysis
python exercise3_code_reviewer.py # Code reviewer
```

---

## Exercise 1: RAG with Ollama + Pydantic Models

**File:** `exercise1_pydantic.py`

**Concept:** Retrieval-Augmented Generation (RAG) lets LLMs answer questions using a private database. Pydantic models ensure your data has the correct structure and types.

**What You'll Build:** A RAG system that searches documents and uses Ollama to generate answers, with type-safe Pydantic models for all data structures.

### Pydantic Models (Already Defined in `rag_models.py`)

**RAGEDocument:**
- `doc_id`: str
- `content`: str

**RAGQuery:**
- `query`: str
- `top_k`: int (default=2)

**RetrievedDocument:**
- `doc_id`: str
- `similarity`: float
- `content`: str

**QueryResponse:**
- `query`: str
- `retrieved_docs`: List[RetrievedDocument]
- `context`: str
- `answer`: str

### Method 1: `text_to_vector(self, text: str) -> List[int]`
**Goal**: Convert text into a binary vector based on vocabulary.
- **Input**: `text` (string)
- **Output**: `vector` (list of 0s and 1s)
- **Logic**: For each word in `self.vocabulary`, check if it appears in the text. If yes, add `1` to the vector; otherwise add `0`.
- **Example**:
  - vocabulary: `["revenue", "software", "storage"]`
  - text: `"The revenue was 50 million"`
  - **Returns**: `[1, 0, 0]`

### Method 2: `cosine_similarity(self, vec1: List[int], vec2: List[int]) -> float`
**Goal**: Calculate similarity score between two vectors (0.0 to 1.0).
- **Input**: `vec1` (list), `vec2` (list)
- **Output**: `score` (float)
- **Logic**:
  1. Calculate **dot product**: Sum of `vec1[i] * vec2[i]` for all indices
  2. Calculate **magnitudes**: `sqrt(sum(x² for x in vec))`
  3. **Formula**: `dot_product / (mag1 * mag2)`
  4. Handle zero magnitudes (return 0.0)
- **Example**:
  - vec1: `[1, 0, 1]`, vec2: `[1, 1, 0]`
  - dot_product: `1*1 + 0*1 + 1*0 = 1`
  - mag1: `sqrt(1² + 0² + 1²) = 1.41`
  - mag2: `sqrt(1² + 1² + 0²) = 1.41`
  - **Returns**: `1 / (1.41 * 1.41) ≈ 0.5`

### Method 3: `retrieve_relevant_docs(self, query_obj: RAGQuery) -> List[RetrievedDocument]`
**Goal**: Find the most similar documents to the query.
- **Input**: `query_obj` (RAGQuery Pydantic model)
- **Output**: List of `RetrievedDocument` models
- **Logic**:
  1. Convert `query_obj.query` to a vector
  2. For each document in `self.database`:
     - Convert document text to vector
     - Calculate similarity with query vector
     - Create a `RetrievedDocument` object
  3. Sort by similarity (highest first)
  4. Return top `query_obj.top_k` documents
- **Example**:
  - query: `"quarterly revenue report"`
  - **Returns**: `[RetrievedDocument(doc_id="doc2", similarity=0.85, content="..."), ...]`

### Method 4: `build_context(self, retrieved_docs: List[RetrievedDocument]) -> str`
**Goal**: Format retrieved documents into a context string for the LLM.
- **Input**: `retrieved_docs` (list of RetrievedDocument)
- **Output**: `context` (string)
- **Logic**: For each document, format as: `"Document 'doc_id' (relevance: 0.XXX):\ncontent\n\n"`
- **Example**:
  ```
  Document 'doc1' (relevance: 0.900):
  Company XYZ Q3 2024 revenue reached 45.2 million.
  
  Document 'doc2' (relevance: 0.750):
  Q4 revenue was 52.8 million dollars.
  ```

### Method 5: `generate_with_ollama(self, query: str, context: str) -> str`
**Goal**: Use Ollama LLM to generate an answer based on the context.
- **Input**: `query` (string), `context` (string)
- **Output**: `answer` (string)
- **Logic**:
  1. Create a system prompt that includes the context
  2. Call `ollama.chat()` with system and user messages
  3. Return the LLM's response
- **Example**:
  - query: `"What was the Q3 revenue?"`
  - context: `"Document 'doc1'... Q3 2024 revenue reached 45.2 million"`
  - **Returns**: `"The Q3 2024 revenue was 45.2 million dollars."`

### Method 6: `generate_response(self, query_obj: RAGQuery) -> QueryResponse`
**Goal**: Complete RAG pipeline returning a structured QueryResponse model.
- **Input**: `query_obj` (RAGQuery)
- **Output**: `QueryResponse` (Pydantic model)
- **Logic**:
  1. Call `retrieve_relevant_docs()` to get similar documents
  2. Call `build_context()` to format context
  3. Call `generate_with_ollama()` to get answer
  4. Return `QueryResponse` with all the data
- **Example**: Returns a complete QueryResponse object with query, retrieved docs, context, and generated answer

---

## Exercise 2: Sentiment Analyzer with JSON Mode

**File:** `eexercise2_sentiment_analyzer.py`

**Concept:** JSON mode forces the LLM to return valid JSON, making it easy to parse structured data. Combined with Pydantic, you get reliable sentiment analysis.

**What You'll Build:** A sentiment analyzer that extracts sentiment, score, key points, and recommendations from product reviews.

### Pydantic Model (Defined in `models.py`)

**ReviewAnalysis:**
- `sentiment`: str ("positive", "negative", or "neutral")
- `score`: float (-1.0 to 1.0)
- `key_points`: List[str] (main points from review)
- `would_recommend`: bool (recommendation)

### Function: `analyze_review_solution(review_text: str, model: str = "gemma3:1b") -> ReviewAnalysis`
**Goal**: Analyze a product review and return structured sentiment data.
- **Input**: `review_text` (string), `model` (string)
- **Output**: `ReviewAnalysis` (Pydantic model)
- **Logic**:
  1. Create a system prompt that explains the JSON structure
  2. Call `ollama.chat()` with `format='json'` parameter
  3. Parse the JSON response with `json.loads()`
  4. Create `ReviewAnalysis` object using `**data` unpacking
  5. Return the ReviewAnalysis object
- **Example**:
  ```python
  review = "Love this coffee maker! Quality is outstanding."
  analysis = analyze_review_solution(review)
  # Returns: ReviewAnalysis(
  #   sentiment="positive",
  #   score=0.9,
  #   key_points=["Quality is outstanding", "User loves product"],
  #   would_recommend=True
  # )
  ```

### Key Concepts

**JSON Mode:**
```python
response = ollama.chat(
    model=model,
    messages=[...],
    format='json'  # Forces valid JSON output
)
```

**Dictionary Unpacking:**
```python
data = {"sentiment": "positive", "score": 0.9, ...}
analysis = ReviewAnalysis(**data)
# Equivalent to: ReviewAnalysis(sentiment="positive", score=0.9, ...)
```

### Test Reviews Provided

1. **Positive**: `"Love this coffee maker! Quality is outstanding. Price was steep but worth it. Highly recommend!"`
2. **Negative**: `"Very disappointed. Product arrived damaged. Customer service was rude. Would not recommend."`
3. **Neutral**: `"It's okay. Does what it should. Price is fair, quality is average. Neutral about recommending."`

---

## Exercise 3: AI Code Reviewer

**File:** `exercise3_code_reviewer.py`

**Concept:** LLMs can review code and provide structured feedback. JSON mode ensures consistent output format.

**What You'll Build:** An automated code reviewer that analyzes Python code and returns structured feedback with issues, suggestions, and refactored code.

### Pydantic Models (Defined in `models.py`)

**CodeSubmission:**
- `filename`: str
- `code`: str

**CodeReview:**
- `rating`: str ("Good", "Fair", or "Poor")
- `issues`: List[str] (problems found)
- `suggestions`: List[str] (improvements)
- `refactored_code`: str (improved version)

### Function: `review_code(submission: CodeSubmission, model: str = 'gemma3:1b') -> CodeReview`
**Goal**: Review Python code and return structured feedback.
- **Input**: `submission` (CodeSubmission model), `model` (string)
- **Output**: `CodeReview` (Pydantic model)
- **Logic**:
  1. Create a prompt asking for code review with JSON structure
  2. Call `ollama.chat()` with `format='json'`
  3. Parse JSON response with `json.loads()`
  4. Return `CodeReview(**result)` using dictionary unpacking
- **Example**:
  ```python
  code = CodeSubmission(
      filename="average.py",
      code="def calculate_average(numbers):\n    total = total + sum(numbers)"
  )
  review = review_code(code)
  # Returns: CodeReview with rating, issues, suggestions, and refactored_code
  ```

### Example Code for Testing

The exercise provides a buggy `calculate_average` function:
```python
def calculate_average(numbers):
    for num in numbers:
        total = total + num  # Bug: 'total' not initialized
    average = total / len(numbers)  # Bug: no check for empty list
    return average
```

Expected issues:
- Variable `total` used before initialization
- No check for empty list (division by zero)

---

## Key Concepts Summary

### 1. Pydantic Models
- Define structure with type hints
- Automatic validation
- Easy conversion from dictionaries

### 2. JSON Mode
```python
ollama.chat(model="gemma3:1b", messages=[...], format='json')
```
- Forces LLM to return valid JSON
- Makes parsing reliable

### 3. Dictionary Unpacking (`**`)
```python
data = {"field1": "value1", "field2": "value2"}
model = MyModel(**data)
# Same as: MyModel(field1="value1", field2="value2")
```

### 4. Type Safety
- Pydantic validates field types automatically
- Catches errors early
- Better IDE autocomplete

---

## Common Patterns

### Pattern 1: LLM with JSON Mode
```python
response = ollama.chat(
    model="gemma3:1b",
    messages=[{"role": "user", "content": prompt}],
    format='json'
)
data = json.loads(response['message']['content'])
result = MyModel(**data)
```

### Pattern 2: RAG Pipeline
```
Query → Vectorize → Find Similar Docs → Build Context → Generate Answer
```

### Pattern 3: Structured Extraction
```
Text Input → LLM with JSON Mode → Parse JSON → Pydantic Model → Type-Safe Output
```

---

## Tips for Success

1. **Always use `format='json'`** when you want structured output
2. **Define clear JSON schema** in your prompts
3. **Handle exceptions** - LLMs can occasionally produce invalid JSON
4. **Test with edge cases** - empty lists, zero values, etc.
5. **Use Pydantic validation** - let it catch type errors for you

## Next Steps

After completing these exercises, you'll be able to:
- Build RAG systems with type-safe models
- Extract structured data from unstructured text
- Create reliable LLM applications with predictable output formats
- Use Ollama for local, private AI applications
