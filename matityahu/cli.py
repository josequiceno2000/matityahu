import argparse
import sys
from pathlib import Path

from matityahu.ingest.everydollar import EveryDollarImporter
from matityahu.storage.database import Database
from matityahu.categorize.rules import Categorizer
from matityahu.budget.loader import BudgetLoader
from matityahu.reports.budget_vs_actual import budget_vs_actual
from matityahu.reports.monthly import (
    income_vs_expenses,
    category_totals,
)

def parse_year_month(value: str):
    try:
        year, month = value.split("-")
        return int(year), int(month)
    except ValueError:
        raise ValueError("Date must be in YYYY-MM format.")

def run_monthly_report(db: Database, year: int, month: int):
    summary = income_vs_expenses(db, year, month)
    categories = category_totals(db, year, month)

    print("\n" + "=" * 60)
    print(f" Monthly Report for {year}-{month:02d} ")
    print("=" * 60 + "\n")

    print(f"Income    : ${summary['income']:,.2f}")
    print(f"Expenses  : ${summary['expenses']:,.2f}")
    print("-" * 60)

    net = summary["net"]
    status = "SURPLUS" if net >= 0 else "DEFICIT"
    print(f"Net ({status}) : ${net:,.2f}\n")
    print("-" * 60)

    if not categories:
        print("No categorized transactions found.\n")
        return

    total_spent = sum(categories.values())

    print("\nSpending by Category:")
    print("-" * 60)
    for category, amount in categories.items():
        percent = (amount / total_spent) * 100
        print(f"{category:<30} ${amount:>8,.2f}  ({percent:>5.1f}%)")
    
    print("=" * 60 + "\n")

def run_budget_report(db, year: int, month: int):
    loader = BudgetLoader(Path("config/budgets.yaml"))
    budget = loader.get_month(year, month)

    if not budget:
        print("No budget found for this month.")
        return
    
    rows = budget_vs_actual(db, budget, year, month)

    print("\n" + "=" * 70)
    print(f" Budget vs Actual Report for {year}-{month:02d} ")
    print("=" * 70)
    print(f"{'Category':<25} {'Budgeted':>10} {'Actual':>10} {'Remaining':>10} {'%':>8}")
    print("-" * 70)

    for r in rows:
        pct = f"{r['percent']:.0f}%" if r['percent'] is not None else "—"
        print(
            f"{r['category']:<25}"
            f"${r['budgeted']:>9,.2f}"
            f"${r['actual']:>9,.2f}"
            f"${r['remaining']:>9,.2f}"
            f"{pct:>8}"
        )
    
    print("=" * 70 + "\n")

def main():
    db = Database()
    db.initialize()

    args = sys.argv[1:]

    if args and args[0] == "report":
        if len(args) != 2:
            print("Usage: report YYYY-MM")
            return
        
        year, month = parse_year_month(args[1])
        run_monthly_report(db, year, month)
        db.close()
        return
    
    if args and args[0] == "budget":
        if len(args) != 2:
            print("Usage: budget YYYY-MM")
            return
        
        year, month = parse_year_month(args[1])
        run_budget_report(db, year, month)
        db.close()
        return
    
    importer = EveryDollarImporter()
    transactions = importer.import_file(
        Path("data/raw/everydollar_last_month.csv")
    )
    print(f"Imported {len(transactions)} transactions from EveryDollar.")

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

    print("\nGuided categorization complete.\n")
    
    db.close()

    

if __name__ == "__main__":
    main()