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
        "total_value_eur": HUMAN_DAILY,
        "status": "active",
        "expires_at_utc": expires_at.isoformat(),
    }).execute()
    return result.data[0] if result.data else None

def expire_human_lists(supabase):
    """Expire lists older than 1 hour."""
    now = _utc_now().isoformat()
    supabase.table("human_lists").update({"status": "expired"}).lt("expires_at_utc", now).eq("status", "active").execute()
