import os
import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock

from main import app
from backend.memory.sqlite import MemoryManager
from backend.llm.provider import OllamaProvider


@pytest.fixture
def temp_memory(tmp_path):
    """Fixture para criar um MemoryManager isolado usando um banco SQLite temporário."""
    db_file = tmp_path / "nyx_test_memory.db"
    return MemoryManager(db_path=str(db_file))


def test_1_criacao(temp_memory):
    """TESTE 1 — criação: Verifica se create_conversation() gera um conversation_id válido."""
    conv_id = temp_memory.create_conversation()
    assert conv_id is not None
    assert isinstance(conv_id, str)
    assert len(conv_id) > 0


def test_2_persistencia(temp_memory):
    """TESTE 2 — persistência: Cria conversa, adiciona mensagem e recupera o histórico."""
    conv_id = temp_memory.create_conversation()
    temp_memory.add_message(conv_id, "user", "Olá, NYX!")
    
    history = temp_memory.get_history(conv_id)
    assert len(history) == 1
    assert history[0]["role"] == "user"
    assert history[0]["content"] == "Olá, NYX!"


def test_3_ordem(temp_memory):
    """TESTE 3 — ordem: Confirma que get_history() retorna na ordem correta (user -> assistant -> user -> assistant)."""
    conv_id = temp_memory.create_conversation()
    temp_memory.add_message(conv_id, "user", "Pergunta 1")
    temp_memory.add_message(conv_id, "assistant", "Resposta 1")
    temp_memory.add_message(conv_id, "user", "Pergunta 2")
    temp_memory.add_message(conv_id, "assistant", "Resposta 2")

    history = temp_memory.get_history(conv_id)
    assert len(history) == 4
    assert history[0] == {"role": "user", "content": "Pergunta 1"}
    assert history[1] == {"role": "assistant", "content": "Resposta 1"}
    assert history[2] == {"role": "user", "content": "Pergunta 2"}
    assert history[3] == {"role": "assistant", "content": "Resposta 2"}


def test_4_continuidade(temp_memory):
    """TESTE 4 — continuidade: Recupera o mesmo conversation_id e adiciona novas mensagens mantendo o histórico."""
    conv_id = temp_memory.create_conversation()
    temp_memory.add_message(conv_id, "user", "Meu nome é Lucas")
    temp_memory.add_message(conv_id, "assistant", "Prazer, Lucas!")

    # Simula continuidade usando o mesmo conversation_id
    temp_memory.add_message(conv_id, "user", "Qual é meu nome?")
    
    history = temp_memory.get_history(conv_id)
    assert len(history) == 3
    assert history[0]["content"] == "Meu nome é Lucas"
    assert history[1]["content"] == "Prazer, Lucas!"
    assert history[2]["content"] == "Qual é meu nome?"


def test_5_isolamento(temp_memory):
    """TESTE 5 — isolamento: Confirma que a conversa A não contém mensagens de B e vice-versa."""
    conv_a = temp_memory.create_conversation()
    conv_b = temp_memory.create_conversation()

    temp_memory.add_message(conv_a, "user", "Mensagem exclusiva da conversa A")
    temp_memory.add_message(conv_b, "user", "Mensagem exclusiva da conversa B")

    history_a = temp_memory.get_history(conv_a)
    history_b = temp_memory.get_history(conv_b)

    assert len(history_a) == 1
    assert history_a[0]["content"] == "Mensagem exclusiva da conversa A"

    assert len(history_b) == 1
    assert history_b[0]["content"] == "Mensagem exclusiva da conversa B"


def test_6_conversa_nova(temp_memory):
    """TESTE 6 — conversa nova: Confirma que uma nova conversa começa totalmente vazia."""
    conv_a = temp_memory.create_conversation()
    temp_memory.add_message(conv_a, "user", "Dado importante da conversa A")

    conv_b = temp_memory.create_conversation()
    history_b = temp_memory.get_history(conv_b)

    assert len(history_b) == 0


def test_7_ollama_api_url():
    """TESTE 7 — OLLAMA_API_URL: Verifica se o provedor respeita a variável de ambiente e o fallback padrão."""
    custom_url = "http://192.168.15.21:11434/api/generate"
    with patch.dict(os.environ, {"OLLAMA_API_URL": custom_url}):
        provider = OllamaProvider()
        assert provider.api_url == custom_url

    # Testa fallback padrão quando a variável não está definida
    with patch.dict(os.environ, {}, clear=True):
        env_backup = os.environ.pop("OLLAMA_API_URL", None)
        try:
            provider = OllamaProvider()
            assert provider.api_url == "http://127.0.0.1:11434/api/generate"
        finally:
            if env_backup:
                os.environ["OLLAMA_API_URL"] = env_backup


def test_8_ollama_model():
    """TESTE 8 — OLLAMA_MODEL: Verifica se a variável OLLAMA_MODEL é respeitada pela implementação atual."""
    custom_model = "llama3:latest"
    with patch.dict(os.environ, {"OLLAMA_MODEL": custom_model}):
        provider = OllamaProvider()
        assert provider.model == custom_model


def test_chat_endpoint_mocked():
    """TESTE DO CHAT — Validação do endpoint /chat/ utilizando mock para o OllamaProvider."""
    client = TestClient(app)
    
    with patch("api.routes.chat.llm_provider.generate") as mock_generate:
        mock_generate.return_value = "Olá! Como posso ajudar?"
        
        # Envio inicial sem conversation_id
        response = client.post("/chat/", json={"message": "Olá"})
        assert response.status_code == 200
        data = response.json()
        assert "conversation_id" in data
        assert data["response"] == "Olá! Como posso ajudar?"
        
        conv_id = data["conversation_id"]
        
        # Envio subsequente com conversation_id existente (continuidade)
        response_cont = client.post("/chat/", json={"message": "Qual é meu nome?", "conversation_id": conv_id})
        assert response_cont.status_code == 200
        data_cont = response_cont.json()
        assert data_cont["conversation_id"] == conv_id
