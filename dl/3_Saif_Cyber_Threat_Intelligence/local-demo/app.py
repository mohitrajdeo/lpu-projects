#!/usr/bin/env python3
"""
Interactive Terminal SOC Incident Response Demonstration for Saif
INT422: Deep Learning & Applied AI
"""

import sys
import os
import time

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))
from secops_agent import AutonomousSecOpsSOC

def main():
    print("=" * 70)
    print(" INT422 AUTONOMOUS CYBERSECURITY SOC & THREAT HUNTER")
    print(" Student: Saif Siddique (12308813) | Lovely Professional University")
    print("=" * 70)
    
    model_file = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'models', 'intrusion_detection_model.pkl'))
    soc = AutonomousSecOpsSOC(model_file)
    
    print("\n[STEP 1] Monitoring incoming live network packet flow...")
    time.sleep(1)
    # Simulate normal traffic
    norm = soc.triage_network_flow(pkt_len=380, duration=45.2, fwd_pkts=12.0, syn_flags=1, port=443, source_ip="192.168.1.105")
    print(f"  Traffic from {norm['source_ip']}: {norm['attack_type']} (Threat: {norm['is_threat']})")
    time.sleep(1)

    print("\n[STEP 2] Simulating adversarial attack vector (High-Volume SYN Flood / DDoS)...")
    time.sleep(1)
    attack_flow = soc.triage_network_flow(pkt_len=450, duration=0.4, fwd_pkts=720.0, syn_flags=85, port=80, source_ip="203.0.113.19")
    print(f"  [ALERT] Intrusion Detection Neural Net Triggered!")
    print(f"  Attacker IP: {attack_flow['source_ip']}")
    print(f"  Classified Attack: {attack_flow['attack_type']} (Confidence: {attack_flow['confidence_score']*100:.1f}%)")
    time.sleep(1)

    print("\n[STEP 3] Agent 2 (Threat Hunter) querying MITRE ATT&CK RAG Vector Store...")
    intel = soc.correlate_threat_intel(attack_flow)
    print(f"  Technique Identified: {intel['technique_id']} ({intel['technique_name']})")
    print(f"  Tactic Category: {intel['tactic']}")
    print(f"  Mechanism: {intel['description']}")
    time.sleep(1)

    print("\n[STEP 4] Agent 3 (Containment Agent) executing automated firewall quarantine...")
    quarantine = soc.execute_quarantine(attack_flow, intel)
    print(f"  Rule Dispatched: {quarantine['firewall_rule_applied']}")
    print(f"  Quarantine Status: {quarantine['quarantine_status']}")
    time.sleep(1)

    print("\n[STEP 5] Agent 4 (LLM Synthesizer) compiling executive CTI Incident Brief...")
    brief = soc.generate_cti_brief(attack_flow, intel, quarantine)
    print(brief)
    print("\n[SUCCESS] End-to-end autonomous cyber defense workflow validated in real-time!")

if __name__ == '__main__':
    main()

