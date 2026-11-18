# worker_ai.py - REAL AI WORKER - Track 1: 24/7 Verification
# Run: pip install openai python-dotenv
# Run: WORKER_ID=W-01-001 python worker_ai.py
import os, time, hashlib, json
from datetime import datetime
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
WORKER_ID = os.getenv("WORKER_ID", "W-01-001")
REGION = os.getenv("REGION", "Africa")

# Local real log - we use this until Supabase is ready
LOG_FILE = "verified_tasks.json"

def verify_task(task_text, worker_output):
    """Real OpenAI verification - not simulation"""
    res = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are CEDARS verification AI. Score 0-100 for accuracy, completeness, no hallucination. Return: SCORE: <number> REASON: <1 line> PASS/FAIL"},
            {"role": "user", "content": f"TASK: {task_text}\n\nWORKER OUTPUT: {worker_output}"}
        ]
    )
    text = res.choices[0].message.content or ""
    return text

def save_verified(task, verification):
    entry = {
        "worker_id": WORKER_ID,
        "region": REGION,
        "task": task,
        "verification": verification,
        "hash": hashlib.sha256((task+verification).encode()).hexdigest()[:16],
        "time": datetime.now().isoformat(),
        "earned_eur": 0, # €0 until real customer payment confirmed - NO FAKE MONEY
        "track": "AI-24/7"
    }
    data = []
    if os.path.exists(LOG_FILE):
        with open(LOG_FILE) as f:
            try: data = json.load(f)
            except: data = []
    data.append(entry)
    with open(LOG_FILE, "w") as f:
        json.dump(data, f, indent=2)
    return entry

print(f"✅ REAL AI WORKER STARTED: {WORKER_ID} | Region: {REGION} | Track: AI 24/7")
print("Waiting for real tasks... Type a task to verify, or press Ctrl+C to stop")

# Demo: 1 real task now to prove it works
test_task = "Translate 'Good morning, welcome to CEDARS EMPIRE' to French"
test_output = "Bonjour, bienvenue chez CEDARS EMPIRE"
print(f"\n🔍 Verifying REAL task: {test_task}")
result = verify_task(test_task, test_output)
print(f"VERIFICATION RESULT: {result}")
saved = save_verified(test_task, result)
print(f"✅ Saved to {LOG_FILE} | Hash: {saved['hash']} | Earned: €0 - waiting for real payment")

# Keep worker alive 24/7 - polls for new tasks in file tasks_to_verify.json
while True:
    time.sleep(5)
    if os.path.exists("tasks_to_verify.json"):
        with open("tasks_to_verify.json") as f:
            try: tasks = json.load(f)
            except: tasks = []
        if tasks:
            t = tasks.pop(0)
            print(f"\n🔍 New real task: {t}")
            v = verify_task(t.get("task",""), t.get("output",""))
            print(f"Result: {v}")
            save_verified(t.get("task",""), v)
            with open("tasks_to_verify.json","w") as f:
                json.dump(tasks, f)
