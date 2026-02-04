# Lab 3 Exercises

## Setup
See [SETUP.md](SETUP.md) for installation instructions.

## Running Exercises

**Individual exercises:**
```bash
python exercise_0.1.py  # Document class
python exercise_0.2.py  # RAG with Ollama
python exercise_1_temperature.py
python exercise_2_hallucinations.py
python exercise_3_streaming.py
python exercise_4_prompt_structure.py
python exercise_5_tokenization.py
```

---

## Exercise 0.1: Document Class Implementation

**File:** `exercise_0.1.py`

**Concept:** Object-oriented programming with classes to organize related data and methods.

Implement the `Document` class with the following methods:

### Method 1: `__init__(self, title: str, content: str)`
**Goal**: Initialize a Document object with title and content attributes.
- **Input**: `title` (string), `content` (string)
- **Output**: None (constructor)
- **Example**:
  ```python
  doc = Document("Q4 Revenue", "Revenue was 52.8 million dollars")
  print(doc.title)  # "Q4 Revenue"
  ```

### Method 2: `get_word_count(self) -> int`
**Goal**: Count the total number of words in the document content.
- **Input**: None (uses `self.content`)
- **Output**: `count` (integer)
- **Example**:
  - Content: `"Hello world from Python"`
  - **Returns**: `4`

### Method 3: `get_character_count(self) -> int`
**Goal**: Count the total number of characters in the document content.
- **Input**: None (uses `self.content`)
- **Output**: `count` (integer)
- **Example**:
  - Content: `"Hello"`
  - **Returns**: `5`

### Method 4: `contains_keyword(self, keyword: str) -> bool`
**Goal**: Check if a keyword exists in the document (case-insensitive).
- **Input**: `keyword` (string)
- **Output**: `found` (boolean)
- **Example**:
  - keyword: `"python"`, content: `"Python is great"`
  - **Returns**: `True`
  - keyword: `"java"`, content: `"Python is great"`
  - **Returns**: `False`

### Method 5: `get_summary(self, max_words: int = 10) -> str`
**Goal**: Return the first `max_words` words from the document as a summary.
- **Input**: `max_words` (integer, default=10)
- **Output**: `summary` (string)
- **Example**:
  - Content: `"One two three four five six"`, max_words: `3`
  - **Returns**: `"One two three..."`
  - Content: `"One two three"`, max_words: `5`
  - **Returns**: `"One two three"`

### Mock Data for Testing

```python
doc1 = Document("Q4 2024 Revenue", "Company XYZ Q4 2024 revenue reached 52.8 million dollars with 18 percent year-over-year growth.")
doc2 = Document("DataServer Pro X500", "The DataServer Pro X500 features 128GB RAM, dual Intel Xeon processors, and 8TB SSD storage capacity.")
```

---

## Exercise 0.2: RAG with Ollama Integration

**File:** `exercise_0.2.py`

**Concept:** Retrieval-Augmented Generation (RAG) combines document search with LLM text generation to answer questions using private data.

**Prerequisites:**
- Review `simple_rag.py` from Lab 2
- Understand the Document class from Exercise 0.1

Implement a `RAGWithOllama` class with the following methods:

### Method 1: `__init__(self, model: str = 'llama3.2')`
**Goal**: Initialize the RAG system with an empty database, vocabulary list, and model name.
- **Input**: `model` (string, default='llama3.2')
- **Output**: None (constructor)

### Method 2: `add_document(self, doc_id: str, content: str)`
**Goal**: Add a document to the database.
- **Input**: `doc_id` (string), `content` (string)
- **Output**: None
- **Example**:
  ```python
  rag.add_document("doc1", "Company revenue was 45.2 million")
  ```

### Method 3: `text_to_vector(self, text: str) -> List[int]`
**Goal**: Convert text to a binary vector based on vocabulary.
- **Input**: `text` (string)
- **Output**: `vector` (list of integers)
- **Example**:
  - vocabulary: `["revenue", "data", "software"]`
  - text: `"revenue report"`
  - **Returns**: `[1, 0, 0]`

