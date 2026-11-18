class TaskStatusManager:
    def __init__(self):
        self.tasks = {}
        self.verifiers = {}

    def update_task_status(self, task_id, status):
        # Update task status
        self.tasks[task_id]['status'] = status

    def update_verifier_availability(self, verifier_id, availability):
        # Update verifier availability
        self.verifiers[verifier_id]['available'] = availability

    def get_task_status(self, task_id):
        # Get task status
        return self.tasks[task_id]['status']

    def get_verifier_availability(self, verifier_id):
        # Get verifier availability
        return self.verifiers[verifier_id]['available']
