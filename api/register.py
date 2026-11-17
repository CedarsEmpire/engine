# api/register.py - ENGINE FIVE Worker Engine
# POST /api/register -> creates worker, returns qualification test
import json
from http.server import BaseHTTPRequestHandler

# In production, replace this with a real database (Supabase / Postgres)
# This is in-memory for Vercel demo, data resets on redeploy
WORKERS = {}

VALID_CONTINENTS = ["Africa", "North America", "South America", "Europe", "Asia", "Oceania"]

class handler(BaseHTTPRequestHandler):
    def _send(self, code, data):
        body = json.dumps(data).encode()
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_OPTIONS(self):
        self._send(200, {"ok": True})

    def do_POST(self):
        try:
            length = int(self.headers.get("Content-Length", 0))
            raw = self.rfile.read(length) if length > 0 else b"{}"
            payload = json.loads(raw.decode() or "{}")
        except:
            return self._send(400, {"ok": False, "error": "Invalid JSON"})

        name = str(payload.get("name", "")).strip()
        email = str(payload.get("email", "")).strip().lower()
        continent = str(payload.get("continent", "")).strip()
        whatsapp = str(payload.get("whatsapp", "")).strip()

        # Real validation - no fake users
        if len(name) < 2:
            return self._send(400, {"ok": False, "error": "Name required"})
        if "@" not in email or "." not in email:
            return self._send(400, {"ok": False, "error": "Valid email required"})
        if continent not in VALID_CONTINENTS:
            return self._send(400, {"ok": False, "error": "Valid continent required"})

        if email in WORKERS:
            return self._send(400, {"ok": False, "error": "Worker already registered"})

        # Create worker - starts UNQUALIFIED, must pass test to earn
        worker = {
            "name": name,
            "email": email,
            "continent": continent,
            "whatsapp": whatsapp,
            "status": "pending_qualification",
            "accuracy": 0,
            "level": "Beginner",
            "balance_eur": 0.0,
            "completed_tasks": 0,
            "daily_earned_eur": 0.0,
            "daily_target_eur": 15.0
        }
        WORKERS[email] = worker

        # Qualification test - 5 sample tasks, need 70% to unlock
        # In production, load from DB. These are real gold tasks.
        qualification = [
            {"id": "Q1", "question": "Image shows a shop selling phones. Label it:", "options": ["Shop", "Car", "Animal"], "answer": "Shop"},
            {"id": "Q2", "question": "AI answer: 'Paris is in Germany'. Is this correct?", "options": ["Correct", "Wrong"], "answer": "Wrong"},
            {"id": "Q3", "question": "Transcribe: 'Hello, how are you?'", "options": ["Hello, how are you?", "Goodbye"], "answer": "Hello, how are you?"},
            {"id": "Q4", "question": "Photo is blurry and unreadable. What to do?", "options": ["Guess", "Flag as Bad Quality"], "answer": "Flag as Bad Quality"},
            {"id": "Q5", "question": "Task pays €3. Client escrow is €0. Should you do it?", "options": ["Yes", "No - No escrow = No work"], "answer": "No - No escrow = No work"},
        ]
        # Don't send answers to frontend in real app - this is for testing
        # For now we send questions without answers
        public_test = [{"id": q["id"], "question": q["question"], "options": q["options"]} for q in qualification]

        return self._send(200, {
            "ok": True,
            "message": "Registered. Pass qualification to unlock paid work.",
            "worker": worker,
            "qualification_test": public_test,
            "pass_mark": "70% (4/5 correct)"
        })

    def do_GET(self):
        return self._send(200, {"ok": True, "engine": "Worker Engine - POST to register"})
