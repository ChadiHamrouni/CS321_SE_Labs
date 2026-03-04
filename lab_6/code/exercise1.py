"""
Exercise 1 - GET endpoints: list local models & running models
Add these routes to routes.py, then test in Postman.
"""

import os
import httpx
from fastapi import APIRouter, HTTPException

OLLAMA = os.getenv("OLLAMA", "http://localhost:11434")
router = APIRouter()


@router.get("/models")
async def list_local_models():
    async with httpx.AsyncClient() as client:
        r = await client.get(f"{OLLAMA}/api/tags")
    if r.is_error:
        raise HTTPException(r.status_code, r.text)
    return r.json()


@router.get("/models/running")
async def list_running_models():
    async with httpx.AsyncClient() as client:
        r = await client.get(f"{OLLAMA}/api/ps")
    if r.is_error:
        raise HTTPException(r.status_code, r.text)
    return r.json()
