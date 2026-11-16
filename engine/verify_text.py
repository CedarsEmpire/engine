# engine/verify/verify_text.py
# AI LOGIC FOR TEXT VERIFICATION
# Engine Five - Global

import os
from supabase import Client
import re

def check_text_validity(text: str, task_type: str):
    """Check if text is valid per task rules."""
    # Example checks
    if task_type == "email":
        # Check if valid email format
        if re.match(r"[^@]+@[^@]+\.[^@]+", text):
            return "approved"
    elif task_type == "phone":
        # Check if valid phone number
        if re.match(r"^\d{9,15}$", text):
            return "approved"
    return "rejected"

def verify_text_ai(task_id: str, verifier_id: str):
    """AI verifies text task."""
    # Get text from Supabase
    supabase = Client(os.getenv("SUPABASE_URL"), os.getenv("SUPABASE_KEY"))
    task = supabase.table("tasks").select("text", "task_type").eq("id", task_id).execute()
    text = task.data[0]["text"]
    task_type = task.data[0]["task_type"]
    
    result = check_text_validity(text, task_type)
    return result
