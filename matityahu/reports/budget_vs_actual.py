from matityahu.reports.monthly import category_totals

def budget_vs_actual(db, budget: dict, year: int, month: int):
    actuals = category_totals(db, year, month)
    
    report = []

    categories = set(budget.keys()) | set(actuals.keys())

    for category in sorted(categories):
        budgeted = budget.get(category, 0)
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