# Project Execution & Demonstration Guide
## Akash Choudhary (Registration No: 12301625 | Roll No: 11)
### Course: INT333 – DevOps Advance Configuration Management

---

## 🎯 Quick Links
- **Word Final Report:** [`final_report/FINAL_PROJECT_REPORT.docx`](final_report/FINAL_PROJECT_REPORT.docx)
- **PDF Final Report:** [`final_report/FINAL_PROJECT_REPORT.pdf`](final_report/FINAL_PROJECT_REPORT.pdf)
- **Interactive Slides (PPT):** [`presentation/index.html`](presentation/index.html)
- **Puppet Manifests & Modules:** [`puppet/`](puppet/)
- **Local Simulation:** [`local-simulation/`](local-simulation/)

---

## 🚀 How to Run the Project Locally

1. Open PowerShell in `local-simulation/`:
   ```powershell
   cd local-simulation
   docker compose up -d
   ```
2. Open your browser:
   - **Agent 1 Web Server:** [http://localhost:8081](http://localhost:8081)
   - **Nagios Console:** [http://localhost:8082](http://localhost:8082) (`nagiosadmin` / `akash12301625`)
3. Execute Drift Remediation & Chaos Tests:
   ```powershell
   .\test_chaos.ps1
   ```
   *Demonstrates manual sabotage of Nginx, Nagios alert detection, and automatic Puppet catalog drift remediation.*

