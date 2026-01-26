# Conceptual Design of Simple RAG

## High-Level Flow

```
User Query
    ↓
Vectorization (Query → List of numbers)
    ↓
Retrieval (Find similar documents in database)
    ↓
Generation (Combine query with retrieved docs)
    ↓
Response Output
```

## Components

- **Database**: Dictionary storing documents (key: doc_id, value: text content)
- **Vocabulary**: List of common words for creating vectors
- **Vectors**: Lists representing text as presence/absence of words (0 or 1)
- **Similarity**: Cosine calculation between query and document vectors
- **Generation**: Simple text synthesis from relevant documents

## Step-by-Step Process

1. **Input Query**: User provides a text question.
2. **Convert to Vector**: Transform query into a list of 0s and 1s based on vocabulary.
3. **Search Database**: Compare query vector with each document vector using cosine similarity.
4. **Select Best Matches**: Retrieve top similar documents (e.g., 2 most relevant).
5. **Build Response**: Create answer by combining query context with retrieved document summaries.
6. **Output**: Return the generated response to user.

## Cosine Similarity Explained

Cosine similarity measures how similar two vectors are, like comparing directions in space.

**Formula**:  
`similarity = (A • B) / (|A| * |B|)`

Where:  
- `A • B` = dot product (sum of A[i] * B[i] for each position i)  
- `|A|` = magnitude of A (sqrt(sum of A[i]²))  
- `|B|` = magnitude of B (sqrt(sum of B[i]²))  

**Simple Explanation**:  
- Dot product: Multiply corresponding elements and add them up. Higher if vectors match in many places.  
- Magnitudes: Length of vectors. Prevents bias toward longer texts.  
- Result: Number from 0 (completely different) to 1 (identical). We pick documents with highest scores.  

**Examples with 3-sized vectors** (Vocabulary: ['cat', 'dog', 'run']):  

- **Moderate similarity (0.5)**:  
  Query "cat run": A = [1, 0, 1]  
  Doc "dog run": B = [0, 1, 1]  
  Calc: Dot=1, |A|=1.41, |B|=1.41, Similarity≈0.5  
  Meaning: Share one word ("run"), moderate relevance.  

- **High similarity (1.0)**:  
  Query "cat dog": A = [1, 1, 0]  
  Doc "cat dog": B = [1, 1, 0]  
  Calc: Dot=2, |A|=1.41, |B|=1.41, Similarity=1.0  
  Meaning: Identical vectors, perfect match.  

- **Low similarity (0.0)**:  
  Query "cat": A = [1, 0, 0]  
  Doc "dog": B = [0, 1, 0]  
  Calc: Dot=0, |A|=1, |B|=1, Similarity=0.0  
  Meaning: No shared words, no relevance.

This helps find documents that share the most words with the query, simulating relevance.

This design uses basic Python data structures (lists, dicts) to simulate vector-based retrieval without external libraries.