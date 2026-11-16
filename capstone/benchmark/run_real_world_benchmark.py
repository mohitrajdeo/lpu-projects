"""
Real-World Industry Benchmark Engine (Member 2 & 6 Responsibility)
NO SYNTHETIC DATA: Evaluates KubeRevive directly on:
1. Real AWS CloudWatch Production Telemetry Outages from the Numenta Anomaly Benchmark (NAB)
2. Real Production Apache & Linux Server Logs from Loghub (LogPAI)
Verified against official NAB ground-truth labeled anomaly windows.
"""

import sys
import os
import json
import time
import numpy as np
import pandas as pd

# Add capstone root to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from kuberevive.anomaly_detection import RollingZScoreDetector, MetricAnomalyDetector, LogAnomalyParser

DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "data", "real_world")


def evaluate_on_real_aws_telemetry(filename, nab_key, metric_col="value"):
    csv_path = os.path.join(DATA_DIR, filename)
    windows_path = os.path.join(DATA_DIR, "nab_ground_truth_windows.json")

    if not os.path.exists(csv_path) or not os.path.exists(windows_path):
        raise FileNotFoundError(f"Missing required real dataset {csv_path}")

    df = pd.read_csv(csv_path)
    df["timestamp"] = pd.to_datetime(df["timestamp"])

    with open(windows_path, "r") as f:
        nab_windows = json.load(f)

    outage_windows = nab_windows.get(nab_key, [])
    
    # Ground Truth binary labeling from verified NAB anomaly windows
    df["ground_truth_anomaly"] = 0
    for start_str, end_str in outage_windows:
        start_dt = pd.to_datetime(start_str)
        end_dt = pd.to_datetime(end_str)
        df.loc[(df["timestamp"] >= start_dt) & (df["timestamp"] <= end_dt), "ground_truth_anomaly"] = 1

    # Run KubeRevive Anomaly Scorer on real AWS telemetry
    stat_detector = RollingZScoreDetector(window_size=25, z_threshold=2.5)
    
    predictions = []
    detection_timestamps = []
    
    for idx, row in df.iterrows():
        val = float(row[metric_col])
        is_anom, z_score, _ = stat_detector.update_and_check("aws_metric", val)
        pred = 1 if is_anom else 0
        predictions.append(pred)
        if pred == 1:
            detection_timestamps.append(row["timestamp"])

    df["kuberevive_predicted"] = predictions

    # Calculate Metrics
    y_true = df["ground_truth_anomaly"].values
    y_pred = df["kuberevive_predicted"].values

    tp = int(np.sum((y_true == 1) & (y_pred == 1)))
    fp = int(np.sum((y_true == 0) & (y_pred == 1)))
    fn = int(np.sum((y_true == 1) & (y_pred == 0)))
    tn = int(np.sum((y_true == 0) & (y_pred == 0)))

    precision = round((tp / (tp + fp) * 100), 2) if (tp + fp) > 0 else 0.0
    recall = round((tp / (tp + fn) * 100), 2) if (tp + fn) > 0 else 0.0
    f1 = round((2 * (precision * recall) / (precision + recall)), 2) if (precision + recall) > 0 else 0.0

    # Calculate Time-to-Detect on the first ground-truth outage window
    mttd_minutes = "N/A"
    if outage_windows and detection_timestamps:
        outage_start = pd.to_datetime(outage_windows[0][0])
        # Find first detection after or during outage window
        subsequent = [t for t in detection_timestamps if t >= outage_start]
        if subsequent:
            first_alert = subsequent[0]
            mttd_minutes = round((first_alert - outage_start).total_seconds() / 60.0, 1)

    # NAB Official Metric: Window-Level Outage Detection
    # In NAB scoring, an outage is successfully caught if at least one alert fires inside each window
    detected_windows = 0
    total_windows = len(outage_windows)
    for start_str, end_str in outage_windows:
        start_dt = pd.to_datetime(start_str)
        end_dt = pd.to_datetime(end_str)
        window_alerts = df[(df["timestamp"] >= start_dt) & (df["timestamp"] <= end_dt) & (df["kuberevive_predicted"] == 1)]
        if len(window_alerts) > 0:
            detected_windows += 1

    window_detection_rate = round((detected_windows / total_windows * 100), 2) if total_windows > 0 else 0.0

    return {
        "dataset": filename,
        "nab_official_key": nab_key,
        "total_real_data_points": len(df),
        "ground_truth_outage_windows": total_windows,
        "successfully_detected_windows": detected_windows,
        "nab_window_detection_rate_pct": window_detection_rate,
        "total_alerts_fired": int(np.sum(y_pred)),
        "first_detection_lead_time": f"{mttd_minutes} mins from window onset",
        "point_level_metrics": {
            "precision_pct": precision,
            "recall_pct": recall,
            "f1_score_pct": f1
        }
    }


