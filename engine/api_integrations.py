# engine/api_integrations.py
import os
import requests
from dataclasses import dataclass

@dataclass
class PayoutRequest:
    amount_cents: int
    currency: str  # e.g. "USD", "GBP"
    destination: str  # payout account / wallet id from provider
    task_id: str
    idempotency_key: str  # prevents double-payout - Stripe best practice

class PayoutProvider:
    """Interface - swap Stripe / Wise / PayPal / Crypto without changing engine."""
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

class CryptoPayoutProvider(PayoutProvider):
    def __init__(self, api_key, api_secret):
        self.api_key = api_key
        self.api_secret = api_secret
        self.base_url = "https://api.coinbase.com/v2"

    def create_payout(self, req: PayoutRequest) -> dict:
        # Coinbase API endpoint for crypto payouts
        endpoint = f"{self.base_url}/accounts/{req.destination}/transactions"
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        data = {
            "type": "send",
            "to": req.destination,
            "amount": {
                "amount": str(req.amount_cents / 100),
                "currency": req.currency
            },
            "idempotency_key": req.idempotency_key
        }
        response = requests.post(endpoint, headers=headers, json=data)
        if response.status_code == 201:
            return response.json()
        else:
            raise RuntimeError(f"Crypto payout failed: {response.text}")

class PayoutService:
    def __init__(self, provider: PayoutProvider):
        self.provider = provider

    def request_payout(self, req: PayoutRequest) -> dict:
        if req.amount_cents <= 0:
            raise ValueError("amount must be > 0")
        if req.currency not in ["USD", "GBP", "EUR", "BTC", "ETH"]:
            raise ValueError("currency not supported")
        # TODO: check DB that task_id is verified + not already paid
        return self.provider.create_payout(req)
