# KubeRevive: 6-Member Work Breakdown Structure (2 Full-Stack, 2 AI/ML, 2 DevOps)

This document establishes the official academic and engineering work division for the 6-member team. To meet university and IEEE evaluation standards, the work is strictly partitioned into **3 specialized two-person tracks**:
1. **Full-Stack Engineering Track (2 Members):** Distributed API Orchestrator, Core Concurrency, Real-Time Observability UI & Client State Gateway.
2. **AI & Machine Learning Track (2 Members):** Dynamic Time-Series Anomaly Detection (Z-Score/EWMA, Isolation Forest) & Dense Vector RAG (Sentence-Transformers) with Semantic Log NLP.
3. **DevOps & SRE Track (2 Members):** Autonomous Remediation Actuators, Safety Guardrails, Chaos Engineering, Physical Hardware Stressing & Quantitative Benchmarks.

---

## Quick Navigation: Individual Member Dossiers

| Member | Track & Specialization | Primary Code Modules | Paper Sections | Individual Guide |
| :--- | :--- | :--- | :--- | :--- |
| **Mohit Sharma** | **Full-Stack 1:** Lead Backend Architect & Event Loop Orchestrator | `dashboard/app.py`, `telemetry/collector.py`, `config/config.yaml` | Abstract, Section I (Intro), Section II (Arch Overview) | [MEMBER_1_FULLSTACK_BACKEND.md](file:///c:/MOHIT/capstone/team_division/MEMBER_1_FULLSTACK_BACKEND.md) |
| **Ananya Iyer** | **Full-Stack 2:** Frontend Observability UI & Operator Gateway | `dashboard/static/index.html`, `dashboard/static/app.js` | Section II-B (Operator UI), Figure 1 Dataflow | [MEMBER_2_FULLSTACK_FRONTEND.md](file:///c:/MOHIT/capstone/team_division/MEMBER_2_FULLSTACK_FRONTEND.md) |
| **Aarav Gupta** | **AI/ML 1:** Time-Series Modeling & Isolation Forest Ensemble | `anomaly_detection/metrics_detector.py`, `tests/test_anomaly_detection.py` | Section III-A (Hybrid Detection), Equations (1)-(4), Figure 2 | [MEMBER_3_AIML_METRICS.md](file:///c:/MOHIT/capstone/team_division/MEMBER_3_AIML_METRICS.md) |
| **Rohan Verma** | **AI/ML 2:** GenAI, Dense Vector RAG & Semantic Log NLP | `agents/rca_agent.py`, `anomaly_detection/log_anomaly_parser.py`, `data/incident_knowledge_base.json` | Section III-B (Log Parser), Section III-C (Agentic RCA & RAG) | [MEMBER_4_AIML_RAG_NLP.md](file:///c:/MOHIT/capstone/team_division/MEMBER_4_AIML_RAG_NLP.md) |
| **Priya Patel** | **DevOps 1:** Autonomous Actuators, Safety Guardrails & Docker | `actuators/remediation_engine.py`, `actuators/verification_sandbox.py`, `telemetry/prometheus_exporter.py` | Section III-D (Actuators & Sandbox), Table II (Runbooks) | [MEMBER_5_DEVOPS_ACTUATORS.md](file:///c:/MOHIT/capstone/team_division/MEMBER_5_DEVOPS_ACTUATORS.md) |
| **Karthik Nair** | **DevOps 2:** Chaos Engineering, Hardware Benchmarking & CI/CD | `simulation/chaos_injector.py`, `simulation/physical_stressor.py`, `benchmark/` scripts, CI/CD | Section IV (Chaos Setup), Section V (Evaluation), Section VI (Threats) | [MEMBER_6_DEVOPS_CHAOS_BENCHMARKS.md](file:///c:/MOHIT/capstone/team_division/MEMBER_6_DEVOPS_CHAOS_BENCHMARKS.md) |

---

## Detailed Track Breakdown

### Track 1: Full-Stack Engineering (Backend & Frontend)

#### Member 1: Mohit Sharma (Lead Backend Architect)
* **Code Responsibility:** Asynchronous orchestration loop in `app.py`, ring-buffer memory bounding in `collector.py`, real `/api/checkout/process` transactional endpoint.
* **Paper Contribution:** Introduction, industry downtime economics (\$9,000/min), MTTD/MTTR bottleneck definitions, high-level multi-agent architectural pipeline.
* **PPT Presentation:** Slides 1, 2, and 3 (Title, Problem Statement, System Architecture).
* **Viva Defense:** Async event loop concurrency, zero memory leakage via circular deques, process-level isolation between AIOps and business logic.

#### Member 2: Ananya Iyer (Frontend Observability & Operator Gateway)
* **Code Responsibility:** High-throughput SPA command center in `index.html` and `app.js`, live metric streaming, chaos trigger buttons, incident status animations.
* **Paper Contribution:** Human-in-the-loop auditability layer, incident state machine documentation (`DETECTED` $\to$ `RESOLVED`), Figure 1 dataflow walkthrough.
* **PPT Presentation:** Slide 12 (Operator Dashboard) and leading the interactive live demo.
* **Viva Defense:** Sub-5ms client rendering via `requestAnimationFrame`, zero-dependency modern ES6 architecture, regulatory compliance (SOC2/ISO 27001) auditability.

---

### Track 2: Artificial Intelligence & Machine Learning

#### Member 3: Aarav Gupta (Time-Series & Isolation Forest Lead)
* **Code Responsibility:** Rolling Z-score with EWMA, multi-variate Isolation Forest (100 isolation trees), hybrid score arbitration in `metrics_detector.py`.
* **Paper Contribution:** Algorithmic formulation of sliding window mean and sample variance, Isolation Forest path length normalization with Euler-Mascheroni constant ($c(n)$ in Eq. 4), Table I ablation analysis.
* **PPT Presentation:** Slide 4 (Hybrid Anomaly Detection Engine).
* **Viva Defense:** Why Isolation Forest ($O(T \cdot \psi \log \psi)$ CPU inference) outperforms GPU-heavy LSTMs, BST average search depth theory, epsilon variance floors during warm-up.

#### Member 4: Rohan Verma (GenAI, Dense RAG & Log NLP Lead)
* **Code Responsibility:** Dense vector RAG pipeline using `all-MiniLM-L6-v2` embeddings in `rca_agent.py`, regex parameter masking in `log_anomaly_parser.py`, 15 real SRE incident postmortems in `incident_knowledge_base.json`.
* **Paper Contribution:** Semantic log template mining formulation, cosine similarity vector retrieval equation, proof of zero-hallucination guarantee over Microsoft RCACopilot.
* **PPT Presentation:** Slide 5 (Agentic RCA Engine & Dense Vector RAG).
* **Viva Defense:** Dense latent space vs keyword Jaccard overlap, why RAG is superior to LLM fine-tuning for cloud postmortems, sliding debounce window suppressing alert storms.

---

### Track 3: DevOps & Site Reliability Engineering (SRE)

#### Member 5: Priya Patel (Infrastructure Actuators & Docker Lead)
* **Code Responsibility:** 4 primary self-healing actuators (rolling restart, canary rollback, HPA scaling, circuit breaking) in `remediation_engine.py`, 15-second stateful cooldown barrier, post-remediation verification in `verification_sandbox.py`, Prometheus exporter.
* **Paper Contribution:** Policy-constrained actuation boundaries, mathematical formulation of cooldown enforcement, Table II remediation runbook catalog.
* **PPT Presentation:** Slide 6 (Autonomous Remediation & Infrastructure Actuation).
* **Viva Defense:** Preventing actuator flapping/thrashing, blue-green canary rollback with zero transaction loss, Prometheus OpenMetrics standards compliance.

#### Member 6: Karthik Nair (Chaos Engineering, Hardware Benchmarks & Research Lead)
* **Code Responsibility:** Chaos injection harness in `chaos_injector.py`, physical OS memory/CPU stressor in `physical_stressor.py` and `live_stress_tester.py`, 40-trial benchmarking harness in `run_benchmark.py`, real AWS NAB evaluation in `run_real_world_benchmark.py`, CI/CD pipeline in `ci.yml`.
* **Paper Contribution:** Section IV (Chaos Setup), Section V (Empirical Results: 95.98% MTTD drop, 97.91% MTTR drop), Section VI (Threats to Validity), Section VII (Conclusion & eBPF future work).
* **PPT Presentation:** Slides 7 & 8 (Chaos & Physical Testing), Slides 9, 10, 11 (Results & NAB AWS Evaluation), Slide 13 (Conclusion).
* **Viva Defense:** Physical `psutil` memory allocation vs software simulation, 40-trial statistical significance under Central Limit Theorem, NAB window-level detection vs point-level scoring.

---

## Full Presentation Agenda & Speaker Flow

| Slide Number | Slide Title | Speaker | Track | Target Duration |
| :---: | :--- | :--- | :--- | :---: |
| **Slide 1** | Project Title & Research Overview | **Mohit Sharma** | Full-Stack | 1.0 min |
| **Slide 2** | Problem Statement & Industry Downtime Bottlenecks | **Mohit Sharma** | Full-Stack | 1.0 min |
| **Slide 3** | End-to-End System Architecture Overview | **Mohit Sharma** | Full-Stack | 1.0 min |
| **Slide 4** | Anomaly Detection: Dynamic Z-Score & Isolation Forest | **Aarav Gupta** | AI/ML | 3.0 min |
| **Slide 5** | Agentic RCA Engine: Dense Vector RAG & Log NLP | **Rohan Verma** | AI/ML | 3.0 min |
| **Slide 6** | Autonomous Remediation Actuators & Safety Cooldown | **Priya Patel** | DevOps | 2.5 min |
| **Slide 7** | Chaos Engineering Testbed & Failure Injection Archetypes | **Karthik Nair** | DevOps | 1.5 min |
| **Slide 8** | Real Physical Hardware Stressor (Physical OS Telemetry) | **Karthik Nair** | DevOps | 1.5 min |
| **Slide 9** | Empirical Results: 40-Trial MTTD & MTTR Benchmark | **Karthik Nair** | DevOps | 1.5 min |
| **Slide 10** | Real-World Validation: Numenta NAB & Loghub Evaluation | **Karthik Nair** | DevOps | 1.5 min |
| **Slide 11** | Ablation Study & Architectural Component Contribution | **Aarav Gupta / Karthik Nair** | AI/ML & DevOps | 1.0 min |
| **Slide 12** | Live Operational Dashboard & Interactive Demo | **Ananya Iyer** | Full-Stack | 2.5 min |
| **Slide 13** | Threats to Validity, Conclusion & Future eBPF Directions | **Karthik Nair** | DevOps | 1.5 min |
| **Q&A** | Committee Examination & Viva Defense | **All 6 Members** | Joint | 5-10 min |
