from fastapi import FastAPI
import uvicorn

from exercise1 import router as ex1_router
from exercise2 import router as ex2_router
from exercise3 import router as ex3_router

app = FastAPI(title="Mini Ollama Bridge")

app.include_router(ex1_router, prefix="/api")
app.include_router(ex2_router, prefix="/api")
app.include_router(ex3_router, prefix="/api")

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)