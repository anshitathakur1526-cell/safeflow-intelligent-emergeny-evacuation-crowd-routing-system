# SafeFlow ML Pipeline Documentation

## Overview
Yeh document SafeFlow project ke Machine Learning pipeline ko explain karta hai.

## 1. Problem Statement
Building emergency ke time par crowd density predict karna taaki safe evacuation routes decide kiye ja sakein.

## 2. Dataset
- **Source:** Synthetic data (1000 rows)
- **Features:**
  - `room_id`: Room ka ID number
  - `time_of_day`: Morning/Afternoon/Evening/Night
  - `is_emergency`: 0 (Normal) ya 1 (Emergency)
  - `sensor_capacity`: Room ki maximum capacity
- **Target Variable:** `crowd_density` (Low/Medium/High)

## 3. Model Selection
- **Algorithm:** Random Forest Classifier
- **Reason:** Yeh algorithm complex patterns ko achhe se handle karta hai aur overfitting se bachata hai.

## 4. Training Process
1. Data ko 80% training aur 20% testing mein divide kiya
2. Text features (time_of_day) ko numbers mein convert kiya
3. Model ko train kiya aur accuracy check ki
4. Model ko `.pkl` file mein save kiya

## 5. Model Performance
- **Accuracy:** ~95% (dummy data par)
- **Prediction Time:** < 1ms per prediction

## 6. Integration with Backend
- Flask backend `predict.py` file ko call karega
- Real-time sensor data input hoga
- Model crowd density predict karega
- Dijkstra's algorithm is prediction ko use karke safe route nikalega

## 7. Files Structure

## 8. Future Improvements
- Real building data se model retrain karna
- Deep Learning models try karna (LSTM for time series)
- Model accuracy ko aur improve karna