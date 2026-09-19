import sqlite3
import uuid
from typing import List, Dict, Optional

class MemoryManager:
    def __init__(self, db_path: str = "nyx_memory.db"):
        self.db_path = db_path
        self._init_db()

    def _get_connection(self):
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn

    def _init_db(self):
        with self._get_connection() as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS conversations (
                    conversation_id TEXT PRIMARY KEY,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            conn.execute("""
                CREATE TABLE IF NOT EXISTS messages (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    conversation_id TEXT,
                    role TEXT,
                    content TEXT,
                    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (conversation_id) REFERENCES conversations (conversation_id)
                )
            """)
            conn.commit()

    def create_conversation(self, conversation_id: Optional[str] = None) -> str:
        if not conversation_id:
            conversation_id = str(uuid.uuid4())
        with self._get_connection() as conn:
            conn.execute(
                "INSERT OR IGNORE INTO conversations (conversation_id) VALUES (?)",
                (conversation_id,)
            )
            conn.commit()
        return conversation_id

    def add_message(self, conversation_id: str, role: str, content: str):
        # Garante que a conversa existe antes de inserir a mensagem
        self.create_conversation(conversation_id)
        with self._get_connection() as conn:
            conn.execute(
                "INSERT INTO messages (conversation_id, role, content) VALUES (?, ?, ?)",
                (conversation_id, role, content)
            )
            conn.commit()

    def get_history(self, conversation_id: str) -> List[Dict[str, str]]:
        with self._get_connection() as conn:
            cursor = conn.execute(
                "SELECT role, content FROM messages WHERE conversation_id = ? ORDER BY id ASC",
                (conversation_id,)
            )
            rows = cursor.fetchall()
            return [{"role": row["role"], "content": row["content"]} for row in rows]
