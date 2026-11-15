# INT422: Deep Learning & Applied AI
# Comprehensive Student & Evaluator Execution Manual v2.0
## How to Run, Test, Present, and Evaluate All 3 Capstone Projects

**Institution:** Department of Computer Science and Engineering, Lovely Professional University  
**Course Code:** INT422 – Deep Learning & Applied AI  
**Course Faculty Guide:** Ms. Manpreet Kaur, Assistant Professor  

---

## 👥 Student & Project Allocation Roster

| Student Name | Registration No. | Roll No. | Assigned Project Domain | Core ML / AI Technology |
| :--- | :--- | :--- | :--- | :--- |
| **Mohit Raj Deo** | **12323329** | **62** | **Project 1: Autonomous Cloud Operations Intelligence (AIOps v2.0)** | Isolation Forest + Vector RAG + Self-Healing SRE Agents + LLM RCA |
| **Akash Choudhary** | **12301625** | **11** | **Project 2: Autonomous Multi-Agent Software Engineering Platform (SWE v2.0)** | Random Forest Defect Classifier + AST Analysis + Multi-Agent Code Swarm + Test Sandbox |
| **Saif Siddique** | **12308813** | **44** | **Project 3: Autonomous SOC Threat Hunter & Incident Response (SecOps v2.0)** | Deep MLP Neural Net + MITRE ATT&CK RAG + Active Defense Zero-Trust Quarantine + CTI |

---

