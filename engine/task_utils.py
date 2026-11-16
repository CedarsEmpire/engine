# task_utils.py
def assign_task(ai_worker_id, task_type):
    # Assign task to AI worker
    task_id = generate_task_id()
    # Save to DB: task_id, ai_worker_id, task_type, status="pending"
    return task_id


Task Status API (task_utils.py):

# task_utils.py
def get_task_status(task_id):
    # Fetch from DB: task_id → status
    return "completed"  # e.g., "pending", "completed", "failed"


Routes (task_routes.py):

# task_routes.py
from payments.task_utils import assign_task, get_task_status

@task_bp.route('/tasks', methods=['POST'])
def create_task():
    task_data = request.json
    ai_worker_id = task_data.get("ai_worker_id")
    task_type = task_data.get("task_type")
    
    task_id = assign_task(ai_worker_id, task_type)
    return jsonify({
        "task_id": task_id,
        "status": "pending"
    }), 200

@task_bp.route('/tasks/<task_id>', methods=['GET'])
def check_task_status(task_id):
    status = get_task_status(task_id)
    return jsonify({
        "task_id": task_id,
        "status": status
    }), 200
