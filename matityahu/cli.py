from pathlib import Path

from matityahu.ingest.everydollar import EveryDollarImporter
from matityahu.storage.database import Database

def main():
    importer = EveryDollarImporter()
    transactions = importer.import_file(
        Path("data/raw/everydollar_last_month.csv")
    )
    print(f"Imported {len(transactions)} transactions from EveryDollar.")

    db = Database()
    db.initialize()
    db.insert_transactions(transactions)
    db.close()

    print(f"Stored {len(transactions)} transactions into the database.")

if __name__ == "__main__":
    main()