# balance_check.py
import requests

def get_user_balance():
    url = "https://api.nowpayments.io/v1/payout/balance"
    headers = {
        "x-api-key": "YOUR_API_KEY",
        "Content-Type": "application/json"
    }
    res = requests.get(url, headers=headers)
    return res.json()

def get_payout_status(payout_id):
    url = f"https://api.nowpayments.io/v1/payout/{payout_id}"
    headers = {
        "x-api-key": "YOUR_API_KEY",
        "Content-Type": "application/json"
    }
    res = requests.get(url, headers=headers)
    return res.json()


For /balance route:

# payout_routes.py
from payments.balance_check import get_user_balance, get_payout_status

@withdraw_bp.route('/balance', methods=['GET'])
def show_balance():
    balance_data = get_user_balance()
    # Process earnings, pending, paid from balance_data
    return jsonify({
        "earnings": balance_data.get("available"),
        "pending": balance_data.get("pending"),
        "paid": balance_data.get("total_paid")
    }), 200
