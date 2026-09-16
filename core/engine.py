import traceback
from ai.ollama_provider import OllamaProvider
from ai.base import BaseLLMProvider

class ToolManager:
    def __init__(self):
        self.tools = {}

    def register_tool(self, tool):
        self.tools[tool.__class__.__name__] = tool

class NyxCore:
    def __init__(self, llm_provider: BaseLLMProvider = None):
        self.llm: BaseLLMProvider = llm_provider or OllamaProvider()
        self.tool_manager = ToolManager()

    async def process_message(self, prompt: str) -> str:
        """Processa a mensagem do usuário utilizando o modelo local com tratamento de erro detalhado."""
        try:
            response = await self.llm.generate_response(prompt)
            return response
        except Exception as e:
            # Imprime o traceback completo no terminal para facilitar o debug
            traceback.print_exc()
            return f"[Erro detalhado no processamento da Nyx: {e}]"