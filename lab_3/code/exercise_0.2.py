# Step 6: RAG with Ollama Integration
# This file extends the RAG system to use Ollama for actual text generation.
# Instead of mock generation, we retrieve relevant documents and use an LLM to generate responses.

from typing import List, Tuple
from math import sqrt
import ollama


class RAGWithOllama:
    """RAG system that uses Ollama for response generation."""
    
    def __init__(self, model: str = 'functiongemma'):
        """Initialize RAG with Ollama model."""
        self.database = {}
        self.vocabulary = [
            'company', 'revenue', 'million', 'dollars', 'growth', 'q3', 'q4', '2024',
            'dataserver', 'pro', 'x500', 'ram', 'gb', 'processors', 'storage', 'capacity',
            'autosync', 'enterprise', 'software', 'synchronization', 'users', 'concurrent',
            'customer', 'satisfaction', 'support', 'approval', 'manufacturing', 'facility',
            'austin', 'units', 'defect', 'rate', 'xeon', 'intel', 'ssd', 'real-time'
        ]
        self.model = model
    
    def add_document(self, doc_id: str, content: str):
        """Add a document to the database."""
        self.database[doc_id] = content
    
    def text_to_vector(self, text: str) -> List[int]:
        """Convert text to a binary vector based on vocabulary."""
        words = text.lower().split()
        vector = []
        for vocab_word in self.vocabulary:
            if vocab_word in words:
                vector.append(1)
            else:
                vector.append(0)
        return vector
    
    def cosine_similarity(self, vec1: List[int], vec2: List[int]) -> float:
        """Calculate cosine similarity between two vectors."""
        if len(vec1) != len(vec2):
            return 0.0
        
        dot_product = 0
        for i in range(len(vec1)):
            dot_product += vec1[i] * vec2[i]
        
        mag1_squared = 0
        for x in vec1:
            mag1_squared += x ** 2
        mag1 = sqrt(mag1_squared)
        
        mag2_squared = 0
        for x in vec2:
            mag2_squared += x ** 2
        mag2 = sqrt(mag2_squared)
        
        if mag1 == 0 or mag2 == 0:
            return 0.0
        
        return dot_product / (mag1 * mag2)
    
    def retrieve_relevant_docs(self, query: str, top_k: int = 2) -> List[Tuple[str, float]]:
        """Retrieve most relevant documents for a query."""
        query_vector = self.text_to_vector(query)
        similarities = []
        
        for doc_id, doc_text in self.database.items():
            doc_vector = self.text_to_vector(doc_text)
            similarity = self.cosine_similarity(query_vector, doc_vector)
            similarities.append((doc_id, round(similarity, 3)))
        
        similarities.sort(key=lambda x: x[1], reverse=True)
        return similarities[:top_k]
    
    def build_context(self, relevant_docs: List[Tuple[str, float]]) -> str:
        """Build context string from retrieved documents."""
        context_parts = []
        for doc_id, similarity in relevant_docs:
            doc_text = self.database[doc_id]
            context_parts.append(f"Document '{doc_id}' (relevance: {similarity:.3f}):\n{doc_text}")
        return "\n\n".join(context_parts)
    
    def generate_with_ollama(self, query: str, context: str) -> str:
        """Generate a response using Ollama LLM with given context."""
        system_prompt = f"""You are a helpful assistant. Use the following context to answer the user's question.
                            If the context doesn't contain relevant information, say so.
                            Context:
                            {context}"""
        
        messages = [
            {'role': 'system', 'content': system_prompt},
            {'role': 'user', 'content': query}
        ]
        
        response = ollama.chat(model=self.model, messages=messages)
        return response['message']['content']
    
    def generate_response(self, query: str) -> str:
        """Generate a response using retrieval and Ollama generation."""
        # Step 1: Retrieve relevant documents
        relevant_docs = self.retrieve_relevant_docs(query, top_k=2)
        
        if not relevant_docs:
            return "No relevant information found."
        
        # Step 2: Build context from retrieved documents
        context = self.build_context(relevant_docs)
        
        # Step 3: Generate response using Ollama
        response = self.generate_with_ollama(query, context)
        return response


# Example usage
if __name__ == "__main__":
    # Create RAG system with Ollama
    rag = RAGWithOllama(model='gemma3:1b')
    
    # Add private company documents
    rag.add_document("doc1", "Company XYZ Q3 2024 revenue reached 45.2 million dollars with 23 percent growth compared to Q2 2024.")
    rag.add_document("doc2", "Company XYZ Q4 2024 revenue reached 52.8 million dollars with 18 percent year-over-year growth.")
    rag.add_document("doc3", "The DataServer Pro X500 features 128GB RAM, dual Intel Xeon processors, and 8TB SSD storage capacity.")
    rag.add_document("doc4", "Our flagship software product AutoSync Enterprise v3.2 includes real-time data synchronization and supports up to 10000 concurrent users.")
    rag.add_document("doc5", "Customer satisfaction survey results show 94 percent approval rating for our technical support team in November 2024.")
    rag.add_document("doc6", "The manufacturing facility in Austin produces 5000 units per month with a defect rate below 0.5 percent.")
    
    # Test queries
    queries = [
        "What is the RAM capacity of the DataServer Pro X500?",
        "What was the Q3 2024 revenue?",
        "What was the Q4 2024 revenue?",
        "How many concurrent users does AutoSync Enterprise support?"
    ]
    
    print("=" * 80)
    print("RAG System with Ollama LLM")
    print("=" * 80)
    
    for query in queries:
        print(f"\nQuery: {query}")
        print("-" * 80)
        response = rag.generate_response(query)
        print(f"Response: {response}")
        print("=" * 80)
