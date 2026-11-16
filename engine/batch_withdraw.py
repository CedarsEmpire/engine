
# timely_withdraw.py
import requests

def pounds_to_crypto(amount_pounds, currency="usdtbsc"):
    # Approx 1 GBP ≈ 1.2 USDT
    conversion = {
        "usdtbsc": 1.2,  # 1 GBP ≈ 1.2 USDT BSC
        "usdcpolygon": 1.2,  # 1 GBP ≈ 1.2 USDC Polygon
        "usdctrx": 1.2  # 1 GBP ≈ 1.2 USDT TRON
    }
    rate = conversion.get(currency, 1.2)
    return amount_pounds * rate

def timely_withdraw(user_wallet, amount_pounds, network="bsc"):
    networks = {
        "bsc": "usdtbsc",
        "polygon": "usdcpolygon",
        "tron": "usdctrx"
    }
    currency = networks.get(network, "usdtbsc")
    
    # Convert pounds to crypto
    crypto_amount = pounds_to_crypto(amount_pounds, currency)
    
    # 15% fee
    fee_percent = 0.15
    fee_amount = crypto_amount * fee_percent
    payout_amount = crypto_amount - fee_amount
    
    # Rest of payout logic...
    url = "https://api.nowpayments.io/v1/payout"
    payload = {
        "address": user_wallet,
        "currency": currency,
        "amount": payout_amount,
        "ipn_callback_url": "https://enginefive.com/webhook/payout"
    }
    res = requests.post(url, json=payload, headers=headers)
    return res.json()
