# security.py - Cybersecurity Module (Updated for Demo)
import jwt
import datetime
import hmac
import hashlib
from functools import wraps
from flask import request, jsonify

SECRET_KEY = "safeflow_super_secret_key_2026"
SENSOR_SECRET = "sensor_hmac_secret_key"

USERS = {
    "admin": {"password": "admin123", "role": "admin"},
    "warden": {"password": "warden123", "role": "warden"},
    "occupant": {"password": "user123", "role": "occupant"}
}

def generate_token(username):
    payload = {
        'username': username,
        'role': USERS[username]['role'],
        'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=1)
    }
    return jwt.encode(payload, SECRET_KEY, algorithm='HS256')

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization')
        if not token:
            return jsonify({'message': 'Token is missing!'}), 401
        try:
            if token.startswith('Bearer '):
                token = token.split(' ')[1]
            data = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
            current_user = data['username']
            current_role = data['role']
        except:
            return jsonify({'message': 'Token is invalid!'}), 401
        return f(current_user, current_role, *args, **kwargs)
    return decorated

def verify_sensor_data(payload, signature):
    # Demo mode bypass: agar signature "demo_signature" hai to accept karo
    if signature == "demo_signature":
        return True
    
    # Normal HMAC verification
    expected_signature = hmac.new(
        SENSOR_SECRET.encode('utf-8'), 
        payload.encode('utf-8'), 
        hashlib.sha256
    ).hexdigest()
    
    return hmac.compare_digest(expected_signature, signature)

def audit_log(action, user, details):
    with open("audit_log.txt", "a") as f:
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        f.write(f"[{timestamp}] User: {user} | Action: {action} | Details: {details}\n")
    print(f"🛡️ AUDIT LOG: {action} by {user}")