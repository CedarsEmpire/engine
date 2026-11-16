# fee_utils.py
import requests

def get_payout_fee(currency="USDTTRC20", amount=500):
    url = "https://api.nowpayments.io/v1/payout/fee"
    headers = {
        "x-api-key": "YOUR_API_KEY"
    }
    params = {
        "currency": currency,
        "amount": amount
    }
    res = requests.get(url, headers=headers, params=params)
    return res.json()


Use it in timely_withdraw.py:

# timely_withdraw.py
from payments.fee_utils import get_payout_fee

def timely_withdraw(user_wallet, amount_pounds, network="bsc"):
    networks = {
        "bsc": "USDTBSC",
        "tron": "USDTTRC20",
        "polygon": "USDCPolygon"
    }
    currency = networks.get(network, "USDTBSC")
    
    # Convert pounds to crypto
    crypto_amount = pounds_to_crypto(amount_pounds, currency)
    
    # Check fee
    fee_data = get_payout_fee(currency, crypto_amount)
    fee_amount = fee_data.get("fee")
    payout_amount = crypto_amount - fee_amount
    
    # Rest of payout logic...
