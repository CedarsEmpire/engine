# pounds_to_crypto.py
import requests

def pounds_to_crypto(amount_pounds, currency):
    # GBP → USD approx (1 GBP ≈ 1.3 USD)
    usd_amount = amount_pounds * 1.3
    
    # USD → Crypto (fetch rate from API)
    url = f"https://api.nowpayments.io/v1/estimate?currency_from=usd&currency_to={currency}&amount_from={usd_amount}"
    headers = {
        "x-api-key": "YOUR_API_KEY"
    }
    res = requests.get(url, headers=headers)
    data = res.json()
    return data.get("estimated_amount")


Use it in timely_withdraw.py:

# timely_withdraw.py
from payments.pounds_to_crypto import pounds_to_crypto

def timely_withdraw(user_wallet, amount_pounds, network="bsc"):
    networks = {
        "bsc": "USDTBSC",
        "polygon": "USDCPolygon",
        "tron": "USDTTRC20"
    }
    currency = networks.get(network, "USDTBSC")
    
    # Convert pounds to crypto
    crypto_amount = pounds_to_crypto(amount_pounds, currency)
    
    # Rest of payout logic...
