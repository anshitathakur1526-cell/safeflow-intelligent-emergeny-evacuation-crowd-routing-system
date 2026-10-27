import joblib
import os
import numpy as np

# Model aur Label Encoder ko load karo
# Path ko aiml/data mein change kiya
model_path = os.path.join('aiml', 'data', 'safeflow_model.pkl')
encoder_path = os.path.join('aiml', 'data', 'label_encoder.pkl')

if os.path.exists(model_path) and os.path.exists(encoder_path):
    model = joblib.load(model_path)
    le_density = joblib.load(encoder_path)
    print("✅ Model loaded successfully!")
else:
    print("❌ Model file not found. Please run the notebook first.")
    model = None
    le_density = None

def get_time_num(time_str):
    time_map = {'Morning': 2, 'Afternoon': 0, 'Evening': 1, 'Night': 3}
    return time_map.get(time_str, 0)

def predict_crowd(room_id, time_of_day, is_emergency, sensor_capacity):
    if model is None:
        return "Error: Model not loaded"
    
    time_num = get_time_num(time_of_day)
    new_data = np.array([[room_id, time_num, is_emergency, sensor_capacity]])
    prediction_num = model.predict(new_data)
    prediction_text = le_density.inverse_transform(prediction_num)
    
    return prediction_text[0]

if __name__ == "__main__":
    result = predict_crowd(room_id=10, time_of_day="Evening", is_emergency=0, sensor_capacity=50)
    print(f" Prediction from Python File: {result}")