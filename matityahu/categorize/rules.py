import yaml
import logging
from pathlib import Path
from typing import Optional

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
logger = logging.getLogger(__name__)

class Categorizer:
    def __init__(self, rules_path: Path):
        self.rules = self._load_rules(rules_path)
        logger.info(f"Loaded {len(self.rules)} categories from {rules_path}")
    
    def _load_rules(self, path: Path) -> dict[str, list[str]]:
        try:
            with path.open() as f:
                data = yaml.safe_load(f)
                return data if data else {}
        except FileNotFoundError:
            logger.error(f"Rules file not found: {path}")
            return {}
    
    def categorize(self, description: str) -> Optional[str]:
        """
        Returns a category name or None if no rule matches.
        """
        desc = description.lower().strip()
        logger.debug(f"Categorizing: '{desc}'")

        for category, keywords in self.rules.items():
            for keyword in keywords:
                clean_keyword = keyword.lower().strip()

                if clean_keyword in desc:
                    logger.info(f"MATCH: Found '{clean_keyword}' in '{desc}' -> Category: {category}")
                    return category
        
        logger.warning(f"NO MATCH: No keywords found for '{desc}'")
        
        return None
    
    def suggest(self, description: str) -> str | None:
        """
        Alias for categorize(), but semantically clearer for suggestions.
        """
        return self.categorize(description)