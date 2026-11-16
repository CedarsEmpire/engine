# api/index.py
# DOORS ONLY - Calls engine, no logic here
# Engine Five - Global

from engine.task_engine import ai_work_motor
from engine.human_verification import create_human_list, expire_human_lists
import os

def api_run_task(task_id: str, task_type: str):
    """API: Run task via AI Motor"""
    return ai_work_motor(supabase, task_id, task_type)

def api_get_human_list(verifier_id: str):
    """API: Get human short list"""
    return create_human_list(supabase, verifier_id)

def api_expire_human_lists():
    """API: Expire human lists every minute"""
    return expire_human_lists(supabase)

# Vercel handler
def main(request):
    path = request.path
    if path == "/run-task":
        task_id = request.query_params.get("task_id")
        task_type = request.query_params.get("task_type")
        return api_run_task(task_id, task_type)
    elif path == "/get-human-list":
        verifier_id = request.query_params.get("verifier_id")
        return api_get_human_list(verifier_id)
    elif path == "/expire-human":
        return api_expire_human_lists()
    else:
        return {"error": "invalid path"}
