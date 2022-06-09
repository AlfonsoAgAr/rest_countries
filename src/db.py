import sqlite3, os

class DB:
    def __init__(self, db_name: str) -> None:
        if db_name not in os.listdir():
            self.db = sqlite3.connect(db_name)
            self.do = self.db.cursor()
            self.do.execute(
                """
                CREATE TABLE IF NOT EXISTS countries(
                    region TEXT,
                    city TEXT,
                    language TEXT,
                    time TEXT
                    );
                """)
            self.db.commit()
        else:
            self.db = sqlite3.connect(db_name)
            self.do = self.db.cursor()
    
    def add(self, region: str, city: str, lang: str, time: str, table: str = 'countries') -> None:
        """
        Add a new element to table.
        """
        self.do.execute(
            f"""
            INSERT INTO {table}(region, city, language, time)
            VALUES(?, ?, ?, ?);
            """,
            (
                region,
                city,
                lang,
                time
            )
        )
        self.db.commit()
    
    def get_all_from(self, table: str) -> list:
        """
        Return all elements from table.
        """
        return [row for row in self.do.execute(f"SELECT * FROM {table}")]