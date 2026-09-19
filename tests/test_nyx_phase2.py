import pytest
import requests
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock

from main import app
from backend.llm.provider import OllamaProvider

client = TestClient(app)

def test_provider_generate_success():
    """Verifica se OllamaProvider.generate funciona corretamente (fluxo síncrono)."""
    provider = OllamaProvider()
    history = [{"role": "user", "content": "Teste síncrono"}]
    
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"response": "resposta do mock"}
    
    with patch("requests.post", return_value=mock_response):
        result = provider.generate(history)
        assert result == "resposta do mock"

def test_provider_generate_connection_error():
    """Verifica se o provider lança RuntimeError (e não OllamaConnectionError) em falha de conexão."""
    provider = OllamaProvider()
    history = [{"role": "user", "content": "Teste erro síncrono"}]
    
    with patch("requests.post", side_effect=requests.exceptions.ConnectionError("Conexão recusada")):
        with pytest.raises(RuntimeError) as exc_info:
            provider.generate(history)
        
        # Confirma que a exceção original ou mensagem foi encapsulada no RuntimeError
        assert "Conexão recusada" in str(exc_info.value) or exc_info.type == RuntimeError

def test_chat_endpoint_success():
    """Verifica se o endpoint /chat/ retorna 200 e formata corretamente a chamada síncrona."""
    with patch("api.routes.chat.llm_provider.generate") as mock_generate:
        mock_generate.return_value = "Resposta da NYX"
        
        response = client.post("/chat/", json={"message": "Olá NYX"})
        
        assert response.status_code == 200
        data = response.json()
        assert "response" in data
        assert data["response"] == "Resposta da NYX"
        assert "conversation_id" in data
        
        # Verifica se o endpoint enviou o history como List[Dict[str, str]]
        args, _ = mock_generate.call_args
        history = args[0]
        assert isinstance(history, list)
        assert history[-1]["role"] == "user"
        assert history[-1]["content"] == "Olá NYX"

def test_chat_endpoint_503_error():
    """Verifica se o endpoint /chat/ captura RuntimeError e retorna HTTP 503."""
    with patch("api.routes.chat.llm_provider.generate", side_effect=RuntimeError("Ollama down")):
        response = client.post("/chat/", json={"message": "Você está aí?"})
        assert response.status_code == 503
