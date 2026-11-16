# engine/human_verification.py
# HUMAN - 10 EUR / DAY - SHORT LIST - 1 HOUR EXPIRY - UTC ONLY
# Engine Five - Global - Do NOT put this logic in api/

from datetime import datetime, timedelta, timezone

HUMAN_DAILY = 10.00
HUMAN_LIST_SIZE = 10  # 10 tasks x 1.00 EUR = 10.00 EUR
HUMAN_EXPIRY_MIN = 60

def _utc_now():
    return datetime.now(timezone.utc)

def _utc_day_start():
    now = _utc_now()
    return now.replace(hour=0, minute=0, second=0, microsecond=0)

def create_human_list(supabase, verifier_id: str):
    """Create short list: 10 tasks, 10 EUR, valid 1 hour."""
    day_start = _utc_day_start().isoformat()

    # Check daily pool - resets 00:00 UTC
    used = supabase.table("human_lists")\
        .select("total_value_eur")\
        .eq("verifier_id", verifier_id)\
        .eq("status", "completed")\
        .gte("created_at", day_start)\
        .execute()

    used_today = sum([r["total_value_eur"] for r in (used.data or [])])
    if used_today >= HUMAN_DAILY:
        return None

    # Get 10 low-confidence tasks only
    tasks = supabase.table("tasks")\
        .select("id")\
        .eq("status", "human_review")\
        .limit(HUMAN_LIST_SIZE)\
        .execute()

    if not tasks.data:
        return None

    task_ids = [t["id"] for t in tasks.data]
    expires_at = _utc_now() + timedelta(minutes=HUMAN_EXPIRY_MIN)

    result = supabase.table("human_lists").insert({
        "verifier_id": verifier_id,
        "tasks": task_ids,
        "total_value_eur": 10.00,
        "status": "active",
        "expires_at_utc": expires_at.isoformat(),
    }).execute()

    return result.data[0] if result.data else None

def expire_human_lists(supabase):
    """If not verified in 1 hour, expire and return to AI queue."""
    now_iso = _utc_now().isoformat()

    expired = supabase.table("human_lists")\
        .select("*")\
        .eq("status", "active")\
        .lt("expires_at_utc", now_iso)\
        .execute()

    for lst in (expired.data or []):
        supabase.table("human_lists")\
            .update({"status": "expired"})\
            .eq("id", lst["id"]).execute()

        for task_id in lst["tasks"]:
            supabase.table("tasks")\
                .update({"status": "queued"})\
                .eq("id", task_id).execute()

    return len(expired.data or [])

def complete_human_task(supabase, task_id: str, verdict: str):
    """verdict = approved / rejected"""
    supabase.table("tasks")\
        .update({"status": verdict})\
        .eq("id", task_id).execute()
    return True
