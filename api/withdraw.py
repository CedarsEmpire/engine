# api/withdraw.py - ENGINE FIVE Payout Engine
# POST /api/withdraw -> request payout, Pounds -> Dollars only, crypto withdrawal
import json
from http.server import BaseHTTPRequestHandler

GBP_TO_USD = 1.27  # Example rate - update daily
MIN_WITHDRAW_USD = 10.0  # Crypto min depends on network fees + exchange rules
VALID_CRYPTO = ["USDT", "USDC", "BTC", "ETH"]
VALID_METHODS = ["Binance", "Trust Wallet", "Coinbase", "Other Exchange"]

class handler(BaseHTTPRequestHandler):
    def _send(self, code, data):
        body = json.dumps(data).encode()
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_OPTIONS(self):
        self._send(200, {"ok": True})

    def do_POST(self):
        try:
            length = int(self.headers.get("Content-Length", 0))
            raw = self.rfile.read(length) if length > 0 else b"{}"
            payload = json.loads(raw.decode() or "{}")
        except:
            return self._send(400, {"ok": False, "error": "Invalid JSON"})

        email = str(payload.get("email", "")).strip().lower()
        gbp_amount = float(payload.get("amount_gbp", 0) or 0)
        crypto = str(payload.get("crypto", "")).strip().upper()
        method = str(payload.get("method", "")).strip()
        address = str(payload.get("address", "")).strip()  # crypto wallet address
        balance_gbp = float(payload.get("balance_gbp", 0) or 0)  # In prod, fetch from DB

        if "@" not in email:
            return self._send(400, {"ok": False, "error": "Valid email required"})
        if crypto not in VALID_CRYPTO:
            return self._send(400, {"ok": False, "error": f"Crypto must be one of: {', '.join(VALID_CRYPTO)}"})
        if method not in VALID_METHODS:
            return self._send(400, {"ok": False, "error": f"Method must be one of: {', '.join(VALID_METHODS)}"})
        if not address:
            return self._send(400, {"ok": False, "error": "Crypto wallet address required"})
        if gbp_amount < 5.0:
            return self._send(400, {"ok": False, "error": "Minimum withdraw is £5"})
        if gbp_amount > balance_gbp:
            return self._send(400, {"ok": False, "error": f"Insufficient approved balance. Balance: £{balance_gbp:.2f}"})
        if gbp_amount <= 0:
            return self._send(400, {"ok": False, "error": "Amount must be > 0"})

        usd_amount = gbp_amount * GBP_TO_USD
        if usd_amount < MIN_WITHDRAW_USD:
            return self._send(400, {"ok": False, "error": f"Converted to ${usd_amount:.2f} USD - below crypto min of ${MIN_WITHDRAW_USD}"})

        # In production: 1) Check balance, 2) Convert, 3) Create payout row, 4) Send to exchange, 5) Log TXID
        return self._send(200, {
            "ok": True,
            "message": f"£{gbp_amount} converted to ${usd_amount:.2f} {crypto} → sent to {method}",
            "payout": {
                "email": email,
                "amount_gbp": round(gbp_amount, 2),
                "amount_usd": round(usd_amount, 2),
                "crypto": crypto,
                "method": method,
                "address": address,
                "status": "processing",
                "note": f"Exchange rate: £1 = ${GBP_TO_USD}"
            },
            "remaining_balance_gbp": round(balance_gbp - gbp_amount, 2)
        })

    def do_GET(self):
        return self._send(200, {
            "ok": True,
            "engine": "Payout Engine - Pounds to Dollars, crypto only",
            "min_withdraw_usd": MIN_WITHDRAW_USD,
            "crypto": VALID_CRYPTO,
            "methods": VALID_METHODS,
            "rate": f"£1 = ${GBP_TO_USD} (update daily)"
        })
