<!DOCTYPE html>
<html>
<head>
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>CEDARS EMPIRE - Shareholder</title>
<style>
*{box-sizing:border-box}
body{font-family:Arial,sans-serif;margin:0;background:#f1f5f9;color:#0f172a}
header{background:linear-gradient(135deg,#0f172a,#1e3a8a);color:#fff;padding:16px 18px;display:flex;justify-content:space-between;align-items:center}
header b{font-size:22px}
header b span{color:#facc15}
header .u{background:rgba(255,255,255,.18);padding:7px 12px;border-radius:20px;font-size:12px}
nav{background:#fff;padding:12px;display:flex;gap:8px;overflow-x:auto;box-shadow:0 2px 10px rgba(0,0,0,.06)}
nav button{border:none;background:#f1f5f9;padding:10px 16px;border-radius:25px;font-weight:800;font-size:13px;white-space:nowrap;cursor:pointer}
nav button.active{background:#0f172a;color:#fff}
.wrap{padding:16px;max-width:950px;margin:auto}
.hero{background:linear-gradient(135deg,#facc15,#f59e0b);border-radius:20px;padding:22px;color:#0f172a;box-shadow:0 10px 25px rgba(245,158,11,.3)}
.hero small{font-weight:800;letter-spacing:1px;opacity:.7}
.hero h1{margin:5px 0;font-size:38px}
.hero p{margin:0;opacity:.8}
.grid{display:grid;grid-template-columns:1fr 1fr 1fr;gap:14px;margin-top:15px}
@media(max-width:650px){.grid{grid-template-columns:1fr}}
.card{background:#fff;padding:18px;border-radius:18px;box-shadow:0 2px 12px rgba(0,0,0,.05);margin-top:15px}
.card small{color:#64748b;font-weight:800}
.card h2{margin:6px 0;font-size:24px}
.btn{background:#0f172a;color:#fff;border:none;padding:13px;border-radius:12px;font-weight:800;width:100%;cursor:pointer;margin-top:10px}
.btn-gold{background:#facc15;color:#0f172a}
input{width:100%;padding:13px;margin:8px 0;border-radius:12px;border:1px solid #e2e8f0}
.badge{display:inline-block;background:#dcfce7;color:#166534;padding:5px 10px;border-radius:20px;font-size:12px;font-weight:800;margin-top:8px}
.progress{background:#e2e8f0;height:10px;border-radius:10px;overflow:hidden;margin-top:10px}
.progress div{background:#22c55e;height:10px;width:65%}
.page{display:none}.page.show{display:block}
table{width:100%;border-collapse:collapse}td{padding:12px 0;border-bottom:1px solid #eee}
</style>
</head>
<body>
<header><b>CEDARS <span>EMPIRE</span> <span style="color:#22c55e;font-size:11px">● Live</span></b><span class="u">ogwal.bemmanuel@gmail.com</span></header>
<nav>
<button onclick="show('home',this)" class="active">🏠 Home</button>
<button onclick="show('about',this)">ℹ️ About Us</button>
<button onclick="show('buy',this)">💰 Buy Share</button>
<button onclick="show('balance',this)">💳 Balance</button>
<button onclick="show('withdraw',this)">↗ Withdraw</button>
<button onclick="show('referral',this)">👥 Referral</button>
<button onclick="show('support',this)">💬 Live Support</button>
</nav>
<div class="wrap">

<div id="home" class="page show">
<div class="hero"><small>WELCOME BACK, SHAREHOLDER</small><h1>€27.05</h1><p>Available Balance • Earned €135.23</p><span class="badge">✓ Verified Shareholder</span></div>
<div class="grid">
<div class="card"><small>AVAILABLE BALANCE</small><h2>€27.05</h2><p>Ready to withdraw</p></div>
<div class="card"><small>EARNED BALANCE</small><h2>€135.23</h2><p>Total ever earned</p></div>
<div class="card"><small>RESERVED BALANCE</small><h2>€0.00</h2><p>Held for pending</p></div>
</div>
<div class="card"><small>YOUR SHARE PROGRESS</small><h2>65% to Next Level</h2><div class="progress"><div></div></div><button class="btn btn-gold" onclick="show('buy',null)">Buy More Shares →</button></div>
</div>

<div id="about" class="page"><div class="card"><h2>About Cedars Empire</h2><p>Cedars Empire is a shareholder community. Members buy shares, grow together, and earn from platform growth.</p><br><p>✅ Transparent balances<br>✅ Fast withdrawals<br>✅ Referral rewards<br>✅ Live support</p></div></div>

<div id="buy" class="page"><div class="card"><h2>💰 Buy Share (Deposit)</h2><p>Buy a share to grow your earnings.</p><input type="number" placeholder="Amount in EUR e.g. 50"><button class="btn btn-gold">Deposit / Buy Share</button><p style="color:#64748b;font-size:12px">Your deposit will be confirmed by admin.</p></div></div>

<div id="balance" class="page"><div class="card"><h2>💳 Balance Table</h2><table><tr><td>Available Balance</td><td style="text-align:right"><b>€27.05</b></td></tr><tr><td>Reserved Balance</td><td style="text-align:right"><b>€0.00</b></td></tr><tr><td>Earned Balance</td><td style="text-align:right"><b>€135.23</b></td></tr></table><button class="btn" onclick="show('withdraw',null)">Withdraw Now</button></div></div>

<div id="withdraw" class="page"><div class="card"><h2>↗ Withdraw</h2><p>Available: <b>€27.05</b></p><input type="number" placeholder="Amount to withdraw"><input type="text" placeholder="Your wallet / bank details"><button class="btn btn-gold">Request Withdrawal</button></div></div>

<div id="referral" class="page"><div class="card"><h2>👥 Referral</h2><p>Invite friends and earn bonus.</p><input value="https://task-nzpxfuvxj-ogwalbemmanuel-5121.vercel.app/?ref=ogwal" readonly><button class="btn">Copy Referral Link</button><p style="color:#64748b">Total referrals: 0 • Bonus: €0.00</p></div></div>

<div id="support" class="page"><div class="card"><h2>💬 Live Support</h2><p>Need help? We reply fast.</p><button class="btn btn-gold">Chat on WhatsApp</button><button class="btn">Email Support</button></div></div>

</div>
<script>
function show(id,btn){
document.querySelectorAll('.page').forEach(p=>p.classList.remove('show'));
document.getElementById(id).classList.add('show');
if(btn){document.querySelectorAll('nav button').forEach(b=>b.classList.remove('active'));btn.classList.add('active');}
window.scrollTo(0,0);
}
</script>
</body>
</html>
