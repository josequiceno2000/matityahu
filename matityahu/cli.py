from pathlib import Path
from matityahu.ingest.everydollar import EveryDollarImporter

def main():
    importer = EveryDollarImporter()
    transactions = importer.import_file(
        Path("data/raw/everydollar_last_month.csv")
    )
    print(f"Imported {len(transactions)} transactions from EveryDollar.")

if __name__ == "__main__":
    main()