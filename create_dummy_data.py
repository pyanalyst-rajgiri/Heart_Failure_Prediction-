import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import os

# 1. Setup Parameters (6 Months Data)
days = 180
readings_per_day = 4  # Har 6 ghante mein 1 reading
total_readings = days * readings_per_day

# 2. Time Series Generate Karna
end_date = datetime.now()
start_date = end_date - timedelta(days=days)
timestamps = [start_date + timedelta(hours=6*i) for i in range(total_readings)]

# 3. Heartbeat Data Generate Karna (Normal Range: 60-100)
np.random.seed(42)  # Same data har baar ke liye
heartbeat = np.random.normal(75, 8, total_readings)

# 4. "Raw" Defects Add Karna (Taaki Data Cleaning ka use dikhe)
# Kuch values ko missing (NaN) banana
for _ in range(20):
    heartbeat[np.random.randint(0, total_readings)] = np.nan

# Kuch values ko extreme high (Outliers) banana
for _ in range(10):
    heartbeat[np.random.randint(0, total_readings)] = np.random.randint(150, 200)

# 5. DataFrame Banana
df = pd.DataFrame({
    'timestamp': timestamps,
    'heartbeat_bpm': heartbeat,
    'patient_id': 'P-101' # Ek hi patient ka record
})

# 6. CSV File Save Karna
file_name = 'raw_heart_monitoring_data.csv'
df.to_csv(file_name, index=False)

print(f"Success! '{file_name}' aapke folder mein ban gayi hai.")
print(f"Total Records: {len(df)}")