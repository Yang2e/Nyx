import os
import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch

from main import app
from backend.memory.sqlite import MemoryManager
from backend.llm.provider import OllamaProvider

@pytest.fixture
def temp_db(tmp_path):
    db_file = tmp_path / "test_nyx.db"
    return str(db_file)

def test_1_create_conversation(temp_db):
    memory = MemoryManager(db_path=temp_db)
    conv_id = memory.create_conversation()
    assert conv_id is not None
    assert len(conv_id) > 0

def test_2_persistence(temp_db):
    memory = MemoryManager(db_path=temp_db)
    conv_id = memory.create_conversation()
    memory.add_message(conv_id, "user", "Olá, NYX")
    history = memory.get_history(conv_id)
    assert len(history) == 1
    assert history[0]["role"] == "user"
    assert history[0]["content"] == "Olá, NYX"

def test_3_history_order(temp_db):
    memory = MemoryManager(db_path=temp_db)
    conv_id = memory.create_conversation()
    memory.add_message(conv_id, "user", "Olá")
    memory.add_message(conv_id, "assistant", "Olá! Como posso ajudar?")
    memory.add_message(conv_id, "user", "Qual é meu nome?")
    
    history = memory.get_history(conv_id)
    assert len(history) == 3
    assert history[0] == {"role": "user", "content": "Olá"}
    assert history[1] == {"role": "assistant", "content": "Olá! Como posso ajudar?"}
    assert history[2] == {"role": "user", "content": "Qual é meu nome?"}

def test_4_continuity(temp_db):
    memory = MemoryManager(db_path=temp_db)
    conv_id = "conv-persistente-123"
    memory.add_message(conv_id, "user", "Meu nome é Teste")
    
    # Simula continuidade recuperando no mesmo ID
    memory.add_message(conv_id, "assistant", "Prazer, Teste!")
    history = memory.get_history(conv_id)
    assert len(history) == 2
    assert history[0]["content"] == "Meu nome é Teste"
    assert history[1]["content"] == "Prazer, Teste!"

def test_5_isolation(temp_db):
    memory = MemoryManager(db_path=temp_db)
    conv_a = "conversation_A"
    conv_b = "conversation_B"
    
    memory.add_message(conv_a, "user", "Mensagem da A")
    memory.add_message(conv_b, "user", "Mensagem da B")
    
    history_a = memory.get_history(conv_a)
    history_b = memory.get_history(conv_b)
    
    assert len(history_a) == 1
    assert history_a[0]["content"] == "Mensagem da A"
    
    assert len(history_b) == 1
    assert history_b[0]["content"] == "Mensagem da B"

def test_6_new_conversation_no_inheritance(temp_db):
    memory = MemoryManager(db_path=temp_db)
    conv_1 = memory.create_conversation()
    memory.add_message(conv_1, "user", "Segredo da conversa 1")
    
    conv_2 = memory.create_conversation()
    history_2 = memory.get_history(conv_2)
    assert len(history_2) == 0

def test_7_ollama_api_url_env():
    with patch.dict(os.environ, {"OLLAMA_API_URL": "http://192.168.15.21:11434/api/generate"}):
        provider = OllamaProvider()
        assert provider.api_url == "http://192.168.15.21:11434/api/generate"

    # Teste de fallback padrão
    with patch.dict(os.environ, {}, clear=True):
        # Remove a variável se existir no ambiente de teste
        env_backup = os.environ.pop("OLLAMA_API_URL", None)
        try:
            provider = OllamaProvider()
            assert provider.api_url == "http://127.0.0.1:11434/api/generate"
        finally:
            if env_backup:
                os.environ["OLLAMA_API_URL"] = env_backup

def test_8_ollama_model_env():
    with patch.dict(os.environ, {"OLLAMA_MODEL": "llama3:latest"}):
        provider = OllamaProvider()
        assert provider.model == "llama3:latest"