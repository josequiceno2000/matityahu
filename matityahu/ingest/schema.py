from dataclasses import dataclass
from datetime import date, datetime
from decimal import Decimal

@dataclass
class Transaction:
    transaction_id: str
    date: date
    description: str
    amount: Decimal
    account: str | None
    source: str
    imported_at: datetime