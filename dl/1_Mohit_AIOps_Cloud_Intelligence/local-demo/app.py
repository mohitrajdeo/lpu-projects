#!/usr/bin/env python3
"""
Interactive Terminal Dashboard for Mohit AIOps Engine
INT422: Deep Learning & Applied AI
"""

import sys
import os
import time

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))
from aiops_agent import AIOpsMultiAgentSystem

def main():
    print("=" * 70)
    print(" INT422 AIOps CLOUD INTELLIGENCE DEMONSTRATION")
    print(" Student: Mohit Raj Deo (12323329) | Lovely Professional University")
    print("=" * 70)
    
    model_file = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'models', 'telemetry_anomaly_detector.pkl'))
    aiops = AIOpsMultiAgentSystem(model_file)
    
    print("\n[STEP 1] Streaming normal server telemetry...")
    normal_check = aiops.monitor_telemetry(cpu=22.4, mem=41.1, latency=11.2, sockets=115)
    print(f"  Telemetry: CPU {normal_check['telemetry']['cpu']}% | RAM {normal_check['telemetry']['memory']}%")
    print(f"  Anomaly Detector: {normal_check['is_anomaly']} (System Healthy - Score: {normal_check['anomaly_score']})")
    time.sleep(1)

    print("\n[STEP 2] Injecting synthetic failure (Sudden Memory Leak + Socket Spike)...")
    time.sleep(1)
    anom_check = aiops.monitor_telemetry(cpu=92.8, mem=91.4, latency=245.0, sockets=480)
    print(f"  Telemetry: CPU {anom_check['telemetry']['cpu']}% | RAM {anom_check['telemetry']['memory']}% | Sockets {anom_check['telemetry']['sockets']}")
    print(f"  [ALERT] Anomaly Detector Triggered! is_anomaly = {anom_check['is_anomaly']} (Score: {anom_check['anomaly_score']})")
    time.sleep(1)

    print("\n[STEP 3] Agent 2 (Investigation Agent) querying Vector RAG...")
    inv = aiops.investigate_incident(anom_check)
    print(f"  RAG Matched Runbook: {inv['retrieved_runbook']['title']}")
    print(f"  Root Cause Identified: {inv['retrieved_runbook']['root_cause']}")
    time.sleep(1)

    print("\n[STEP 4] Agent 3 (Remediation Agent) executing self-healing action...")
    rem = aiops.execute_remediation(inv)
    print(f"  Dispatched Command: {rem['dispatched_command']}")
    print(f"  Remediation State: {rem['remediation_status']}")
    time.sleep(1)

    print("\n[STEP 5] Agent 4 (LLM Synthesizer) compiling executive RCA report...")
    rca = aiops.synthesize_rca_report(anom_check, inv, rem)
    print(rca)
    print("\n[SUCCESS] End-to-end AIOps self-healing pipeline verified!")

if __name__ == '__main__':
    main()

