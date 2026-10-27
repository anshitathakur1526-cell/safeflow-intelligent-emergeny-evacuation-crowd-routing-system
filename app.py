from flask import Flask, jsonify, request
import sqlite3
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), 'aiml')))
from predict import predict_crowd

from database import init_db

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), 'core')))
from routing import dijkstra, get_graph_from_db

app = Flask(__name__)

with app.app_context():
    init_db()
    print("✅ Database Connected Successfully!")

@app.route('/')
def home():
    return "SafeFlow Server is Running!"

@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.get_json()
        room_id = data.get('room_id')
        time_of_day = data.get('time_of_day')
        is_emergency = data.get('is_emergency')
        sensor_capacity = data.get('sensor_capacity')
        result = predict_crowd(room_id, time_of_day, is_emergency, sensor_capacity)
        return jsonify({"status": "success", "prediction": result})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})

@app.route('/nodes', methods=['GET'])
def get_nodes():
    try:
        conn = sqlite3.connect('safeflow.db')
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM nodes')
        nodes = cursor.fetchall()
        conn.close()
        nodes_list = [{"id": n[0], "name": n[1], "floor": n[2], "is_exit": n[3]} for n in nodes]
        return jsonify({"status": "success", "nodes": nodes_list})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})

@app.route('/edges', methods=['GET'])
def get_edges():
    try:
        conn = sqlite3.connect('safeflow.db')
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM edges')
        edges = cursor.fetchall()
        conn.close()
        edges_list = [{"id": e[0], "from_node": e[1], "to_node": e[2], "distance": e[3]} for e in edges]
        return jsonify({"status": "success", "edges": edges_list})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})

@app.route('/route', methods=['POST'])
def get_route():
    try:
        data = request.get_json()
        start_node = data.get('start_node')
        end_node = data.get('end_node')
        graph, nodes = get_graph_from_db()
        cost, path = dijkstra(graph, start_node, end_node)
        if path:
            path_names = [nodes.get(n, f"Unknown({n})") for n in path]
            return jsonify({"status": "success", "path": path_names, "total_distance": cost})
        else:
            return jsonify({"status": "error", "message": "No path found!"})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})

@app.route('/block_path', methods=['POST'])
def block_path():
    try:
        data = request.get_json()
        n1 = data.get('from_node')
        n2 = data.get('to_node')
        conn = sqlite3.connect('safeflow.db')
        cursor = conn.cursor()
        cursor.execute('UPDATE edges SET distance = 99999 WHERE (from_node=? AND to_node=?) OR (from_node=? AND to_node=?)', (n1, n2, n2, n1))
        conn.commit()
        conn.close()
        return jsonify({"status": "success", "message": f"Path between Node {n1} and {n2} is now BLOCKED!"})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})

@app.route('/smart_route', methods=['POST'])
def smart_route():
    try:
        data = request.get_json()
        room_id = data.get('room_id')
        time_of_day = data.get('time_of_day')
        is_emergency = data.get('is_emergency')
        sensor_capacity = data.get('sensor_capacity')
        start_node = data.get('start_node')
        end_node = data.get('end_node')
        crowd_density = predict_crowd(room_id, time_of_day, is_emergency, sensor_capacity)
        print(f"🤖 ML Prediction: {crowd_density}")
        graph, nodes = get_graph_from_db()
        cost, path = dijkstra(graph, start_node, end_node, crowd_density=crowd_density)
        if path:
            path_names = [nodes.get(n, f"Unknown({n})") for n in path]
            return jsonify({"status": "success", "predicted_crowd": crowd_density, "safest_path": path_names, "effective_cost": cost})
        else:
            return jsonify({"status": "error", "message": "No safe path found!"})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})

if __name__ == '__main__':
    app.run(debug=True)