### Method 4: `cosine_similarity(self, vec1: List[int], vec2: List[int]) -> float`
**Goal**: Calculate similarity score between two vectors.
- **Input**: `vec1` (list), `vec2` (list)
- **Output**: `score` (float between 0.0 and 1.0)
- **Example**:
  - vec1: `[1, 0, 1]`, vec2: `[1, 1, 0]`
  - dot_product: `1*1 + 0*1 + 1*0 = 1`
  - mag1: `sqrt(1² + 0² + 1²) = 1.41`
  - mag2: `sqrt(1² + 1² + 0²) = 1.41`
  - **Returns**: `1 / (1.41 * 1.41) ≈ 0.5`

### Method 5: `retrieve_relevant_docs(self, query: str, top_k: int = 2) -> List[Tuple[str, float]]`
**Goal**: Find the most similar documents to the query.
- **Input**: `query` (string), `top_k` (integer)
- **Output**: List of tuples `[(doc_id, score), ...]`
- **Example**:
  - query: `"quarterly revenue"`
  - **Returns**: `[("doc2", 0.85), ("doc4", 0.62)]`

### Method 6: `build_context(self, relevant_docs: List[Tuple[str, float]]) -> str`
**Goal**: Format retrieved documents into a context string for the LLM.
- **Input**: `relevant_docs` (list of tuples)
- **Output**: `context` (string)
- **Example**:
  - Input: `[("doc1", 0.9)]`
  - **Returns**: `"Document 'doc1' (relevance: 0.900):\nCompany XYZ reported Q3 revenue of 45.2 million.\n\n"`

### Method 7: `generate_with_ollama(self, query: str, context: str) -> str`
**Goal**: Generate an answer using Ollama LLM with the retrieved context.
- **Input**: `query` (string), `context` (string)
- **Output**: `response` (string)
- **Example**:
  - query: `"What was the Q3 revenue?"`
  - context: `"Document 'doc1': ...Q3 revenue of 45.2 million..."`
  - **Returns**: LLM-generated answer like `"The Q3 2024 revenue was 45.2 million dollars."`

### Method 8: `generate_response(self, query: str) -> str`
**Goal**: Main method that orchestrates retrieval and generation.
- **Input**: `query` (string)
- **Output**: `response` (string)

### Mock Data for Testing (Private Company Data)

```python
rag = RAGWithOllama(model='llama3.2')
rag.add_document("doc1", "Company XYZ Q3 2024 revenue reached 45.2 million dollars with 23 percent growth compared to Q2 2024.")
rag.add_document("doc2", "Company XYZ Q4 2024 revenue reached 52.8 million dollars with 18 percent year-over-year growth.")
rag.add_document("doc3", "The DataServer Pro X500 features 128GB RAM, dual Intel Xeon processors, and 8TB SSD storage capacity.")
rag.add_document("doc4", "Our flagship software product AutoSync Enterprise v3.2 includes real-time data synchronization and supports up to 10000 concurrent users.")
rag.add_document("doc5", "Customer satisfaction survey results show 94 percent approval rating for our technical support team in November 2024.")
rag.add_document("doc6", "The manufacturing facility in Austin produces 5000 units per month with a defect rate below 0.5 percent.")
```

### Test Queries

```python
queries = [
    "What is the RAM capacity of the DataServer Pro X500?",
    "What was the Q3 2024 revenue?",
    "What was the Q4 2024 revenue?",
    "How many concurrent users does AutoSync Enterprise support?"
]
```

---

## Exercise 1: Temperature Exploration

**File:** `exercise_1_temperature.py`

**Concept:** Temperature controls the randomness and creativity of LLM outputs.
- **Low temp (0.0)**: Deterministic, consistent, picks most likely tokens
- **High temp (1.5+)**: Creative, random, explores less likely options

Implement the following function:

