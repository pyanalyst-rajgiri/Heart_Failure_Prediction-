from django.shortcuts import render
from django.shortcuts import redirect # Ye upar import section mein add karein
from datetime import datetime, timedelta
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.utils
import json
import os

# Path setup
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
raw_csv_path = os.path.join(BASE_DIR, 'raw_heart_monitoring_data.csv')

def index(request):
    try:
        # 1. Read Raw Data
        df = pd.read_csv(raw_csv_path)

        # Ensure timestamp is in datetime format for analysis
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        
        # 2. Automated Cleaning
        df['heartbeat_bpm'] = df['heartbeat_bpm'].interpolate()
        
        # 3. Analytics Logic
        avg_bpm = round(df['heartbeat_bpm'].mean(), 1)
        max_bpm = round(df['heartbeat_bpm'].max(), 1)
        min_bpm = round(df['heartbeat_bpm'].min(), 1)
        
        # Risk Calculation based on 6 months data
        high_bpm_count = df[df['heartbeat_bpm'] > 100].shape[0]
        risk_percentage = round((high_bpm_count / len(df)) * 100, 2)
        
        std_dev = df['heartbeat_bpm'].std()
        status = "NORMAL"
        if risk_percentage > 5: status = "MODERATE RISK"
        if risk_percentage > 15: status = "HIGH RISK"
        if std_dev > 15: 
            status = "UNSTABLE / ARRHYTHMIA DETECTED"

        # --- GRAPH 1: Main Trend (6 Months Line Chart) ---
        fig_trend = px.line(df, x='timestamp', y='heartbeat_bpm', 
                            title='Longitudinal Heart Rate Trend (6 Months)',
                            labels={'heartbeat_bpm': 'BPM', 'timestamp': 'Date'},
                            template='plotly_dark')
        fig_trend.update_traces(line_color='#00d2ff')
        fig_trend.update_layout(paper_bgcolor='#1a1a1a', plot_bgcolor='#1a1a1a', font_color='#ccc')

        # --- GRAPH 2: Frequency Distribution (Histogram) ---
        # Ye dikhayega ki heart rate mostly kis range mein rehta hai
        fig_hist = px.histogram(df, x="heartbeat_bpm", nbins=30, 
                                title="Heart Rate Frequency Distribution",
                                labels={'heartbeat_bpm': 'BPM'},
                                template='plotly_dark')
        fig_hist.update_traces(marker_color='#ff0055')
        fig_hist.update_layout(paper_bgcolor='#1a1a1a', plot_bgcolor='#1a1a1a', font_color='#ccc')

        # --- GRAPH 3: Daily Average (Bar Chart) ---
        # Data ko daily basis par resample kar rahe hain averages ke liye
        daily_df = df.resample('D', on='timestamp').mean().reset_index()
        fig_daily = px.bar(daily_df, x='timestamp', y='heartbeat_bpm',
                           title="Daily Average Heart Rate",
                           labels={'heartbeat_bpm': 'Avg BPM', 'timestamp': 'Date'},
                           template='plotly_dark')
        fig_daily.update_traces(marker_color='#00ff00')
        fig_daily.update_layout(paper_bgcolor='#1a1a1a', plot_bgcolor='#1a1a1a', font_color='#ccc')

        # Convert all charts to JSON
        chart_trend_json = json.dumps(fig_trend, cls=plotly.utils.PlotlyJSONEncoder)
        chart_hist_json = json.dumps(fig_hist, cls=plotly.utils.PlotlyJSONEncoder)
        chart_daily_json = json.dumps(fig_daily, cls=plotly.utils.PlotlyJSONEncoder)

        # Context to send to HTML
        context = {
            'chart_trend': chart_trend_json,
            'chart_hist': chart_hist_json,
            'chart_daily': chart_daily_json,
            'status': status,
            'avg_bpm': avg_bpm,
            'max_bpm': max_bpm,
            'min_bpm': min_bpm,
            'risk_score': risk_percentage,
            'start_date': df['timestamp'].dt.date.min(),
            'end_date': df['timestamp'].dt.date.max()
        }
        return render(request, 'index.html', context)

    except Exception as e:
        return render(request, 'index.html', {'status': 'ERROR', 'error_msg': str(e)})

def predict(request):
    return render(request, 'index.html')


def simulate(request, mode):
    # Common Setup
    days = 180
    readings_per_day = 4
    total_readings = days * readings_per_day
    
    end_date = datetime.now()
    start_date = end_date - timedelta(days=days)
    timestamps = [start_date + timedelta(hours=6*i) for i in range(total_readings)]
    
    # Mode Selection Logic
    np.random.seed(None) # Randomness reset
    
    if mode == 'danger':
        # HIGH RISK DATA
        heartbeat = np.random.normal(110, 15, total_readings) 
        for _ in range(50):
            heartbeat[np.random.randint(0, total_readings)] = np.random.randint(150, 190)
            
    elif mode == 'unstable':
        # ARRHYTHMIA DATA (Zig-Zag)
        heartbeat = np.random.normal(loc=85, scale=25, size=total_readings)
        
    else:
        # NORMAL DATA (Default)
        heartbeat = np.random.normal(75, 10, total_readings)
        for _ in range(15):
             heartbeat[np.random.randint(0, total_readings)] = np.random.randint(110, 160)

    # Save to CSV
    df = pd.DataFrame({'timestamp': timestamps, 'heartbeat_bpm': heartbeat})
    df.to_csv(raw_csv_path, index=False)
    
    # Page Refresh (Wapas Dashboard par bhejo)
    return redirect('index')