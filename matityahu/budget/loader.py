import yaml
from pathlib import Path

class BudgetLoader:
    def __init__(self, path: Path):
        self.path = path
        self.data = self._load()

    def _load(self):
        if not self.path.exists():
            return {}
        with open(self.path, "r") as f:
            return yaml.safe_load(f) or {}
    
    def get_month(self, year: int, month: int):
        key = f"{year:04d}-{month:02d}"
        return self.data.get(key, {})