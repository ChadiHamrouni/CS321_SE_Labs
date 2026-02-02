
from typing import List, Tuple
import math 

# Database: Dictionary storing documents (key: doc_id, value: text content)
database = {
    'doc1': 'Prompt engineering involves crafting effective inputs for language models.',
    'doc2': 'is a versatile Python programming language used in data science and AI.',
    'doc3': 'Machine learning algorithms learn patterns from data to make predictions.',
    'doc4': 'Natural language processing helps computers understand human text.'
}

# Vocabulary: Common words for vectorization (simplified bag-of-words approach)
vocabulary = [
    'prompt', 'engineering', 'language', 'models', 'python', 'programming',
    'data', 'science', 'machine', 'learning', 'natural', 'processing', 'text'
]

def text_to_vector(text: str) -> List[int]:
    """Convert text to a binary vector (1 if word present, 0 otherwise)"""
    words = text.lower().split()
    vector = []
    for vocab_word in vocabulary:
        if vocab_word in words:
            vector.append(1)
        else:
            vector.append(0)
    return vector


def cosine_similarity(vec1: List[int], vec2: List[int]) -> float:
    """Calculate cosine similarity between two vectors."""
    if len(vec1) != len(vec2):
        return 0.0
    
    # Dot product
    dot_product = 0
    for i in range(len(vec1)):
        dot_product += vec1[i] * vec2[i]
    
    # Magnitudes
    mag1_squared = 0
    for x in vec1:
        mag1_squared += x ** 2
    mag1 = math.sqrt(mag1_squared)
    
    mag2_squared = 0
    for x in vec2:
        mag2_squared += x ** 2
    mag2 = math.sqrt(mag2_squared)
    
    if mag1 == 0 or mag2 == 0:
        return 0.0
    
    return dot_product / (mag1 * mag2)

def retrieve_relevant_docs(query: str, top_k: int = 2) -> List[Tuple[str, float]]:
    """Retrieve most relevant documents for a query based on similarity

    Returns List[Tuple[str, float]] because:
    - Tuples allow heterogeneous types (str for doc_id, float for score)
    - List[List[str, float]] is invalid Python syntax (lists can't mix types in type hints)
    - Tuples are immutable, preventing accidental modification of results
    """
    query_vector = text_to_vector(query)

    similarities = []

    for doc_id, doc_text in database.items():
        doc_vector = text_to_vector(doc_text)
        similarity = cosine_similarity(query_vector, doc_vector)
        similarities.append((doc_id, similarity))
 
    # Sort by similarity (highest first)
    similarities.sort(key=lambda x: x[1], reverse=True)

    # Return top_k results
    return similarities[:top_k]

def generate_response(query: str) -> str:
    """Generate a response using retrieved documents"""
    relevant_docs = retrieve_relevant_docs(query)
    
    # Simple generation: Combine query with most relevant document
    if relevant_docs:
        best_doc_id, similarity = relevant_docs[0]
        best_doc_text = database[best_doc_id]
        response = f"Based on relevant information (similarity: {similarity:.2f}): {best_doc_text}"
    else:
        response = "No relevant information found."
    
    return response

# Example usage
if __name__ == "__main__":
    queries = [
        "How does prompt engineering work?",
        "Tell me about Python programming",
        "What is machine learning?"
    ]
    
    for query in queries:
        print(f"\nQuery: {query}")
        relevant = retrieve_relevant_docs(query)
        print(f"Most relevant docs: {relevant}")
        response = generate_response(query)
        print(f"Generated response: {response}")