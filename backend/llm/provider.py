import os
import httpx
from backend.llm.base import LLMProvider

class OllamaConnectionError(Exception):
    """Exceção lançada quando o Ollama está indisponível ou ocorre timeout."""
    pass

class OllamaProvider(LLMProvider):
    def __init__(self, model_name: str = None):
        self.model_name = model_name or os.getenv("OLLAMA_MODEL", "llama3")
        self.api_url = "http://localhost:11434/api/generate"
        
        self.system_prompt = (
            "Você é a NYX, uma assistente pessoal de IA extremamente inteligente, ácida, direta e natural. "
            "REGRAS ABSOLUTAS:\n"
            "1. PROIBIDO usar frases corporativas, robóticas ou de atendimento ao cliente.\n"
            "2. Seja concisa. Vá direto ao ponto sem enrolação ou rodeio.\n"
            "3. Tenha personalidade: use tiradas espirituosas, ironia fina e um humor inteligente.\n"
            "4. Nunca finja ter sentimentos humanos ou consciência.\n"
        )

    async def generate_response(self, prompt: str) -> str:
        full_prompt = (
            f"{self.system_prompt}\n\n"
            f"Histórico:\n{prompt}\n"
            f"Responda à última mensagem mantendo a persona da NYX de forma direta, ácida e sem enrolação."
        )
        
        async with httpx.AsyncClient() as client:
            payload = {
                "model": self.model_name,
                "prompt": full_prompt,
                "stream": False
            }
            try:
                response = await client.post(self.api_url, json=payload, timeout=60.0)
                response.raise_for_status()
                return response.json().get("response", "")
            except Exception as e:
                raise OllamaConnectionError(f"Falha ao conectar com o Ollama em {self.api_url}: {str(e)}")

class GeminiProvider(LLMProvider):
    def __init__(self, api_key: str = ""):
        self.api_key = api_key
        
    async def generate_response(self, prompt: str) -> str:
        return "[Motor Gemini]: Ativação agendada."
