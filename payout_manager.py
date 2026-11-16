# engine/payout_manager.py
from api_integrations import PayoutService, PayoutRequest
from human_verification import HumanVerifier
from datetime import datetime, timedelta

class PayoutManager:
    def __init__(self, payout_service):
        self.payout_service = payout_service
        self.batch_payouts = []
        self.batch_threshold = 100  # Batch payouts above $100
        self.batch_window = timedelta(hours=24)  # Batch payouts every 24 hours
        self.payout_tracking = {}  # Track payouts

    def add_to_batch(self, req: PayoutRequest):
        self.batch_payouts.append(req)
        if sum(req.amount_cents for req in self.batch_payouts) >= self.batch_threshold * 100:
            self.process_batch_payouts()

    def process_batch_payouts(self):
        # Process batch payouts every 24 hours or when threshold reached
        if self.batch_payouts:
            batch_req = PayoutRequest(
                amount_cents=sum(req.amount_cents for req in self.batch_payouts),
                currency=self.batch_payouts[0].currency,
                destination="batch_payout_wallet",  # Update with real wallet ID
                task_id="batch",
                idempotency_key=f"batch-{datetime.now().isoformat()}"
            )
            result = self.payout_service.request_payout(batch_req)
            self.track_payout(batch_req, result)
            self.batch_payouts = []

    def process_ai_payout(self, task_id, amount, currency):
        # Create payout request for AI worker
        req = PayoutRequest(
            amount_cents=int(amount * 100),
            currency=currency,
            destination="ai_worker_wallet",  # Update with real wallet ID
            task_id=task_id,
            idempotency_key=f"ai-{task_id}"
        )
        if amount >= self.batch_threshold:
            self.add_to_batch(req)
        else:
            result = self.payout_service.request_payout(req)
            self.track_payout(req, result)
            return result

    def process_human_payout(self, human_verifier: HumanVerifier):
        # Create payout request for human verifier
        req = PayoutRequest(
            amount_cents=int(human_verifier.earnings * 100),
            currency="USD",
            destination="human_verifier_wallet",  # Update with real wallet ID
            task_id=human_verifier.request.task_id,
            idempotency_key=f"human-{human_verifier.request.task_id}"
        )
        if human_verifier.earnings >= self.batch_threshold:
            self.add_to_batch(req)
        else:
            result = self.payout_service.request_payout(req)
            self.track_payout(req, result)
            return result

    def track_payout(self, req: PayoutRequest, result):
        # Track payout in payout_tracking dictionary
        self.payout_tracking[req.task_id] = {
            "amount": req.amount_cents / 100,
            "currency": req.currency,
            "destination": req.destination,
            "status": result["status"] if result else "failed"
        }

    def get_payout_report(self):
        # Generate payout report
        return self.payout_tracking

# Example usage
payout_service = PayoutService(provider=StripePayoutProvider())
payout_manager = PayoutManager(payout_service)

# AI worker payout
payout_manager.process_ai_payout(task_id="123", amount=10.87, currency="USD")

# Human verifier payout
verifier = HumanVerifier(task_id="123", ai_decision="approve")
verifier.complete_verification(human_decision="approve")
payout_manager.process_human_payout(verifier)

# Get payout report
print(payout_manager.get_payout_report())


Cryptocurrency Integration
To integrate with cryptocurrencies, update api_integrations.py to include crypto payout providers (e.g., Coinbase, Binance).


# engine/api_integrations.py
class CryptoPayoutProvider(PayoutProvider):
    def __init__(self, api_key, api_secret):
        self.api_key = api_key
        self.api_secret = api_secret
        self.base_url = "https://api.coinbase.com/v2"

    def create_payout(self, req: PayoutRequest) -> dict:
        # Implement crypto payout logic using Coinbase API
        # ...
        pass
