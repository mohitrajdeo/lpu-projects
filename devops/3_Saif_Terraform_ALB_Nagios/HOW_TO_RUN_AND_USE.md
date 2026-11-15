# Project Execution & Demonstration Guide
## Saif Siddique (Registration No: 12308813 | Roll No: 44)
### Course: INT333 – DevOps Advance Configuration Management

---

## 🎯 Quick Links
- **Word Final Report:** [`final_report/FINAL_PROJECT_REPORT.docx`](final_report/FINAL_PROJECT_REPORT.docx)
- **PDF Final Report:** [`final_report/FINAL_PROJECT_REPORT.pdf`](final_report/FINAL_PROJECT_REPORT.pdf)
- **Interactive Slides (PPT):** [`presentation/index.html`](presentation/index.html)
- **Multi-Tier Terraform Code:** [`terraform/`](terraform/)
- **Local Simulation:** [`local-simulation/`](local-simulation/)

---

## 🚀 How to Run the Project Locally

1. Open PowerShell in `local-simulation/`:
   ```powershell
   cd local-simulation
   docker compose up -d
   ```
2. Open your browser:
   - **ALB Ingress Endpoint:** [http://localhost:8083](http://localhost:8083) (Distributes traffic across Node 1 and Node 2)
   - **Nagios Console:** [http://localhost:8084](http://localhost:8084) (`nagiosadmin` / `saif12308813`)
3. Execute Load Balancer Chaos Tests:
   ```powershell
   .\test_chaos.ps1
   ```
   *Demonstrates memory exhaustion detection via NRPE, node health drainage by the ALB, and automated recovery.*

