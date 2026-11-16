# user_verification.py
import requests

def verify_user_kyc(user_id, verification_code):
    url = f"https://api.nowpayments.io/v1/payout/{user_id}/verify"
    headers = {
        "x-api-key": "YOUR_API_KEY",
        "Content-Type": "application/json"
    }
    payload = {
        "verification_code": verification_code
    }
    res = requests.post(url, json=payload, headers=headers)
    return res.json()

def check_verification_status(user_id):
    # Check if user passed KYC and 60-day check
    url = f"https://api.nowpayments.io/v1/user/{user_id}/status"
    headers = {
        "x-api-key": "YOUR_API_KEY",
        "Content-Type": "application/json"
    }
    res = requests.get(url, headers=headers)
    return res.json()


For /verify route:

# payout_routes.py
from payments.user_verification import verify_user_kyc, check_verification_status

@withdraw_bp.route('/verify', methods=['POST'])
def verify_user():
    data = request.json
    user_id = data.get('user_id')
    code = data.get('verification_code')
    
    if not user_id or not code:
        return jsonify({"error": "user_id and code required"}), 400
    
    result = verify_user_kyc(user_id, code)
    return jsonify(result), 200

@withdraw_bp.route('/verify/status', methods=['GET'])
def get_verification_status():
    user_id = request.args.get('user_id')
    if not user_id:
        return jsonify({"error": "user_id required"}), 400
    
    status = check_verification_status(user_id)
    return jsonify({
        "kyc_passed": status.get("kyc"),
        "verified_60_days": status.get("verified")
    }), 200
