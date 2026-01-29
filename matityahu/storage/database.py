import sqlite3
from pathlib import Path
from typing import Iterable

from matityahu.ingest.schema import Transaction

DB_PATH = Path("data/matityahu.db")

class Database:
    def __init__(self, path: Path = DB_PATH):
        self.path = path
        self._ensure_parent_dir()
        self.conn = sqlite3.connect(self.path)
        self.conn.row_factory = sqlite3.Row

    def _ensure_parent_dir(self):
        self.path.parent.mkdir(parents=True, exist_ok=True)
    
    def initialize(self):
        with self.conn:
            self.conn.execute(
                """
                CREATE TABLE IF NOT EXISTS transactions (
                    id TEXT PRIMARY KEY,
                    date TEXT NOT NULL,
                    description TEXT NOT NULL,
                    amount TEXT NOT NULL,
                    account TEXT,
                    source TEXT NOT NULL,
                    imported_at TEXT NOT NULL
                );
                """
            )
        
    def insert_transactions(self, transactions: Iterable[Transaction]):
        with self.conn:
            self.conn.executemany(
                """
                INSERT OR IGNORE INTO transactions (
                    id, 
                    date, 
                    description,  
                    amount, 
                    account, 
                    source, 
                    imported_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?);
                """,
                [
                    (
                        tx.transaction_id,
                        tx.date.isoformat(),
                        tx.description,
                        str(tx.amount),
                        tx.account,
                        tx.source,
                        tx.imported_at.isoformat(),
                    )
                    for tx in transactions
                ]
            )
        
    def close(self):
            self.conn.close()