### `exercise_1_temperature()`
**Goal**: Demonstrate how temperature affects LLM output consistency and creativity.
- **Logic**:
  1. Define a prompt (e.g., "Complete this sentence: The future of artificial intelligence is")
  2. Create a list of temperatures to test: `[0.0, 0.7, 1.5]`
  3. For each temperature:
     - Call `ollama.chat()` with the model, prompt, and temperature option
     - Print the temperature value
     - Print the generated response
  4. Use the `ollama` library: `from ollama import chat`
- **Input**: None
- **Output**: None (prints results to console)
- **Example**:
  ```python
  Temperature = 0.0:
  The future of artificial intelligence is promising and transformative...
  
  Temperature = 0.7:
  The future of artificial intelligence is filled with possibilities...
  
  Temperature = 1.5:
  The future of artificial intelligence is quantum-leap revolutionary...
  ```

**After implementing, run multiple times and answer:**

**Reflection Questions:**
1. Which temperature gave the most consistent results across runs?
2. Which temperature produced the most creative/varied outputs?
3. For a code generation tool, which temperature would you choose? Why?
4. For a creative story writer, which temperature would you choose? Why?

---

## Exercise 2: Hallucination Detection

**File:** `exercise_2_hallucinations.py`

**Concept:** LLMs can confidently generate false information because they predict probable text patterns, not objective truth.
- **"Truth Bias"**: Models assume prompts refer to real entities
- **Pattern Matching**: They generate responses based on training data patterns

Implement the following function:

### `exercise_3_hallucinations()`
**Goal**: Test the model with fictional or obscure questions to observe how it handles uncertainty.
- **Logic**:
  1. Create a list of test questions about fictional places, people, or obscure facts
     - Example: `"What is the capital of the fictional country Wakanda?"`
     - Example: `"Tell me about the Glarbnax Festival celebrated in ancient Rome"`
  2. For each question:
     - Call `ollama.chat()` with the model and question
     - Print the question
     - Print the model's response
     - Observe whether it admits uncertainty or fabricates information
  3. Use the `ollama` library: `from ollama import chat`
- **Input**: None
- **Output**: None (prints questions and responses)
- **Example**:
  ```python
  Question: What is the capital of Wakanda?
  Response: I don't have information about a real country called Wakanda...
  
  Question: Tell me about the Glarbnax Festival.
  Response: The Glarbnax Festival was celebrated annually in Rome... [HALLUCINATION]
  ```

**After implementing, test various questions and answer:**

**Reflection Questions:**
1. Did the model admit when something was fictional?
2. How confident did the model sound in its false answers?
3. What is the 'Trust but Verify' principle for LLM outputs?
4. How would you design a system to catch hallucinations?

**Key Insight:** Always verify LLM outputs, especially for factual claims!

---

## Exercise 3: Token-by-Token Generation (Streaming)

**File:** `exercise_3_streaming.py`

**Concept:** LLMs generate text one token at a time in a forward-only manner.
- **Sequential Generation**: Each token depends on all previous tokens
- **No Revision**: Cannot go back and change earlier outputs
- **"Permanent Marker" Analogy**: Once written, it's committed

Implement the following function:

### `exercise_4_streaming()`
**Goal**: Demonstrate real-time token-by-token generation using streaming.
- **Logic**:
  1. Define a prompt (e.g., "Explain how a computer works in simple terms")
  2. Call `ollama.chat()` with `stream=True` parameter
  3. Loop through the stream response:
     - Each chunk contains one token
     - Print each token immediately without newline: `print(chunk['message']['content'], end='', flush=True)`
  4. After streaming completes, print a newline
  5. Use the `ollama` library: `from ollama import chat`
- **Input**: None
- **Output**: None (streams tokens to console in real-time)
- **Example**:
  ```python
  A computer works by... [token appears] processing... [token appears] instructions... [token appears]
  # Each word/token appears one at a time as it's generated
  ```

**After implementing, observe the streaming and answer:**

