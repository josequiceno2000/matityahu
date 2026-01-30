from collections import defaultdict
from typing import Dict, List
from matityahu.storage.database import Database

def category_totals(db: Database, year: int, month: int) -> Dict[str, float]:
    """
    Returns total spending per category for a given month.
    """
    ym = f"{year:04d}-{month:02d}"

    query = """
    SELECT
        category,
        SUM(amount) as total
    FROM transactions
    WHERE
        category IS NOT NULL
        AND amount < 0
        AND strftime('%Y-%m', date) = ?
    GROUP BY category
    ORDER BY total ASC;
    """

    rows = db.query(query, (ym,))
    return {row["category"]: abs(row["total"]) for row in rows}

def income_vs_expenses(db: Database, year: int, month: int) -> Dict[str, float]:
    """
    Returns total income and total expenses for a given month.
    """
    ym = f"{year:04d}-{month:02d}"

    query = """
    SELECT
        SUM(CASE WHEN amount > 0 THEN amount ELSE 0 END) as income,
        SUM(CASE WHEN amount < 0 THEN amount ELSE 0 END) as expenses
    FROM transactions
    WHERE
        strftime('%Y-%m', date) = ?;
    """

    row = db.query_one(query, (ym,))
    income = row["income"] or 0
    expenses = abs(row["expenses"] or 0)

    return {
        "income": income,
        "expenses": expenses,
        "net": income - expenses,
    }

def daily_cashflow(db: Database, year: int, month: int) -> List[dict]:
    """
    Returns daily cashflow for a given month.
    """
    ym = f"{year:04d}-{month:02d}"

    query = """
    SELECT
        date,
        SUM(amount) as net
    FROM transactions
    WHERE
        strftime('%Y-%m', date) = ?
    GROUP BY date
    ORDER BY date;
    """

    return db.query(query, (ym,))
    

    

    