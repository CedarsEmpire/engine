# verify_receipt.py
# AI LOGIC FOR RECEIPT VERIFICATION
# Engine Five - Global

import os
from supabase import Client
from PIL import Image
import pytesseract
import cv2
import numpy as np

def extract_receipt_data(image_path: str):
    """Extract date, amount, merchant from receipt image."""
    # Preprocess image
    img = cv2.imread(image_path)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    text = pytesseract.image_to_string(gray)
    
    # Parse text for data
    date = None
    amount = None
    merchant = None
    
    # Simple regex parsing (you'll need real logic here)
    for line in text.splitlines():
        if "date" in line.lower():
            date = line.split(":")[-1].strip()
        elif "total" in line.lower():
            amount = line.split(":")[-1].strip()
        elif "merchant" in line.lower():
            merchant = line.split(":")[-1].strip()
    
    return {
        "date": date,
        "amount_eur": amount,
        "merchant_name": merchant
    }

def verify_receipt_ai(task_id: str, verifier_id: str):
    """AI verifies receipt task."""
    # Get receipt image from Supabase
    supabase = Client(os.getenv("SUPABASE_URL"), os.getenv("SUPABASE_KEY"))
    task = supabase.table("tasks").select("receipt_image_url").eq("id", task_id).execute()
    image_url = task.data[0]["receipt_image_url"]
    
    # Download image and verify
    image_path = f"/tmp/{task_id}.jpg"
    # (download image logic here)
    
    data = extract_receipt_data(image_path)
    # (AI check logic here - e.g., check date format, amount > 0)
    
    # Example simple check
    if data["date"] and data["amount_eur"] and data["merchant_name"]:
        return "approved"
    return "rejected"
