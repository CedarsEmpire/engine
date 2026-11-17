# api/verify.py - ENGINE FIVE Verification Engine
# POST /api/verify -> AI pre-check + gold task + human approve
import json
from http.server import BaseHTTPRequestHandler
import random

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

        task_id = str(payload.get("task_id", "")).strip()
        worker_email = str(payload.get("worker_email", "")).strip().lower()
        answer = str(payload.get("answer", "")).strip()
        # In prod, fetch task + worker from DB

        # AI pre-check
        ai_flags = []
        if len(answer) < 2:
            ai_flags.append("Answer too short")
        if "copy-paste" in answer.lower():
            ai_flags.append("Possible copy-paste")

        # Gold task check (10% chance)
        gold_task = random.random() < 0.1
        if gold_task:
            # Example gold task - in prod, load from DB
            gold_answer = "Shop" if task_id == "T-1" else "Correct"
            if answer != gold_answer:
                return self._send(200, {
                    "ok": False,
                    "verified": False,
                    "reason": "Gold task failed",
                    "accuracy_drop": True
                })

        # Human approval needed if AI flags
        if ai_flags:
            return self._send(200, {
                "ok": True,
                "verified": False,
                "ai_flags": ai_flags,
                "status": "pending_human_review"
            })

        # All good
        return self._send(200, {
            "ok": True,
            "verified": True,
            "message": "Answer approved",
            "payout_eur": 3.0  # Example payout
        })

