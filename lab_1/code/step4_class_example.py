# Step 4: Class Example - Live Coding Demonstration
# This file demonstrates object-oriented programming concepts with a simple class.
# We'll create a Document class relevant to RAG systems, with attributes and methods.
# This will be shown live, then instantiated and used in examples.


class Document:
    """A simple Document class for storing and processing text documents."""
    
    def __init__(self, title: str, content: str):
        """Initialize a Document with title and content."""
        self.title = title
        self.content = content
    
    def get_word_count(self) -> int:
        """Return the number of words in the document content."""
        return len(self.content.split())
    
    def get_character_count(self) -> int:
        """Return the number of characters in the document content."""
        return len(self.content)
    
    def contains_keyword(self, keyword: str) -> bool:
        """Check if the document contains a specific keyword (case-insensitive)."""
        return keyword.lower() in self.content.lower()
    
    def get_summary(self, max_words: int = 10) -> str:
        """Return a summary of the document (first max_words words)."""
        words = self.content.split()
        summary_words = words[:max_words]
        return " ".join(summary_words) + ("..." if len(words) > max_words else "")

# Example usage (to be demonstrated live)
if __name__ == "__main__":
    # Create document instances
    doc1 = Document("Python Basics", "Python is a programming language used for data science and AI.")
    doc2 = Document("Machine Learning", "Machine learning algorithms learn from data to make predictions.")
    
    # Use methods
    print(f"Document 1 title: {doc1.title}")
    print(f"Document 1 word count: {doc1.get_word_count()}")
    print(f"Document 1 character count: {doc1.get_character_count()}")
    print(f"Document 1 contains 'python': {doc1.contains_keyword('python')}")
    print(f"Document 1 summary: {doc1.get_summary()}")
    
    print(f"\nDocument 2 title: {doc2.title}")
    print(f"Document 2 contains 'learning': {doc2.contains_keyword('learning')}")
    print(f"Document 2 summary: {doc2.get_summary(5)}")