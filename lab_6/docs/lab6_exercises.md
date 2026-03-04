# Lab 6: FastAPI + Ollama Bridge

## What is an Endpoint?
An **endpoint** is a URL that your API exposes so that other programs (or tools like Postman) can send requests to it. Each endpoint has a **method** (GET or POST) and does one specific job.

- **GET** — read/fetch data, no body needed
- **POST** — send data in the body, get a result back

In this lab your FastAPI server sits **between** the client (Postman) and Ollama. It receives your request, forwards it to Ollama, and returns the response. This pattern is called a **proxy API** and is common in real products to add auth, logging, or hide internal services.

```
┌─────────┐        POST /api/chat         ┌─────────────┐       POST /api/chat      ┌────────┐
│ Postman │  ────────────────────────────► │  FastAPI    │ ────────────────────────► │ Ollama │
│ (client)│ ◄────────────────────────────  │  (your API) │ ◄────────────────────────  │        │
└─────────┘        JSON response           └─────────────┘       JSON response       └────────┘
```

**Why not call Ollama directly?**
You could — but wrapping it in your own API lets you control access, validate inputs, swap models, and add features without the client ever knowing.

## Postman as our Frontend
In a real app a frontend — like a React Native mobile app or a React website — would send these HTTP requests. **Postman is standing in for that frontend.** It lets us fire requests and inspect responses without writing any UI code, which is exactly what you want when you are still building and testing the backend.

**Why developers use Postman:**
- Test any endpoint instantly without building a UI first
- Inspect the full response (status code, headers, body) in one place
- Save and share requests with your team so everyone tests the same way
- Catch bugs in your API before a frontend developer ever touches it

Think of Postman as the fastest way to prove your backend works — then hand it off to the frontend team with confidence.

## Prerequisites
- `pip install fastapi uvicorn httpx python-dotenv pydantic`
- Pull the required models:
  ```bash
  ollama pull llama3.2
  ollama pull qwen3-embedding:0.6b
  ```

## Before Every Test
1. **Ollama must be running** — start it from the Ollama app or `ollama serve`
2. **Start the API server** — `uvicorn main:app --reload` inside `lab_6/code/`

## Overview
Each exercise file is a FastAPI router. Study the endpoints, then wire them into `main.py` and test in Postman.

| File | Endpoints |
|------|-----------|
| `exercise1.py` | `GET /models`, `GET /models/running` |
| `exercise2.py` | `POST /chat` (streaming), `POST /models/info` |
| `exercise3.py` | `POST /embed`, `POST /generate/options` |

## Running
Each exercise file defines a FastAPI router. Add it to `main.py` then start the server:

```python
# main.py
from exercise1 import router as ex1
from exercise2 import router as ex2
from exercise3 import router as ex3

app.include_router(ex1, prefix="/api")
app.include_router(ex2, prefix="/api")
app.include_router(ex3, prefix="/api")
```

```bash
uvicorn main:app --reload
```

## Testing with Postman
1. Open Postman → **New Request**
2. Set method + URL (e.g. `GET http://localhost:8000/api/models`)
3. For POST: **Body → raw → JSON**, paste the body below, hit **Send**

**GET endpoints** (no body needed):
- `GET http://localhost:8000/api/models`
- `GET http://localhost:8000/api/models/running`

**POST endpoints**:

`POST /api/chat`
```json
{
  "model": "llama3.2",
  "messages": [{"role": "user", "content": "Write a haiku about couscous."}]
}
```

`POST /api/models/info`
```json
{ "model": "llama3.2" }
```

`POST /api/embed` *(requires `qwen3-embedding:0.6b` pulled)*
```json
{ "input": "The sky is blue", "model": "qwen3-embedding:0.6b" }
```

`POST /api/generate/options`
```json
{
  "prompt": "Name a colour.",
  "options": { "temperature": 0, "seed": 42 }
}
```

