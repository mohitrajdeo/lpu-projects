# INT422: Deep Learning & Applied AI — Capstone Project Guide v2.0
# Project 1: Autonomous Cloud Operations Intelligence (AIOps)

**Student Name:** Mohit Raj Deo  
**Registration Number:** 12323329 | **Roll Number:** 62  
**Faculty Guide:** Ms. Manpreet Kaur, Assistant Professor, Department of CSE, Lovely Professional University  

---

## 🎯 1. Project Overview & Theoretical Foundation

Cloud-native microservice applications face sudden, high-impact failures including progressive heap memory leaks, thread starvation, CPU saturation, and socket queue thrashing. This project establishes an **Autonomous Cloud Operations Intelligence (AIOps v2.0)** platform that detects anomalies in real-time telemetry, retrieves appropriate remediation runbooks via vector RAG, and autonomously dispatches healing actions within sub-15-second response times.

### The 4 Mandatory Applied AI Technologies:
1. **Machine Learning (ML / DL):** Scikit-Learn **Isolation Forest** trained on multidimensional telemetry vectors (`[CPU%, RAM%, Latency(ms), Sockets]`) combined with rolling trend gradients ($\frac{d\text{CPU}}{dt}$, $\frac{d\text{RAM}}{dt}$).
2. **Vector RAG (Retrieval-Augmented Generation):** In-memory semantic vector store containing production SRE runbooks (`Runbook-104: High Memory & Socket Thrashing`, `Runbook-108: Compute Throttling`, `Runbook-212: Network Queue Exhaustion`, `Runbook-305: Database Pool Lockup`).
3. **Autonomous AI Agents:** LangGraph-inspired 4-agent state machine swarm:
   - `Agent 1: Telemetry Monitoring Agent` — continuously evaluates resource metrics and health indices.
   - `Agent 2: Incident Investigation Agent` — executes vector similarity search to identify probable root causes.
   - `Agent 3: Autonomous Remediation Agent` — dispatches self-healing commands and monitors health probe restoration.
   - `Agent 4: LLM RCA Synthesizer` — drafts structured executive root cause analysis reports.
4. **Large Language Model (LLM):** Reasoner synthesizing comprehensive post-mortem reports with Mean Time to Recovery (MTTR) calculation, SLA impact metrics, and compliance audit logs.

---

## 📁 2. Deliverables & File Directory

```
c:\MOHIT\dl\1_Mohit_AIOps_Cloud_Intelligence\
│
├── final_report/
│   ├── FINAL_PROJECT_REPORT.docx     # 12+ page comprehensive academic report (Word)
│   ├── FINAL_PROJECT_REPORT.pdf      # Official submission PDF (with embedded charts)
│   ├── diagram_aiops_architecture.png # High-res multi-agent architecture diagram
│   └── chart_telemetry_anomaly.png   # ML Isolation Forest decision boundary chart
│
├── presentation/
│   └── index.html                    # 16:9 interactive HTML5 presentation deck
│
├── src/
│   └── aiops_agent.py                # Multi-Agent AIOps v2.0 Engine
│
├── models/
│   └── telemetry_anomaly_detector.pkl # Trained Scikit-Learn Isolation Forest model
│
├── data/
│   └── telemetry_dataset.csv         # 10,000-sample time-series telemetry dataset
│
├── local-demo/
│   └── app.py                        # Interactive terminal execution demo
│
└── HOW_TO_RUN.md                     # This comprehensive execution manual
```

---

## 🚀 3. Step-by-Step Execution Guide

### Option A: Interactive Command-Line Terminal Demo
To run the automated terminal demonstration illustrating the complete 5-step self-healing loop:

```powershell
# Navigate to the local-demo directory
cd c:\MOHIT\dl\1_Mohit_AIOps_Cloud_Intelligence\local-demo

# Execute the demonstration
python app.py
```

#### What You Will Observe:
1. **Normal Telemetry Baseline:** Ingests baseline metrics (`CPU: 22.4%`, `RAM: 41.1%`, `Latency: 11.2ms`, `Sockets: 115`). The Isolation Forest computes decision score `+0.1527` (System Healthy, `is_anomaly = False`).
2. **Chaos Injection:** Simulates an unhandled memory leak (`CPU: 92.8%`, `RAM: 91.4%`, `Latency: 245.0ms`, `Sockets: 480`). Decision score drops to `-0.2995` (`is_anomaly = True`).
3. **Vector RAG Matching:** The Investigation Agent matches symptom vectors against enterprise runbooks, retrieving `Runbook-104` with 88.6% confidence.
4. **Autonomous Self-Healing:** Remediation Agent dispatches `systemctl restart web-portal.service && systemctl reload nginx` and verifies recovery.
5. **Executive RCA Brief:** Synthesizes structured markdown post-mortem with MTTR: 12 seconds.

---

### Option B: Unified Web Dashboard (Port 8000)
To interact with the live graphical command center:

```powershell
python -m uvicorn server:app --app-dir c:\MOHIT\dl\dashboard --host 0.0.0.0 --port 8000
```
1. Open your browser to **`http://localhost:8000`**.
2. Select **Project 1: Cloud Operations Intelligence (Mohit Raj Deo)**.
3. Drag the **CPU**, **RAM**, **Latency**, and **Sockets** sliders in real time.
4. Click preset chaos buttons:
   - `Memory Leak (RB-104)`
   - `CPU Saturation (RB-108)`
   - `Network Thrashing (RB-212)`
5. Observe the live updating sparkline trend chart, radial health index gauge, and live agent terminal log.

---

## 🔌 4. REST API Endpoint Reference

The AIOps engine is exposed via a production-grade FastAPI endpoint:

- **Endpoint:** `POST /api/aiops/telemetry`
- **Headers:** `Content-Type: application/json`

### Example Request Body:
```json
{
  "cpu": 94.5,
  "memory": 91.2,
  "latency": 240.0,
  "sockets": 430.0
}
```

### Example JSON Response:
```json
{
  "monitoring": {
    "is_anomaly": true,
    "anomaly_score": -0.2995,
    "system_health_index": 27.8,
    "trend_gradients": { "cpu_gradient": 70.4, "mem_gradient": 50.1 },
    "telemetry": { "cpu": 94.5, "memory": 91.2, "latency": 240.0, "sockets": 430.0 }
  },
  "investigation": {
    "incident_type": "MEMORY_LEAK",
    "severity": "CRITICAL",
    "rag_confidence": 0.886,
    "retrieved_runbook": {
      "title": "Runbook-104: High Memory & Socket Thrashing Remediation",
      "action_command": "systemctl restart web-portal.service && systemctl reload nginx",
      "estimated_recovery_time_sec": 12
    }
  },
  "remediation": {
    "remediation_status": "EXECUTED_SUCCESSFULLY",
    "verification_status": "SYSTEM_HEALTH_RESTORED_TO_OK"
  },
  "rca_report": "=== EXECUTIVE ROOT CAUSE ANALYSIS ==="
}
```

---

## 📊 5. Presentation Mode & Exporting Slides

1. Double-click `presentation/index.html` to open in Google Chrome or Microsoft Edge.
2. Use **`Right Arrow`** or **`Space`** to navigate forward, and **`Left Arrow`** to navigate backward.
3. Press **`F`** to toggle full-screen presentation mode.
4. Press **`Ctrl + P`** to export the entire 16:9 presentation directly to PDF (Select *Save as PDF*, *Landscape*, and ensure *Background graphics* is checked).
