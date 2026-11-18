# engine/ledger_update.py
from db import get_db

def credit(user_id, amount, task_id, type="HUMAN_TASK"):
    # NEVER do UPDATE users SET balance = X
    # ALWAYS INSERT into ledger
    conn = get_db()
    conn.execute("INSERT INTO ledger (user_id, type, amount, task_id) VALUES (?,?,?,?)",
                 (user_id, type, amount, task_id))
    conn.commit()
