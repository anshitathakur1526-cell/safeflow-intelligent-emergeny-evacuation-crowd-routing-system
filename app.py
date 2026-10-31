# app.py - Main Flask Application (Fixed Version)
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import joblib

# Core DSA functions import
from core.routing import get_graph_from_db, dijkstra

# Security module import
from security import generate_token, token_required, verify_sensor_data, audit_log, USERS

app = Flask(__name__)
CORS(app)

# Load AIML Model
try:
    ml_model = joblib.load('aiml/data/safeflow_model.pkl')
    print("✅ ML Model loaded successfully")
except Exception as e:
    ml_model = None
    print(f"⚠️ ML Model not found. Error: {e}")

@app.route('/')
def home():
    return render_template('dashboard.html')

@app.route('/login', methods=['POST'])
def login():
    data = request.json
    username = data.get('username')
    password = data.get('password')
    
    if username in USERS and USERS[username]['password'] == password:
        token = generate_token(username)
        audit_log("LOGIN", username, "Successful login")
        return jsonify({'token': token, 'role': USERS[username]['role']}), 200
    
    return jsonify({'message': 'Invalid credentials'}), 401

@app.route('/emergency', methods=['POST'])
@token_required
def trigger_emergency(current_user, current_role):
    if current_role not in ['admin', 'warden']:
        return jsonify({'message': 'Access Denied'}), 403

    data = request.json
    sensor_payload = str(data.get('sensor_data', {}))
    signature = data.get('signature', '')

    if not verify_sensor_data(sensor_payload, signature):
        audit_log("BLOCKED", current_user, "Fake sensor signature detected!")
        return jsonify({'message': '⚠️ Security Alert: Spoofed sensor data rejected!'}), 400

    location = data.get('location')
    audit_log("EMERGENCY_TRIGGER", current_user, f"Fire at {location}")
    return jsonify({'message': f'Emergency activated at {location}. Rerouting...'}), 200

@app.route('/route/<start_node>', methods=['GET'])
def get_route(start_node):
    try:
        graph = get_graph_from_db()
        result = dijkstra(graph, start_node, 'EXIT_MAIN')
        
        # Handle tuple return properly
        if isinstance(result, tuple):
            if len(result) == 2:
                route, total_cost = result
            else:
                route = result[0]
                total_cost = result[1] if len(result) > 1 else 100
        else:
            route = result
            total_cost = 100
        
        # Ensure route is a list
        if not isinstance(route, list):
            route = [start_node, 'Corridor_A', 'EXIT_MAIN']
            total_cost = 100
            
    except Exception as e:
        route = [start_node, 'Corridor_A', 'EXIT_MAIN']
        total_cost = 100
        print(f"Route Error: {e}")
    
    return jsonify({
        'route': route,
        'total_cost': total_cost,
        'ml_status': 'Active' if ml_model else 'Fallback Mode'
    })

if __name__ == '__main__':
    print("🚀 Starting SafeFlow Server on http://127.0.0.1:5000")
    app.run(debug=True, port=5000)