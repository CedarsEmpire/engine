# engine/verify/verify_voice_transcription.py
# AI LOGIC FOR VOICE TRANSCRIPTION VERIFICATION
# Engine Five - Global

import os
from supabase import Client

def check_transcription_accuracy(transcription_data: dict):
    """Check if voice transcription is accurate."""
    # Example checks
    required_fields = ["transcript_text", "confidence_score", "audio_duration"]
    if not all(field in transcription_data for field in required_fields):
        return "rejected"
    
    if transcription_data["confidence_score"] < 0.75:
        return "rejected"
    
    return "approved"

def verify_voice_transcription_ai(task_id: str, verifier_id: str):
    """AI verifies voice transcription task."""
    # Get transcription data from Supabase
    supabase = Client(os.getenv("SUPABASE_URL"), os.getenv("SUPABASE_KEY"))
    task = supabase.table("tasks").select("transcription_data").eq("id", task_id).execute()
    transcription_data = task.data[0]["transcription_data"]
    
    result = check_transcription_accuracy(transcription_data)
    return result


Update task_engine.py
Add to task_engine.py:

from engine.verify.verify_voice_transcription import verify_voice_transcription_ai

# ...
elif task_type == "voice_transcription":
    results = [verify_voice_transcription_ai(task_id, vid) for vid in verifier_ids]
