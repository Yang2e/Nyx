import os
import requests
from typing import List, Dict

class OllamaProvider:
    def __init__(self):
        self.api_url = os.getenv(
            "OLLAMA_API_URL",
            "http://127.0.0.1:11434/api/generate"
        )
        self.model = os.getenv("OLLAMA_MODEL", "llama3:latest")

    def generate(self, history: List[Dict[str, str]]) -> str:
        # Formata o histórico em prompt de texto simples ou estruturado para o Ollama
        prompt_lines = []
        for msg in history:
            role = msg.get("role")
            content = msg.get("content")
            if role == "user":
                prompt_lines.append(f"User: {content}")
            elif role == "assistant":
                prompt_lines.append(f"Assistant: {content}")
        prompt_lines.append("Assistant: ")
        full_prompt = "\n".join(prompt_lines)

        payload = {
            "model": self.model,
            "prompt": full_prompt,
            "stream": False
        }

        try:
            response = requests.post(self.api_url, json=payload, timeout=30)
            if response.status_code != 200:
                raise RuntimeError(f"Erro no Ollama: {response.status_code} - {response.text}")
            data = response.json()
            return data.get("response", "")
        except requests.RequestException as e:
            raise RuntimeError(f"Falha de conexão com Ollama: {str(e)}")
