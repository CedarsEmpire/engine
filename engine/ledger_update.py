# ledger_update.py
import psycopg2
from payout_logic import process_payout

def update_ledger(user_id, amount, type):
    conn = psycopg2.connect(dbname='enginefive')
    cur = conn.cursor()
    cur.execute("INSERT INTO ledger (user_id, amount, type) VALUES (%s, %s, %s)", (user_id, amount, type))
    conn.commit()
    cur.close()

# Cron job: daily payouts & ledger update
def daily_payouts():
    users = get_verified_users()
    for user in users:
        earnings = calculate_earnings(user['id'])
        payout_id = process_payout(user['id'], earnings)
        update_ledger(user['id'], earnings, 'earn')
        update_ledger(user['id'], -earnings, 'payout')
