# engine/task_engine.py
# Engine Five - Global

import os
from supabase import Client
from engine.verify.verify_receipt import verify_receipt_ai
from engine.verify.verify_photo import verify_photo_ai
from engine.verify.verify_text import verify_text_ai
from engine.verify.verify_military_equipment import verify_military_equipment_ai
from engine.verify.verify_data_annotation import verify_data_annotation_ai
from engine.verify.verify_voice_transcription import verify_voice_transcription_ai

def process_task(task_id: str, task_type: str, verifier_ids: list):
    """Process task with multiple verifiers."""
    supabase = Client(os.getenv("SUPABASE_URL"), os.getenv("SUPABASE_KEY"))
    
    # Run verifiers based on task type
    if task_type == "receipt":
        results = [verify_receipt_ai(task_id, vid) for vid in verifier_ids]
    elif task_type == "photo":
        results = [verify_photo_ai(task_id, vid) for vid in verifier_ids]
    elif task_type == "text":
        results = [verify_text_ai(task_id, vid) for vid in verifier_ids]
    elif task_type == "military_equipment":
        results = [verify_military_equipment_ai(task_id, vid) for vid in verifier_ids]
    elif task_type == "data_annotation":
        results = [verify_data_annotation_ai(task_id, vid) for vid in verifier_ids]
    elif task_type == "voice_transcription":
        results = [verify_voice_transcription_ai(task_id, vid) for vid in verifier_ids]
    else:
        return "error: task type not supported"
    
    # Aggregate results
    approval_count = results.count("approved")
    if approval_count >= len(verifier_ids) * 0.7:  # 70% approval needed
        supabase.table("tasks").update({"status": "approved"}).eq("id", task_id).execute()
        return "approved"
    else:
        supabase.table("tasks").update({"status": "rejected"}).eq("id", task_id).execute()
        return "rejected"

# Example usage
task_id = "task_123"
task_type = "voice_transcription"
verifier_ids = ["verifier1", "verifier2", "verifier3"]
result = process_task(task_id, task_type, verifier_ids)
print(result)
