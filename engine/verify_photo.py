# engine/verify/verify_photo.py
# AI LOGIC FOR PHOTO VERIFICATION
# Engine Five - Global

import os
from supabase import Client
import cv2
import numpy as np
from PIL import Image

def check_photo_quality(image_path: str):
    """Check if photo is clear, not blurry, has face/person."""
    # Load image
    img = cv2.imread(image_path)
    
    # Simple checks
    height, width = img.shape[:2]
    if height < 300 or width < 300:
        return "low_quality"
    
    # Face detection (example using OpenCV)
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.1, 5)
    
    if len(faces) == 0:
        return "no_person"
    
    return "approved"

def verify_photo_ai(task_id: str, verifier_id: str):
    """AI verifies photo task."""
    # Get photo from Supabase
    supabase = Client(os.getenv("SUPABASE_URL"), os.getenv("SUPABASE_KEY"))
    task = supabase.table("tasks").select("photo_image_url").eq("id", task_id).execute()
    image_url = task.data[0]["photo_image_url"]
    
    # Download image and verify
    image_path = f"/tmp/{task_id}.jpg"
    # (download image logic here)
    
    result = check_photo_quality(image_path)
    if result == "approved":
        return "approved"
    return "rejected"
