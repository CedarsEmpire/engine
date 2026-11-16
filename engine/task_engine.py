# engine/task_engine.py
# AI WORK MOTOR - 3 VERIFIERS - SELF-COOLING 60 MIN - CREDIT 90 MIN
# Engine Five - Global - Multiple Task Types

import time
from datetime import datetime, timedelta, timezone
from verify_receipt import verify_receipt_ai
from verify_photo import verify_photo_ai
from verify_text import verify_text_ai

AI_VERIFIER_COUNT = 3
COOLING_MIN = 60
CREDIT_MIN = 90
MAX_AI_TASK_RETRIES = 5

def _utc_now():
    return datetime.now(timezone.utc)

def ai_work_motor(supabase, task_id: str, task_type: str):
    """AI runs task, 3 verifiers, self-cooling 60 min, credit 90 min."""
    verifiers = supabase.table("verifiers").select("id").eq("type", "ai").limit(AI_VERIFIER_COUNT).execute()
    verifier_ids = [v["id"] for v in (verifiers.data or [])]
    if len(verifier_ids) < AI_VERIFIER_COUNT:
        return None

    # Task-specific AI logic
    if task_type == "receipt":
        results = [verify_receipt_ai(task_id, vid) for vid in verifier_ids]
    elif task_type == "photo":
        results = [verify_photo_ai(task_id, vid) for vid in verifier_ids]
    elif task_type == "text":
        results = [verify_text_ai(task_id, vid) for vid in verifier_ids]
    else:
        return None

    # Majority vote
    approved = results.count("approved") > (AI_VERIFIER_COUNT // 2)
    verdict = "approved" if approved else "rejected"
    supabase.table("tasks").update({"status": verdict}).eq("id", task_id).execute()
    return verdict


engine/human_verification.py

# engine/human_verification.py
# HUMAN - 10 EUR / DAY - SHORT LIST - 1 HOUR EXPIRY - UTC ONLY
# Engine Five - Global - Multiple Task Types

from datetime import datetime, timedelta, timezone

HUMAN_DAILY = 10.00
HUMAN_LIST_SIZE = 10
HUMAN_EXPIRY_MIN = 60

def _utc_now():
    return datetime.now(timezone.utc)

def create_human_list(supabase, verifier_id: str):
    """Create short list: 10 tasks, 10 EUR, valid 1 hour."""
    day_start = _utc_now().replace(hour=0, minute=0, second=0, microsecond=0).isoformat()
    used = supabase.table("human_lists").select("total_value_eur").eq("verifier_id", verifier_id).eq("status", "completed").gte("created_at", day_start).execute()
    used_today = sum([r["total_value_eur"] for r in (used.data or [])])
    if used_today >= HUMAN_DAILY:
        return None

    tasks = supabase.table("tasks").select("id", "task_type").eq("status", "human_review").limit(HUMAN_LIST_SIZE).execute()
    task_ids = [t["id"] for t in (tasks.data or [])]
    expires_at = _utc_now() + timedelta(minutes=HUMAN_EXPIRY_MIN)
    result = supabase.table("human_lists").insert({
        "verifier_id": verifier_id,
        "tasks": task_ids,
        "total_value_eur": 10.00,
        "status": "active",
        "expires_at_utc": expires_at.isoformat(),
    }).execute()
    return result.data[0] if result.data else None


api/index.py

# api/index.py
# DOORS ONLY - Calls engine, no logic here
# Engine Five - Global

from engine.task_engine import ai_work_motor
from engine.human_verification import create_human_list

def api_run_task(task_id: str, task_type: str):
    return ai_work_motor(supabase, task_id, task_type)

def api_get_human_list(verifier_id: str):
    return create_human_list(supabase, verifier_id)

def main(request):
    path = request.path
    if path == "/run-task":
        task_id = request.query_params.get("task_id")
        task_type = request.query_params.get("task_type")
        return api_run_task(task_id, task_type)
    elif path == "/get-human-list":
        verifier_id = request.query_params.get("verifier_id")
        return api_get_human_list(verifier_id)
    else:
        return {"error": "invalid path"}