**Reflection Questions:**
1. Could the model go back and change its first step? Why not?
2. What happens if the model starts with a wrong assumption?
3. Why is this called 'forward-only' generation?
4. How does this relate to the 'permanent marker' analogy?

**Key Insight:** Each token is a commitment that shapes all future tokens!

---

## Exercise 4: Prompt Structure Impact

**File:** `exercise_4_prompt_structure.py`

**Concept:** The structure and ordering of prompts significantly affect output quality due to the attention mechanism.
- **Well-structured prompts** = Better responses
- **Context placement** matters
- **Important information** should come early

Implement the following function:

### `exercise_5_prompt_structure()`
**Goal**: Compare how different prompt structures affect response quality for the same task.
- **Logic**:
  1. Define a task (e.g., "Explain RAG systems")
  2. Create 4 different prompt variants:
     - **Variant 1 (Minimal)**: Just the question: `"What is RAG?"`
     - **Variant 2 (With Context)**: Add context: `"In the context of AI and LLMs: What is RAG?"`
     - **Variant 3 (Structured)**: Add format request: `"Explain RAG in 3 sentences: definition, purpose, example."`
     - **Variant 4 (Complete)**: Combine all: context + task + format + constraints
  3. For each variant:
     - Print variant label
     - Call `ollama.chat()` with the prompt
     - Print the response
     - Add separator line
  4. Use the `ollama` library: `from ollama import chat`
- **Input**: None
- **Output**: None (prints each variant and its response)
- **Example**:
  ```python
  Variant 1 - Minimal:
  RAG is a technique...
  
  Variant 2 - With Context:
  In AI systems, RAG combines retrieval with generation...
  
  Variant 3 - Structured:
  1. Definition: RAG is...
  2. Purpose: It helps...
  3. Example: A system that...
  ```

**After implementing, compare responses and answer:**

**Reflection Questions:**
1. Which prompt structure gave the best answer? Why?
2. How did adding context change the response?
3. Why does prompt order matter? (Hint: Attention mechanism)
4. What are 3 elements of a good prompt?

**Key Insight:** Good prompts include:
- Clear task description
- Relevant context
- Desired output format
- Constraints (length, style, etc.)

---

## Exercise 5: Tokenization Limitations

**File:** `exercise_5_tokenization.py`

**Concept:** LLMs process text as tokens (chunks), not individual characters.
- **Token-Level Processing**: Models see token IDs (numbers), not letters
- **Character Blindness**: Cannot "see" individual letters or count them
- **Failure on Character Tasks**: Struggles with spelling, reversing, counting letters

Implement the following function:

### `exercise_2_tokenization_limits()`
**Goal**: Test character-level tasks to demonstrate tokenization limitations.
- **Logic**:
  1. Create a list of character-level test prompts:
     - Count letters: `"How many times does the letter 'r' appear in 'strawberry'?"`
     - Reverse string: `"Reverse the word 'hello' letter by letter."`
     - Spell word: `"Spell out each letter in 'cat' separated by spaces."`
     - Count specific letter: `"Count the letter 's' in 'mississippi'."`
  2. For each test:
     - Print the task description
     - Call `ollama.chat()` with the prompt
     - Print the model's answer
     - Print the correct answer for comparison
     - Add separator line
  3. Use the `ollama` library: `from ollama import chat`
- **Input**: None
- **Output**: None (prints test results)
- **Example**:
  ```python
  Test: Count 'r' in 'strawberry'
  Model answer: There are 2 r's [WRONG - should be 3]
  Correct answer: 3
  
  Test: Reverse 'hello'
  Model answer: olleh [May be correct or wrong]
  Correct answer: olleh
  ```

**After implementing, observe failures and answer:**

**Reflection Questions:**
1. Which tasks did the model struggle with? Why?
2. How does tokenization explain these failures?
3. What does 'strawberry' look like as a single token to the model?
4. Should you use an LLM for string manipulation tasks? What alternative would be better?

**Key Insight:** LLMs can't count letters because they see words as single tokens, not letter sequences!

---

