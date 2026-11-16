from http.server import BaseHTTPRequestHandler

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html; charset=utf-8')
        self.end_headers()
        html = """
        <html><head><title>Engine Five Dashboard</title>
        <style>
            body{font-family:sans-serif;text-align:center;padding:50px;background:#111;color:white}
            h1{color:#00ff88}.box{background:#222;padding:20px;border-radius:15px;max-width:500px;margin:auto}
            .btn{background:#00ff88;color:#111;padding:10px 20px;border-radius:8px;text-decoration:none;margin:10px;display:inline-block}
        </style>
        </head><body>
        <h1>ENGINE FIVE DASHBOARD</h1>
        <div class='box'>
            <p>Status: Ready</p>
            <p>Balance: 0.00 UGX</p>
            <a class='btn' href='#tasks'>Tasks</a>
            <a class='btn' href='#payout'>Payout</a>
            <a class='btn' href='#verify'>Verify</a>
            <hr style='margin:20px 0;border:none;border-top:1px solid #333'>
            <p><a style='color:#00ff88' href='/api/index.py'>Test API Endpoint</a></p>
        </div>
        </body></html>
        """
        self.wfile.write(html.encode())
        return

