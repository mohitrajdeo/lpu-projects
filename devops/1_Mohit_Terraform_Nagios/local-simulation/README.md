# INT333 Local Simulation & Chaos Testing Suite

This directory contains a complete containerized simulation of the **INT333 Capstone Architecture** for **Mohit Raj Deo (12323329)**.

It allows you to run, test, and capture live screenshots of the entire system on your local machine using Docker without incurring any AWS cloud billing.

---

## Architecture Components

1. **`web-portal` (Node.js/Express):** Interactive Developer Web Portal & Telemetry Dashboard running on port 3000.
2. **`code-runner` (Python 3.12):** Autonomous backend code execution daemon listening on port 9010.
3. **`nginx-proxy` (Nginx):** Public reverse proxy listening on port 80, routing `/` to web portal and `/api/execute` to port 9010.
4. **`nagios-core` (Nagios 4.5):** Continuous observability daemon and Apache web console listening on port 8080.

---

## 🚀 Quick Start (1-Click Run)

### 1. Launch the Cluster
Open PowerShell or Terminal in this folder (`c:\MOHIT\devops\local-simulation`) and run:
```powershell
docker compose up -d
```

### 2. Access the Live Services in Browser
- **Developer Web Portal:** Open [http://localhost](http://localhost)
- **Nagios Monitoring Console:** Open [http://localhost:8080](http://localhost:8080)
  - **Username:** `nagiosadmin`
  - **Password:** `int333devopspassword`

---

## 🧪 Execute Chaos Engineering Test Cases (TC-01 to TC-05)

Run the automated validation script:
- On Windows (PowerShell):
  ```powershell
  .\test_chaos.ps1
  ```
- On Linux / WSL:
  ```bash
  chmod +x test_chaos.sh
  ./test_chaos.sh
  ```

This script automatically executes all 5 test cases from the project synopsis:
- **TC-01:** Verifies clean provisioning and container status.
- **TC-02:** Validates HTTP 200 health check and code execution on port 9010.
- **TC-03:** Terminates Nginx proxy and validates that Nagios flags port 80 connection failure.
- **TC-04:** Kills port 9010 runner and verifies dual-tier isolation (HTTP 80 remains UP while port 9010 reports CRITICAL).
- **TC-05:** Restarts services and confirms automatic recovery back to GREEN OK.

