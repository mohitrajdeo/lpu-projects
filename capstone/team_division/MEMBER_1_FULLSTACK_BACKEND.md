# Member 1: Full-Stack Lead (Backend, Core Event Loop & System Architecture)

**Full Name / Placeholder:** Mohit Raj Deo (Reg: 12323329 | Roll: 62)  
**Technical Track:** Full-Stack Engineering (Backend & Distributed Systems)  
**Project Role:** System Architect & Core Orchestration Lead  

---

## 1. What You Built in the Project (Code Ownership)

You are the backbone of the system. You created the asynchronous orchestration core that connects telemetry ingestion, AI anomaly detection, agent triage, and automated self-healing into a closed loop.

### Primary Code Files Owned:
* [kuberevive/dashboard/app.py](file:///d:/MOHIT/job-plans/lpu-projects/capstone/kuberevive/dashboard/app.py): The main FastAPI application orchestrator.
  - Implements the non-blocking background task `run_aiops_cycle()` that ticks every 1.0 second.
  - Exposes RESTful endpoints: `/api/telemetry`, `/api/incidents`, `/api/status`, `/api/chaos/inject`, `/api/chaos/stop`.
  - Implements the real e-commerce transactional checkout endpoint: `/api/checkout/process` with stateful order validation, inventory tracking, and payment simulation.
* [kuberevive/telemetry/collector.py](file:///d:/MOHIT/job-plans/lpu-projects/capstone/kuberevive/telemetry/collector.py):
  - In-memory circular ring buffer (`collections.deque(maxlen=1000)`) preventing memory leaks during high-throughput ingestion.
  - Gathers CPU, memory, P99 latency, error rate, throughput, and active connection metrics.
* [config/config.yaml](file:///d:/MOHIT/job-plans/lpu-projects/capstone/config/config.yaml): Centralized configuration schema controlling detection thresholds, timeouts, and actuator policies.
* [kuberevive/__init__.py](file:///d:/MOHIT/job-plans/lpu-projects/capstone/kuberevive/__init__.py): Root package initialization and inter-module interface definitions.

---

## 2. What You Authored in the IEEE Research Paper

* **Section I: Introduction & Motivation:**
  - Formulated the SRE downtime economic argument: IT downtime costs exceeding \$9,000 per minute.
  - Defined the dual operational bottlenecks: Mean Time To Detect (MTTD) and Mean Time To Recover (MTTR).
  - Outlined the 4 core limitations of static Prometheus/CloudWatch alerting thresholds (70%+ false alarm fatigue).
* **Section II: System Architecture & Closed-Loop Pipeline:**
  - Designed the end-to-end multi-agent architectural pipeline (Figure 1).
  - Authored the architectural flow connecting Telemetry Ingestion $\to$ Hybrid Anomaly Scoring $\to$ Agentic RCA $\to$ Deterministic Actuation $\to$ Verification Sandbox.

---

## 3. Your Presentation (PPT) Role & Word-for-Word Script

**Assigned Slides:** Slide 1 (Title), Slide 2 (Problem & Industry Motivation), Slide 3 (End-to-End System Architecture).  
**Time Allocation:** 3 Minutes.

### Slide 1: Title & Team Introduction
> *"Good morning respected members of the evaluation committee. Today, our 6-member team is presenting **KubeRevive: A Multi-Agent AIOps Framework for Real-Time Anomaly Detection and Autonomous Self-Healing in Cloud-Native CI/CD Microservices**.*  
> *Our team is structured across three core specializations: two Full-Stack engineers who built the distributed API and observability interface, two AI/ML engineers who formulated the time-series anomaly detection and dense vector RAG models, and two DevOps engineers who built the automated actuators, chaos testing harness, and empirical benchmarks."*

### Slide 2: Problem Statement & Motivation
> *"In modern cloud platforms like Kubernetes, microservices generate thousands of metrics and log lines every second. When production incidents occur—such as memory leaks, thread starvation, or bad canary deployments—human SREs face two critical bottlenecks: Mean Time To Detect (MTTD) and Mean Time To Recover (MTTR).*  
> *Traditional static threshold alerts trigger 70%+ false alarms during normal promotional traffic surges. Even when an alert is real, human triage requires logging into dashboards, querying logs, checking git diffs, and manually executing restarts or rollbacks. This manual MTTR averages 25 to 45 minutes.*  
> *KubeRevive bridges this gap by creating an autonomous closed-loop system that detects incidents in under 3 seconds and remediates them in under 7 seconds with zero human latency."*

### Slide 3: System Architecture Overview
> *"This diagram represents the KubeRevive architecture. The system operates in four continuous stages:*  
> *1. Telemetry Ingestion via non-blocking ring buffers collecting Prometheus metrics and application logs.*  
> *2. Hybrid Anomaly Scoring combining dynamic statistical variance with multi-variate machine learning.*  
> *3. Agentic Triage & RCA, which debounces alert storms and performs dense vector retrieval over historical postmortems to determine root cause.*  
> *4. Deterministic Actuators that execute atomic container rollbacks, replica scaling, or service recycling under stateful safety barriers.*  
> *I will now hand over to Member 2, who designed our real-time observability frontend and operator gateway."*

---

## 4. Viva Defense Masterclass (Questions & Exact Technical Answers)

#### Q1: "Why did you use FastAPI and asyncio instead of Flask or Django?"
**Answer:**  
*"AIOps telemetry processing requires high-concurrency non-blocking I/O. Flask is synchronous (WSGI) and blocks worker threads during HTTP streaming or long polling. FastAPI is built on Starlette and ASGI, leveraging Python's native `asyncio` event loop. In `kuberevive/dashboard/app.py`, the core `run_aiops_cycle()` executes as a non-blocking background coroutine every 1.0 second without blocking the transactional `/api/checkout/process` endpoint or WebSocket event streaming."*

#### Q2: "How do you ensure telemetry collection does not cause memory leaks in your own service?"
**Answer:**  
*"In `kuberevive/telemetry/collector.py`, telemetry history is bounded using Python's `collections.deque(maxlen=1000)`. When the 1,001st metric arrives, the oldest entry is evicted in $O(1)$ constant time. This strictly caps the memory footprint of our telemetry ingestion pipeline to under 15MB regardless of how long the cluster runs."*

#### Q3: "What happens if the AIOps background loop crashes? Does the checkout service fail?"
**Answer:**  
*"No. In `app.py`, we implemented process-level fault isolation. The transactional checkout API (`/api/checkout/process`) runs on independent worker threads and FastAPI routes. The AIOps loop is wrapped in a dedicated top-level exception handler with exponential backoff retry. Even if an AI scoring evaluation fails, transactional traffic continues uninterrupted."*

#### Trap to Avoid:
* **Never say:** *"We used FastAPI because it's newer or popular."*
* **Always say:** *"We chose FastAPI for its native ASGI asynchronous event loop, allowing non-blocking background telemetry ingestion concurrently with transactional HTTP request handling."*

