import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# 6 Mahine ka data (180 days)
days = 180
readings_per_day = 4  # Har 6 ghante mein 1 reading
total_readings = days * readings_per_day

# Dates create karna
end_date = datetime.now()
start_date = end_date - timedelta(days=days)
timestamps = [start_date + timedelta(hours=6*i) for i in range(total_readings)]

# Heartbeat data (Normal range 60-100 with some spikes)
np.random.seed(42)
heartbeat = np.random.normal(75, 10, total_readings)

# Thodi "Gadbad" (Outliers) add karna taaki graph real lage
for _ in range(15):
    heartbeat[np.random.randint(0, total_readings)] = np.random.randint(110, 160)

# DataFrame aur CSV save
df = pd.DataFrame({'timestamp': timestamps, 'heartbeat_bpm': heartbeat})
df.to_csv('raw_heart_monitoring_data.csv', index=False)

print("SUCCESS: 'raw_heart_monitoring_data.csv' file ban gayi hai!")