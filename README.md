# CS321 Software Engineering - Lab Materials

Course labs for CS321 Prompt Engineering

## 📚 Lab Overview

### Lab 1: Python Basics
Introduction to Python fundamentals
- Basic syntax and data types
- String manipulation
- Student exercises

### Lab 2: Introduction to RAG Systems
Understanding Retrieval Augmented Generation
- Simple RAG implementation
- Vector similarity
- Ollama integration basics
- Document retrieval

### Lab 3: Prompt Engineering & Understanding LLMs 
Hands-on exploration of how LLMs work
- **Temperature & creativity control**
- **Tokenization limitations**
- **Hallucination detection**
- **Token-by-token generation**
- **Prompt structure optimization**

### Lab 4: Structured Output with Pydantic & JSON Mode 
Building reliable LLM applications with type-safe structured output
- **Pydantic models for type safety**
- **JSON mode for reliable structured data**
- **RAG system with type-safe models**
- **Sentiment analysis from reviews**
- **AI-powered code reviewer**
- **Dictionary unpacking patterns**

### Lab 5: AI Pull Request Reviewer System 
Building a self-correcting AI code review pipeline
- **Multi-step LLM pipeline**
- **Self-rechecking PR loop**
- **Pydantic models for code reviews**
- **AI bug fix generation**
- **Iterative code improvement**

### Lab 6: FastAPI + Ollama 
Building a REST API that proxies Ollama using FastAPI
- **FastAPI router & endpoint design**
- **HTTP methods**
- **Proxy API pattern**
- **Streaming vs non-streaming responses**
- **Text embeddings**
- **Sampling options (temperature, seed, top-k)**
- **Testing APIs with Postman**


### Lab 7: AI Agents with the OpenAI Agents SDK
Building autonomous agents that use tools and browse the web — powered by a local Ollama model
- **Agent loop concept (tool call → result → reasoning)**
- **`@function_tool` decorator and docstring-driven tool descriptions**
- **Pydantic models to constrain tool inputs (`Literal` enums)**
- **Web search and page fetching via DuckDuckGo (no API key)**
- **Multi-turn conversation history**

### Lab 8: Multi-Agent Systems
Building a multi-agent system with a triage router and three specialist agents — powered by a local Ollama model
- **Triage agent that routes to specialists via `handoff()`**
- **Research Agent — web search via DuckDuckGo**
- **Math Agent — arithmetic and unit conversions**
- **Writing Agent — summarise and improve text**
- **Handoff tracing to see which agent handled each request**


## 📖 Resources
- [Ollama Website](https://ollama.com)
- [Ollama Python Library](https://github.com/ollama/ollama-python)
---

**Course**: CS321 Software Engineering  
**Institution**: Mediterranean Institute of Technology (MEDTECH)  
