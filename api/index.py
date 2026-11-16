from http.server import BaseHTTPRequestHandler

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html; charset=utf-8')
        self.end_headers()
        html = """
        <html><head><title>Engine Five Dashboard</title>
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <style>
            body{font-family:sans-serif;text-align:center;padding:30px;background:#111;color:white}
            h1{color:#00ff88;font-size:28px}
            .box{background:#222;padding:25px;border-radius:15px;max-width:520px;margin:auto}
            .big{font-size:32px;font-weight:bold}
            .small{color:#aaa;font-size:14px}
            .btn{background:#00ff88;color:#111;padding:12px 22px;border-radius:8px;text-decoration:none;margin:8px;display:inline-block;font-weight:bold}
            .btn2{background:#333;color:white;padding:12px 22px;border-radius:8px;text-decoration:none;margin:8px;display:inline-block}
            input{padding:12px;border-radius:8px;border:none;width:80%;font-size:18px;text-align:center;margin-top:10px}
            .convert{background:#1a1a1a;padding:15px;border-radius:12px;margin-top:20px}
        </style>
        </head><body>
        <h1>ENGINE FIVE DASHBOARD</h1>
        <div class='box'>
            <p>Status: Ready</p>
            <p class='small'>Main Currency: British Pound (GBP) - Global</p>
            <p class='big' id='balanceGBP'>Balance: £0.00 GBP</p>
            <p id='balanceUSD'>≈ $0.00 USD</p>
            <p class='small'>Rate: 1 GBP = 1.321 USD | Updated: 16 Nov 2026</p>

            <a class='btn' href='#tasks'>Tasks</a>
            <a class='btn' href='#payout'>Payout</a>
            <a class='btn2' href='#verify'>Verify</a>

            <div class='convert'>
                <h3>Currency Converter</h3>
                <p class='small'>Type GBP to see USD instantly</p>
                <input type='number' id='gbpInput' value='10' oninput='convert()' placeholder='Enter GBP'>
                <p class='big' id='result'>£10.00 = $13.21</p>
                <button onclick="setCurrency('GBP')" class='btn'>Show in £ GBP</button>
                <button onclick="setCurrency('USD')" class='btn2'>Show in $ USD</button>
            </div>

            <hr style='margin:20px 0;border:none;border-top:1px solid #333'>
            <p><a style='color:#00ff88' href='/api/index.py'>Test API Endpoint</a></p>
        </div>

        <script>
            const RATE = 1.321;
            let balanceGBP = 0.00;
            function convert(){
                let gbp = parseFloat(document.getElementById('gbpInput').value) || 0;
                let usd = gbp * RATE;
                document.getElementById('result').innerText = '£' + gbp.toFixed(2) + ' = $' + usd.toFixed(2);
            }
            function setCurrency(cur){
                if(cur === 'GBP'){
                    document.getElementById('balanceGBP').innerText = 'Balance: £' + balanceGBP.toFixed(2) + ' GBP';
                    document.getElementById('balanceUSD').innerText = '≈ $' + (balanceGBP * RATE).toFixed(2) + ' USD';
                } else {
                    document.getElementById('balanceGBP').innerText = 'Balance: $' + (balanceGBP * RATE).toFixed(2) + ' USD';
                    document.getElementById('balanceUSD').innerText = '≈ £' + balanceGBP.toFixed(2) + ' GBP';
                }
            }
            convert();
        </script>
        </body></html>
        """
        self.wfile.write(html.encode())
        return
