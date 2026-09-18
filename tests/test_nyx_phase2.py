import pytest
from unittest.mock import AsyncMock, patch
from fastapi.testclient import TestClient
from main import app
from backend.llm.provider import OllamaProvider, OllamaConnectionError
from backend.core.states import NyxState, get_orb_state

client = TestClient(app)

def test_ollama_model_fallback():
    provider = OllamaProvider()
    assert provider.model_name == "llama3"

@patch.dict("os.environ", {"OLLAMA_MODEL": "llama3.2-custom"})
def test_ollama_model_env_config():
    provider = OllamaProvider()
    assert provider.model_name == "llama3.2-custom"

def test_nyx_states_mapping():
    assert get_orb_state(NyxState.STARTING) == "idle"
    assert get_orb_state(NyxState.LISTENING) == "listening"
    assert get_orb_state(NyxState.THINKING) == "thinking"
    assert get_orb_state(NyxState.RESPONDING) == "responding"
    assert get_orb_state(NyxState.ERROR) == "error"
    assert get_orb_state(NyxState.SHUTTING_DOWN) == "idle"

@patch("backend.llm.provider.OllamaProvider.generate_response", side_effect=OllamaConnectionError("Conexão recusada"))
def test_chat_endpoint_ollama_unavailable(mock_generate):
    response = client.post("/chat/", json={"message": "Olá NYX"})
    assert response.status_code == 503
    assert "Erro de Conexão Ollama" in response.json()["detail"]