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
        self.ensure_category_column()
        
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
    
    def ensure_category_column(self):
         with self.conn:
              cols = self.conn.execute(
                   "PRAGMA table_info(transactions);"
              ).fetchall()

              column_names = {col["name"] for col in cols}

              if "category" not in column_names:
                   self.conn.execute(
                        "ALTER TABLE transactions ADD COLUMN category TEXT;"
                   )
    
    def fetch_uncategorized(self):
         cur = self.conn.execute(
              "SELECT id, description FROM transactions WHERE category IS NULL;"
         )
         return cur.fetchall()
    
    def update_category(self, transaction_id: str, category: str):
         with self.conn:
              self.conn.execute(
                   """
                   UPDATE transactions 
                   SET category = ? 
                   WHERE id = ?;
                   """,
                   (category, transaction_id)
              )

    def close(self):
            self.conn.close()