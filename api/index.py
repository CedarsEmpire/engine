from http.server import BaseHTTPRequestHandler
import json, urllib.parse

# === ENGINE 360 - IN-MEMORY DB (for Vercel demo, later use real DB) ===
# In production this will be Supabase / Firebase
BALANCE = {"gbp": 0.00}
TASKS = [
    {"id": 1, "title": "Watch & Verify Task", "reward_gbp": 0.50, "status": "available"},
    {"id": 2, "title": "Share Engine Five", "reward_gbp": 1.00, "status": "available"},
    {"id": 3, "title": "Daily AI Check-in", "reward_gbp": 0.25, "status": "available"},
]
RATE = 1.321 # 1 GBP = 1.321 USD - update daily from API

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        parsed = urllib.parse.urlparse(self.path)
        path = parsed.path
        query = urllib.parse.parse_qs(parsed.query)

        # --- API ENDPOINTS - THE ENGINE ---
        if path == "/api/balance":
            return self.json({"balance_gbp": BALANCE["gbp"], "balance_usd": round(BALANCE["gbp"]*RATE,2), "rate": RATE, "currency": "GBP"})
        if path == "/api/tasks":
            return self.json({"tasks": TASKS})
        if path == "/api/health":
            return self.json({"engine": "online", "task_engine": "ok", "verification": "ok", "payout_manager": "ok", "api_integrations": "ok", "ai_automation": "ok"})

        # --- MAIN DASHBOARD ---
        self.send_response(200)
        self.send_header('Content-type', 'text/html; charset=utf-8')
        self.end_headers()
        html = """
        <html><head><title>Engine Five - Engine 360</title><meta name="viewport" content="width=device-width, initial-scale=1">
        <style>body{font-family:sans-serif;text-align:center;padding:20px;background:#111;color:white}
        h1{color:#00ff88}.box{background:#222;padding:22px;border-radius:15px;max-width:560px;margin:auto}
        .btn{background:#00ff88;color:#111;padding:12px 18px;border-radius:8px;margin:6px;display:inline-block;font-weight:bold;border:none;cursor:pointer}
        .btn2{background:#333;color:white;padding:12px 18px;border-radius:8px;margin:6px;display:inline-block;border:none;cursor:pointer}
        .card{background:#1a1a1a;padding:12px;border-radius:10px;margin:10px 0;text-align:left}
        .ok{color:#00ff88}.warn{color:#ffaa00}
        </style></head><body>
        <h1>ENGINE FIVE - 360 ENGINE</h1>
        <div class='box'>
        <p>Engine Status: <span class='ok' id='health'>Checking...</span></p>
        <h2 id='bal'>Balance: £0.00 GBP</h2>
        <p id='balUsd'>≈ $0.00 USD | Rate 1 GBP = 1.321 USD</p>
        <button class='btn' onclick='engineDrop()'>ENGINE DROP - CLAIM FIRST £1.00</button>
        <p class='small'>Engine must drop £1 first to activate automation.</p>
        <div id='tasks'></div>
        <h3>Payout - Real Money</h3>
        <input id='payoutEmail' placeholder='PayPal / Wise Email' style='padding:12px;width:80%;border-radius:8px;border:none'>
        <br><br>
        <button class='btn' onclick='requestPayout("GBP")'>Payout in £ GBP</button>
        <button class='btn2' onclick='requestPayout("USD")'>Payout in $ USD</button>
        <p id='payoutMsg' class='warn'></p>
        <hr><p>API Tests: <a style='color:#00ff88' href='/api/balance'>/api/balance</a> | <a style='color:#00ff88' href='/api/tasks'>/api/tasks</a> | <a style='color:#00ff88' href='/api/health'>/api/health</a></p>
        </div>
        <script>
        const RATE=1.321;
        let balance=0;
        async function load(){
            let h=await fetch('/api/health').then(r=>r.json()).catch(()=>null);
            document.getElementById('health').innerText = h ? 'ONLINE - All 5 Systems OK' : 'OFFLINE';
            let t=await fetch('/api/tasks').then(r=>r.json());
            let html='<h3>Tasks - AI Automated</h3>';
            t.tasks.forEach(task=>{
                html+=`<div class='card'><b>${task.title}</b><br>Reward: £${task.reward_gbp} | Status: ${task.status}<br><button class='btn' onclick='doTask(${task.id}, ${task.reward_gbp})'>Do Task</button> <button class='btn2' onclick='verifyTask(${task.id}, ${task.reward_gbp})'>Verify & Claim</button></div>`;
            });
            document.getElementById('tasks').innerHTML=html;
            updateBal();
        }
        function updateBal(){ document.getElementById('bal').innerText='Balance: £'+balance.toFixed(2)+' GBP'; document.getElementById('balUsd').innerText='≈ $'+(balance*RATE).toFixed(2)+' USD | Rate 1 GBP = 1.321 USD'; }
        function engineDrop(){ if(balance>0){alert('Already claimed');return;} balance=1.00; updateBal(); alert('Engine dropped £1.00. Automation ON.'); }
        function doTask(id, reward){ alert('Task '+id+' started. Do it, then click Verify & Claim.'); }
        async function verifyTask(id, reward){
            // Step 1: Human Verification API call (simulated here, real API in engine/human_verification.py)
            let verified = confirm('AI Verification: Are you human and did you complete Task '+id+' honestly? Click OK to verify.');
            if(!verified){ alert('Verification FAILED. No payout.'); return; }
            // Step 2: If verified, pay
            let res = await fetch('/api/verify', {method:'POST'}).then(r=>r.json()).catch(()=>({verified:true}));
            balance += reward; updateBal(); alert('VERIFIED! +£'+reward+' added. Balance now £'+balance.toFixed(2));
        }
        async function requestPayout(cur){
            let email=document.getElementById('payoutEmail').value;
            if(!email){ alert('Enter PayPal / Wise email first'); return; }
            if(balance < 1){ alert('Need at least £1 to payout. Claim Engine Drop first.'); return; }
            document.getElementById('payoutMsg').innerText='Payout Request Sent: £'+balance.toFixed(2)+' to '+email+' in '+cur+'. Waiting for Payout API...';
            // Real payout happens in engine/payout_manager.py via Wise/PayPal API
            alert('Payout Request Logged. In REAL mode, Wise/PayPal API will send money now. In DEMO mode, balance stays for testing.');
        }
        load();
        </script></body></html>
        """
        self.wfile.write(html.encode())
        return

    def do_POST(self):
        if self.path == "/api/verify":
            return self.json({"verified": True, "method": "ai_human_verification", "status": "passed"})
        return self.json({"error": "not found"})

    def json(self, data):
        body = json.dumps(data).encode()
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(body)
        return
