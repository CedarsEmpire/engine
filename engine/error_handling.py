# with_error_handling.py
import logging
logging.basicConfig(filename='enginefive.log', level=logging.INFO)

def process_payout(user_id, amount):
    try:
        payout_id = nowpayments.create_payout(...)
        logging.info(f"Payout {payout_id} for {user_id}")
        return payout_id
    except Exception as e:
        logging.error(f"Error for {user_id}: {e}")
        return None

@app.route('/payout', methods=['POST'])
def payout():
    try:
        user_id = request.json['user_id']
        amount = request.json['amount']
        payout_id = process_payout(user_id, amount)
        return jsonify({'payout_id': payout_id}), 200
    except KeyError:
        return jsonify({'error': 'Missing data'}), 400
    except Exception as e:
        return jsonify({'error': 'Server issue'}), 500
