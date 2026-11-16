# Lovely Professional University — Capstone Projects Portfolio

**School of Computer Science & Engineering | Lovely Professional University**  
Dual-Course Academic Suite:
* **INT422:** Deep Learning & Applied AI
* **INT333:** DevOps Advance Configuration Management

---

## 🏛️ Executive Summary

This repository contains the complete, production-grade academic engineering portfolio for three Lovely Professional University students across two advanced computing disciplines:

```
                            LPU-PROJECTS REPOSITORY
                                       │
        ┌──────────────────────────────┴──────────────────────────────┐
        ▼                                                             ▼
   INT422 (Deep Learning)                                   INT333 (DevOps)
   Core AI/ML Application Base                              Production Ingress & Observability
   ┌──────────────────────────────────────────┐             ┌──────────────────────────────────────────┐
   │ 1. Mohit Raj Deo (12323329 | Roll 62)    │             │ 1. Mohit Raj Deo (12323329 | Roll 62)    │
   │    AIOps Cloud Intelligence (Port 5001)  │ ──────────► │    Terraform AWS DMZ + Nagios (Port 80)  │
   ├──────────────────────────────────────────┤             ├──────────────────────────────────────────┤
   │ 2. Akash Choudhary (12301625 | Roll 11)  │             │ 2. Akash Choudhary (12301625 | Roll 11)  │
   │    Autonomous SWE Platform (Port 5002)   │ ──────────► │    Puppet Master/Agent + NRPE (Port 8081)│
   ├──────────────────────────────────────────┤             ├──────────────────────────────────────────┤
   │ 3. Saif Siddique (12308813 | Roll 44)    │             │ 3. Saif Siddique (12308813 | Roll 44)    │
   │    SOC Cyber Threat Hunter (Port 5003)   │ ──────────► │    Terraform Multi-Tier ALB (Port 8083)  │
   └──────────────────────────────────────────┘             └──────────────────────────────────────────┘
                                       │
                                       ▼
                   Unified Master Operations Hub (Port 8000)
                   React 18 SPA + Real-Time Neural Mesh Poller
```

---

## 👥 Student Engineering Breakdown

### 1. Mohit Raj Deo (Registration No: `12323329` | Roll No: `62`)
* **INT422 (Deep Learning):** **Autonomous Cloud Operations Intelligence (AIOps v2.0)**
  * **Core Model:** Unsupervised Isolation Forest (100 Trees, 256 sub-sample, 5.0% contamination threshold) + Vectorized RAG over 8 SRE SOP Runbooks.
  * **Front-End:** React 19 + Vite Single-Page Application in **Hard Electric Blue (`#2563eb`)** on **Port 5001**.
  * **Directory:** [`dl/1_Mohit_AIOps_Cloud_Intelligence/`](./dl/1_Mohit_AIOps_Cloud_Intelligence/)
* **INT333 (DevOps):** **Terraform AWS Multi-Tier DMZ & Continuous Nagios Core 4.5 Observability**
  * **Infrastructure:** HashiCorp Terraform AWS VPC manifests deploying Tier 1 public DMZ (Nginx Reverse Proxy on Port 80 routing to AIOps Port 5001) and Tier 2 private isolation (backend code-runner on Port 9010), monitored continuously by Nagios Core 4.5 on Port 8080.
  * **Directory:** [`devops/1_Mohit_Terraform_Nagios/`](./devops/1_Mohit_Terraform_Nagios/)
  * **Chaos Test:** `test_chaos.ps1` -> **5/5 PASS (100%)**

---

### 2. Akash Choudhary (Registration No: `12301625` | Roll No: `11`)
* **INT422 (Deep Learning):** **Autonomous Multi-Agent Software Engineering Platform (v2.0)**
  * **Core Model:** Random Forest Regressor (120 Trees) + Python Abstract Syntax Tree (AST) Concrete Visitor + McCabe Cyclomatic Complexity ($M = E - N + 2P$) + Halstead Software Science + In-Memory Dynamic Sandbox with 100% statement coverage.
  * **Front-End:** React 19 + Vite Single-Page Application in **Hard Violet (`#7c3aed`)** on **Port 5002**.
  * **Directory:** [`dl/2_Akash_Autonomous_SWE_System/`](./dl/2_Akash_Autonomous_SWE_System/)
* **INT333 (DevOps):** **Puppet Master/Agent Desired State Configuration & Nagios NRPE Monitoring**
  * **Infrastructure:** Declarative Puppet manifests (`nginx_server`, `ssh_hardening`, `nrpe_monitoring`) managing the host running the SWE AI platform on Port 8081. Out-of-band drift triggers Nagios NRPE CRITICAL alerts, and Puppet automatically self-heals the node back to GREEN OK.
  * **Directory:** [`devops/2_Akash_Puppet_Nagios/`](./devops/2_Akash_Puppet_Nagios/)
  * **Chaos Test:** `test_chaos.ps1` -> **5/5 PASS (100%)**

---

