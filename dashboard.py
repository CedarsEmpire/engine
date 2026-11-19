from flask import Flask, request, render_template_string
import os

app = Flask(__name__)

HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>CEDARS EMPIRE - Shareholder</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            background-color: #f0f0f0;
            margin: 0;
            padding: 0;
        }
        .header {
            background-color: #333;
            color: #fff;
            padding: 1em;
            text-align: center;
        }
        .nav {
            background-color: #444;
            padding: 0.5em;
        }
        .nav a {
            color: #fff;
            text-decoration: none;
            margin-right: 20px;
        }
        .content {
            padding to: 20px;
            max-width: 800px;
            margin: auto;
        }
        .card {
            background-color: #fff;
            padding: 20px;
            border: 1px solid #ddd;
            border-radius: 10px;
            box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
            margin-bottom: 20px;
        }
        .btn {
            background-color: #4CAF50;
            color: #fff;
            padding: 10px 20px;
            border: none;
            border-radius: 5px;
            cursor: pointer;
        }
    </style>
</head>
<body>
    <div class="header">
        <h1>CEDARS EMPIRE</h1>
    </div>
    <div class="nav">
        <a href="?page=home">Home</a>
        <a href="?page=about">About Us</a>
        <a href="?page=buy">Buy Share</a>
        <a href="?page=balance">Balance</a>
        <a href="?page=withdraw">Withdraw</a>
        <a href="?page=referral">Referral</a>
        <a href="?page=support">Live Support</a>
    </div>
    <div class="content">
        {% if page == 'home' %}
        <div class="card">
            <h2>Welcome to Cedars Empire</h2>
            <p>Your shareholder dashboard.</p>
        </div>
        <div class="card">
            <h2>Your Balance</h2>
            <p>Available: €27.05</p>
            <p>Earned: €135.23</p>
        </div>
        {% elif page == 'about' %}
        <div class="card">
            <h2>About Us</h2>
            <p>Cedars Empire is a shareholder community.</p>
        </div>
        {% elif page == 'buy' %}
        <div class="card">
            <h2>Buy Share</h2>
            <p>Buy a share to grow your earnings.</p>
            <input type="number" placeholder="Amount">
            <button class="btn">Deposit / Buy Share</button>
        </div>
        {% elif page == 'balance' %}
        <div class="card">
            <h2>Balance Table</h2>
            <table>
                <tr>
                    <td>Available Balance</td>
                    <td>€27.05</td>
                </tr>
                <tr>
                    <td>Reserved Balance</td>
                    <td>€0.00</td>
                </tr>
                <tr>
                    <td>Earned Balance</td>
                    <td>€135.23</td>
                </tr>
            </table>
        </div>
        {% elif page == 'withdraw' %}
        <div class="card">
            <h2>Withdraw</h2>
            <p>Available: €27.05</p>
            <input type="number" placeholder="Amount">
            <input type="text" placeholder="Wallet / Bank details">
            <button class="btn">Request Withdrawal</button>
        </div>
        {% elif page == 'referral' %}
        <div class="card">
            <h2>Referral</h2>
            <p>Share your link and earn.</p>
            <input value="https://cedarsempire.vercel.app/?ref=ogwal" readonly>
            <button class="btn">Copy Link</button>
        </div>
        {% elif page == 'support' %}
        <div class="card">
            <h2>Live Support</h2>
            <p>Need help? Contact support.</p>
            <button class="btn">Chat on WhatsApp</button>
        </div>
        {% endif %}
    </div>
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
