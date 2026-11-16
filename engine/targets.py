# targets.py
targets = {
    "ai_workers": 2500,  # £2500 daily
    "human_verifications": 15  # £15 daily
}


Check progress (progress_routes.py):

# progress_routes.py
from payments.targets import targets

@progress_bp.route('/targets', methods=['GET'])
def check_targets():
    return jsonify({
        "ai_workers": targets["ai_workers"],
        "human_verifications": targets["human_verifications"]
    }), 200
