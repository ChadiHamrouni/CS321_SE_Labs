"""
Exercise 2 - Streaming chat + model info
Add these routes to routes.py, then test in Postman.
"""

import os
import httpx
from fastapi import APIRouter, HTTPException
from models import ChatRequest, ModelInfoRequest

OLLAMA = os.getenv("OLLAMA", "http://localhost:11434")
LLM = os.getenv("LLM", "gemma3:1b")
router = APIRouter()


@router.post("/chat")
async def chat(req: ChatRequest):
    body = {
        "model": req.model or LLM,
        "messages": [m.model_dump() for m in req.messages],
        "stream": False,
    }
    async with httpx.AsyncClient(timeout=120) as client:
        r = await client.post(f"{OLLAMA}/api/chat", json=body)
    if r.is_error:
        raise HTTPException(r.status_code, r.text)
    return r.json()


@router.post("/models/info")
async def model_info(req: ModelInfoRequest):
    body = {"model": req.model, "verbose": req.verbose}
    async with httpx.AsyncClient() as client:
        r = await client.post(f"{OLLAMA}/api/show", json=body)
    if r.is_error:
        raise HTTPException(r.status_code, r.text)
    return r.json()
