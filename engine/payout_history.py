# payout_history.py
import requests

def get_payouts(batch_id=None, status=None, order_by="id", order="asc", 
               date_from=None, date_to=None, limit=20, page=0):
    url = "https://api.nowpayments.io/v1/payout/list"
    headers = {
        "x-api-key": "YOUR_API_KEY"
    }
    params = {
        "batch_id": batch_id,
        "status": status,
        "order_by": order_by,
        "order": order,
        "date_from": date_from,
        "date_to": date_to,
        "limit": limit,
        "page": page
    }
    res = requests.get(url, headers=headers, params=params)
    return res.json()

