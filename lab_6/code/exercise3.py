"""
Exercise 3 - Embeddings + generation with sampling options
Add these routes to routes.py, then test in Postman.
note: for /embed pull an embedding model first: ollama pull qwen3-embedding:0.6b
"""

import os
import httpx
from fastapi import APIRouter, HTTPException
from models import EmbedRequest, GenerateWithOptionsRequest, SamplingOptions

OLLAMA = os.getenv("OLLAMA", "http://localhost:11434")
EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "qwen3-embedding:0.6b")
router = APIRouter()


@router.post("/embed")
async def embed(req: EmbedRequest):
    body = {"model": req.model or EMBEDDING_MODEL, "input": req.input}
    async with httpx.AsyncClient(timeout=60) as client:
        r = await client.post(f"{OLLAMA}/api/embed", json=body)
    if r.is_error:
        raise HTTPException(r.status_code, r.text)
    return r.json()


