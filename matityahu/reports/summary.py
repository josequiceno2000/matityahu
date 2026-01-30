
from matityahu.reports.monthly import MonthlyReport


def monthly_summary(db, month):
    report = MonthlyReport(db)

    income, expenses = report.income_vs_expenses(month)[0]
    net = income + expenses # expenses is negative

    categories = report.by_category(month)

    return {
        "month": month,
        "income": income,
        "expenses": abs(expenses),
        "net": net,
        "categories": categories
    }

