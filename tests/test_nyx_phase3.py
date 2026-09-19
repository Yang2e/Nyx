import os
import pytest
from unittest.mock import patch

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
    """TESTE 3 — ordem: Confirma que get_history() retorna na ordem correta."""
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
    """TESTE 4 — continuidade: Mantém histórico ao adicionar novas mensagens com o mesmo ID."""
    conv_id = temp_memory.create_conversation()
    temp_memory.add_message(conv_id, "user", "Meu nome é Lucas")
    temp_memory.add_message(conv_id, "assistant", "Prazer, Lucas!")

    temp_memory.add_message(conv_id, "user", "Qual é meu nome?")
    
    history = temp_memory.get_history(conv_id)
    assert len(history) == 3


def test_5_isolamento(temp_memory):
    """TESTE 5 — isolamento: Confirma que a conversa A não contém mensagens de B."""
    conv_a = temp_memory.create_conversation()
    conv_b = temp_memory.create_conversation()

    temp_memory.add_message(conv_a, "user", "Mensagem A")
    temp_memory.add_message(conv_b, "user", "Mensagem B")

    assert temp_memory.get_history(conv_a)[0]["content"] == "Mensagem A"
    assert temp_memory.get_history(conv_b)[0]["content"] == "Mensagem B"


def test_6_conversa_nova(temp_memory):
    """TESTE 6 — conversa nova: Nova conversa começa totalmente vazia."""
    conv_a = temp_memory.create_conversation()
    temp_memory.add_message(conv_a, "user", "Dado A")

    conv_b = temp_memory.create_conversation()
    assert len(temp_memory.get_history(conv_b)) == 0


def test_7_ollama_api_url():
    """TESTE 7 — OLLAMA_API_URL: Verifica se o provedor respeita a variável e o fallback."""
    custom_url = "http://192.168.15.21:11434/api/generate"
    with patch.dict(os.environ, {"OLLAMA_API_URL": custom_url}):
        provider = OllamaProvider()
        assert provider.api_url == custom_url

    with patch.dict(os.environ, {}, clear=True):
        env_backup = os.environ.pop("OLLAMA_API_URL", None)
        try:
            provider = OllamaProvider()
            assert provider.api_url == "http://127.0.0.1:11434/api/generate"
        finally:
            if env_backup:
                os.environ["OLLAMA_API_URL"] = env_backup


def test_8_ollama_model():
    """TESTE 8 — OLLAMA_MODEL: Verifica atributo correto (.model) na implementação."""
    custom_model = "llama3:latest"
    with patch.dict(os.environ, {"OLLAMA_MODEL": custom_model}):
        provider = OllamaProvider()
        assert provider.model == custom_model
