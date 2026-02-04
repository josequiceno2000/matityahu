def validate_categories(budget_categories: list, actual_categories: list):
    """
    Compares the categories defined in your budget for the month 
    against what is actually in your database.
    """
    budget_set = set(budget_categories)
    actual_set = set(actual_categories)

    # These are categories you spent money in, but forgot to put in your budgets.yaml
    unbudgeted = actual_set - budget_set

    if unbudgeted:
        print("\n" + "!" * 60)
        print("⚠️  UNBUDGETED SPENDING DETECTED")
        print("The following categories have transactions but no budget entries:")
        for c in sorted(unbudgeted):
            print(f"  - {c}")
        print("!" * 60 + "\n")
    
    # Optional: You could also find categories you budgeted for but didn't use
    # unused = budget_set - actual_set