# engine/human_verification.py
from dataclasses import dataclass
from datetime import datetime, timedelta
import logging

logging.basicConfig(level=logging.INFO)

@dataclass
class HumanVerificationRequest:
    task_id: str
    ai_decision: str  # e.g. "approve", "flagged"
    verification_window_minutes: int = 60  # 1 hour human window
    target_earnings: float = 15.0  # $15 target for self-verification

class HumanVerifier:
    def __init__(self, task_id, ai_decision):
        self.request = HumanVerificationRequest(
            task_id=task_id,
            ai_decision=ai_decision
        )
        self.verified = False
        self.verification_time = None
        self.earnings = 0.0

    def start_verification(self):
        logging.info(f"Human verifying task {self.request.task_id} (AI: {self.request.ai_decision})")
        # Simulate human verification process (60 minutes)
        self.verification_time = datetime.now() + timedelta(minutes=self.request.verification_window_minutes)
        return self.verification_time

    def complete_verification(self, human_decision):
        if datetime.now() > self.verification_time:
            logging.error(f"Verification window expired for task {self.request.task_id}")
            return False
        self.verified = True
        if human_decision == "approve":
            self.earnings = self.request.target_earnings
        logging.info(f"Human verified task {self.request.task_id}: {human_decision}, Earnings: ${self.earnings}")
        return human_decision == "approve"

# Example usage
verifier = HumanVerifier(task_id="123", ai_decision="approve")
verification_time = verifier.start_verification()
# Human verifies task within 60 minutes
verifier.complete_verification(human_decision="approve")
