# regional_engine_api.py (e.g. Africa Engine)
from flask import Flask, request, jsonify
from db import get_user, verify_user

app = Flask(__name__)

@app.route('/signup', methods=['POST'])
def signup():
    data = request.json
    # Create user in Africa engine
    user_id = get_user(data['phone'], data['email'])
    return jsonify({'user_id': user_id})

@app.route('/verify', methods=['POST'])
def verify():
    user_id = request.json['user_id']
    # 60-day verification logic
    status = verify_user(user_id)
    return jsonify({'status': status})

if __name__ == '__main__':
    app.run(debug=True, host='af.enginefive.com')
