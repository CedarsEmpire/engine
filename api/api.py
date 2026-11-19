from flask import Flask, jsonify

app = Flask(__name__)

# Sample data
shareholder_data = {
    "investment_overview": {"investment_amount": 1000, "investment_date": "2022-01-01"},
    "balance_and_earnings": {"balance": 1500, "earnings": 500},
    "transaction_history": [{"date": "2022-01-01", "amount": 1000}, {"date": "2022-01-15", "amount": 500}],
}

@app.route('/api/investment-overview', methods=['GET'])
def get_investment_overview():
    return jsonify(shareholder_data["investment_overview"])

@app.route('/api/balance-and-earnings', methods=['GET'])
def get_balance_and_earnings():
    return jsonify(shareholder_data["balance_and_earnings"])

@app.route('/api/transaction-history', methods=['GET'])
def get_transaction_history():
    return jsonify(shareholder_data["transaction_history"])

if __name__ == '__main__':
    app.run(debug=True, port=5000)
