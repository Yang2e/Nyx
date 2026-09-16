from abc import ABC, abstractmethod
from typing import Any, Dict

class BaseTool(ABC):
    name: str
    description: str

    @abstractmethod
    async def execute(self, arguments: Dict[str, Any]) -> str:
        pass