# db.py - OUTSIDE, root level
import sqlite3

def get_db():
    conn = sqlite3.connect("cedars.db", check_same_thread=False)
    conn.execute("""
    CREATE TABLE IF NOT EXISTS ledger (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id TEXT NOT NULL, -- 'CENTRAL_ENGINE' or 'user_123'
        type TEXT NOT NULL, -- 'AI_TASK' or 'HUMAN_TASK' or 'WITHDRAW'
        amount REAL NOT NULL,
        task_id TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)
    return conn

def get_balance(user_id):
    conn = get_db()
    row = conn.execute("SELECT COALESCE(SUM(amount),0) FROM ledger WHERE user_id=?", (user_id,)).fetchone()
    return row[0]
