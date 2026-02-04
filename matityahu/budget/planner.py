from pathlib import Path
import yaml

from matityahu.reports.formatting import validate_categories
from matityahu.storage.database import Database

ESSENTIAL_GROUPS = [
    "debt",
    "housing",
    "food",
    "transportation",
    "insurance"
]

FLEX_GROUPS = [
    "giving",
    "savings",
    "personal",
    "lifestyle",
    "health",
]

def prompt_amount(label: str) -> float:
    while True:
        raw = input(f"{label} $").strip()
        try:
            value = float(raw)
            if value < 0:
                raise ValueError()
            return round(value, 2)
        except ValueError:
            print("Enter a valid non-negative dollar amount.")


def run_zero_sum_planner(year: int, month: int):
    print("\n" + "=" * 60)
    print(f" Zero-Sum Budget Planning Wizard ({year}-{month:02d}) ")
    print("=" * 60)

    total_income = prompt_amount("Expected total monthly income")
    remaining = total_income

    print(f"\nStarting balance: ${remaining:,.2f}\n")

    budget = {}

    def allocate_group(group: str, categories: list[str]):
        nonlocal remaining
        print(f"\n--- {group.upper()} ---")
        budget[group] = {}

        for cat in categories:
            print(f"\nRemaining: ${remaining:,.2f}")
            amount = prompt_amount(f"{cat.replace('_', ' ').title()}")

            remaining -= amount
            budget[group][cat] = amount

            if remaining < 0:
                print("\n⚠️ WARNING: You have allocated more than your income!")
                print(f"Over by: ${abs(remaining):,.2f}\n")


    category_structure = {
        "debt": ["discover", "mom_and_dad", "student_loan"],
        "housing": ["rent", "utilities", "furniture", "pet_rent", "lizzy_rent", "lizzy_utilities", "lizzy_pet_rent"],
        "food": ["groceries", "eating_out_delivery", "pet_food", "coffee"],
        "transportation": ["gas", "repairs", "airfare", "other_car_fees", "oil_change"],
        "insurance": ["car_insurance", "renters_insurance", "health_insurance", "pet_insurance"],
        "giving": ["church", "maria_giving", "jose_giving"],
        "savings": ["emergency_fund", "retirement", "other_taxes", "rome"],
        "personal": ["clothing", "maria_fun_money", "jose_fun_money", "health_hygiene", "haircuts"],
        "lifestyle": ["pet", "personal_development", "entertainment", "gifts_for_maria", "gifts_for_jose", "subscriptions", "romantic", "christmas", "phone", "miscellaneous", "internet", "internet_lizzy", "business_expenses"],
        "health": ["doctor"],
    }

    print("\nESSENTIAL CATEGORIES (must budget these first)")
    for group in ESSENTIAL_GROUPS:
        allocate_group(group, category_structure[group])

    print("\n" + "=" * 60)
    print(" BUDGET SUMMARY ")
    print("=" * 60)
    
    allocated = total_income - remaining
    print(f"Income     : ${total_income:,.2f}")
    print(f"Allocated  : ${allocated:,.2f}")
    print(f"\nRemaining: ${remaining:,.2f}" + ("  ⚠️ OVERBUDGET" if remaining < 0 else ""))

    if remaining != 0:
        print("\n⚠️ Zero-sum not achieved. Consider adjusting flexible categories.")
    else:
        print("\n✅ Zero-sum achieved. Budget balances to $0.")

    flat = []
    for group in budget.values():
        flat.extend(group.keys())
    
    db = Database()
    db.initialize()
    validate_categories(flat, db.get_categories())
    db.close()

    save = input("\nSave this budget to budgets.yaml? (y/N): ").strip().lower()
    if save == "y":
        save_budget(year, month, budget)
        print("Budget saved successfully.")
    else:
        print("Budget not saved.")  

def save_budget(year: int, month: int, new_budget: dict):
    path = Path("config/budgets.yaml")
    ym = f"{year}-{month:02d}"

    if path.exists():
        with path.open() as f:
            data = yaml.safe_load(f) or {}   
    else:
        data = {}
    
    data[ym] = new_budget

    with path.open("w") as f:
        yaml.safe_dump(data, f, sort_keys=False)