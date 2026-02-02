# Lab 3 Exercises

## Exercise 1: Document Class Implementation

### Task
Implement the `Document` class with the following methods:

### Document Class Methods

1. **`__init__(self, title: str, content: str)`**
   - Constructor that initializes a document with a title and content

2. **`get_word_count(self) -> int`**
   - Returns the total number of words in the document content
   - Example: Content "Hello world from Python" → Returns `4`

3. **`get_character_count(self) -> int`**
   - Returns the total number of characters in the document content
   - Example: Content "Hello" → Returns `5`

4. **`contains_keyword(self, keyword: str) -> bool`**
   - Checks if a keyword exists in the document (case-insensitive)
   - Example: keyword="python", content="Python is great" → Returns `True`
   - Example: keyword="java", content="Python is great" → Returns `False`

5. **`get_summary(self, max_words: int = 10) -> str`**
   - Returns the first `max_words` words from the document
   - Adds "..." if the document is longer than `max_words`
   - Example: Content "One two three four five six", max_words=3 → Returns `"One two three...`
   - Example: Content "One two three", max_words=5 → Returns `"One two three"`

### Mock Data for Testing

```python
doc1 = Document("Python Basics", "Python is a programming language used for data science and AI.")
doc2 = Document("Machine Learning", "Machine learning algorithms learn from data to make predictions.")
doc3 = Document("RAG Systems", "Retrieval Augmented Generation combines information retrieval with language models to generate accurate responses.")
```

---

## Exercise 2: RAG System Implementation

### Prerequisites
- Review `simple_rag.py` from Lab 2 before attempting this exercise
- Understand the Document class from Exercise 1

### Task
Create a simple RAG (Retrieval Augmented Generation) system that:
- Stores multiple documents
- Searches documents by keyword
- Retrieves relevant documents
- Generates responses based on retrieved content

### Mock Data for RAG System

```python
documents = [
    Document("Python Introduction", "Python is a high-level programming language known for its simplicity and readability."),
    Document("Data Science Tools", "Python libraries like pandas and numpy are essential for data science work."),
    Document("Machine Learning Basics", "Machine learning involves training models on data to make predictions."),
    Document("Deep Learning", "Deep learning uses neural networks with multiple layers to learn complex patterns."),
    Document("RAG Overview", "Retrieval Augmented Generation improves AI responses by retrieving relevant context.")
]
```

---

## Exercise 3: RAG with Ollama Integration

### Prerequisites
- Complete Exercise 2 (RAG System Implementation)
- Review `ollama_example.py` from Lab 2
- Understand how to use `ollama.chat()` function

### Task
Update your implemented RAG class to integrate Ollama LLM for generating actual responses instead of mock responses.

Your RAG system should have three separate functions:

1. **`retrieve_relevant_docs(query: str, top_k: int) -> List[Tuple[str, float]]`**
   - Input: User query string, number of documents to retrieve
   - Output: List of tuples containing (document_id, similarity_score)
   - Example: query="quarterly revenue" → Returns `[("doc2", 0.85), ("doc4", 0.62)]`

2. **`build_context(relevant_docs: List[Tuple[str, float]]) -> str`**
   - Input: List of retrieved documents with scores
   - Output: Formatted context string combining all document contents
   - Example: Input `[("doc1", 0.9)]` → Returns `"Document 'doc1' (relevance: 0.900):\nCompany XYZ reported Q3 revenue..."`

3. **`generate_with_ollama(query: str, context: str) -> str`**
   - Input: User query and formatted context
   - Output: LLM-generated response using the context
   - Uses `ollama.chat()` with system prompt containing the context
   - Example: query="What was the Q3 revenue?", context="..." → Returns actual LLM response based on retrieved private data

### Mock Data for Testing (Private Company Data)

```python
rag.add_document("doc1", "Company XYZ Q3 2024 revenue reached 45.2 million dollars with a 23 percent growth compared to Q2.")
rag.add_document("doc2", "The DataServer Pro X500 features 128GB RAM, dual Intel Xeon processors, and 8TB SSD storage capacity.")
rag.add_document("doc3", "Our flagship software product AutoSync Enterprise v3.2 includes real-time data synchronization and supports up to 10000 concurrent users.")
rag.add_document("doc4", "Customer satisfaction survey results show 94 percent approval rating for our technical support team in November 2024.")
rag.add_document("doc5", "The manufacturing facility in Austin produces 5000 units per month with a defect rate below 0.5 percent.")
```

### Test Queries

```python
queries = [
    "What is the RAM capacity of the DataServer Pro X500?",
    "What was the Q3 2024 revenue?",
    "How many concurrent users does AutoSync Enterprise support?"
]
```

---

- Ensure all implementations run without errors
- Test all methods with the provided mock data
- Verify expected outputs match actual outputs
- For Exercise 3, verify that Ollama generates meaningful responses based on retrieved context
