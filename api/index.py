from flask import Flask
app = Flask(__name__)

@app.route('/')
def home():
    return "Engine Five is LIVE - minimal test OK"
