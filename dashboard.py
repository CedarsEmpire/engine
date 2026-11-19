from flask import Flask, request, render_template_string
import os

app = Flask(__name__)

# SHAREHOLDER ONLY - NO Command Center data here
# No AI Workers, No Central Reserve, No Engine, No AI Target

HTML = """
<!DOCTYPE html>
<html>
<head>
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>CEDARS EMPIRE - Shareholder</title>
<style>
body{font-family:Arial;background:#f8fafc;margin:0;color:#0f172a}
header{background:white;padding:15px 20px;display:flex;justify-content:space-between;align-items:center;box-shadow:0 1px 5px #ddd}
header b{font-size:20px}
nav{background:white;padding:12px 20px;display:flex;gap:10px;flex-wrap:wrap;border-bottom:1px solid #e2e8f0}
nav a{text-decoration:none;color:#0f172a;background:#f1f5f9;padding:10px 14px;border-radius:20px;font-weight:bold}
nav a.active{background:#0f172a;color:white}
.wrap{padding:20px;max-width:900px;margin:auto}
.card{background:white;padding:20px;border-radius:14px;margin-bottom:15px;box-shadow:0 1px 5px #ddd}
.btn{background:#facc15;border:none;padding:12px 18px;border-radius:10px;font-weight:bold;width:100%;cursor:pointer}
input{width:100%;padding:12px;margin:8px 0;border-radius:10px;border:1px solid #cbd5e1;box-sizing:border-box}
h2{margin:0 0 10px 0}
.small{color:#64748b;font-size:13px}
</style>
</head>
<body>
<header><b>CEDARS EMPIRE <span style="color:green;font-size:12px">● Live</span></b><span>ogwal.bemmanuel@gmail.com</span></header>
<nav>
<a href="/?page=home" class="{{'active' if page=='home' else ''}}">Home</a>
<a href="/?page=about" class="{{'active' if page=='about' else ''}}">About Us</a>
<a href="/?page=buy" class="{{'active' if page=='buy' else ''}}">Buy Share</a>
<a href="/?page=balance" class="{{'active' if page=='balance' else ''}}">Balance</a>
<a href="/?page=withdraw" class="{{'active' if page=='withdraw' else ''}}">Withdraw</a>
<a href="/?page=referral" class="{{'active' if page=='referral' else ''}}">Referral</a>
<a href="/?page=support" class="{{'active' if page=='support' else ''}}">Live Support</a>
</nav>
<div class="wrap">
{% if page == 'home' %}
<div class="card"><h2>Welcome to Cedars Empire</h2><p>Your shareholder dashboard. Buy shares, track your balance and withdraw your earnings.</p></div>
<div class="card"><h2>Your Balance</h2><p style="font-size:28px"><b>€27.05</b> Available</p><p class="small">Earned Balance: €135.23</p><a href="/?page=balance"><button class="btn">View Balance</button></a></div>
{% elif page == 'about' %}
<div class="card"><h2>About Us</h2><p>Cedars Empire is a shareholder platform. Members buy shares and earn from platform growth. This dashboard is for shareholders only.</p></div>
{% elif page == 'buy' %}
<div class="card"><h2>Buy Share (Deposit)</h2><p>Choose amount to buy a share.</p><input type="number" placeholder="Amount in EUR"><button class="btn">Deposit / Buy Share</button><p class="small">Payment will be confirmed by admin.</p></div>
{% elif page == 'balance' %}
<div class="card"><h2>Balance Table - Shareholder</h2><table style="width:100%"><tr><td>Available Balance</td><td><b>€27.05</b></td></tr><tr><td>Reserved Balance</td><td><b>€0.00</b></td></tr><tr><td>Earned Balance</td><td><b>€135.23</b></td></tr></table><p class="small">This is YOUR balance only. No platform reserve shown here.</p></div>
{% elif page == 'withdraw' %}
<div class="card"><h2>Withdraw</h2><p>Available to withdraw: <b>€27.05</b></p><input type="number" placeholder="Amount to withdraw"><input type="text" placeholder="Your wallet / bank details"><button class="btn">Request Withdrawal</button></div>
{% elif page == 'referral' %}
<div class="card"><h2>Referral</h2><p>Share your link and earn.</p><input value="https://cedarsempire.vercel.app/?ref=ogwal" readonly><button class="btn">Copy Link</button></div>
{% elif page == 'support' %}
<div class="card"><h2>Live Support</h2><p>Need help? Contact support.</p><button class="btn">Chat on WhatsApp</button></div>
{% endif %}
</div>
</body>
</html>
"""

@app.route('/')
def index():
    page = request.args.get('page', 'home')
    if page not in ['home','about','buy','balance','withdraw','referral','support']:
        page = 'home'
    return render_template_string(HTML, page=page)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
