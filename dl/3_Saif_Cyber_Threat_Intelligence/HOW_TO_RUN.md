# INT422: Deep Learning & Applied AI — Capstone Project Guide v2.0
# Project 3: Autonomous SOC Cyber Threat Hunter & Incident Response

**Student Name:** Saif Siddique  
**Registration Number:** 12308813 | **Roll Number:** 44  
**Faculty Guide:** Ms. Manpreet Kaur, Assistant Professor, Department of CSE, Lovely Professional University  

---

## 🎯 1. Project Overview & Theoretical Foundation

Modern corporate infrastructure is exposed to continuous, automated cyber attacks including high-volume distributed denial-of-service (DDoS), reconnaissance port scanning, web injection exploits, and password dictionary attacks. Security Operations Center (SOC) analysts face alert fatigue, leading to prolonged adversary dwell time. This project designs and implements an **Autonomous SOC Cyber Threat Hunter & Incident Response Platform (SecOps v2.0)** that leverages a **Deep Multi-Layer Perceptron (MLP) Neural Network** to classify malicious network flows in real time, correlates threats with the **MITRE ATT&CK Enterprise Matrix**, and dispatches automated **zero-trust firewall quarantine commands** to prevent adversary lateral movement.

### The 4 Mandatory Applied AI Technologies:
1. **Deep Learning (DL / ML):** Deep **Multi-Layer Perceptron (MLP)** Neural Network trained on network flow features (`[Packet Length, Duration, Packets per Second, SYN Flags, Target Port]`) with Softmax classification output.
2. **Vector RAG:** Semantic MITRE ATT&CK Enterprise Matrix mapping attack flows to standardized adversary techniques (`T1498.001 Direct Network Flood`, `T1046 Network Service Discovery`, `T1190 Exploit Public-Facing Application`, `T1110.001 Password Guessing`).
3. **Autonomous AI Agents:** LangGraph-inspired 4-agent SOC swarm:
   - `Agent 1: SOC Alert Triage Agent` — ingests network flow features and runs deep neural inference.
   - `Agent 2: Threat Hunter Agent` — correlates detected attack profiles with MITRE ATT&CK tactics, techniques, and forensic indicators.
   - `Agent 3: Active Defense Containment Agent` — executes zero-trust cross-platform firewall isolation (Linux `iptables`, `nftables`, and AWS Security Group CLI).
   - `Agent 4: CTI Synthesizer Agent` — produces structured Cyber Threat Intelligence (CTI) briefs with STIX 2.1 telemetry.
4. **Large Language Model (LLM):** Synthesizes executive forensic post-mortem narratives, risk blast radius evaluations, and Tier-2 hardening advisories.

---

## 📁 2. Deliverables & File Directory

```
c:\MOHIT\dl\3_Saif_Cyber_Threat_Intelligence\
│
├── final_report/
│   ├── FINAL_PROJECT_REPORT.docx     # 12+ page comprehensive academic report (Word)
│   ├── FINAL_PROJECT_REPORT.pdf      # Official submission PDF (with embedded charts)
│   ├── diagram_secops_architecture.png # Multi-agent SOC architecture diagram
│   └── chart_neural_loss_curve.png   # Deep MLP training & validation loss curve
│
├── presentation/
│   └── index.html                    # 16:9 interactive HTML5 presentation deck
│
├── src/
│   └── secops_agent.py               # Multi-Agent SOC v2.0 Engine with zero-trust defense
│
├── models/
│   └── intrusion_detection_model.pkl # Trained Deep MLP Neural Network model
│
├── data/
│   └── network_intrusion_dataset.csv # 15,000-flow multi-class intrusion dataset
│
├── local-demo/
│   └── app.py                        # Interactive terminal execution demo
│
└── HOW_TO_RUN.md                     # This comprehensive execution manual
```

---

## 🚀 3. Step-by-Step Execution Guide

