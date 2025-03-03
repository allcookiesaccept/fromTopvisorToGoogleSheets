from abc import ABC, abstractmethod
from typing import List, Dict


class DatabaseInterface(ABC):
    @abstractmethod
    def create(self, table_name: str, data: Dict):
        """Insert a new record into the specified table."""
        pass

    @abstractmethod
    def read(self, table_name: str, filters: Dict = None) -> List[Dict]:
        """Retrieve records from the specified table."""
        pass

    @abstractmethod
    def update(self, table_name: str, filters: Dict, data: Dict):
        """Update records in the specified table."""
        pass

    @abstractmethod
    def delete(self, table_name: str, filters: Dict):
        """Delete records from the specified table."""
        pass