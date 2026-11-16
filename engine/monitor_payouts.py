# monitor_payouts.py
from prometheus_client import start_http_server, Counter, Gauge
import logging
import nowpayments
import alertmanager

# Metrics
payout_success = Counter('payout_success', 'Payouts succeeded')
payout_fail = Counter('payout_fail', 'Payouts failed')
payout_latency = Gauge('payout_latency', 'Payout processing time')

logging.basicConfig(filename='payout_monitor.log', level=logging.INFO)

def process_payout(user_id, amount):
    try:
        start_time = time.time()
        payout_id = nowpayments.create_payout(...)
        payout_success.inc()
        payout_latency.set(time.time() - start_time)
        logging.info(f"Payout {payout_id} for {user_id}")
        return payout_id
    except Exception as e:
        payout_fail.inc()
        alertmanager.send_alert('Payout failed', user_id, str(e))
        logging.error(f"Error for {user_id}: {e}")
        return None

if __name__ == '__main__':
    start_http_server(8000)  # Prometheus endpoint
    # Run with payouts logic