## 📑 Table of Contents
1. [Project Architecture & Directory Layout](#1-project-architecture--directory-layout)
2. [Mandatory 4-Technology Integration Matrix](#2-mandatory-4-technology-integration-matrix)
3. [Master Production Interactive Dashboard (Live on Port 8000)](#3-master-production-interactive-dashboard)
4. [How to View and Submit the Final Reports (.docx & .pdf)](#4-how-to-view-and-submit-the-final-reports)
5. [How to Present the 16:9 Presentation Decks](#5-how-to-present-the-169-presentation-decks)
6. [Project 1 (Mohit Raj Deo) - Step-by-Step Execution Guide](#6-project-1-mohit-raj-deo---step-by-step-execution-guide)
7. [Project 2 (Akash Choudhary) - Step-by-Step Execution Guide](#7-project-2-akash-choudhary---step-by-step-execution-guide)
8. [Project 3 (Saif Siddique) - Step-by-Step Execution Guide](#8-project-3-saif-siddique---step-by-step-execution-guide)
9. [Clean Submission ZIP Archives & Distribution Packages](#9-clean-submission-zip-archives--distribution-packages)

---

## 1. Project Architecture & Directory Layout

The workspace is organized into three completely autonomous, self-contained folders with zero external npm or node_modules bloat:

```
c:\MOHIT\dl\
│
├── 1_Mohit_AIOps_Cloud_Intelligence/     # Mohit Raj Deo (12323329 | Roll: 62)
│   ├── final_report/                     # FINAL_PROJECT_REPORT.docx & .pdf + Architecture Diagram + Anomaly Plot
│   ├── presentation/                     # Interactive HTML5 16:9 Presentation Deck (index.html)
│   ├── src/                              # Multi-Agent Engine v2.0 (aiops_agent.py)
│   ├── models/                           # Trained ML Model (telemetry_anomaly_detector.pkl)
│   ├── data/                             # Telemetry Time-Series Dataset (telemetry_dataset.csv)
│   ├── local-demo/                       # Interactive CLI Demo (app.py)
│   └── HOW_TO_RUN.md                     # Standalone quickstart guide
│
├── 2_Akash_Autonomous_SWE_System/        # Akash Choudhary (12301625 | Roll: 11)
│   ├── final_report/                     # FINAL_PROJECT_REPORT.docx & .pdf + Architecture Diagram + Confusion Matrix
│   ├── presentation/                     # Interactive HTML5 16:9 Presentation Deck (index.html)
│   ├── src/                              # Multi-Agent Engine v2.0 (swe_agents.py with real AST analysis)
│   ├── models/                           # Trained ML Model (code_defect_classifier.pkl)
│   ├── data/                             # Software Code Metrics Dataset (code_metrics_defects.csv)
│   ├── local-demo/                       # Interactive CLI Demo (app.py)
│   └── HOW_TO_RUN.md                     # Standalone quickstart guide
│
├── 3_Saif_Cyber_Threat_Intelligence/     # Saif Siddique (12308813 | Roll: 44)
│   ├── final_report/                     # FINAL_PROJECT_REPORT.docx & .pdf + Architecture Diagram + Loss Curve
│   ├── presentation/                     # Interactive HTML5 16:9 Presentation Deck (index.html)
│   ├── src/                              # Multi-Agent Engine v2.0 (secops_agent.py with MITRE matrix)
│   ├── models/                           # Trained Deep MLP Neural Network (intrusion_detection_model.pkl)
│   ├── data/                             # Network Intrusion Flow Dataset (network_intrusion_dataset.csv)
│   ├── local-demo/                       # Interactive CLI Demo (app.py)
│   └── HOW_TO_RUN.md                     # Standalone quickstart guide
│
├── dashboard/                            # Unified Master Production Web Dashboard v2.0
│   ├── server.py                         # FastAPI + Uvicorn Async REST API
│   └── static/                           # Glassmorphic Single Page Application + Artifact Downloads
│
├── EXECUTION_GUIDE_AND_USER_MANUAL.md   # This comprehensive manual (Markdown)
├── HOW_TO_USE_AND_EXECUTION_MANUAL.docx  # Formatted Word Manual with embedded graphics
├── HOW_TO_USE_AND_EXECUTION_MANUAL.pdf   # Official PDF Manual
├── Mohit_12323329_AIOps_DL_Project.zip   # Mohit's standalone submission zip
├── Akash_12301625_SWE_DL_Project.zip    # Akash's standalone submission zip
├── Saif_12308813_SecOps_DL_Project.zip  # Saif's standalone submission zip
└── ALL_3_INT422_DL_PROJECTS_MASTER.zip   # Master submission archive for all 3 projects
```

---

## 2. Mandatory 4-Technology Integration Matrix

Every project strictly satisfies the four compulsory pillars defined in the INT422 capstone syllabus:

| Mandatory Pillar | Project 1: Mohit (AIOps) | Project 2: Akash (SWE) | Project 3: Saif (SecOps) |
| :--- | :--- | :--- | :--- |
| **1. LLM (Large Language Model)** | Generates structured Executive Root Cause Analysis (RCA) reports with MTTR estimation, SLA impact analysis, and compliance audit. | Decomposes natural-language user specifications into architecture blueprints, modular class interfaces, and clean docstrings. | Synthesizes SOC Cyber Threat Intelligence (CTI) incident briefs, forensic narratives, and Tier-2 hardening advisories. |
| **2. AI Agents** | LangGraph 4-Agent Swarm: Telemetry Monitor -> RAG Investigator -> Self-Healing Remediation -> RCA Synthesizer. | LangGraph 5-Agent Swarm: System Architect -> Developer -> Static AST Analyzer -> ML Quality Reviewer -> Sandbox Test Engineer. | LangGraph 4-Agent Swarm: SOC Triage Agent -> MITRE Threat Hunter -> Active Containment Healer -> CTI Brief Synthesizer. |
| **3. Machine Learning / Deep Learning** | Scikit-Learn **Isolation Forest** trained on telemetry vectors (`[cpu, mem, latency, sockets]`) with decision score boundary. | Scikit-Learn **Random Forest Classifier** trained on code metrics (`[loc, cyclomatic, halstead, ast_depth, params]`). | Deep **Multi-Layer Perceptron (MLP)** Neural Network trained on network flows (`[pkt_len, duration, fwd_pkts, syn_flags, port]`). |
| **4. Vector RAG** | In-memory semantic vector store mapping anomaly signatures to enterprise SRE runbooks (Runbook-104, 108, 212, 305). | Knowledge base of Gang of Four (GoF) structural patterns, Token Bucket, LRU Cache, and OWASP secure coding standards. | Enterprise MITRE ATT&CK Matrix vector mappings (T1498.001 DDoS, T1046 PortScan, T1190 SQLi, T1110.001 Brute Force). |

---

## 3. Master Production Interactive Dashboard

The dashboard provides a live, interactive command center where evaluators can test every feature in real time:

- **URL:** `http://localhost:8000`
- **Backend:** `FastAPI` + `Uvicorn` asynchronous REST service.
- **Frontend:** Glassmorphic Single Page Application (`index.html`) with real-time SVG telemetry gauges, interactive sliders, red-team attack injection presets, and streaming agent execution consoles.

### Starting the Dashboard:
```powershell
# From the project root (c:\MOHIT\dl\):
python -m uvicorn server:app --app-dir c:\MOHIT\dl\dashboard --host 0.0.0.0 --port 8000
```
Open your browser to `http://localhost:8000` to interact with:
- **Tab 1 (AIOps):** Adjust CPU, RAM, Latency sliders; click `Memory Leak (Runbook-104)` to watch the Isolation Forest trigger an alert, query RAG, and execute autonomous self-healing.
- **Tab 2 (SWE):** Select `Rate Limiter Middleware` or `Thread-Safe LRU Cache`; click `Trigger Multi-Agent SWE Swarm` to see AST analysis, cyclomatic complexity, maintainability index, and passing sandbox unit tests.
- **Tab 3 (SecOps):** Select `🚨 SYN Flood (DDoS)` or `🚨 SQL Injection`; click `⚡ Ingest & Mitigate` to watch the Deep Neural Net classify the attack, map MITRE ATT&CK techniques, and dispatch zero-trust firewall isolation rules.
- **Tab 4 (Hub):** One-click download access to all Word reports, PDF documents, HTML presentation decks, and submission ZIP archives for both INT422 (Deep Learning) and INT333 (DevOps).

---

## 4. How to View and Submit the Final Reports

Per academic guidelines, all final project reports are prepared in **both Microsoft Word (`.docx`) and Adobe PDF (`.pdf`)** formats. Embedded directly inside each document are the high-resolution architecture diagrams and ML training plots.

### Direct File Paths:
- **Mohit Raj Deo (12323329):**
  - Word: `c:\MOHIT\dl\1_Mohit_AIOps_Cloud_Intelligence\final_report\FINAL_PROJECT_REPORT.docx`
  - PDF: `c:\MOHIT\dl\1_Mohit_AIOps_Cloud_Intelligence\final_report\FINAL_PROJECT_REPORT.pdf`
- **Akash Choudhary (12301625):**
  - Word: `c:\MOHIT\dl\2_Akash_Autonomous_SWE_System\final_report\FINAL_PROJECT_REPORT.docx`
  - PDF: `c:\MOHIT\dl\2_Akash_Autonomous_SWE_System\final_report\FINAL_PROJECT_REPORT.pdf`
- **Saif Siddique (12308813):**
  - Word: `c:\MOHIT\dl\3_Saif_Cyber_Threat_Intelligence\final_report\FINAL_PROJECT_REPORT.docx`
  - PDF: `c:\MOHIT\dl\3_Saif_Cyber_Threat_Intelligence\final_report\FINAL_PROJECT_REPORT.pdf`

---

## 5. How to Present the 16:9 Presentation Decks

Each project includes an interactive, browser-based 16:9 presentation slide deck:
- Mohit: `c:\MOHIT\dl\1_Mohit_AIOps_Cloud_Intelligence\presentation\index.html`
- Akash: `c:\MOHIT\dl\2_Akash_Autonomous_SWE_System\presentation\index.html`
- Saif: `c:\MOHIT\dl\3_Saif_Cyber_Threat_Intelligence\presentation\index.html`

### Controls for Presentation Mode:
- **`Right Arrow (→)` or `Space`:** Advance to the next slide.
- **`Left Arrow (←)`:** Return to the previous slide.
- **`F` Key:** Toggle Fullscreen presentation view.
- **`Ctrl + P` (Print):** Exports the slide deck directly to a 16:9 presentation PDF (Select Landscape layout, Background graphics checked, Margins none).

---

## 6. Project 1 (Mohit Raj Deo) - Step-by-Step Execution Guide

### Local Terminal Demo:
```powershell
python c:\MOHIT\dl\1_Mohit_AIOps_Cloud_Intelligence\local-demo\app.py
```
### Verification Workflow:
1. Streams baseline server telemetry (CPU: 22%, RAM: 41%, Latency: 11ms). ML outputs `is_anomaly = False`.
2. Injects simulated memory leak chaos (CPU: 92%, RAM: 91%, Sockets: 480).
3. Isolation Forest outputs `is_anomaly = True` with anomaly score `-0.2995`.
4. RAG engine matches `Runbook-104: High Memory & Socket Thrashing Remediation`.
5. Remediation Agent dispatches `systemctl restart web-portal.service && systemctl reload nginx`.
6. LLM Synthesizer generates the formatted Executive RCA report.

---

## 7. Project 2 (Akash Choudhary) - Step-by-Step Execution Guide

### Local Terminal Demo:
```powershell
python c:\MOHIT\dl\2_Akash_Autonomous_SWE_System\local-demo\app.py
```
### Verification Workflow:
1. Ingests natural-language user prompt: `"Design and implement a robust sliding-window API Rate Limiter in Python"`.
2. Architect Agent retrieves Token Bucket / Sliding Window architectural pattern from RAG.
3. Developer Agent synthesizes modular Python implementation.
4. Static AST Analyzer parses the code tree, calculating LOC, Cyclomatic Complexity, and Maintainability Index (MI).
5. Defect Quality ML model evaluates code metrics and assigns risk classification (`CLEAN - Production Ready`).
6. Sandbox Test Engineer executes test assertions, verifying 100% statement test coverage.

---

## 8. Project 3 (Saif Siddique) - Step-by-Step Execution Guide

### Local Terminal Demo:
```powershell
python c:\MOHIT\dl\3_Saif_Cyber_Threat_Intelligence\local-demo\app.py
```
### Verification Workflow:
1. Ingests network packet flow metrics (`[pkt_len=450, duration=0.8s, fwd_pkts=620, syn_flags=75, port=80]`).
2. Deep MLP Neural Network flags anomaly with 100% confidence, classifying threat as `DDoS`.
3. Threat Hunter Agent correlates flow with MITRE ATT&CK technique `T1498.001 (Direct Network Flood)`.
4. Active Defense Agent dispatches multi-platform containment commands (`iptables`, `nftables`, and `aws ec2 revoke-security-group-ingress`).
5. Synthesizes executive Cyber Threat Intelligence (CTI) incident brief.

---

## 9. Clean Submission ZIP Archives & Distribution Packages

All packages have been cleaned of `__pycache__`, temporary files, and bloat:

| Archive Filename | Size | Included Contents | Intended Recipient |
| :--- | :--- | :--- | :--- |
| `Mohit_12323329_AIOps_DL_Project.zip` | ~1.7 MB | Project 1 standalone code, model, dataset, reports (.docx & .pdf), and slides. | Mohit Raj Deo (Submission Portal) |
| `Akash_12301625_SWE_DL_Project.zip` | ~1.4 MB | Project 2 standalone code, model, dataset, reports (.docx & .pdf), and slides. | Akash Choudhary (Submission Portal) |
| `Saif_12308813_SecOps_DL_Project.zip` | ~1.1 MB | Project 3 standalone code, model, dataset, reports (.docx & .pdf), and slides. | Saif Siddique (Submission Portal) |
| `ALL_3_INT422_DL_PROJECTS_MASTER.zip` | ~4.2 MB | All 3 complete projects, datasets, models, dashboard, and execution manuals. | Course Evaluator / Faculty Submission |

All files are ready for academic evaluation and final grading.

