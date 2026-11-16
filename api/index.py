from http.server import BaseHTTPRequestHandler
import json

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        data = {
            "status": "live",
            "company": "99.9% Robotic Company",
            "engine": "engine-five",
            "message": "Engine deployed. First daily income not yet dropped."
        }
        self.wfile.write(json.dumps(data).encode())
        return
