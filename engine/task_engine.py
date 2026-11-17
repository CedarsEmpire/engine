# engine/task_engine.py
import targets
import human_verification
import ai_workers

class TaskEngine:
    def __init__(self, region):
        self.region = region
        self.targets = targets.Targets(region)
        self.tasks = []

    def create_task(self, task_type, client):
        # Real task from a real client
        if self.targets.enabled:
            task = {
                'type': task_type,
                'client': client,
                'status': 'pending'
            }
            self.tasks.append(task)
            return task
        return None

    def assign_ai(self, task):
        # AI does pre-labelling
        ai_workers.process(task)

    def assign_human(self, task):
        # Human does final check
        human_verification.check(task)
        # €15 reward if QA passes
        if task['status'] == 'verified':
            return targets.Targets.HUMAN_VERIFICATION_REWARD
        return 0
