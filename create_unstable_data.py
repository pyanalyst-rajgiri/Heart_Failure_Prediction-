import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# Parameters
days = 180
readings_per_day = 4
total_readings = days * readings_per_day

# Time generate karna
end_date = datetime.now()
start_date = end_date - timedelta(days=days)
timestamps = [start_date + timedelta(hours=6*i) for i in range(total_readings)]

# --- UNSTABLE DATA LOGIC ---
np.random.seed(50)

# Mean 85 rakha hai (jo safe hai), lekin 'scale=25' ka matlab hai 
# ye 35 se lekar 135 tak wild jump karega!
heartbeat = np.random.normal(loc=85, scale=25, size=total_readings)

# Save file
df = pd.DataFrame({'timestamp': timestamps, 'heartbeat_bpm': heartbeat})
df.to_csv('raw_heart_monitoring_data.csv', index=False)

print("ALERT: 'Unstable/Fluctuating' Patient Data Generated!")