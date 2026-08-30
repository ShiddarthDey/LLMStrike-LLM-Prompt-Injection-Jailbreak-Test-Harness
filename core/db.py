import os
import sqlite3
from datetime import datetime, timezone

DB_PATH = os.path.join("reports", "results.db")

def init_db(db_path: str = DB_PATH):
    os.makedirs(os.path.dirname(db_path), exist_ok=True)
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS results (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT NOT NULL,
            attack_id TEXT,
            category TEXT,
            prompt TEXT,
            response TEXT,
            error TEXT,
            verdict TEXT,
            severity TEXT
        )
    """)
    conn.commit()
    conn.close()

def save_result(attack_id: str, category: str, prompt: str, response: str, error: str = None, verdict: str = None, severity: str = None, db_path: str = DB_PATH):
    ts = datetime.now(timezone.utc).isoformat()
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO results (timestamp, attack_id, category, prompt, response, error, verdict, severity) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
        (ts, attack_id, category, prompt, response, error, verdict, severity)
    )
    conn.commit()
    conn.close()