### 3. Saif Siddique (Registration No: `12308813` | Roll No: `44`)
* **INT422 (Deep Learning):** **Next-Gen Autonomous SOC Threat Hunter & Active Defense (v2.0)**
  * **Core Model:** Deep Multi-Layer Perceptron (MLP) Neural Network:
    $$\text{Input}(5) \longrightarrow \text{Dense}(64, \text{ReLU}) \longrightarrow \text{Dense}(32, \text{ReLU}) \longrightarrow \text{Softmax}(4)$$
    Trained with Adam optimizer ($lr=0.001$), Categorical Cross-Entropy, achieving **99.1% evaluation accuracy** on CIC-IDS2017. Mapped to MITRE ATT&CK (`T1498.001`, `T1046`, `T1190`) with automated synthesis of Linux `iptables`, `nftables`, and AWS WAF rules.
  * **Front-End:** React 19 + Vite Single-Page Application in **Hard Crimson (`#dc2626`)** on **Port 5003**.
  * **Directory:** [`dl/3_Saif_Cyber_Threat_Intelligence/`](./dl/3_Saif_Cyber_Threat_Intelligence/)
* **INT333 (DevOps):** **Terraform Multi-Tier ALB & Multi-AZ Cluster High Availability**
  * **Infrastructure:** HashiCorp Terraform AWS Application Load Balancer balancing traffic across two availability zones (`Node 1 Primary` in AZ-1a and `Node 2 Secondary` in AZ-1b) on Port 8083. Features automated connection draining (15s delay) and Nagios HA monitoring on Port 8084.
  * **Directory:** [`devops/3_Saif_Terraform_ALB_Nagios/`](./devops/3_Saif_Terraform_ALB_Nagios/)
  * **Chaos Test:** `test_chaos.ps1` -> **5/5 PASS (100%)**

---

## 🎨 Design System: Real Hard Solid Colours

All web frontends use a high-contrast, tactile neo-brutalist design system:
* **Solid Jet Black:** `#060911` (base canvas & terminal backgrounds)
* **Deep Slate:** `#0c1220` (surface) and `#111a2e` (cards)
* **Hard Solid Border:** `2px solid #2e3d5b` (structural containers)
* **Hard Electric Blue:** `#2563eb` (Mohit AIOps theme)
* **Hard Crimson:** `#dc2626` (Saif SecOps theme)
* **Hard Emerald:** `#059669` (health / normal status)
* **Hard Violet:** `#7c3aed` (Akash SWE theme)
* **Tactile 3D Buttons:** `box-shadow: 0 4px 0 #000;` (depresses 4px on press)

---

## 🚀 Running the Microservices

### Prerequisites
* Python 3.10+ (with `fastapi`, `uvicorn`, `scikit-learn`, `numpy`, `joblib`, `pydantic`)
* Node.js 18+ (for building React UI; production builds are pre-compiled into `dist/`)

### Launch Commands
```powershell
# 1. Master Command Center (Port 8000)
powershell -ExecutionPolicy Bypass -File c:\MOHIT\dl\dashboard\run_dashboard.ps1

# 2. Mohit AIOps Cloud Intelligence (Port 5001)
powershell -ExecutionPolicy Bypass -File c:\MOHIT\dl\1_Mohit_AIOps_Cloud_Intelligence\run_aiops.ps1

# 3. Akash Autonomous SWE Platform (Port 5002)
powershell -ExecutionPolicy Bypass -File c:\MOHIT\dl\2_Akash_Autonomous_SWE_System\run_swe.ps1

# 4. Saif SOC Cyber Threat Hunter (Port 5003)
powershell -ExecutionPolicy Bypass -File c:\MOHIT\dl\3_Saif_Cyber_Threat_Intelligence\run_secops.ps1
```

---

## 📦 Submission ZIP Packages & Official Documentation

All 6 project packages are built with **0% npm bloat** and located in [`6_PROJECT_ZIPS/`](./6_PROJECT_ZIPS/):

| # | Student | Course | Package Name | Files | Size |
| :-: | :--- | :--- | :--- | :-: | :-: |
| 1 | Mohit Raj Deo (12323329) | INT422 (DL) | `1_Mohit_12323329_INT422_DL_AIOps_Project.zip` | 24 | 1.93 MB |
| 2 | Mohit Raj Deo (12323329) | INT333 (DevOps) | `2_Mohit_12323329_INT333_DevOps_Terraform_Nagios.zip` | 36 | 1.37 MB |
| 3 | Akash Choudhary (12301625) | INT422 (DL) | `3_Akash_12301625_INT422_DL_SWE_Project.zip` | 24 | 1.53 MB |
| 4 | Akash Choudhary (12301625) | INT333 (DevOps) | `4_Akash_12301625_INT333_DevOps_Puppet_Nagios.zip` | 24 | 1.37 MB |
| 5 | Saif Siddique (12308813) | INT422 (DL) | `5_Saif_12308813_INT422_DL_SecOps_Project.zip` | 24 | 1.30 MB |
| 6 | Saif Siddique (12308813) | INT333 (DevOps) | `6_Saif_12308813_INT333_DevOps_Terraform_ALB.zip` | 26 | 1.25 MB |

### Reports & Synopses
* All final reports are provided in 3 formats: Word `.docx` (14–16 pages), Official `.pdf`, and Print-Ready `.html`.
* Synopses are included in each student's DevOps folder and mirrored on the Master Operations Center.

