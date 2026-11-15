# Project Execution & Demonstration Guide
## Mohit Raj Deo (Registration No: 12323329 | Roll No: 62)
### Course: INT333 – DevOps Advance Configuration Management

---

## 🎯 Quick Links
- **Word Final Report:** [`final_report/FINAL_PROJECT_REPORT.docx`](final_report/FINAL_PROJECT_REPORT.docx)
- **PDF Final Report:** [`final_report/FINAL_PROJECT_REPORT.pdf`](final_report/FINAL_PROJECT_REPORT.pdf)
- **Interactive Slides (PPT):** [`presentation/index.html`](presentation/index.html)
- **AWS Terraform Code:** [`terraform/`](terraform/)
- **Local Test Environment:** [`local-simulation/`](local-simulation/)

---

## 🚀 How to Run the Project Locally (1-Click Demo)

1. Open PowerShell in `local-simulation/`:
   ```powershell
   cd local-simulation
   docker compose up -d
   ```
2. Open your web browser:
   - **Developer Web Portal:** [http://localhost](http://localhost)
     - Test writing code in Python, JavaScript, or Bash and clicking **Execute on Daemon**.
     - View the live CPU, memory, and latency metrics in the telemetry sidebar.
   - **Nagios Monitoring Console:** [http://localhost:8080](http://localhost:8080)
     - Username: `nagiosadmin`
     - Password: `int333devopspassword`
     - Click **Services** in the left menu to view the green status of `HTTP_Web_Portal_Uptime` (Port 80) and `TCP_Code_Execution_Engine` (Port 9010).

3. Run the Automated Chaos Validation Suite:
   ```powershell
   .\test_chaos.ps1
   ```
   This automatically runs test cases **TC-01 through TC-05**:
   - **TC-01:** Verifies cluster provisioning.
   - **TC-02:** Sends normal web requests and code execution payloads.
   - **TC-03:** Injects front-end failure (stops Nginx) -> Nagios escalates to CRITICAL on port 80 while port 9010 remains healthy.
   - **TC-04:** Injects backend failure (kills port 9010 runner) -> Nagios triggers CRITICAL on port 9010 while port 80 remains healthy (isolating the failure).
   - **TC-05:** Restarts daemons -> Nagios detects recovery and returns to GREEN OK.

---

## 📽️ How to Present the Slides (PPT)
1. Open `presentation/index.html` in Chrome or Edge.
2. Press **`F`** to enter fullscreen presentation mode.
3. Use **`→`** or **Space** to advance slides, **`←`** to go back.
4. Press **`Ctrl + P`** with *Landscape* orientation to export every slide to PDF.

