from abc import ABC, abstractmethod
from pathlib import Path
from typing import List

from .schema import Transaction

class TransactionImporter(ABC):
    source_name: str

    @abstractmethod
    def import_file(self, path: Path) -> list[Transaction]:
        """
       Parse a source-specific file and return a list of Transaction objects.
        """
        raise NotImplementedError