class MonthlyReport:
    def __init__(self, db):
        self.db = db
    
    def _get_date_filler(self, month_str: str):
        # input: "2026-01" -> output: "01/%/2026"
        year, month = month_str.split("-")
        return f"{month}/%/{year}"
    
    def income_vs_expenses(self, month_str: str):
        date_pattern = self._get_date_filler(month_str)
        query = """
            SELECT
                SUM(CASE WHEN amount > 0 THEN amount ELSE 0 END) AS income,
                SUM(CASE WHEN amount < 0 THEN amount ELSE 0 END) as expenses
            FROM transactions
            WHERE date like ?
        """
        return self.db.query(query, (date_pattern,)).fetchone()
    
    def by_category(self, month_str: str):
        date_pattern = self._get_date_filler(month_str)
        query = """
            SELECT category, SUM(amount) as total
            FROM transactions
            WHERE date LIKE ? AND category IS NOT NULL
            GROUP BY category
            ORDER BY total DESC
        """
        return self.db.execute(query, (date_pattern,)).fetchall()
            
    

    