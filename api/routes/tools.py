from fastapi import APIRouter
from pydantic import BaseModel
from typing import Dict, Any
from backend.tools.manager import ToolManager

router = APIRouter()
tool_manager = ToolManager()

class ToolExecutionRequest(BaseModel):
    tool_name: str
    arguments: Dict[str, Any]

class ToolExecutionResponse(BaseModel):
    result: str

@router.post("/execute", response_model=ToolExecutionResponse)
async def execute_tool_endpoint(request: ToolExecutionRequest):
    result = await tool_manager.execute_tool(request.tool_name, request.arguments)
    return ToolExecutionResponse(result=result)