from fastapi import APIRouter
from pydantic import BaseModel
from app.services.ai_service import generate_response
from app.services.safety import is_emergency, disclaimer

router = APIRouter()

class ChatRequest(BaseModel):
    message: str

@router.post("/chat")
def chat(req: ChatRequest):
    if is_emergency(req.message):
        return {"response": "🚨 Please seek immediate medical help."}
    reply = generate_response(req.message)
    return {"response": reply + disclaimer()}
