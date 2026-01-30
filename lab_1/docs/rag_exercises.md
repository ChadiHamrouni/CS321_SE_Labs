# RAG Project: Step-by-Step Implementation Guide

Retrieval-Augmented Generation (RAG) helps an AI answer questions using a specific set of documents. Here is the flow:

```
[User Query] → [Vectorize] → [Find Similar Docs] → [Generate Answer]
```

## Part 1: Core Logic Functions

In this part, you will implement the functions for processing text and finding matches.

### Exercise 1: `text_to_vector(text)`
**Goal**: Convert a string into a list of numbers (0 or 1) based on a vocabulary.
- **Logic**: For every word in your vocabulary list, check if it exists in the `text`. If yes, add a `1` to the result list; if no, add a `0`.
- **Input**: `text` (string)
- **Output**: `vector` (list of integers)
- **Example**:
  - `vocabulary = ["cat", "dog", "run"]`
  - `text = "the cat is fast"`
  - **Returns**: `[1, 0, 0]`

### Exercise 2: `cosine_similarity(vec1, vec2)`
**Goal**: Calculate a similarity score between two lists of numbers.
- **Logic**: 
  1. Calculate the **Dot Product**: Multiply numbers at the same index and sum them up.
     - *Example*: `[1, 0]` and `[1, 1]` → `(1*1) + (0*1) = 1`.
  2. Calculate **Magnitudes**: Square every number in the vector, sum them, and take the square root.
  3. **Formula**: `dot_product / (mag1 * mag2)`. Handle cases where magnitude is 0!
- **Input**: `vec1` (list), `vec2` (list)
- **Output**: `score` (float between 0.0 and 1.0)
- **Full Calculation Example**:
  - `vec1 = [1, 0, 1]`
  - `vec2 = [0, 1, 1]`
  - **Dot Product**: `(1*0) + (0*1) + (1*1) = 1`
  - **Magnitude 1**: `sqrt(1^2 + 0^2 + 1^2) = sqrt(2) ≈ 1.41`
  - **Magnitude 2**: `sqrt(0^2 + 1^2 + 1^2) = sqrt(2) ≈ 1.41`
  - **Mag1 * Mag2**: `1.41 * 1.41 = 1.9881` (roughly 2)
  - **Final Score**: `1 / 1.9881 ≈ 0.5`
  - **Returns**: `0.5`

### Exercise 3: `retrieve_relevant_docs(query, top_k)`
**Goal**: Find the most similar documents in a database.
- **Logic**:
  1. Turn the `query` into a vector.
  2. For every document in the database (dictionary), turn its text into a vector.
  3. Calculate similarity between query vector and document vector.
  4. Store the `(doc_id, score)` in a list.
  5. Sort the list by score (highest first) and return the first `top_k` items.
- **Input**: `query` (string), `top_k` (int)
- **Output**: List of tuples `[(doc_id, score), ...]`

### Exercise 4: `generate_response(query)`
**Goal**: Create a final answer using the best match.
- **Logic**: Call `retrieve_relevant_docs`. Take the text of the best matching document from the database and format it into a helpful string.
- **Input**: `query` (string)
- **Output**: `response` (string)

---

## Part 2: Refactoring to a Class

Now, take your logic and organize it inside a class called `SimpleRAG`.

### Exercise 5: The `SimpleRAG` Class
**Goal**: Encapsulate the database and vocabulary into one object.
1. **`__init__(self)`**: Initialize `self.database` (dict) and `self.vocabulary` (list).
2. **`add_document(self, doc_id, content)`**: A new method to add entries to your database.
3. **Move Functions**: Take your functions from Part 1 and make them methods of this class. 
   - *Note*: Add `self` as the first parameter to every function and use `self.vocabulary` or `self.database` instead of global variables!

---

## Part 3: Running the Application

Follow these steps at the bottom of your file to test your code:

1. **Create Object**: Create an instance of your class (e.g., `rag = SimpleRAG()`).
2. **Add Data**: Add 3-4 documents about different topics (Python, AI, Cooking, etc.).
3. **Test Queries**: Define a list of 2-3 questions.
4. **Print Results**: Iterate through your questions, call your generate method, and print the response.
