from http.server import BaseHTTPRequestHandler

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        html = """
        <html><head><title>Engine Five</title>
        <style>body{font-family:sans-serif;text-align:center;padding:50px;background:#111;color:white}h1{color:#00ff88}.box{background:#222;padding:20px;border-radius:15px;max-width:500px;margin:auto}</style>
        </head><body>
        <h1>🚀 ENGINE FIVE IS LIVE</h1>
        <div class='box'><p>Your Python Engine is deployed on Vercel!</p><p>Status: ✅ Ready</p><p><a style='color:#00ff88' href='/api/index.py'>Test API</a></p></div>
        </body></html>
        """
        self.wfile.write(html.encode())
        return