def evaluate_on_real_server_logs():
    log_path = os.path.join(DATA_DIR, "apache_production_2k.log")
    if not os.path.exists(log_path):
        return {"error": "Apache log not found"}

    parser = LogAnomalyParser()
    total_lines = 0
    errors_detected = 0

    with open(log_path, "r", encoding="utf-8", errors="ignore") as f:
        for line in f:
            total_lines += 1
            res = parser.parse_log(line, service="apache-httpd")
            if res["is_error"]:
                errors_detected += 1

    top_templates = parser.get_recent_error_summary(5)
    return {
        "dataset": "Loghub Apache Production Logs",
        "total_lines_parsed": total_lines,
        "real_errors_isolated": errors_detected,
        "top_error_templates": top_templates
    }


def run_full_real_world_benchmark():
    print("=" * 80)
    print("  🏆 KUBEREVIVE REAL-WORLD BENCHMARK EVALUATION (NAB & LOGHUB)")
    print("  Evaluating on Real AWS CloudWatch Outages & Production Web Server Logs")
    print("=" * 80)

    # 1. Real AWS AutoScaling Group Misconfiguration Outage
    print("\n[TEST 1] Real AWS AutoScaling Group (ASG) CPU Outage (NAB benchmark)...")
    res_asg = evaluate_on_real_aws_telemetry(
        "aws_asg_misconfiguration.csv",
        "realKnownCause/cpu_utilization_asg_misconfiguration.csv"
    )
    print(f"  • Total Real AWS Telemetry Points:  {res_asg['total_real_data_points']:,}")
    print(f"  • Ground Truth Outage Windows:      {res_asg['ground_truth_outage_windows']}")
    print(f"  • Successfully Detected Windows:    {res_asg['successfully_detected_windows']}/{res_asg['ground_truth_outage_windows']} ({res_asg['nab_window_detection_rate_pct']}%)")
    print(f"  • Early Warning Lead Time:          {res_asg['first_detection_lead_time']}")

    # 2. Real AWS EC2 Request Latency System Failure
    print("\n[TEST 2] Real AWS EC2 Request Latency System Failure (NAB benchmark)...")
    res_lat = evaluate_on_real_aws_telemetry(
        "aws_ec2_latency_failure.csv",
        "realKnownCause/ec2_request_latency_system_failure.csv"
    )
    print(f"  • Total Real AWS Telemetry Points:  {res_lat['total_real_data_points']:,}")
    print(f"  • Ground Truth Outage Windows:      {res_lat['ground_truth_outage_windows']}")
    print(f"  • Successfully Detected Windows:    {res_lat['successfully_detected_windows']}/{res_lat['ground_truth_outage_windows']} ({res_lat['nab_window_detection_rate_pct']}%)")
    print(f"  • Early Warning Lead Time:          {res_lat['first_detection_lead_time']}")

    # 3. Real Production Apache Web Server Logs from Loghub
    print("\n[TEST 3] Real Production Apache Web Server Logs (Loghub / LogPAI)...")
    res_log = evaluate_on_real_server_logs()
    print(f"  • Total Production Logs Parsed: {res_log['total_lines_parsed']:,} lines")
    print(f"  • Real Critical Errors Isolated: {res_log['real_errors_isolated']}")
    print("  • Isolated Real Error Templates:")
    for t in res_log['top_error_templates'][:3]:
        print(f"    - [{t['count']} occurrences] {t['template'][:75]}...")

    # Compile Final Artifact
    final_report = {
        "evaluation_type": "Real-World Industrial Dataset Benchmark",
        "benchmark_suites": [
            "Numenta Anomaly Benchmark (NAB) - Amazon Web Services (AWS) Real Outages",
            "Loghub / LogPAI - Apache Production Web Server Access & Error Logs"
        ],
        "aws_asg_outage": res_asg,
        "aws_ec2_latency_outage": res_lat,
        "loghub_apache_logs": res_log
    }

    out_file = os.path.join(os.path.dirname(__file__), "real_world_benchmark_results.json")
    with open(out_file, "w") as f:
        json.dump(final_report, f, indent=2)

    print("\n" + "=" * 80)
    print(f"  ✔ Real-world benchmark completed! Results saved to:\n    {out_file}")
    print("=" * 80)
    return final_report


if __name__ == "__main__":
    run_full_real_world_benchmark()
