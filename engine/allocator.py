import random

class TaskAllocator:
    def __init__(self, human_verifiers):
        self.human_verifiers = human_verifiers

    def allocate_task(self, task_data):
        # Allocate task to human verifier based on availability and expertise
        available_verifiers = [verifier for verifier in self.human_verifiers if verifier['available']]
        if available_verifiers:
            selected_verifier = random.choice(available_verifiers)
            selected_verifier['available'] = False
            return selected_verifier['id']
        else:
            # No available human verifiers, allocate to AI verifier
            return 'AI'

    def release_verifier(self, verifier_id):
        for verifier in self.human_verifiers:
            if verifier['id'] == verifier_id:
                verifier['available'] = True
                break
