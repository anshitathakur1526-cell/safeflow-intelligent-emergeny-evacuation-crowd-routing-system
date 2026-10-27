# SafeFlow API Documentation

## Overview
SafeFlow Intelligent Emergency Evacuation & Crowd Routing System ka REST API.

## Base URL
http://127.0.0.1:5000

---

## API Endpoints

### 1. Home Route
GET /
Server status check karne ke liye.
Response: SafeFlow Server is Running!

### 2. ML Crowd Prediction
POST /predict
ML model se crowd density predict karo.
Request Body: {"room_id": 10, "time_of_day": "Evening", "is_emergency": 1, "sensor_capacity": 50}
Response: {"status": "success", "prediction": "Medium"}

### 3. Get All Nodes
GET /nodes
Database se saare nodes (rooms aur exits) fetch karo.

### 4. Get All Edges
GET /edges
Database se saare edges (raaste) fetch karo.

### 5. Basic Routing (Dijkstra)
POST /route
Do nodes ke beech shortest path nikalo.
Request Body: {"start_node": 1, "end_node": 4}
Response: {"status": "success", "path": ["Room 101", "Corridor A", "Main Exit"], "total_distance": 30.5}

### 6. Block Path (Emergency)
POST /block_path
Kisi raaste ko block karo.
Request Body: {"from_node": 1, "to_node": 3}

### 7. Smart Route (ML + DSA Integration)
POST /smart_route
ML prediction ke saath safest path nikalo.
Request Body: {"room_id": 10, "time_of_day": "Evening", "is_emergency": 1, "sensor_capacity": 50, "start_node": 1, "end_node": 4}
Response: {"status": "success", "predicted_crowd": "Medium", "safest_path": ["Room 101", "Corridor A", "Main Exit"], "effective_cost": 45.75}

---

## Technology Stack
- Backend: Flask (Python)
- Database: SQLite
- ML: Scikit-learn, Random Forest Classifier
- Routing: Dijkstra's Algorithm with Priority Queue (heapq)
- Cost Model: Dynamic weight (Low=1x, Medium=1.5x, High=3x)

---

## Project Structure
safeflow-intelligent-emergency-evacuation-crowd-routing-system/
├── app.py (Main Flask app)
├── database.py (DB initialization)
├── safeflow.db (SQLite database)
├── API_DOCUMENTATION.md (Yeh file)
├── aiml/ (ML Model files)
│   ├── predict.py
│   ├── visualize.py
│   ├── ml_pipeline.md
│   └── data/ (crowd_data.csv, safeflow_model.pkl, label_encoder.pkl, crowd_analysis.png)
└── core/ (DSA Engine)
    ├── routing.py (Dijkstra)
    ├── cost_model.py (Cost calculation)
    └── simulation.py (Crowd simulation)

---

## How to Run
1. pip install flask scikit-learn pandas numpy matplotlib seaborn
2. python app.py
3. Server starts on http://127.0.0.1:5000

---

## Team Members
- Anshita: AIML (ML Model, Visualization, Integration)
- Anshulika & Shagun: Cybersecurity
- Shared: Core DSA Engine, Database, Backend API

---

## Future Enhancements
- Real-time sensor data integration
- Multi-floor building support
- WebSocket for live updates
- Frontend dashboard
- Advanced ML models (LSTM)