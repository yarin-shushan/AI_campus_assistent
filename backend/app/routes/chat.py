from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from app.ai_agent import ask_smart_campus
from app.auth import get_current_user
from app.models.user import User

router = APIRouter(prefix="/chat", tags=["chat"])

class QueryRequest(BaseModel):
    query: str

@router.post("/ask")
async def ask(request: QueryRequest, current_user: User = Depends(get_current_user)):
    if not request.query.strip():
        raise HTTPException(status_code=400, detail="Query cannot be empty.")
        
    try:
        # Pass the student's natural language question and context to our orchestration logic
        response = ask_smart_campus(request.query, current_user)
        
        return {
            "response": response
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
