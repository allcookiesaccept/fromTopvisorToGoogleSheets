import sqlite3
from pathlib import Path
from typing import List, Dict
from db.db_interface import DatabaseInterface

class SQLiteDB(DatabaseInterface):
    def __init__(self, db_path: str = "data.db"):
        self.db_path = db_path
        self.conn = None
        self._initialize_db()

    def _initialize_db(self):
        """Initialize the database and create tables if they don't exist."""
        self.conn = sqlite3.connect(self.db_path)
        cursor = self.conn.cursor()

        # Example: Create a table for project data
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS project_data (
                date TEXT,
                project_id INTEGER,
                region_index INTEGER,
                all_positions INTEGER,
                top_1_3 INTEGER,
                top_1_10 INTEGER,
                top_11_30 INTEGER,
                top_31_50 INTEGER,
                top_51_100 INTEGER,
                avg_position REAL,
                visibility REAL,
                folder_id INTEGER,
                PRIMARY KEY (date, project_id, region_index)
            )
        """)
        self.conn.commit()

    def create(self, table_name: str, data: Dict):
        """Insert a new record into the specified table."""
        cursor = self.conn.cursor()
        columns = ", ".join(data.keys())
        placeholders = ", ".join(["?"] * len(data))
        query = f"INSERT OR IGNORE INTO {table_name} ({columns}) VALUES ({placeholders})"
        cursor.execute(query, list(data.values()))
        self.conn.commit()

    def read(self, table_name: str, filters: Dict = None) -> List[Dict]:
        """Retrieve records from the specified table."""
        cursor = self.conn.cursor()
        query = f"SELECT * FROM {table_name}"
        params = []

        if filters:
            conditions = " AND ".join([f"{key} = ?" for key in filters.keys()])
            query += f" WHERE {conditions}"
            params = list(filters.values())

        cursor.execute(query, params)
        rows = cursor.fetchall()
        columns = [column[0] for column in cursor.description]
        return [dict(zip(columns, row)) for row in rows]

    def update(self, table_name: str, filters: Dict, data: Dict):
        """Update records in the specified table."""
        cursor = self.conn.cursor()
        set_clause = ", ".join([f"{key} = ?" for key in data.keys()])
        where_clause = " AND ".join([f"{key} = ?" for key in filters.keys()])
        query = f"UPDATE {table_name} SET {set_clause} WHERE {where_clause}"
        cursor.execute(query, list(data.values()) + list(filters.values()))
        self.conn.commit()

    def delete(self, table_name: str, filters: Dict):
        """Delete records from the specified table."""
        cursor = self.conn.cursor()
        where_clause = " AND ".join([f"{key} = ?" for key in filters.keys()])
        query = f"DELETE FROM {table_name} WHERE {where_clause}"
        cursor.execute(query, list(filters.values()))
        self.conn.commit()

    def close(self):
        """Close the database connection."""
        if self.conn:
            self.conn.close()