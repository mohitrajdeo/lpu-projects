# INT422: Deep Learning & Applied AI — Capstone Project Guide v2.0
# Project 2: Autonomous Multi-Agent Software Engineering Platform (SWE)

**Student Name:** Akash Choudhary  
**Registration Number:** 12301625 | **Roll Number:** 11  
**Faculty Guide:** Ms. Manpreet Kaur, Assistant Professor, Department of CSE, Lovely Professional University  

---

## 🎯 1. Project Overview & Theoretical Foundation

Converting high-level software requirements into robust, bug-free, production-grade source code is an immense engineering challenge. Standard single-prompt LLM code generators frequently introduce security vulnerabilities, poor concurrency handling, and high cognitive complexity. This project develops an **Autonomous Multi-Agent Software Engineering Platform (SWE v2.0)** that translates natural-language specifications into modular Python code, performs **real Abstract Syntax Tree (AST)** static auditing, evaluates defect risk via a trained **Random Forest Classifier**, and validates execution inside a dynamic sandbox.

### The 4 Mandatory Applied AI Technologies:
1. **Large Language Model (LLM):** Architecture reasoning and code synthesizer decomposing natural language requirements into modular classes and structured interfaces.
2. **Autonomous AI Agents:** LangGraph-inspired 5-agent collaborative swarm:
   - `Agent 1: System Architect Agent` — analyzes requirements and retrieves Gang of Four (GoF) structural patterns.
   - `Agent 2: Developer Agent` — synthesizes clean, documented, modular Python classes.
   - `Agent 3: Static AST Analyzer Agent` — parses the code tree using Python's native `ast` module to compute exact cyclomatic complexity and the Maintainability Index (MI).
   - `Agent 4: Defect Quality Reviewer Agent` — applies the trained Random Forest classifier to predict defect probability.
   - `Agent 5: Sandbox Test Engineer Agent` — executes dynamic unit tests and calculates statement test coverage.
3. **Machine Learning (ML / DL):** Scikit-Learn **Random Forest Classifier** trained on the PROMISE Software Defect dataset (`[LOC, Cyclomatic Complexity, Halstead Volume, AST Depth, Parameter Count]`).
4. **Vector RAG:** In-memory architectural pattern repository containing token bucket rate limiters, LRU caches, and OWASP secure coding guidelines.

---

## 📁 2. Deliverables & File Directory

```
c:\MOHIT\dl\2_Akash_Autonomous_SWE_System\
│
├── final_report/
│   ├── FINAL_PROJECT_REPORT.docx     # 12+ page comprehensive academic report (Word)
│   ├── FINAL_PROJECT_REPORT.pdf      # Official submission PDF (with embedded charts)
│   ├── diagram_swe_architecture.png  # Multi-agent SWE platform architecture diagram
│   └── chart_defect_confusion_matrix.png # Random Forest confusion matrix plot
│
├── presentation/
│   └── index.html                    # 16:9 interactive HTML5 presentation deck
│
├── src/
│   └── swe_agents.py                 # Multi-Agent SWE v2.0 Engine with real AST analysis
│
├── models/
│   └── code_defect_classifier.pkl    # Trained Scikit-Learn Random Forest model
│
├── data/
│   └── code_metrics_defects.csv      # Software defect & complexity metrics dataset
│
├── local-demo/
│   └── app.py                        # Interactive terminal execution demo
│
└── HOW_TO_RUN.md                     # This comprehensive execution manual
```

---

## 🚀 3. Step-by-Step Execution Guide

### Option A: Interactive Command-Line Terminal Demo
To run the automated terminal demonstration showcasing multi-agent requirement decomposition, code synthesis, AST analysis, and sandbox execution:

```powershell
# Navigate to the local-demo directory
cd c:\MOHIT\dl\2_Akash_Autonomous_SWE_System\local-demo

# Execute the demonstration
python app.py
```

#### What You Will Observe:
1. **User Requirement Parsing:** Ingests user prompt `"Design and implement a robust sliding-window API Rate Limiter in Python"`.
2. **Architect Agent & RAG:** Identifies module requirements and retrieves Token Bucket / Sliding Window architectural design guidelines.
3. **Developer Agent Synthesis:** Synthesizes clean class `RateLimiter` with auto-cleanup of expired client IP keys.
4. **Static AST Analysis:** Computes physical lines of code (`LOC: 19`), cyclomatic complexity (`CC: 4`), AST tree depth (`10`), and Maintainability Index (`55.5 / 100`).
5. **Machine Learning Defect Audit:** Random Forest classifies the code artifact as `CLEAN (Production Ready)` with defect probability `1.2%`.
6. **Sandbox Unit Testing:** Compiles code into a sandboxed execution dictionary, runs 3 automated unit test assertions, and verifies 100% statement coverage.

---

### Option B: Unified Web Dashboard (Port 8000)
To interact with the live graphical command center:

```powershell
python -m uvicorn server:app --app-dir c:\MOHIT\dl\dashboard --host 0.0.0.0 --port 8000
```
1. Open your browser to **`http://localhost:8000`**.
2. Select **Project 2: Autonomous SWE Platform (Akash Choudhary)**.
3. Choose a pattern preset:
   - `Rate Limiter Middleware`
   - `Thread-Safe LRU Cache`
   - `JWT Token Validator`
4. Click **`🚀 Trigger Multi-Agent SWE Swarm`**.
5. Observe the live code quality radar chart, AST maintainability metrics, defect risk probability, and passing sandbox tests.

---

## 🔌 4. REST API Endpoint Reference

- **Endpoint:** `POST /api/swe/generate`
- **Headers:** `Content-Type: application/json`

### Example Request Body:
```json
{
  "prompt": "Build a high-performance sliding window API Rate Limiter in Python with auto cleanup"
}
```

### Example JSON Response:
```json
{
  "specification": {
    "topic": "RATE_LIMITER",
    "module_name": "rate_limiter_module.py",
    "recommended_pattern": "Token Bucket / Sliding Window Log",
    "security_policy": "Prevent memory exhaustion from untracked client IP key buildup"
  },
  "code_data": {
    "module_name": "rate_limiter_module.py",
    "metrics": {
      "loc": 19,
      "cyclomatic_complexity": 4,
      "halstead_volume": 197.3,
      "ast_depth": 10,
      "maintainability_index": 55.5
    },
    "code": "import time\nfrom collections import deque..."
  },
  "defect_audit": {
    "risk_label": "CLEAN (Production Ready)",
    "defect_probability": 0.012,
    "maintainability_rating": "ACCEPTABLE"
  },
  "test_results": {
    "test_suite_status": "PASS",
    "tests_executed": 3,
    "tests_passed": 3,
    "coverage_pct": 100.0
  }
}
```

---

## 📊 5. Presentation Mode & Exporting Slides

1. Double-click `presentation/index.html` to open in Google Chrome or Microsoft Edge.
2. Use **`Right Arrow`** or **`Space`** to navigate forward, and **`Left Arrow`** to navigate backward.
3. Press **`F`** to toggle full-screen presentation mode.
4. Press **`Ctrl + P`** to export the entire 16:9 presentation directly to PDF.
