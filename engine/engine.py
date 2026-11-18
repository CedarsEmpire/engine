from generator import TaskGenerator
from verifier import TaskVerifier
from allocator import TaskAllocator
from human_verification_interface import HumanVerificationInterface

class Engine:
    def __init__(self):
        self.task_generator = TaskGenerator()
        self.task_verifier = TaskVerifier()
        self.task_allocator = TaskAllocator(human_verifiers=[
            {'id': 1, 'available': True},
            {'id': 2, 'available': True},
            {'id': 3, 'available': True}
        ])

    def run(self):
        task_data = self.task_generator.generate_task()
        verifier_id = self.task_allocator.allocate_task(task_data)
        if verifier_id == 'AI':
            verification_result = self.task_verifier.verify_task(task_data)
        else:
            # Human verification
            interface = HumanVerificationInterface(task_data)
            interface.run()
            # Get verification result from interface
            verification_result = True  # or False
        # Update task status and verifier availability
        self.task_allocator.release_verifier(verifier_id)
