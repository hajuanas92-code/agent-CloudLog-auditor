import sqlite3
from datetime import datetime

DB_FILE = "history.db"


def init_db():
    """
    Creates the history table if it doesn't already exist. Safe to call
    every time the app starts — CREATE TABLE IF NOT EXISTS won't wipe
    existing data.
    """
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS fix_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT,
            root_cause TEXT,
            pr_url TEXT
        )
    """)
    conn.commit()
    conn.close()


def add_history_entry(root_cause: str, pr_url: str):
    """
    Saves one completed fix (root cause + PR link) with the current time.
    """
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO fix_history (timestamp, root_cause, pr_url) VALUES (?, ?, ?)",
        (datetime.now().strftime("%Y-%m-%d %H:%M:%S"), root_cause, pr_url),
    )
    conn.commit()
    conn.close()


def get_all_history():
    """
    Returns all past entries, newest first.
    """
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("SELECT timestamp, root_cause, pr_url FROM fix_history ORDER BY id DESC")
    rows = cursor.fetchall()
    conn.close()
    return rows