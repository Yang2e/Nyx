from fastapi import APIRouter
from pydantic import BaseModel
from typing import Optional, List
import uuid
from backend.memory.sqlite import MemoryManager
from backend.llm.provider import OllamaProvider
from backend.llm.tools import web_search

router = APIRouter(tags=["chat"])

memory = MemoryManager()
llm = OllamaProvider()

class ChatRequest(BaseModel):
    message: str
    conversation_id: Optional[str] = None

class ChatResponse(BaseModel):
    response: str
    conversation_id: str

@router.post("/", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest):
    conv_id = request.conversation_id or str(uuid.uuid4())
    
    memory.save_message(conv_id, "user", request.message)
    
    # 1. Palavras de busca expandidas
    search_context = ""
    keywords = ["quem é", "o que é", "notícia", "últimas", "quanto custa", "pesquise", "busca", "receita"]
    if any(keyword in request.message.lower() for keyword in keywords):
        search_results = await web_search(request.message)
        search_context = f"\nContexto extra da web:\n{search_results}\n"

    history = memory.get_history(conv_id)
    formatted_history = "\n".join([f"{role}: {content}" for role, content in history])
    
    # 2. System Prompt explicitando a função da NYX
    system_instruction = (
        "Você é a NYX, uma assistente virtual útil e direta. "
        "Responda à solicitação do usuário de forma completa e clara.\n\n"
    )
    
    full_prompt_input = f"{system_instruction}{formatted_history}{search_context}"
    
    response_text = await llm.generate_response(full_prompt_input)
    
    memory.save_message(conv_id, "assistant", response_text)
    
    return ChatResponse(response=response_text, conversation_id=conv_id)
@router.get("/conversations", response_model=List[str])
async def list_conversations():
    return memory.get_all_conversations()