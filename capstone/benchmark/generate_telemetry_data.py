"""
Synthetic Telemetry Generator for KubeRevive Benchmarking
Generates multi-metric time-series data including normal operational traffic
and injected anomaly regimes (CPU spikes, memory leaks, latency surges, error storms).
"""

import numpy as np
import pandas as pd
import os

def generate_dataset(n_samples=1500, random_seed=42):
    np.random.seed(random_seed)
    
    # Base timestamps (1-second intervals)
    timestamps = pd.date_range("2024-03-01 00:00:00", periods=n_samples, freq="1s")
    
    # Baseline normal metrics with realistic diurnal/noise patterns
    t = np.linspace(0, 10, n_samples)
    base_rps = 100 + 25 * np.sin(t) + np.random.normal(0, 4, n_samples)
    base_cpu = 25 + 10 * np.sin(t) + np.random.normal(0, 3, n_samples)
    base_mem = 35 + 2 * (t / 10) + np.random.normal(0, 1, n_samples)
    base_lat = 45 + 5 * np.sin(t) + np.random.exponential(4, n_samples)
    base_err = np.random.exponential(0.2, n_samples)
    labels = np.zeros(n_samples, dtype=int)
    anomaly_types = ["normal"] * n_samples

    # Anomaly Phase 1: CPU Throttling (Samples 300 to 380)
    base_cpu[300:380] += np.linspace(35, 65, 80) + np.random.normal(0, 3, 80)
    base_lat[320:380] += np.linspace(50, 200, 60)
    labels[300:380] = 1
    for i in range(300, 380):
        anomaly_types[i] = "cpu_spike"

    # Anomaly Phase 2: Memory Leak (Samples 650 to 800)
    ramp = np.linspace(0, 58, 150)
    base_mem[650:800] += ramp
    labels[720:800] = 1  # Triggered once memory surpasses safe threshold
    for i in range(720, 800):
        anomaly_types[i] = "memory_leak"

    # Anomaly Phase 3: Error Rate & Latency Storm (Samples 1050 to 1150)
    base_err[1050:1150] += np.random.uniform(25, 60, 100)
    base_lat[1050:1150] += np.random.uniform(400, 1200, 100)
    labels[1050:1150] = 1
    for i in range(1050, 1150):
        anomaly_types[i] = "http_500_storm"

    # Clip values to physically realistic boundaries
    df = pd.DataFrame({
        "timestamp": timestamps,
        "request_rate_rps": np.clip(base_rps, 1, 500).round(2),
        "cpu_usage_pct": np.clip(base_cpu, 1, 100).round(2),
        "memory_usage_pct": np.clip(base_mem, 5, 100).round(2),
        "latency_ms": np.clip(base_lat, 5, 5000).round(2),
        "error_rate_pct": np.clip(base_err, 0, 100).round(2),
        "is_anomaly": labels,
        "anomaly_type": anomaly_types
    })
    
    output_path = os.path.join(os.path.dirname(__file__), "..", "data", "sample_telemetry.csv")
    df.to_csv(output_path, index=False)
    print(f"[+] Successfully generated {len(df)} samples into {output_path}")
    print(f"    Total Anomaly Points: {df['is_anomaly'].sum()} ({(df['is_anomaly'].mean()*100):.2f}%)")
    return df

if __name__ == "__main__":
    generate_dataset()

