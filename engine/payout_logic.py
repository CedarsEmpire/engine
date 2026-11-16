# payout_logic.py
import nowpayments

def process_payout(user_id, amount):
    # Get user wallet
    wallet = get_user_wallet(user_id)
    # Call NOWPayments API
    payout = nowpayments.create_payout(
        address=wallet['address'],
        currency='usdtbsc',
        amount=amount,
        ipn_callback_url='https://enginefive.com/webhook'
    )
    return payout['id']

def webhook_handler(data):
    # NOWPayments callback
    if data['status'] == 'finished':
        update_payout_status(data['payout_id'], 'confirmed')
