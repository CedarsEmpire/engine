# engine/task_engine.py
import random
from datetime import datetime

class AIWorker:
    def __init__(self, task_id, currency="USD"):
        self.task_id = task_id
        self.currency = currency
        self.status = "pending"

    def execute_task(self):
        outcome = random.choice(["success", "failure"])
        self.status = outcome
        return outcome

    def payout(self):
        if self.status == "success":
            print(f"Payout triggered for task {self.task_id} in {self.currency}")
            return True
        return False

# Example usage
worker = AIWorker(task_id=123, currency="USD")
outcome = worker.execute_task()
if outcome == "success":
    worker.payout()
