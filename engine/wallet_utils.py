
# wallet_utils.py
import requests

def validate_wallet_address(address, currency="eth", extra_id=None):
    url = "https://api.nowpayments.io/v1/payout/validate-address"
    headers = {
        "x-api-key": "YOUR_API_KEY",
        "Content-Type": "application/json"
    }
    payload = {
        "address": address,
        "currency": currency,
        "extra_id": extra_id
    }
    res = requests.post(url, json=payload, headers=headers)
    return res.json()


Use it in timely_withdraw.py:

# timely_withdraw.py
from payments.wallet_utils import validate_wallet_address

def timely_withdraw(user_wallet, amount, network="bsc"):
    # Validate wallet first
    currency = networks.get(network, "usdtbsc")
    valid = validate_wallet_address(user_wallet, currency)
    if not valid.get("is_valid"):
        raise ValueError("Invalid wallet address")
    
    # Rest of payout logic...
