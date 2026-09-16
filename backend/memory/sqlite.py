import sqlite3
from typing import List, Dict, Any, Optional

class MemoryManager:
    def __init__(self, db_path="nyx_memory.db"):
        self.db_path = db_path
        self._init_db()

    def _init_db(self):
        with sqlite3.connect(self.db_path) as conn:
            # Tabela de conversas para gerenciar sessões
            conn.execute("""
                CREATE TABLE IF NOT EXISTS conversations (
                    id TEXT PRIMARY KEY,
                    title TEXT,
                    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            # Tabela de mensagens detalhada
            conn.execute("""
                CREATE TABLE IF NOT EXISTS messages (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    conversation_id TEXT,
                    role TEXT,
                    content TEXT,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (conversation_id) REFERENCES conversations(id)
                )
            """)

            # Tabela de memória de longo prazo / fatos sobre o usuário
            conn.execute("""
                CREATE TABLE IF NOT EXISTS user_memory (
                    key TEXT PRIMARY KEY,
                    value TEXT,
                    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
                )
            """)
            conn.commit()

    def create_conversation(self, conversation_id: str, title: str = "Nova Conversa"):
        with sqlite3.connect(self.db_path) as conn:
            conn.execute(
                "INSERT OR IGNORE INTO conversations (id, title) VALUES (?, ?)",
                (conversation_id, title)
            )
            conn.commit()

    def save_message(self, conversation_id: str, role: str, content: str):
        with sqlite3.connect(self.db_path) as conn:
            # Garante que a conversa existe na tabela principal
            conn.execute(
                "INSERT OR IGNORE INTO conversations (id, title) VALUES (?, ?)",
                (conversation_id, "Conversa Principal" if conversation_id == "default" else conversation_id)
            )
            # Salva a mensagem
            conn.execute(
                "INSERT INTO messages (conversation_id, role, content) VALUES (?, ?, ?)",
                (conversation_id, role, content)
            )
            # Atualiza o timestamp da conversa
            conn.execute(
                "UPDATE conversations SET updated_at = CURRENT_TIMESTAMP WHERE id = ?",
                (conversation_id,)
            )
            conn.commit()

    def get_history(self, conversation_id: str, limit: int = 50) -> List[Dict[str, str]]:
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            # Busca as últimas 'limit' mensagens ordenadas cronologicamente
            cursor.execute(
                """
                SELECT role, content FROM (
                    SELECT role, content, id FROM messages 
                    WHERE conversation_id = ? 
                    ORDER BY id DESC LIMIT ?
                ) ORDER BY id ASC
                """,
                (conversation_id, limit)
            )
            rows = cursor.fetchall()
            return [{"role": row[0], "content": row[1]} for row in rows]

    def get_all_conversations(self) -> List[str]:
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT id FROM conversations ORDER BY updated_at DESC")
            rows = cursor.fetchall()
            return [row[0] for row in rows]

    def set_user_fact(self, key: str, value: str):
        """Salva um fato ou preferência de longo prazo sobre o usuário."""
        with sqlite3.connect(self.db_path) as conn:
            conn.execute(
                """
                INSERT INTO user_memory (key, value, updated_at) 
                VALUES (?, ?, CURRENT_TIMESTAMP)
                ON CONFLICT(key) DO UPDATE SET value = excluded.value, updated_at = CURRENT_TIMESTAMP
                """,
                (key, value)
            )
            conn.commit()

    def get_user_fact(self, key: str) -> Optional[str]:
        """Recupera um fato de longo prazo."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT value FROM user_memory WHERE key = ?", (key,))
            row = cursor.fetchone()
            return row[0] if row else None