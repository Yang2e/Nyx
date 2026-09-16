from backend.tools.base import BaseTool

class TranslatorTool(BaseTool):
    @property
    def name(self) -> str:
        return "translator"

    @property
    def description(self) -> str:
        return "Simula uma ferramenta de tradução simples."

    async def execute(self, text: str, target_lang: str = "en") -> str:
        return f"[Traduzido para {target_lang}]: {text}"