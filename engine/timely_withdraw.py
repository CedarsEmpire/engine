# payout_routes.py
from flask import Blueprint, request, jsonify
from payments.timely_withdraw import timely_withdraw

withdraw_bp = Blueprint('withdraw', __name__)

@withdraw_bp.route('/withdraw', methods=['POST'])
def process_withdraw():
    data = request.json
    user_wallet = data.get('wallet')
    amount_pounds = data.get('amount')
    network = data.get('network', 'bsc')  # default BSC
    
    if not user_wallet or not amount_pounds:
        return jsonify({"error": "wallet and amount required"}), 400
    
    # Min/max checks
    min_amount = 100
    max_amount = 20000
    if amount_pounds < min_amount:
        return jsonify({"error": f"minimum withdraw £{min_amount}"}), 400
    if amount_pounds > max_amount:
        return jsonify({"error": f"maximum withdraw £{max_amount}"}), 400
    
    try:
        result = timely_withdraw(user_wallet, amount_pounds, network)
        return jsonify(result), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
