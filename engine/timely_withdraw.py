import requests

def get_network_fees():
    # Approx fees in USD
    return {
        "bsc": 0.20,     # BNB Smart Chain
        "polygon": 0.10,  # Polygon
        "tron": 1.00      # TRON
    }

def timely_withdraw(user_wallet, amount_usd, network="bsc"):
    networks = {
        "bsc": "usdtbsc",    # BNB Smart Chain
        "polygon": "usdcpolygon",  # Polygon
        "tron": "usdctrx"    # TRON
    }
    currency = networks.get(network, "usdtbsc")  # default BSC
    fees = get_network_fees()
    network_fee_usd = fees.get(network, 0.20)
    
    # 15% fee on amount
    fee_percent = 0.15
    fee_amount_usd = amount_usd * fee_percent
    payout_amount_usd = amount_usd - fee_amount_usd
    
    # Convert USD to USDT ~1:1
    payout_amount = payout_amount_usd
    total_fee_usd = network_fee_usd + fee_amount_usd
    
    url = "https://api.nowpayments.io/v1/payout"
    headers = {
        "x-api-key": "YOUR_API_KEY",
        "Content-Type": "application/json"
    }
    payload = {
        "address": user_wallet,
        "currency": currency,
        "amount": payout_amount,
        "ipn_callback_url": "https://enginefive.com/webhook/payout"
    }
    res = requests.post(url, json=payload, headers=headers)
    return {
        "payout_id": res.json().get("id"),
        "amount_sent": payout_amount_usd,
        "total_fee": total_fee_usd,
        "network_fee": network_fee_usd,
        "percent_fee": fee_amount_usd,
        "status": res.json().get("status")
    }

# Example:
result = timely_withdraw("0x...", 100, network="polygon")
print(result)
# Output: 
# {
#   'payout_id': '123',
#   'amount_sent': 85.0,
#   'total_fee': 15.1,
#   'network_fee': 0.1,
#   'percent_fee': 15.0,
#   'status': 'CREATED'
# }
