from http.server import BaseHTTPRequestHandler
import json
import urllib.parse

BALANCE = {"gbp": 0.00}
RATE = 1.321

TASKS = [
    {"id": 1, "title": "AI Task - Daily Check", "reward_gbp": 1.50, "status": "Available", "type": "AI"},
    {"id": 2, "title": "Human Verify Task", "reward_gbp": 2.25, "status": "Available", "type": "HUMAN"},
    {"id": 3, "title": "AI Task - Content Check", "reward_gbp": 1.50, "status": "Available", "type": "AI"},
    {"id": 4, "title": "Human Verify Task - Share Check", "reward_gbp": 2.25, "status": "Available", "type": "HUMAN"},
]

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        parsed = urllib.parse.urlparse(self.path)
        path = parsed.path

        if path == "/api/balance":
            return self.send_json({"balance_gbp": BALANCE["gbp"], "balance_usd": round(BALANCE["gbp"] * RATE, 2), "rate": RATE})
        if path == "/api/tasks":
            return self.send_json({"tasks": TASKS})
        if path == "/api/health":
            return self.send_json({"engine": "online", "ai": "ok", "human": "ok", "payout": "ok"})

        self.send_response(200)
        self.send_header('Content-type', 'text/html; charset=utf-8')
        self.end_headers()
        html = """<!DOCTYPE html><html><head><meta charset='utf-8'><meta name='viewport' content='width=device-width, initial-scale=1'><title>Engine Five</title><style>*{box-sizing:border-box}body{margin:0;font-family:Inter,system-ui,Arial,sans-serif;background:#f4f6f8;color:#111}.top{background:#0f172a;color:#fff;padding:16px 20px;display:flex;justify-content:space-between;align-items:center}.top b{font-size:18px;letter-spacing:.5px}.pill{background:#22c55e;color:#fff;padding:6px 12px;border-radius:999px;font-size:12px;font-weight:700}.wrap{max-width:900px;margin:20px auto;padding:0 14px;display:grid;grid-template-columns:1fr 1fr;gap:16px}.card{background:#fff;border:1px solid #e5e7eb;border-radius:14px;padding:18px;box-shadow:0 2px 10px rgba(0,0,0,.04)}.full{grid-column:1/-1}.label{font-size:12px;color:#6b7280;text-transform:uppercase;letter-spacing:.8px}.big{font-size:36px;font-weight:800;margin:6px 0}.sub{color:#6b7280;font-size:14px}input,select{width:100%;padding:12px;border:1px solid #d1d5db;border-radius:10px;font-size:15px;margin-top:8px}label{font-size:13px;font-weight:600}button{border:0;border-radius:10px;padding:12px 16px;font-weight:700;cursor:pointer} .btn-primary{background:#16a34a;color:#fff;width:100%} .btn-dark{background:#0f172a;color:#fff} .btn-ghost{background:#eef2f7;color:#111}table{width:100%;border-collapse:collapse}th{font-size:12px;text-align:left;color:#6b7280;padding:10px 8px;border-bottom:1px solid #eee}td{padding:12px 8px;border-bottom:1px solid #f1f1f1;font-size:14px}.row{display:flex;gap:10px;margin-top:12px}.row button{flex:1}.badge{font-size:11px;padding:4px 8px;border-radius:999px;background:#e0f2fe}.badge.h{background:#fef3c7}.msg{font-size:13px;color:#16a34a;margin-top:10px;min-height:18px}@media(max-width:700px){.wrap{grid-template-columns:1fr}.big{font-size:30px}}</style></head><body><div class='top'><b>ENGINE FIVE</b><span class='pill' id='health'>● ONLINE</span></div><div class='wrap'><div class='card'><div class='label'>Balance</div><div class='big' id='bal'>£0.00</div><div class='sub' id='balUsd'>$0.00 USD • 1 GBP = 1.321 USD</div><div class='row'><button class='btn-primary' onclick='engineDrop()'>Claim £1.00</button></div></div><div class='card'><div class='label'>Payout</div><form onsubmit='return requestPayout(event)'><label>Email</label><input id='payoutEmail' type='email' placeholder='PayPal / Wise email' required><label>Currency</label><select id='payoutCur'><option value='GBP'>GBP £</option><option value='USD'>USD $</option></select><div class='row'><button class='btn-dark' type='submit'>Request Payout</button></div><div class='msg' id='payoutMsg'></div></form></div><div class='card full'><div class='label'>Tasks</div><table><thead><tr><th>Task</th><th>Type</th><th>Reward</th><th>Status</th><th></th></tr></thead><tbody id='tasks'></tbody></table></div></div><script>const RATE=1.321;let balance=0;async function load(){let h=await fetch('/api/health').then(r=>r.json()).catch(()=>null);document.getElementById('health').innerText=h?'● ONLINE':'● OFFLINE';let t=await fetch('/api/tasks').then(r=>r.json());let rows='';t.tasks.forEach(task=>{rows+="<tr><td><b>"+task.title+"</b></td><td><span class='badge "+(task.type=='HUMAN'?'h':'')+"'>"+task.type+"</span></td><td>£"+task.reward_gbp.toFixed(2)+"</td><td>"+task.status+"</td><td><button class='btn-ghost' onclick='doTask("+task.id+")'>Start</button> <button class='btn-dark' onclick='verifyTask("+task.id+", "+task.reward_gbp+")'>Verify & Claim</button></td></tr>";});document.getElementById('tasks').innerHTML=rows;updateBal();}function updateBal(){document.getElementById('bal').innerText='£'+balance.toFixed(2);document.getElementById('balUsd').innerText='$'+(balance*RATE).toFixed(2)+' USD • 1 GBP = 1.321 USD';}function engineDrop(){if(balance>0){alert('Already claimed');return;}balance=1.00;updateBal();}function doTask(id){alert('Task '+id+' started');}async function verifyTask(id, reward){let ok=confirm('Verify Task '+id+'?');if(!ok) return;await fetch('/api/verify',{method:'POST'}).then(r=>r.json()).catch(()=>({}));balance+=reward;updateBal();}function requestPayout(e){e.preventDefault();let email=document.getElementById('payoutEmail').value;let cur=document.getElementById('payoutCur').value;if(balance<1){document.getElementById('payoutMsg').innerText='Minimum payout £1.00';return false;}document.getElementById('payoutMsg').innerText='Payout requested: £'+balance.toFixed(2)+' to '+email+' ('+cur+')';return false;}load();</script></body></html>"""
        self.wfile.write(html.encode())
        return

    def do_POST(self):
        if self.path == "/api/verify":
            return self.send_json({"verified": True, "status": "passed"})
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
