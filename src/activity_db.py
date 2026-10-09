
import sqlite3
import pandas as pd
from pathlib import Path
from datetime import datetime

BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "database" / "cinematch.db"


def init_db():
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)

    with sqlite3.connect(DB_PATH) as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS user_activity (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT,
                action TEXT NOT NULL,
                movie_title TEXT,
                genre TEXT,
                activity_time TEXT NOT NULL
            )
        """)


def log_activity(action, movie_title="", genre="", username="Guest"):
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute("""
            INSERT INTO user_activity
            (username, action, movie_title, genre, activity_time)
            VALUES (?, ?, ?, ?, ?)
        """, (
            username,
            action,
            movie_title,
            genre,
            datetime.now().isoformat(timespec="seconds")
        ))


def get_activities():
    with sqlite3.connect(DB_PATH) as conn:
        return pd.read_sql_query(
            "SELECT * FROM user_activity ORDER BY id DESC",
            conn
        )