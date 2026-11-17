# engine/payout_logic.py
import pounds_to_crypto
import targets

class PayoutLogic:
    def __init__(self, worker):
        self.worker = worker
        self.balance = 0
        self.ai_target = targets.Targets.AI_DAILY_TARGET  # €2500 daily

    def update_balance(self, amount):
        self.balance += amount

    def check_ai_payout(self):
        if self.worker.type == 'AI' and self.balance >= self.ai_target:
            # Payout €2500 (or balance if less)
            payout_amount = min(self.balance, self.ai_target)
            crypto_amount = pounds_to_crypto.convert(payout_amount)
            # Crypto payout logic here
            self.balance -= payout_amount
            return crypto_amount
        return 0

    def payout_crypto(self):
        if self.balance > 0:
            # Human €15 payout + AI target payout
            if self.worker.type == 'human':
                crypto_amount = pounds_to_crypto.convert(self.balance)
                self.balance = 0
                return crypto_amount
            elif self.worker.type == 'AI':
                return self.check_ai_payout()
        return 0
