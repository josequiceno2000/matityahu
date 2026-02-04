import csv
import re
from datetime import datetime
from pathlib import Path
from matityahu.ingest.schema import Transaction

def normalize_date(date_str: str) -> str:
    """Converts 01/30/26 (MM/DD/YY) to 2026-01-30 (YYYY-MM-DD)."""
    try:
        dt = datetime.strptime(date_str, "%m/%d/%y")
        return dt.strftime("%Y-%m-%d")
    except ValueError:
        return date_str

def clean_amount(amount_str: str) -> float:
    """Turns '-$48.91' or '$3,426.86' into a float."""
    if not amount_str:
        return 0.0
    clean_str = re.sub(r'[^\d.-]', '', amount_str)
    return float(clean_str)

class AscendImporter:
    def import_file(self, path: Path) -> list[Transaction]:
        transactions = []
        
        with path.open(newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)

            for row in reader:
                tx = Transaction(
                    transaction_id=row['Transaction ID'],
                    date=normalize_date(row['Date']),
                    description=row['Description'].strip(),
                    # We use the 'Amount' column header here
                    amount=clean_amount(row['Amount']),
                    account=row['Account ID'],
                    source="ascend",
                    imported_at=datetime.now()
                )
                transactions.append(tx)
                
        return transactions