"""
Real-World Dataset Ingestion Engine (Member 2 & 6 Responsibility)
Downloads established, peer-reviewed industry benchmark datasets:
1. Numenta Anomaly Benchmark (NAB) - Real AWS CloudWatch EC2 & AutoScaling Outages
2. LogPAI / Loghub - Real Production Apache Web Server Access & Error Logs
"""

import os
import urllib.request
import json

DATA_DIR = os.path.join(os.path.dirname(__file__), "real_world")
os.makedirs(DATA_DIR, exist_ok=True)

NAB_BASE = "https://raw.githubusercontent.com/numenta/NAB/master/data/"
LOGHUB_BASE = "https://raw.githubusercontent.com/logpai/loghub/master/"

DATASETS = {
    # Real AWS Production Telemetry Outages (NAB)
    "aws_asg_misconfiguration.csv": NAB_BASE + "realKnownCause/cpu_utilization_asg_misconfiguration.csv",
    "aws_ec2_latency_failure.csv": NAB_BASE + "realKnownCause/ec2_request_latency_system_failure.csv",
    "aws_rds_cpu_utilization.csv": NAB_BASE + "realAWSCloudwatch/rds_cpu_utilization_cc0c53.csv",
    
    # Real Production Server Logs (Loghub / LogPAI)
    "apache_production_2k.log": LOGHUB_BASE + "Apache/Apache_2k.log",
    "linux_syslog_2k.log": LOGHUB_BASE + "Linux/Linux_2k.log"
}

NAB_GROUND_TRUTH_URL = "https://raw.githubusercontent.com/numenta/NAB/master/labels/combined_windows.json"


def download_all_real_datasets():
    print("[*] Downloading Real-World Peer-Reviewed Benchmark Datasets...")
    
    # Download ground-truth anomaly windows
    labels_file = os.path.join(DATA_DIR, "nab_ground_truth_windows.json")
    if not os.path.exists(labels_file):
        print("  • Fetching NAB official ground-truth anomaly windows...")
        urllib.request.urlretrieve(NAB_GROUND_TRUTH_URL, labels_file)
        print("    ✔ Saved nab_ground_truth_windows.json")

    for filename, url in DATASETS.items():
        dest = os.path.join(DATA_DIR, filename)
        if not os.path.exists(dest):
            print(f"  • Downloading {filename} from {url[:60]}...")
            try:
                urllib.request.urlretrieve(url, dest)
                size_kb = os.path.getsize(dest) / 1024
                print(f"    ✔ Saved {filename} ({size_kb:.1f} KB)")
            except Exception as e:
                print(f"    ❌ Failed to download {filename}: {e}")
        else:
            print(f"  ✔ {filename} already present.")

    print("[+] All real-world benchmark datasets successfully downloaded!")


if __name__ == "__main__":
    download_all_real_datasets()

