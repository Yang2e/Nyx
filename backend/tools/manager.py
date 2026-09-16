from typing import Dict, Any
from backend.tools.base import BaseTool
from backend.tools.translator import TranslatorTool
# Importe outras ferramentas aqui conforme necessário (ex: calculator, weather, etc.)

class ToolManager:
    def __init__(self):
        self.tools: Dict[str, BaseTool] = {}
        # Registra automaticamente as ferramentas padrão ao inicializar
        self.register_defaults()

    def register_tool(self, tool: BaseTool):
        self.tools[tool.name] = tool

    def register_defaults(self):
        # Aqui você adiciona todas as ferramentas disponíveis no sistema
        self.register_tool(TranslatorTool())

    async def execute_tool(self, tool_name: str, arguments: Dict[str, Any]) -> str:
        if tool_name not in self.tools:
            return f"Erro: Ferramenta '{tool_name}' não encontrada."
        
        tool = self.tools[tool_name]
        try:
            # Desempacota os argumentos caso venham como dicionário
            if isinstance(arguments, dict):
                return await tool.execute(**arguments)
            return await tool.execute(arguments)
        except Exception as e:
            return f"Erro ao executar a ferramenta '{tool_name}': {str(e)}"