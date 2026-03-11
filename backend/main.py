from fastapi import FastAPI, Depends
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from sqlmodel import Session
from database import get_session

app = FastAPI(title="Smart Campus Assistant")

# Allow requests from Next.js 
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # For dev purposes
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

from app.routes.auth import router as auth_router
app.include_router(auth_router)

from app.routes.chat import router as chat_router
app.include_router(chat_router)

@app.get("/health")
async def health():
    return {"status": "ok"}
