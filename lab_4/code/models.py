"""
Pydantic models for Lab 4 exercises.
These models provide type safety and clear structure for our LLM experiments.
"""

from pydantic import BaseModel
from typing import List


"""
Exercise 2: Product Review Analysis with Pydantic.
Models for product reviews and analysis results.
"""
    
class ReviewAnalysis(BaseModel):
    """Simplified product review analysis."""
    sentiment: str
    score: float
    key_points: List[str]
    would_recommend: bool
    

"""
Exercise 3: Code Review Assistant with Pydantic.
Models for code submission and review feedback.
"""
    
class CodeSubmission(BaseModel):
    """Code submitted for review."""
    filename: str
    code: str


class CodeReview(BaseModel):
    """Feedback from the code reviewer."""
    rating: str
    issues: List[str]
    suggestions: List[str]
    refactored_code: str

"""
Exercise 1: RAG with Ollama Integration + Pydantic.
Complete production-like RAG system using Pydantic models, Cosine Similarity, and Ollama.
"""

class RAGEDocument(BaseModel):
    """Represents a document in the RAG system."""
    doc_id: str
    content: str


class RAGQuery(BaseModel):
    """Query for the RAG system."""
    query: str
    top_k: int = 2


class RetrievedDocument(BaseModel):
    """Document with similarity score after retrieval."""
    doc_id: str
    similarity: float
    content: str


class QueryResponse(BaseModel):
    """Full RAG response with retrieval info and generated answer."""
    query: str
    retrieved_docs: List[RetrievedDocument]
    context: str
    answer: str


