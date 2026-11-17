from flask import Flask, request, jsonify

app = Flask(__name__)

# Try to import your engine, but don't crash if supabase is missing
try:
    from engine.task_engine import ai_work_motor
    from engine.human_verification import create_human_list, expire_human_lists
    from engine.db import supabase
    ENGINE_OK = True
except Exception as e:
    print("Engine import failed:", e)
    ENGINE_OK = False
    supabase = None

@app.route('/')
def home():
    return "Engine Five is LIVE"

@app.route('/run-task')
def run_task():
    task_id = request.args.get("task_id")
    task_type = request.args.get("task_type")
    if not ENGINE_OK:
        return jsonify({"error": "engine not loaded"}), 500
    result = ai_work_motor(supabase, task_id, task_type)
    return jsonify({"ok": True, "result": str(result)})

@app.route('/get-human-list')
def get_human_list():
    verifier_id = request.args.get("verifier_id")
    if not ENGINE_OK:
        return jsonify({"error": "engine not loaded"}), 500
    result = create_human_list(supabase, verifier_id)
    return jsonify({"ok": True, "result": str(result)})

@app.route('/expire-human')
def expire_human():
    if not ENGINE_OK:
        return jsonify({"error": "engine not loaded"}), 500
    result = expire_human_lists(supabase)
    return jsonify({"ok": True, "result": str(result)})
