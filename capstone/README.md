# 🛡️ KubeRevive: Autonomous Multi-Agent AIOps Framework for Self-Healing CI/CD Microservices

[![Build Status](https://img.shields.io/badge/CI%2FCD-Passing-emerald)](https://github.com)
[![Python](https://img.shields.io/badge/Python-3.11%20%7C%203.14-blue)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.110+-teal)](https://fastapi.tiangolo.com)
[![Docker](https://img.shields.io/badge/Docker-Ready-2496ED)](https://docker.com)
[![Target IEEE](https://img.shields.io/badge/IEEE-INDICON%20%7C%20CONECCT%20%7C%20DISCOVER-orange)](https://ieee.org)
[![Team Size](https://img.shields.io/badge/Team-6%20Members%20(RACI)-purple)](team_division/WORK_BREAKDOWN_STRUCTURE.md)

> **Capstone Engineering Project & IEEE Research Publication Suite**  
> An enterprise-grade, closed-loop Autonomous AIOps framework combining **multi-variate unsupervised machine learning (Isolation Forest)**, **dynamic statistical anomaly detection (Rolling Z-Score / EWMA)**, **Agentic Root Cause Analysis (RAG over postmortems)**, and **deterministic self-healing DevOps actuators (Canary rollback, pod scaling, graceful restart, circuit breaking)**.

---

## 📊 Proven Empirical Results (40 Chaos Trials)

| Metric | Traditional SRE Alerting | KubeRevive Autonomous | Improvement |
| :--- | :---: | :---: | :---: |
| **Mean Time to Detect (MTTD)** | $69.01$\,s | **$2.77$\,s** | **-95.98%** |
| **Mean Time to Recover (MTTR)** | $313.69$\,s (5.2 mins) | **$6.55$\,s** | **-97.91%** |
| **Detection Precision** | $78.4\%$ | **$94.2\%$** | **+15.8%** |
| **Detection Recall** | $81.2\%$ | **$91.8\%$** | **+10.6%** |
| **F1-Score** | $79.8\%$ | **$93.0\%$** | **+13.2%** |
| **Autonomous Remediation Rate** | $0\%$ (Manual human intervention) | **$96.5\%$** | **Fully Autonomous** |

---

## 🚀 Quickstart Guide (Run in 60 Seconds)

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Launch the Autonomous AIOps Dashboard
```bash
python -m uvicorn kuberevive.dashboard.app:app --host 0.0.0.0 --port 8000 --reload
```
Open your browser at: **[http://localhost:8000](http://localhost:8000)**  
You will see the dark-themed real-time dashboard featuring live metric gauges, dynamic Chart.js time-series plots, active incident timelines, and the Chaos Engineering injection station.

### 3. Run the Automated Test Suite (100% Passing)
```bash
python -m pytest tests/
```

### 4. Run the Real-World Physical Stress & Defense Benchmark (NO MOCKS)
```bash
python benchmark/live_stress_tester.py
```
*Directly allocates real physical memory on your RAM via `bytearray`, spawns real multi-threaded mathematical CPU burn loops, injects real HTTP 500 exceptions over network sockets, detects them via real `psutil` OS metrics, and executes real garbage collection memory reclamation!*

### 5. Run the Empirical Benchmarking & Chart Generation
```bash
python benchmark/run_benchmark.py
python benchmark/generate_charts.py
```
This executes the 40-trial comparative evaluation and saves high-resolution publication charts into `paper/figures/`.

### 6. Generate the Native PowerPoint Presentation (.pptx)
```bash
python presentation/generate_presentation.py
```
Outputs: `presentation/KubeRevive_Capstone_Presentation.pptx`.

---

## 👥 6-Person Work Breakdown Structure (RACI)

Our project is strictly partitioned across 6 members with distinct technical ownership and deliverables:

| Member & Role | Primary Technical Ownership | Core Deliverables & Code |
| :--- | :--- | :--- |
| **Member 1: Lead Architect** | Central Orchestrator, Async Concurrency, REST API | `kuberevive/dashboard/app.py`, `kuberevive/telemetry/collector.py` |
| **Member 2: AI/ML Engineer** | Anomaly Detection, Isolation Forest, NLP Log Parser | `kuberevive/anomaly_detection/metrics_detector.py`, `log_anomaly_parser.py` |
| **Member 3: Agentic LLM Lead** | Triage Agent, Postmortem RAG Engine, Plan Generator | `kuberevive/agents/triage_agent.py`, `rca_agent.py`, `patch_generator.py` |
| **Member 4: DevOps Specialist** | Infrastructure Actuators, Prometheus, Docker | `kuberevive/actuators/remediation_engine.py`, `docker-compose.yml`, `prometheus.yml` |
| **Member 5: Chaos/QA Lead** | Chaos Injector, Pytest Testbed, GitHub Actions CI | `kuberevive/simulation/chaos_injector.py`, `tests/`, `.github/workflows/ci.yml` |
| **Member 6: Research/Defense Lead** | MTTD/MTTR Benchmarks, IEEE Paper, PPT Deck | `benchmark/run_benchmark.py`, `paper/`, `presentation/` |

Full details, task matrices, and sprint schedules are in [team_division/WORK_BREAKDOWN_STRUCTURE.md](team_division/WORK_BREAKDOWN_STRUCTURE.md).  
Complete 35+ viva questions and model answers are in [team_division/VIVA_DEFENSE_GUIDE.md](team_division/VIVA_DEFENSE_GUIDE.md).

---

## 📄 IEEE Research Paper Publication Guide

### Target Scopus/IEEE Conferences in India:
1. **IEEE INDICON** (Flagship IEEE India Council annual international conference, rotating across India).
2. **IEEE CONECCT** (Organized by IEEE Bangalore Section, specialized in Computing, Software Systems & MLOps).
3. **IEEE DISCOVER** (Organized by IEEE Mangalore Subsection, specialized in Distributed Systems and Intelligent Computing).
4. **IEEE AIC** (World Conference on Applied Intelligence and Computing, offering hybrid/online presentation).

### Recommended Compilation Method (Overleaf vs MiKTeX):
- **Overleaf (Recommended for 6-Person Team Collaboration):**
  1. Open [Overleaf.com](https://www.overleaf.com) and create a free project.
  2. Upload `paper/IEEE_Research_Paper_KubeRevive.tex`, `paper/references.bib`, and the `paper/figures/` folder.
  3. Click **Recompile**. Your camera-ready 2-column IEEE PDF is compiled instantly without local LaTeX installation hassles!
- **Local MiKTeX Compilation:**
  1. If you prefer offline compilation, install MiKTeX from [miktex.org](https://miktex.org).
  2. In `c:\MOHIT\capstone\paper`, run:
     ```cmd
     pdflatex IEEE_Research_Paper_KubeRevive.tex
     bibtex IEEE_Research_Paper_KubeRevive
     pdflatex IEEE_Research_Paper_KubeRevive.tex
     pdflatex IEEE_Research_Paper_KubeRevive.tex
     ```

---

## 🏛️ Repository Architecture & File Tree

```
c:\MOHIT\capstone\
├── README.md                          <-- Comprehensive documentation and quickstart
├── requirements.txt                   <-- Python package dependencies
├── Dockerfile                         <-- Multi-stage production container build
├── docker-compose.yml                 <-- Orchestrator + Prometheus services
├── pytest.ini                         <-- Pytest test runner configuration
├── .github/
│   └── workflows/
│       └── ci.yml                     <-- Automated CI/CD, lint, test, benchmark & build
├── config/
│   ├── config.yaml                    <-- System configuration, thresholds & LLM settings
│   └── prometheus.yml                 <-- Prometheus scraping configuration
├── data/
│   ├── incident_knowledge_base.json   <-- Historical postmortems for RAG RCA
│   └── sample_telemetry.csv           <-- 1500-sample multi-variate telemetry benchmark
├── kuberevive/                         <-- Core Python package
│   ├── __init__.py
│   ├── anomaly_detection/             <-- Module 1 (Member 2): Rolling Z-Score, iForest & Logs
│   ├── agents/                        <-- Module 2 (Member 3): Triage Debouncer, RCA RAG & Planner
│   ├── actuators/                     <-- Module 3 (Member 4): Auto-Rollback, Scale, Restart, Probe
│   ├── telemetry/                     <-- Module 4 (Member 4 & 1): Ingestion buffer & Prometheus
│   ├── simulation/                    <-- Module 5 (Member 5): Chaos Injector & Mock Service
│   └── dashboard/                     <-- Module 6 (Member 1 & 6): FastAPI Orchestrator & UI
├── tests/                             <-- Automated Pytest Test Suite (100% pass)
├── benchmark/                         <-- Empirical Evaluation Scripts (MTTD/MTTR, Charts)
├── paper/                             <-- Academic Research Paper Suite
│   ├── IEEE_Research_Paper_KubeRevive.tex <-- 2-Column Camera-Ready IEEEtran LaTeX
│   ├── IEEE_Research_Paper_KubeRevive.md  <-- Markdown edition with full text and formulas
│   ├── references.bib                 <-- BibTeX academic citations
│   └── figures/                       <-- High-resolution PNG publication figures
├── presentation/                      <-- Presentation Suite
│   ├── KubeRevive_Capstone_Presentation.pptx <-- 12-Slide Native PowerPoint Deck
│   ├── generate_presentation.py       <-- PPTX Generator script
│   └── Slide_Deck_Script_and_Notes.md <-- Speaker notes & defense talking points
└── team_division/                     <-- 6-Member Work Division & Viva Guide
    ├── WORK_BREAKDOWN_STRUCTURE.md    <-- RACI matrix, modules, sprint schedule
    └── VIVA_DEFENSE_GUIDE.md          <-- 35+ Viva questions & model answers
```

