import yaml
from pathlib import Path
from typing import Optional

class Categorizer:
    def __init__(self, rules_path: Path):
        self.rules = self._load_rules(rules_path)
    
    def _load_rules(self, path: Path) -> dict[str, list[str]]:
        with path.open() as f:
            return yaml.safe_load(f) or {}
    
    def categorize(self, description: str) -> Optional[str]:
        """
        Returns a category name or None if no rule matches.
        """
        desc = description.lower()

        for category, keywords in self.rules.items():
            for keyword in keywords:
                if keyword in desc:
                    return category
        
        return None