"""
Exercise 7: RAG with Ollama Integration + Pydantic.
Complete production-like RAG system using Pydantic models, Cosine Similarity, and Ollama.
"""

from typing import List
from math import sqrt
import ollama

from models import RAGEDocument, RAGQuery, RetrievedDocument, QueryResponse

class RAGWithOllama:
    """RAG system that uses Ollama for response generation with Pydantic models."""
    
    def __init__(self, model: str = 'gemma3:1b'):
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

    
    def add_document_model(self, doc: RAGEDocument):
        """Add a document using Pydantic model."""
        self.database[doc.doc_id] = doc.content
    
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
        
        mag1 = sqrt(sum(x**2 for x in vec1))
        mag2 = sqrt(sum(x**2 for x in vec2))
        
        if mag1 == 0 or mag2 == 0:
            return 0.0
        
        return dot_product / (mag1 * mag2)
    
    def retrieve_relevant_docs(self, query_obj: RAGQuery) -> List[RetrievedDocument]:
        """Retrieve most relevant documents using Pydantic models."""
        query_vector = self.text_to_vector(query_obj.query)
        retrieved = []
        
        for doc_id, doc_text in self.database.items():
            doc_vector = self.text_to_vector(doc_text)
            similarity = self.cosine_similarity(query_vector, doc_vector)
            
            retrieved.append(
                RetrievedDocument(
                    doc_id=doc_id,
                    similarity=round(similarity, 3),
                    content=doc_text
                )
            )
        
        retrieved.sort(key=lambda x: x.similarity, reverse=True)
        return retrieved[:query_obj.top_k]
    
    def build_context(self, retrieved_docs: List[RetrievedDocument]) -> str:
        """Build context string from retrieved documents."""
        context_parts = []
        for doc in retrieved_docs:
            context_parts.append(
                f"Document '{doc.doc_id}' (relevance: {doc.similarity:.3f}):\n{doc.content}"
            )
        return "\n\n".join(context_parts)
    
    def generate_with_ollama(self, query: str, context: str) -> str:
        """Generate a response using Ollama LLM with given context."""
        system_prompt = f"""You are a helpful assistant. Use the following context to answer the user's question.
        If the context doesn't contain relevant information, say so explicitly.

        Context:
        {context}"""
        
        messages = [
            {'role': 'system', 'content': system_prompt},
            {'role': 'user', 'content': query}
        ]
        
        response = ollama.chat(model=self.model, messages=messages)
        return response['message']['content']
    
    def generate_response(self, query_obj: RAGQuery) -> QueryResponse:
        """Generate a complete RAG response with Pydantic model."""
        # Step 1: Retrieve relevant documents
        retrieved = self.retrieve_relevant_docs(query_obj)
        
        if not retrieved:
            return QueryResponse(
                query=query_obj.query,
                retrieved_docs=[],
                context="",
                answer="No relevant information found in the database."
            )
        
        # Step 2: Build context
        context = self.build_context(retrieved)
        
        # Step 3: Generate response using Ollama
        answer = self.generate_with_ollama(query_obj.query, context)
        
        # Step 4: Return structured response
        return QueryResponse(
            query=query_obj.query,
            retrieved_docs=retrieved,
            context=context,
            answer=answer
        )


def run_exercise():
    """Run the RAG system with various queries."""
    print("=" * 80)
    print("RAG System with Ollama + Pydantic Models")
    print("=" * 80)
    
    # Initialize RAG system
    rag = RAGWithOllama(model='gemma3:1b')
    
    # Add documents using Pydantic models
    print("\n📝 Adding documents using Pydantic models...")
    doc1 = RAGEDocument(
        doc_id="doc1",
        content="Company XYZ Q3 2024 revenue reached 45.2 million dollars with 23 percent growth compared to Q2 2024."
    )
    rag.add_document_model(doc1)
    
    doc2 = RAGEDocument(
        doc_id="doc2",
        content="Company XYZ Q4 2024 revenue reached 52.8 million dollars with 18 percent year-over-year growth."
    )
    rag.add_document_model(doc2)
    
    doc3 = RAGEDocument(
        doc_id="doc3",
        content="The DataServer Pro X500 features 128GB RAM, dual Intel Xeon processors, and 8TB SSD storage capacity."
    )
    rag.add_document_model(doc3)
    
    doc4 = RAGEDocument(
        doc_id="doc4",
        content="Our flagship software product AutoSync Enterprise v3.2 includes real-time data synchronization and supports up to 10000 concurrent users."
    )
    rag.add_document_model(doc4)
    
    doc5 = RAGEDocument(
        doc_id="doc5",
        content="Customer satisfaction survey results show 94 percent approval rating for our technical support team in November 2024."
    )
    rag.add_document_model(doc5)
    
    doc6 = RAGEDocument(
        doc_id="doc6",
        content="The manufacturing facility in Austin produces 5000 units per month with a defect rate below 0.5 percent."
    )
    rag.add_document_model(doc6)
    
    doc7 = RAGEDocument(
        doc_id="doc7",
        content="The new X600 server model scheduled for Q2 2025 will feature 256GB RAM and 16TB storage capacity."
    )
    rag.add_document_model(doc7)
    print(f"Added {len(rag.database)} documents")
    
    # Test queries using Pydantic models
    query_texts = [
        "What is the RAM capacity of the DataServer Pro X500?",
        "What was the Q3 2024 revenue?",
        "What was the Q4 2024 revenue?",
        "How many concurrent users does AutoSync Enterprise support?",
        "What new server model is planned for 2025?"
    ]
    
    for query_text in query_texts:
        print(f"\n{'='*80}")
        print(f"❓ Query: {query_text}")
        print(f"{'='*80}")
        
        # Create RAGQuery Pydantic model
        query = RAGQuery(query=query_text, top_k=3)
        
        # Get response
        response = rag.generate_response(query)
        
        # Display retrieved documents
        print("\n📚 Retrieved Documents:")
        for doc in response.retrieved_docs:
            print(f"   • {doc.doc_id} (similarity: {doc.similarity:.3f})")
            print(f"     {doc.content[:80]}...")
        
        # Display answer
        print("\n🤖 Generated Answer:")
        print(response.answer)


if __name__ == "__main__":
    run_exercise()