from http.server import BaseHTTPRequestHandler

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        html = """
        <html><head><meta name="viewport" content="width=device-width, initial-scale=1">
        <style>
        body{margin:0;font-family:Arial;background:#0a0a0a;color:white;text-align:center}
        .hero{padding:80px 20px;background:linear-gradient(135deg,#111,#2b1055,#7597de)}
        h1{font-size:48px;margin:0} p{font-size:18px;opacity:.8;max-width:600px;margin:20px auto}
        .btn{display:inline-block;background:white;color:black;padding:14px 28px;border-radius:30px;text-decoration:none;font-weight:bold;margin-top:10px}
        .box{display:flex;gap:15px;justify-content:center;flex-wrap:wrap;padding:40px 20px}
        .card{background:#1a1a1a;padding:25px;border-radius:15px;width:250px}
        </style></head>
        <body>
        <div class="hero">
        <h1>ENGINE FIVE</h1>
        <p>We build bold ideas into real products. Fast, clean, and made to last.</p>
        <a class="btn" href="#">Start Your Project</a>
        </div>
        <div class="box">
        <div class="card"><h3>🚀 Build</h3><p>Websites & apps that launch fast.</p></div>
        <div class="card"><h3>🎨 Design</h3><p>Clean design that people remember.</p></div>
        <div class="card"><h3>📈 Grow</h3><p>Systems that help your business grow.</p></div>
        </div>
        <p style="padding-bottom:40px">© 2026 Engine Five</p>
        </body></html>
        """
        self.wfile.write(html.encode())
        return
