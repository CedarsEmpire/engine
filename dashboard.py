from flask import Flask, render_template_string, request, redirect
import os

app = Flask(__name__)

HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>CEDARS EMPIRE</title>
    <style>
        body { font-family: Arial; background: #f0f0f0; }
        .nav { background: #333; color: white; padding: 10px; }
        .nav a { color: white; margin-right: 20px; }
        .card { background: white; padding: 20px; margin: 20px; border-radius: 10px; }
    </style>
</head>
<body>
    <div class="nav">
        <a href="?page=home">Home</a>
        <a href="?page=about">About Us</a>
        <a href="?page=buy">Buy Share (Deposit)</a>
        <a href="?page=balance">Balance</a>
        <a href="?page=withdraw">Withdraw</a>
        <a href="?page=referral">Referral</a>
        <a href="?page=support">Live Support</a>
    </div>
    
    {% if page == 'home' %}
    <div class="card">
        <h2>Welcome to Cedars Empire</h2>
        <p>Your investment platform</p>
    </div>
    {% elif page == 'about' %}
    <div class="card">
        <h2>About Us</h2>
        <p>Cedars Empire uses AI to generate returns for investors.</p>
    </div>
    {% elif page == 'buy' %}
    <div class="card">
        <h2>Buy Share (Deposit)</h2>
        <form>
            <input type="number" placeholder="Amount">
            <button>Deposit</button>
        </form>
    </div>
    {% elif page == 'balance' %}
    <div class="card">
        <h2>Balance</h2>
        <p>Available: €2.81</p>
        <p>Earned: €14.04</p>
    </div>
    {% elif page == 'withdraw' %}
    <div class="card">
        <h2>Withdraw</h2>
        <form>
            <input type="number" placeholder="Amount">
            <button>Withdraw</button>
        </form>
    </div>
    {% elif page == 'referral' %}
    <div class="card">
        <h2>Referral</h2>
        <p>Your link: https://cedarsempire.com/?ref=yourid</p>
    </div>
    {% elif page == 'support' %}
    <div class="card">
        <h2>Live Support</h2>
        <p>Chat with us: <a href="#">Support Chat</a></p>
    </div>
    {% endif %}
</body>
</html>
"""

@app.route('/')
def index():
    page = request.args.get('page', 'home')
    return render_template_string(HTML, page=page)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
