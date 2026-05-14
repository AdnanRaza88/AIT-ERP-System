from fastapi import APIRouter
from pydantic import BaseModel
from backend.services.chatbot_engine import engine

router = APIRouter(prefix="/api/chatbot", tags=["chatbot"])


class ChatMessage(BaseModel):
    message: str


@router.post("/ask")
def ask(payload: ChatMessage):
    return {"reply": engine.reply(payload.message)}