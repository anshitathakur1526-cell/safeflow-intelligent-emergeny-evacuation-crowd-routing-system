import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# 1. Data load karo
csv_path = os.path.join('aiml', 'data', 'crowd_data.csv')
df = pd.read_csv(csv_path)

print("📊 Data Visualization Shuru...")

# 2. Figure size set karo
plt.figure(figsize=(15, 10))

# --- Graph 1: Crowd Density Distribution (Bar Chart) ---
plt.subplot(2, 2, 1)
sns.countplot(x='crowd_density', data=df, palette='viridis')
plt.title('Crowd Density Distribution')
plt.xlabel('Density Level')
plt.ylabel('Count')

# --- Graph 2: Emergency vs Normal Crowd (Box Plot) ---
plt.subplot(2, 2, 2)
sns.boxplot(x='is_emergency', y='actual_crowd', data=df, palette='Set2')
plt.title('Crowd: Emergency vs Normal')
plt.xlabel('Emergency (0=No, 1=Yes)')
plt.ylabel('Actual Crowd Count')

# --- Graph 3: Time of Day vs Crowd (Bar Chart) ---
plt.subplot(2, 2, 3)
sns.barplot(x='time_of_day', y='actual_crowd', data=df, estimator='mean', palette='coolwarm')
plt.title('Average Crowd by Time of Day')
plt.xlabel('Time of Day')
plt.ylabel('Average Crowd Count')

# --- Graph 4: Room Capacity vs Actual Crowd (Scatter Plot) ---
plt.subplot(2, 2, 4)
sns.scatterplot(x='sensor_capacity', y='actual_crowd', hue='crowd_density', data=df, palette='Set1')
plt.title('Capacity vs Actual Crowd')
plt.xlabel('Sensor Capacity')
plt.ylabel('Actual Crowd')

# 3. Layout adjust karo aur save karo
plt.tight_layout()
plt.savefig('aiml/data/crowd_analysis.png', dpi=150)
print("✅ Graphs saved to aiml/data/crowd_analysis.png")
plt.show()