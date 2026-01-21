import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# Parameters
days = 180
readings_per_day = 4
total_readings = days * readings_per_day

# Dates
end_date = datetime.now()
start_date = end_date - timedelta(days=days)
timestamps = [start_date + timedelta(hours=6*i) for i in range(total_readings)]

# --- DANGER DATA LOGIC ---
np.random.seed(99) 
# Normal insan ka 75 hota hai, hum yahan patient ka AVERAGE hi 110 kar rahe hain (Critical Condition)
heartbeat = np.random.normal(110, 15, total_readings) 

# Beech-beech mein Heart Failure Attack (Extreme Spikes: 160+ BPM)
for _ in range(50):
    heartbeat[np.random.randint(0, total_readings)] = np.random.randint(150, 190)

# Save
df = pd.DataFrame({'timestamp': timestamps, 'heartbeat_bpm': heartbeat})
df.to_csv('raw_heart_monitoring_data.csv', index=False)

print("ALERT: 'High Risk' Patient Data Generated! Dashboard check karein.")