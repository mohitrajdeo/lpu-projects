# Local Simulation & ALB Chaos Testing Suite
## Saif Siddique (12308813) - INT333 Capstone

This folder provides a local Docker container cluster simulating the AWS Application Load Balancer, backend application nodes, and Nagios Core.

### Quick Start
1. Start the cluster:
   ```powershell
   docker compose up -d
   ```
2. Web Endpoints:
   - ALB Ingress Endpoint: [http://localhost:8083](http://localhost:8083) (Distributes traffic between Node 1 and Node 2)
   - Nagios Monitoring Dashboard: [http://localhost:8084](http://localhost:8084) (`nagiosadmin` / `saif12308813`)
3. Execute Load Balancer Chaos Tests (TC-01 to TC-05):
   ```powershell
   .\test_chaos.ps1
   ```

