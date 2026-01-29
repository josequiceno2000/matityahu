import csv
import uuid
from datetime import datetime
from decimal import Decimal
from pathlib import Path

from .base import TransactionImporter
from .schema import Transaction

class EveryDollarImporter(TransactionImporter):
    source_name = "everydollar"

    def import_file(self, path: Path) -> list[Transaction]:
        transactions: list[Transaction] = []

        with path.open(newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)

            for row in reader:
                amount = Decimal(row["Amount"])

                # EveryDollar exports expenses as negative amounts and income as positive.
                if row.get("Type", "").lower() == "expense":
                    amount = -abs(amount)

                tx = Transaction(
                    transaction_id=str(uuid.uuid4()),
                    date=datetime.strptime(row["Date"], "%m/%d/%Y").date(),
                    description=row["Merchant"].strip().lower(),
                    amount=amount,
                    account=row.get("Account"),
                    source=self.source_name,
                    imported_at=datetime.now(),
                )

                transactions.append(tx)
                
        return transactions