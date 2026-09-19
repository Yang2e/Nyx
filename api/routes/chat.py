import os
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional, List, Dict

from backend.memory.sqlite import MemoryManager
from backend.llm.provider import OllamaProvider
from backend.core.states import NyxState, get_orb_state

router = APIRouter()
memory_manager = MemoryManager()
llm_provider = OllamaProvider()

class ChatRequest(BaseModel):
    message: str
    conversation_id: Optional[str] = None

class ChatResponse(BaseModel):
    response: str
    conversation_id: str
    state: str

@router.post("/chat/", response_model=ChatResponse)
def chat_endpoint(payload: ChatRequest):
    conv_id = payload.conversation_id
    if not conv_id:
        conv_id = memory_manager.create_conversation()
    else:
        memory_manager.create_conversation(conv_id)

    # Salva mensagem do usuário
    memory_manager.add_message(conv_id, "user", payload.message)

    # Recupera histórico da conversa
    history = memory_manager.get_history(conv_id)

    try:
        # Envia histórico para o LLM
        response_text = llm_provider.generate(history)
    except Exception as e:
        raise HTTPException(status_code=503, detail=f"Ollama indisponível: {str(e)}")

    # Salva resposta do assistente
    memory_manager.add_message(conv_id, "assistant", response_text)

    current_state = get_orb_state()

    return ChatResponse(
        response=response_text,
        conversation_id=conv_id,
        state=current_state.value if hasattr(current_state, "value") else str(current_state)
    )
