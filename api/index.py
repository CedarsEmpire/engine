from flask import Flask

app = Flask(__name__)

@app.route('/')
def home():
    return "Engine Five is LIVE - minimal test OK"

@app.route('/run-task')
def run_task():
    return "run-task route is working"
