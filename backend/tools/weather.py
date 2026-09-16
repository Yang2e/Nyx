from typing import Any, Dict
from backend.tools.base import BaseTool

class WeatherTool(BaseTool):
    name = "weather"
    description = "Consulta a condição climática de uma cidade."

    async def execute(self, arguments: Dict[str, Any]) -> str:
        city = arguments.get("city", "sua localidade")
        # Aqui você poderá plugar uma API real de clima no futuro (ex: OpenWeatherMap)
        return f"O clima atual em {city} está ensolarado com 24°C."