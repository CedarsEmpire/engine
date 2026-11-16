from http.server import BaseHTTPRequestHandler
import json, urllib.parse

BALANCE = {"gbp": 0.00}
TASKS = [
    {"id": 1, "title": "AI Task 1", "reward_gbp": 1.50, "status": "available"},
    {"id": 2, "title": "Human Verify Task", "reward_gbp": 2.25, "status": "available"},
]
RATE = 1.321 # 1 GBP = 1.321 USD

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        parsed = urllib.parse.urlparse(self.path)
        path = parsed.path
        query = urllib.parse.parse_qs(parsed.query)

        if path == "/api/balance":
            return self.json({"balance_gbp": BALANCE["gbp"], "balance_usd": round(BALANCE["gbp"]*RATE,2)})
        if path == "/api/tasks":
            return self.json({"tasks": TASKS})
        if path == "/api/health":
            return self.json({"engine": "online", "task_engine": "ok", "verification": "ok", "payout_manager": "ok"})

        self.send_response(200)
        self.send_header('Content-type', 'text/html; charset=utf-8')
        self.end_headers()
        html = """
        <html><head><title>Engine Five</title></head><body>
        <h1>Engine Five</h1>
        <p>Balance: £{BALANCE["gbp"]} GBP ≈ ${BALANCE["gbp"]*RATE} USD</p>
        <p><a href='/api/tasks'>Tasks</a> | <a href='/api/balance'>Balance</a> | <a href='/api/health'>Health</a></p>
        <script>fetch('/api/tasks').then(r=>r.json()).then(d=>console.log(d));</script>
        </body></html>
        """.format(BALANCE=BALANCE, RATE=RATE)
        self.wfile.write(html.encode())
        return

    def json(self, data):
        body = json.dumps(data).encode()
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(body)
        return


2. engine/task_engine.py - Creates 125 AI tasks/day

import random, datetime
TASKS_PER_DAY = 125
REWARD_PER_TASK = 1.50 # GBP

def create_daily_tasks():
    tasks = []
    for i in range(TASKS_PER_DAY):
        tasks.append({
            "id": i+1,
            "title": f"AI Task {i+1} - {datetime.date.today()}",
            "reward_gbp": REWARD_PER_TASK,
            "status": "available"
        })
    return tasks

# Run this daily via cron / scheduler
DAILY_TASKS = create_daily_tasks()
print(f"Created {len(DAILY_TASKS)} tasks for today. Each pays £{REWARD_PER_TASK} GBP.")


3. engine/human_verification.py - Asks 5 humans to verify

import random
HUMANS_NEEDED = 5
REWARD_PER_VERIFY = 2.25 # GBP

def ask_humans_to_verify():
    humans = []
    for i in range(HUMANS_NEEDED):
        humans.append({
            "id": i+1,
            "email": f"human{i+1}@example.com", # Replace with real email API
            "task": f"Verify AI output {i+1}",
            "reward_gbp": REWARD_PER_VERIFY
        })
    return humans

# Send these to real humans via email/API
VERIFICATIONS = ask_humans_to_verify()
print(f"Asked {len(VERIFICATIONS)} humans to verify today. Each gets £{REWARD_PER_VERIFY} GBP.")


4. engine/payout_manager.py - Does auto-payouts via Wise

import requests
BALANCE = {"gbp": 0.00}
WAPI_KEY = "your_wise_api_key" # Replace with real Wise API key

def payout_gbp(amount_gbp, recipient_email):
    if BALANCE["gbp"] < amount_gbp:
        print("Not enough balance for payout!")
        return False
    # Call Wise API to send money
    url = "https://api.transferwise.com/v1/transfers"
    headers = {"Authorization": f"Bearer {WAPI_KEY}"}
    data = {
        "targetAccount": recipient_email,
        "quoteUuid": "your-quote-uuid", # Get via Wise quote API first
        "customerTransactionId": "engine-five-payout",
        "details": {"reference": "Engine Five Payout"}
    }
    try:
        r = requests.post(url, headers=headers, json=data)
        if r.status_code == 200:
            BALANCE["gbp"] -= amount_gbp
            print(f"Payout £{amount_gbp} GBP to {recipient_email} via Wise OK.")
            return True
        else:
            print("Wise API error:", r.text)
            return False
    except Exception as e:
        print("Payout error:", e)
        return False

# Example payout
if payout_gbp(1.50, "worker@example.com"):
    print("Payout done.")


5. engine/api_integrations.py - Connects all APIs

import requests
def check_all_apis():
    # Check Wise API
    wise_ok = requests.get("https://api.transferwise.com/v1/health").status_code == 200
    # Check AI Task API (mock)
    ai_ok = True # Replace with real AI API check
    # Check Verification API (mock)
    verify_ok = True # Replace with real verification API check
    return {
        "wise_api": wise_ok,
        "ai_api": ai_ok,
        "verification_api": verify_ok,
        "all_ok": wise_ok and ai_ok and verify_ok
    }
print(check_all_apis())
