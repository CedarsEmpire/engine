# payout_routes.py
from payments.payout_history import get_payouts

@withdraw_bp.route('/payouts', methods=['GET'])
def list_payouts():
    status = request.args.get('status')  # sending, completed, failed
    limit = int(request.args.get('limit', 20))
    page = int(request.args.get('page', 0))
    
    payouts = get_payouts(status=status, limit=limit, page=page)
    return jsonify({
        "payouts": payouts.get("data"),
        "total": payouts.get("total"),
        "page": page,
        "limit": limit
    }), 200

