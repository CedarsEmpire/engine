# engine/payout_logic.py
import pounds_to_crypto

class PayoutLogic:
    def __init__(self, worker):
        self.worker = worker
        self.balance = 0

    def update_balance(self, amount):
        self.balance += amount

    def payout_crypto(self):
        if self.balance > 0:
            crypto_amount = pounds_to_crypto.convert(self.balance)
            # Crypto payout logic here
            self.balance = 0
            return crypto_amount
        return 0
