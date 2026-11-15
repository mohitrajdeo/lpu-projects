# INT333: DevOps Advance Configuration Management
## Capstone Project Implementation & Final Deliverables

**Institution:** Department of Computer Science & Engineering, Lovely Professional University  
**Student Name:** Mohit Raj Deo  
**Registration No:** 12323329  
**Roll No:** 62 | **Section:** RK2O2315  
**Course Code:** INT333 – DevOps Advance Configuration Management  
**Project Title:** *Automated Cloud Infrastructure Provisioning with Terraform and Continuous Monitoring with Nagios Core for Website and Code Execution Services*  
**Faculty Guide:** Ms. Manpreet Kaur, Assistant Professor  
**Academic Session:** 2026–2027  

---

## 📂 Project Directory Structure

```
c:\MOHIT\devops\
├── final_report/                         # Comprehensive Academic Final Project Report
│   ├── FINAL_PROJECT_REPORT.md           # Full report in clean Markdown
│   └── FINAL_PROJECT_REPORT.html         # Publication-grade printable report (1-click PDF export)
│
├── presentation/                         # Interactive Presentation Deck (PPT)
│   ├── index.html                        # Modern HTML5 presentation (16:9 slides, dark glassmorphism)
│   └── presentation_guide.md             # Guide for presenting & exporting to PDF/PPTX
│
├── terraform/                            # Production AWS Terraform Code (Unit IV)
│   ├── versions.tf                       # Provider requirements (AWS >= 5.0)
│   ├── variables.tf                      # Topology parameters (VPC, CIDRs, AMI)
│   ├── vpc.tf                            # AWS VPC 10.100.0.0/16, Dual-AZ Subnets, IGW, Route Tables
│   ├── security_groups.tf                # Least-privilege firewalls (isolates Port 9010)
│   ├── brain.tf                          # Web Portal & Code Runner EC2 instance + Elastic IP
│   ├── nagios.tf                         # Nagios Observability Server EC2 instance + Elastic IP
│   ├── outputs.tf                        # Public URLs and endpoints
│   ├── terraform.tfvars.example          # Sample variables file
│   └── scripts/
│       ├── web_portal_userdata.sh        # Zero-touch cloud-init for Web & Runner
│       └── nagios_userdata.sh            # Zero-touch cloud-init for Nagios & Plugins
│
├── app/                                  # Application Layer & Services
│   ├── code-runner/                      # Autonomous Backend Code Runner (Port 9010)
│   │   ├── runner.py                     # Python 3 socket server executing sandboxed code
│   │   └── Dockerfile                    # Container definition
│   └── portal/                           # Developer Web Portal UI (Port 3000)
│       ├── server.js                     # Express server & API reverse proxy
│       ├── package.json
│       └── public/
│           └── index.html                # Interactive Playground & Live Telemetry UI
│
├── nagios/                               # Nagios Continuous Observability (Unit III)
│   ├── nagios.cfg                        # Master Nagios configuration
│   └── conf.d/
│       ├── hosts.cfg                     # Monitored host definitions
│       ├── services.cfg                  # Tier 1 (HTTP:80), Tier 2 (TCP:9010), Tier 3 (Ping)
│       ├── commands.cfg                  # Active plugin command definitions
│       └── contacts.cfg                  # Alert notification contacts
│
├── local-simulation/                     # Local Hybrid Docker Environment (Zero-Cost Testing)
│   ├── docker-compose.yml                # Multi-container orchestration (Portal + Runner + Nginx + Nagios)
│   ├── nginx.conf                        # Nginx reverse proxy configuration
│   ├── nagios-local.cfg                  # Nagios probe definitions for local cluster
│   ├── test_chaos.ps1                    # Automated PowerShell Chaos Test Runner (TC-01 to TC-05)
│   ├── test_chaos.sh                     # Automated Bash Chaos Test Runner
│   └── README.md                         # Instructions for local demo
│
└── [Original Synopses PDFs]
    ├── Mohit_Raj_Deo_Project_Synopsis.pdf
    ├── Akash_12301625_Puppet_Nagios_Synopsis.pdf
    └── Saif_12308813_Terraform_Nagios_Synopsis.pdf
```

---

## 🎯 Quick Navigation & Deliverables

| Deliverable | File Path | Description |
| :--- | :--- | :--- |
| **Academic Final Report** | [`final_report/FINAL_PROJECT_REPORT.html`](final_report/FINAL_PROJECT_REPORT.html) | Fully styled academic report with cover page, certificate, declaration, architecture, code, and test logs. Has a 1-click **Print / Save as PDF** button. |
| **Presentation Deck (PPT)** | [`presentation/index.html`](presentation/index.html) | 12-slide modern HTML5 presentation. Navigate with Arrow keys / Space, press `F` for fullscreen, press `Ctrl+P` to export to PDF. |
| **AWS Terraform Code** | [`terraform/`](terraform/) | Complete declarative HashiCorp HCL templates for provisioning AWS VPC, subnets, EC2 nodes, and security boundaries. |
| **Developer Web Portal** | [`app/portal/public/index.html`](app/portal/public/index.html) | Full-stack interactive code editor, real-time telemetry dashboard, and socket status gauges. |
| **Port 9010 Code Runner** | [`app/code-runner/runner.py`](app/code-runner/runner.py) | Lightweight sandboxed execution daemon listening on port 9010. |
| **Nagios Observability** | [`nagios/conf.d/services.cfg`](nagios/conf.d/services.cfg) | Dual-tier active service probes (`check_http`, `check_tcp:9010`, `check_ping`). |
| **Chaos Test Suite** | [`local-simulation/test_chaos.ps1`](local-simulation/test_chaos.ps1) | Automated verification script executing test cases **TC-01 through TC-05**. |

---

## 🧪 Chaos Engineering & Test Results (TC-01 to TC-05)

All 5 test cases from the project synopsis have been verified:

1. **TC-01 (Provisioning):** Environment provisions deterministically in &lt; 4 minutes with 0 errors.
2. **TC-02 (Normal Traffic):** Web portal loads successfully; HTTP 80 and TCP 9010 report `OK (Green)`.
3. **TC-03 (Front-End Failure):** Stopping Nginx causes `check_http` to enter `SOFT CRITICAL` &rarr; `HARD CRITICAL`, while backend port 9010 remains green (isolating the failure).
4. **TC-04 (Backend Failure):** Stopping port 9010 daemon triggers immediate CRITICAL alert on `check_tcp:9010`, while web portal HTTP check remains green.
5. **TC-05 (Auto-Recovery):** Restarting stopped daemons is automatically detected by Nagios in the next check cycle, restoring services to `HARD OK (Green)`.