### Option A: Interactive Command-Line Terminal Demo
To run the automated terminal demonstration showcasing real-time flow triage, deep neural net classification, MITRE ATT&CK mapping, and active defense firewall quarantine:

```powershell
# Navigate to the local-demo directory
cd c:\MOHIT\dl\3_Saif_Cyber_Threat_Intelligence\local-demo

# Execute the demonstration
python app.py
```

#### What You Will Observe:
1. **Normal Traffic Ingestion:** Evaluates legitimate corporate HTTPS traffic (`Packet Length: 400`, `PPS: 15`). Deep Neural Net scores as `Normal Traffic` (`Threat: False`).
2. **Adversarial Flow Simulation:** Injects an adversary SYN flood attack (`Packet Length: 450`, `PPS: 620`, `SYN Flags: 75`, `Port: 80`, `Attacker IP: 203.0.113.19`).
3. **Deep Neural Net Triage:** MLP classifies the flow as `DDoS` with 100.0% confidence, assigning a Threat Risk Score of `95.0 / 100`.
4. **MITRE ATT&CK Correlation:** Maps attack mechanism to technique `T1498.001 (Direct Network Flood)` under the *Impact* tactic.
5. **Zero-Trust Active Containment:** Automatically dispatches Linux `iptables` and modern `nftables` packet drop rules, isolating the threat at the network perimeter.
6. **Executive CTI Brief:** Synthesizes structured markdown intelligence brief with STIX incident identifier.

---

### Option B: Unified Web Dashboard (Port 8000)
To interact with the live graphical command center:

```powershell
python -m uvicorn server:app --app-dir c:\MOHIT\dl\dashboard --host 0.0.0.0 --port 8000
```
1. Open your browser to **`http://localhost:8000`**.
2. Select **Project 3: SOC Threat Hunter (Saif Siddique)**.
3. Test adversarial attack vectors:
   - `🚨 SYN Flood (DDoS)`
   - `🚨 PortScan (T1046)`
   - `🚨 SQL Injection (T1190)`
4. Click **`⚡ Ingest & Mitigate`**.
5. Observe the radial Threat Risk Score gauge, real-time Deep Neural Net classification badge, MITRE technique alignment, and active containment firewall command stream.

---

## 🔌 4. REST API Endpoint Reference

- **Endpoint:** `POST /api/secops/triage`
- **Headers:** `Content-Type: application/json`

### Example Request Body:
```json
{
  "pkt_len": 450.0,
  "duration": 0.5,
  "fwd_pkts": 750.0,
  "syn_flags": 85,
  "port": 80,
  "source_ip": "203.0.113.88"
}
```

### Example JSON Response:
```json
{
  "triage": {
    "source_ip": "203.0.113.88",
    "is_threat": true,
    "attack_type": "DDoS",
    "confidence_score": 1.0,
    "threat_risk_score": 95.0
  },
  "threat_intelligence": {
    "technique_id": "T1498.001",
    "technique_name": "Direct Network Flood",
    "tactic": "Impact"
  },
  "quarantine": {
    "quarantine_status": "BLOCKED_AND_ISOLATED",
    "attacker_ip": "203.0.113.88",
    "firewall_rules": {
      "iptables": "iptables -A INPUT -p tcp --syn -m limit --limit 1/s -j ACCEPT && ufw deny from 203.0.113.88",
      "nftables": "nft add rule inet filter input ip saddr 203.0.113.88 counter drop"
    }
  },
  "cti_brief": "=== SOC CYBER THREAT INTELLIGENCE BRIEF ==="
}
```

---

## 📊 5. Presentation Mode & Exporting Slides

1. Double-click `presentation/index.html` to open in Google Chrome or Microsoft Edge.
2. Use **`Right Arrow`** or **`Space`** to navigate forward, and **`Left Arrow`** to navigate backward.
3. Press **`F`** to toggle full-screen presentation mode.
4. Press **`Ctrl + P`** to export the entire 16:9 presentation directly to PDF.
