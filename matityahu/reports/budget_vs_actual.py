from matityahu.reports.monthly import category_totals

def flatten_budget(nested_budget: dict) -> dict:
    """
    Turns {'Housing': {'rent': 1000}} into {'rent': 1000}.
    Handles both nested groups and direct category/value pairs.
    """
    flat = {}
    for key, value in nested_budget.items():
        if isinstance(value, dict):
            for sub_key, sub_val in value.items():
                flat[sub_key] = sub_val
        else:
            flat[key] = value
    return flat

def budget_vs_actual(db, budget: dict, year: int, month: int):
    flat_budget = flatten_budget(budget)
    actuals = category_totals(db, year, month)
    
    report = []

    categories = set(flat_budget.keys()) | set(actuals.keys())

    for category in sorted(categories):
        budgeted = flat_budget.get(category, 0)
        actual = actuals.get(category, 0)
        diff = budgeted - actual

        percent = (actual / budgeted * 100) if budgeted > 0 else None

        report.append({
            "category": category,
            "budgeted": budgeted,
            "actual": actual,
            "remaining": diff,
            "percent": percent,
        })
        
    return report   