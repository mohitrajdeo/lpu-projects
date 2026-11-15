# Local Simulation & Drift Remediation Suite
## Akash Choudhary (12301625) - INT333 Capstone

This folder provides a local Docker container cluster reproducing the Puppet Agent and Nagios Core environment.

### Quick Start
1. Start the cluster:
   ```powershell
   docker compose up -d
   ```
2. Web Endpoints:
   - Puppet Agent 1 Web Server: [http://localhost:8081](http://localhost:8081)
   - Nagios Monitoring Dashboard: [http://localhost:8082](http://localhost:8082) (`nagiosadmin` / `akash12301625`)
3. Execute Chaos & Drift Remediation Test (TC-01 to TC-05):
   ```powershell
   .\test_chaos.ps1
   ```

