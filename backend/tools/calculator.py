from typing import Any, Dict
from backend.tools.base import BaseTool
import math

class CalculatorTool(BaseTool):
    name = "calculator"
    description = "Realiza operações matemáticas básicas (soma, subtração, multiplicação, divisão)."

    async def execute(self, arguments: Dict[str, Any]) -> str:
        expression = arguments.get("expression", "")
        try:
            # Segurança básica para avaliar expressões matemáticas simples
            allowed_chars = "0123456789+-*/(). "
            if not all(c in allowed_chars for c in expression):
                return "Erro: Caracteres inválidos na expressão matemática."
            result = eval(expression)
            return f"O resultado de {expression} é {result}"
        except Exception as e:
            return f"Erro ao calcular: {str(e)}"