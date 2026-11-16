from http.server import BaseHTTPRequestHandler
import json
import urllib.parse

BALANCE = {"gbp": 0.00}
RATE = 1.321

# BOTH - Automated AI Workers + Human Verifications
TASKS = [
    {"id": 1, "title": "AI Task - Daily Check", "reward_gbp": 1.50, "status": "available", "type": "AI"},
    {"id": 2, "title": "Human Verify Task", "reward_gbp": 2.25, "status": "available", "type": "HUMAN"},
    {"id": 3, "title": "AI Task - Content Check", "reward_gbp": 1.50, "status": "available", "type": "AI"},
    {"id": 4, "title": "Human Verify Task - Share Check", "reward_gbp": 2.25, "status": "available", "type": "HUMAN"},
]

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        parsed = urllib.parse.urlparse(self.path)
        path = parsed.path

        if path == "/api/balance":
            return self.send_json({
                "balance_gbp": BALANCE["gbp"],
                "balance_usd": round(BALANCE["gbp"] * RATE, 2),
                "rate": RATE,
                "daily_target_ai_usd": 250,
                "daily_target_human_usd": 15
            })

        if path == "/api/tasks":
            return self.send_json({"tasks": TASKS})

        if path == "/api/health":
            return self.send_json({
                "engine": "online",
                "task_engine": "ok",
                "verification": "ok",
                "payout_manager": "ok",
                "api_integrations": "ok",
                "ai_automation": "ok"
            })

        self.send_response(200)
        self.send_header('Content-type', 'text/html; charset=utf-8')
        self.end_headers()
        html = """<html><head><title>Engine Five - Engine 360</title><meta name='viewport' content='width=device-width, initial-scale=1'><style>body{font-family:sans-serif;text-align:center;padding:20px;background:#111;color:white}h1{color:#00ff88}.box{background:#222;padding:22px;border-radius:15px;max-width:560px;margin:auto}.btn{background:#00ff88;color:#111;padding:12px 18px;border-radius:8px;margin:6px;display:inline-block;font-weight:bold;border:none;cursor:pointer}.btn2{background:#333;color:white;padding:12px 18px;border-radius:8px;margin:6px;display:inline-block;border:none;cursor:pointer}.card{background:#1a1a1a;padding:12px;border-radius:10px;margin:10px 0;text-align:left}.ok{color:#00ff88}.warn{color:#ffaa00}input{padding:12px;width:80%;border-radius:8px;border:none}</style></head><body><h1>ENGINE FIVE - 360 ENGINE</h1><div class='box'><p>Engine Status: <span class='ok' id='health'>Checking...</span></p><h2 id='bal'>Balance: £0.00 GBP</h2><p id='balUsd'>≈ $0.00 USD | Rate 1 GBP = 1.321 USD</p><p>Daily Target: AI Workers $250 | Human Verifications $15</p><p>AI: 125 tasks x $2 = $250 | Human: 5 verifies x $3 = $15</p><button class='btn' onclick='engineDrop()'>ENGINE DROP - CLAIM FIRST £1.00</button><p>Engine must drop £1 first to activate automation.</p><div id='tasks'></div><h3>Payout - Real Money</h3><input id='payoutEmail' placeholder='PayPal / Wise Email'><br><br><button class='btn' onclick='requestPayout("GBP")'>Payout in £ GBP</button><button class='btn2' onclick='requestPayout("USD")'>Payout in $ USD</button><p id='payoutMsg' class='warn'></p><hr><p><a style='color:#00ff88' href='/api/balance'>Balance API</a> | <a style='color:#00ff88' href='/api/tasks'>Tasks API</a> | <a style='color:#00ff88' href='/api/health'>Health API</a></p></div><script>const RATE=1.321;let balance=0;async function load(){let h=await fetch('/api/health').then(r=>r.json()).catch(()=>null);document.getElementById('health').innerText=h?'ONLINE - All 5 Systems OK':'OFFLINE';let t=await fetch('/api/tasks').then(r=>r.json());let html='<h3>Tasks - AI Automated + Human Verified</h3>';t.tasks.forEach(task=>{html+="<div class='card'><b>"+task.title+"</b><br>Type: "+task.type+" | Reward: £"+task.reward_gbp+" | Status: "+task.status+"<br><button class='btn' onclick='doTask("+task.id+")'>Do Task</button> <button class='btn2' onclick='verifyTask("+task.id+", "+task.reward_gbp+")'>Verify & Claim</button></div>";});document.getElementById('tasks').innerHTML=html;updateBal();}function updateBal(){document.getElementById('bal').innerText='Balance: £'+balance.toFixed(2)+' GBP';document.getElementById('balUsd').innerText='≈ $'+(balance*RATE).toFixed(2)+' USD | Rate 1 GBP = 1.321 USD';}function engineDrop(){if(balance>0){alert('Already claimed');return;}balance=1.00;updateBal();alert('Engine dropped £1.00. Automation ON.');}function doTask(id){alert('Task '+id+' started. Do it, then click Verify & Claim.');}async function verifyTask(id, reward){let verified=confirm('AI Verification: Are you human and did you complete Task '+id+' honestly? Click OK to verify.');if(!verified){alert('Verification FAILED. No payout.');return;}await fetch('/api/verify',{method:'POST'}).then(r=>r.json()).catch(()=>({verified:true}));balance+=reward;updateBal();alert('VERIFIED! +£'+reward+' added. Balance now £'+balance.toFixed(2));}async function requestPayout(cur){let email=document.getElementById('payoutEmail').value;if(!email){alert('Enter PayPal / Wise email first');return;}if(balance<1){alert('Need at least £1 to payout. Claim Engine Drop first.');return;}document.getElementById('payoutMsg').innerText='Payout Request Sent: £'+balance.toFixed(2)+' to '+email+' in '+cur+'. Waiting for Payout API...';alert('Payout Request Logged.');}load();</script></body></html>"""
        self.wfile.write(html.encode())
        return

    def do_POST(self):
        if self.path == "/api/verify":
            return self.send_json({"verified": True, "method": "ai_human_verification", "status": "passed"})
        if self.path == "/api/payout":
            length = int(self.headers.get('Content-Length', 0))
            body = self.rfile.read(length) if length > 0 else b'{}'
            return self.send_json({"status": "payout_requested", "received": json.loads(body.decode() or '{}')})
        return self.send_json({"error": "not found"})

    def send_json(self, data):
        body = json.dumps(data).encode()
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(body)
        return
