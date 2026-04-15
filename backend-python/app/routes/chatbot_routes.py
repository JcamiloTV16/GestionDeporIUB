from fastapi import APIRouter
from pydantic import BaseModel
from app.controllers.chatbot_controller import detectar_intencion

router = APIRouter()

class ChatMessage(BaseModel):
    mensaje: str

@router.post("/chatbot/", tags=["Chatbot"])
async def chatbot(data: ChatMessage):
    resultado = detectar_intencion(data.mensaje)
    return resultado
