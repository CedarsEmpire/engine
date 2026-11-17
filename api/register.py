from http.server import BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
import json
from engine.secure_api import hash_password, validate_email, check_password
from engine.db import connect_db
import re

class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        path = urlparse(self.path).path
        if path == "/api/register":
            length = int(self.headers.get('Content-Length', 0))
            body = self.rfile.read(length).decode('utf-8')
            data = json.loads(body)

            # Required fields
            name = data.get('name')
            country_code = data.get('country_code')  # e.g., "Ug +256"
            phone_number = data.get('phone_number')
            email = data.get('email')
            password = data.get('password')
            role = data.get('role')  # worker, client, verifier
            human_signup = data.get('human_signup')  # true for human only

            if not name or not country_code or not phone_number or not email or not password or not role or not human_signup:
                self.send_response(400)
                self.end_headers()
                self.wfile.write(json.dumps({'error': 'Missing fields'}).encode('utf-8'))
                return

            # Validate email
            if not validate_email(email):
                self.send_response(400)
                self.end_headers()
                self.wfile.write(json.dumps({'error': 'Invalid email'}).encode('utf-8'))
                return

            # Validate phone (simple check)
            full_phone = country_code.split('+')[1] + phone_number
            if not re.match(r'^\d{5,15}$', phone_number):
                self.send_response(400)
                self.end_headers()
                self.wfile.write(json.dumps({'error': 'Invalid phone number'}).encode('utf-8'))
                return

            # Check human_signup is true
            if human_signup != 'true' and human_signup is not True:
                self.send_response(400)
                self.end_headers()
                self.wfile.write(json.dumps({'error': 'Only human signups allowed'}).encode('utf-8'))
                return

            db = connect_db()
            cursor = db.cursor()
            cursor.execute("SELECT * FROM users WHERE email=%s", (email,))
            if cursor.fetchone():
                self.send_response(400)
                self.end_headers()
                self.wfile.write(json.dumps({'error': 'Email exists'}).encode('utf-8'))
                return

            hashed = hash_password(password)
            cursor.execute("INSERT INTO users (name, country_code, phone_number, email, password, role, consign_agreement) VALUES (%s, %s, %s, %s, %s, %s, true)", (name, country_code, full_phone, email, hashed, role))
            db.commit()

            self.send_response(200)
            self.end_headers()
            self.wfile.write(json.dumps({'success': True, 'message': 'Registered'}).encode('utf-8'))
            return

        elif path == "/api/login":
            length = int(self.headers.get('Content-Length', 0))
            body = self.rfile.read(length).decode('utf-8')
            data = json.loads(body)

            email = data.get('email')
            password = data.get('password')
            save_password = data.get('save_password')  # optional

            if not email or not password:
                self.send_response(400)
                self.end_headers()
                self.wfile.write(json.dumps({'error': 'Missing fields'}).encode('utf-8'))
                return

            db = connect_db()
            cursor = db.cursor()
            cursor.execute("SELECT password FROM users WHERE email=%s", (email,))
            user = cursor.fetchone()
            if not user:
                self.send_response(401)
                self.end_headers()
                self.wfile.write(json.dumps({'error': 'No user'}).encode('utf-8'))
                return

            if not check_password(password, user[0]):
                self.send_response(401)
                self.end_headers()
                self.wfile.write(json.dumps({'error': 'Wrong password'}).encode('utf-8'))
                return

            # return token
            self.send_response(200)
            self.end_headers()
            self.wfile.write(json.dumps({'success': True, 'token': 'example-token', 'save_password': save_password}).encode('utf-8'))
            return

        self.send_response(404)
        self.end_headers()
        self.wfile.write(json.dumps({'error': 'Not found'}).encode('utf-8'))
        return
