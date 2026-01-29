from pathlib import Path

from matityahu.ingest.everydollar import EveryDollarImporter
from matityahu.storage.database import Database
from matityahu.categorize.rules import Categorizer

def main():
    importer = EveryDollarImporter()
    transactions = importer.import_file(
        Path("data/raw/everydollar_last_month.csv")
    )
    print(f"Imported {len(transactions)} transactions from EveryDollar.")

    db = Database()
    db.initialize()
    db.insert_transactions(transactions)
    print(f"Stored {len(transactions)} transactions into the database.")

    categorizer = Categorizer(Path("config/categories.yaml"))

    rows = db.fetch_uncategorized()
    categorized = 0

    for row in rows:
        category = categorizer.categorize(row["description"])
        if category:
            db.update_category(row["id"], category)
            categorized += 1
    
    db.close()

    print(f"Categorized {categorized} transactions.")

if __name__ == "__main__":
    main()