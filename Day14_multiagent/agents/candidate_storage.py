import sqlite3
from datetime import datetime


class CandidateStorage:

    def __init__(self):

        self.db_path = "database/candidates.db"

        self.create_table()


    def create_table(self):

        connection = sqlite3.connect(self.db_path)

        cursor = connection.cursor()

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS candidates (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            resume_name TEXT,

            candidate_profile TEXT,

            created_at TEXT
        )
        """)

        connection.commit()

        connection.close()


    def save_candidate(
        self,
        resume_name,
        candidate_profile
    ):

        connection = sqlite3.connect(self.db_path)

        cursor = connection.cursor()

        cursor.execute("""
        INSERT INTO candidates (
            resume_name,
            candidate_profile,
            created_at
        )

        VALUES (?, ?, ?)
        """,

        (
            resume_name,
            candidate_profile,
            datetime.now().strftime(
                "%Y-%m-%d %H:%M:%S"
            )
        ))

        connection.commit()

        connection.close()

        print(
            "\nCandidate information stored successfully."
        )