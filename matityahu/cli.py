import argparse
import sys
from pathlib import Path

from matityahu.ingest.everydollar import EveryDollarImporter
from matityahu.storage.database import Database
from matityahu.categorize.rules import Categorizer
from matityahu.reports.monthly import MonthlyReport


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
    
    if not rows:
        print("No uncategorized transactions found.")
        return

    print(f"Found {len(rows)} uncategorized transactions.\n")

    for row in rows:
        desc = row["description"]
        amount = row["amount"]
        suggested = categorizer.suggest(desc)

        print("-" * 50)
        print(f"Description : {desc}")
        print(f"Amount      : {amount}")
        print(f"Suggestion  : {suggested or 'None'}")
        choice = input(
            "Enter category "
            "[enter=accept, text=new/existing, s=skip]"
        ).strip()

        if choice.lower() == "s":
            print("Skipped.\n")
            continue

        category = suggested if choice == "" else choice

        db.update_category(row["id"], category)
        print(f"→ Categorized as '{category}'")
    
    db.close()

    print("\nGuided categorization complete.")

if __name__ == "__main__":
    main()