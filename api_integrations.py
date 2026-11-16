# engine/api_integrations.py
# Production-ready structure - benchmarked from Stripe / Wise
# No demo payouts. Real money only moves via real provider APIs + env keys.
import os
from dataclasses import dataclass

@dataclass
class PayoutRequest:
    amount_cents: int
    currency: str  # e.g. "USD", "GBP"
    destination: str  # payout account / wallet id from provider
    task_id: str
    idempotency_key: str  # prevents double-payout - Stripe best practice

class PayoutProvider:
    """Interface - swap Stripe / Wise / PayPal without changing engine."""
    def create_payout(self, req: PayoutRequest) -> dict:
        raise NotImplementedError

class StripePayoutProvider(PayoutProvider):
    def __init__(self):
        self.api_key = os.environ.get("STRIPE_SECRET_KEY")
        if not self.api_key:
            raise RuntimeError("Missing STRIPE_SECRET_KEY - set in env / GitHub Secrets, never in code")

    def create_payout(self, req: PayoutRequest) -> dict:
        # Real implementation uses stripe SDK:
        # import stripe; stripe.api_key = self.api_key
        # return stripe.Payout.create(amount=req.amount_cents, currency=req.currency, ...)
        # For now: fail loudly instead of faking success
        raise NotImplementedError("Connect real Stripe SDK + account before enabling payouts")

class PayoutService:
    def __init__(self, provider: PayoutProvider):
        self.provider = provider

    def request_payout(self, req: PayoutRequest) -> dict:
        if req.amount_cents <= 0:
            raise ValueError("amount must be > 0")
        if req.currency not in ["USD", "GBP", "EUR"]:
            raise ValueError("currency not supported")
        # TODO: check DB that task_id is verified + not already paid
        return self.provider.create_payout(req)
