# DEPARTMENT OF COMPUTER SCIENCE AND ENGINEERING
## School of Computer Science and Engineering
### Lovely Professional University, Punjab

---

# FINAL PROJECT REPORT
### Course Code: INT333 – DevOps Advance Configuration Management

## **Centralized Server Configuration Management with Puppet and Continuous Service Monitoring using Nagios Core**

---

### **Submitted By:**
- **Name:** Akash Choudhary
- **Registration No:** 12301625
- **Roll No:** 11
- **Program:** B.Tech Computer Science and Engineering (DevOps Specialization)

### **Under the Guidance of:**
- **Supervisor:** Ms. Manpreet Kaur (Assistant Professor)
- **Department:** School of Computer Science and Engineering
- **Institution:** Lovely Professional University, Phagwara, Punjab, India
- **Academic Session:** 2024–2025 / 2026–2027

---

<div style="page-break-after: always;"></div>

## CERTIFICATE

This is to certify that the project entitled **"Centralized Server Configuration Management with Puppet and Continuous Service Monitoring using Nagios Core"** submitted by **Akash Choudhary (Registration No: 12301625, Roll No: 11)** in partial fulfillment of the requirements for the award of the degree of **Bachelor of Technology in Computer Science and Engineering (DevOps)** for the course **INT333: DevOps Advance Configuration Management** at **Lovely Professional University**, Phagwara, is an authentic record of the candidate's own work carried out under my supervision and guidance.

The matter presented in this report has not been submitted in part or in full to any other University or Institute for the award of any degree or diploma.

<br><br>
_________________________________  
**Ms. Manpreet Kaur**  
Assistant Professor (Project Guide)  
School of Computer Science and Engineering  
Lovely Professional University, Punjab  

---

<div style="page-break-after: always;"></div>

## CANDIDATE DECLARATION

I hereby declare that the work presented in this project report entitled **"Centralized Server Configuration Management with Puppet and Continuous Service Monitoring using Nagios Core"** submitted to the Department of Computer Science and Engineering, Lovely Professional University, is an authentic record of my original work, design, implementation, and experimental validation under the supervision of **Ms. Manpreet Kaur**, Assistant Professor.

<br><br>
_________________________________  
**Akash Choudhary**  
Registration No: 12301625 | Roll No: 11  
School of Computer Science and Engineering  
Lovely Professional University  

---

<div style="page-break-after: always;"></div>

## ABSTRACT

In enterprise IT and modern cloud operations, managing heterogeneous server clusters through ad-hoc manual SSH interventions leads to severe operational degradation, compliance violations, and unpredictable outages across production fleets. Over time, servers deviate from their approved baseline configurations—a phenomenon known as **configuration drift** that creates unmaintainable "snowflake" servers. Furthermore, configuration management tools alone cannot provide real-time incident awareness; while tools like Puppet enforce desired states during periodic catalog runs (e.g., every 30 minutes), outages occurring between runs remain undetected without active daemon monitoring.

This project delivers an integrated, enterprise-grade systems management and observability architecture combining **Centralized Configuration Management with Puppet** (Course Unit II) and **Continuous Service Monitoring with Nagios Core** (Course Unit III). 

The architecture deploys an authenticated **Puppet Master-Agent** topology where the Puppet Server coordinates managed agent nodes using mutual TLS certificate signing over port `8140`. Custom reusable Puppet modules—including `nginx_server`, `ssh_hardening`, and `nrpe_monitoring`—are authored using declarative Puppet DSL and ERB templates. Concurrently, a dedicated **Nagios Core 4.5** server actively monitors control plane reachability (port 8140), web ingress (port 80 via `check_http`), and deep host OS health (CPU load, memory consumption, root disk space, process existence) via the **Nagios Remote Plugin Executor (NRPE)** on port `5666`.

A 5-stage chaos engineering validation suite (`TC-01` through `TC-05`) demonstrates that intentional sabotages—such as manual service termination (`systemctl stop nginx`) and configuration file tampering—are immediately detected and flagged as **CRITICAL** by Nagios Core within seconds, and then automatically corrected and returned to compliance upon Puppet agent catalog execution (`puppet agent -t`). The project demonstrates a closed-loop, resilient DevOps framework that guarantees zero configuration drift and high service availability.

---

<div style="page-break-after: always;"></div>

# CHAPTER 1: INTRODUCTION & OBJECTIVES

## 1.1 Background
Enterprises rely on hundreds of servers to host business-critical services. Manual administration results in inconsistent patch levels, broken dependencies, and security oversights. 
- **Unit II: Configuration Management with Puppet** provides declarative automation to define system state as code.
- **Unit III: Continuous Monitoring with Nagios Core** provides second-by-second visibility into infrastructure and application health.

## 1.2 Problem Statement
- **The "Snowflake" Server Dilemma:** When configurations are applied manually, each server becomes unique. If an engineer disables a firewall rule or terminates a web daemon locally, traditional environments remain broken until noticed.
- **Delayed Drift Remediation:** Puppet audits system state periodically. However, if a web daemon crashes 1 minute after an agent catalog run, waiting 29 minutes for the next catalog run causes unacceptable downtime. Real-time alerting via Nagios Core bridges this gap.

## 1.3 Key Objectives
1. Implement an authenticated Puppet Master-Agent topology with mutual TLS encryption on port `8140`.
2. Author modular declarative manifests (`nginx_server`, `ssh_hardening`, `nrpe_monitoring`).
3. Deploy an independent Nagios Core server configured with an Apache CGI dashboard.
4. Configure NRPE on managed agent nodes to expose CPU, memory, disk, and process telemetry to Nagios.
5. Execute sabotage and chaos tests (`TC-01` to `TC-05`) proving closed-loop drift remediation and alert transitions.

---

<div style="page-break-after: always;"></div>

# CHAPTER 2: SYSTEM ARCHITECTURE & MASTER-AGENT TOPOLOGY

```
ENTERPRISE MANAGEMENT NETWORK
+-----------------------------------------------------------------------------+
| +---------------------------------+ +---------------------------------+ |
| | Puppet Master Server            | | Nagios Monitoring Server        | |
| | (Ubuntu 24.04 Server)           | | (Ubuntu 24.04 Server)           | |
| |                                 | |                                 | |
| | * Puppet Server Daemon (:8140)  | | * Nagios Core 4.5.2 Engine      | |
| | * SSL Certificate Authority     | | * Apache Web Dashboard (CGI)    | |
| | * Module Registry (site.pp)     | | * check_http / check_tcp        | |
| | * Catalog Compilation Engine    | | * check_nrpe Remote Probes      | |
| +----------------+----------------+ +----------------+----------------+ |
|                  |                                   |                  |
|                  | (SSL Port 8140 Catalog)           | (NRPE Port 5666) |
| +----------------v-----------------------------------v----------------+ |
| | Managed Server Fleet (Agent Nodes)                                  | |
| |                                                                     | |
| | +---------------------------+         +---------------------------+ | |
| | | Web Server Node (Agent 1) |         | App Service Node (Agent 2)| | |
| | | * Puppet Agent Client     |         | * Puppet Agent Client     | | |
| | | * Nginx Service (Port 80) |         | * Backend Daemon (Port 80)| | |
| | | * SSH Hardening Baseline  |         | * SSH Hardening Baseline  | | |
| | | * NRPE Daemon (Port 5666) |         | * NRPE Daemon (Port 5666) | | |
| | +---------------------------+         +---------------------------+ | |
| +---------------------------------------------------------------------+ |
+-----------------------------------------------------------------------------+
```

---

<div style="page-break-after: always;"></div>

# CHAPTER 3: PUPPET MODULES IMPLEMENTATION

## 3.1 Node Classification (`site.pp`)
```puppet
node 'agent1.devops.local' {
  include nginx_server
  include ssh_hardening
  include nrpe_monitoring
}

node 'agent2.devops.local' {
  include ssh_hardening
  include nrpe_monitoring
}
```

## 3.2 Nginx Server Module (`nginx_server/manifests/init.pp`)
```puppet
class nginx_server {
  package { 'nginx':
    ensure => installed,
  }

  file { '/var/www/html/index.html':
    ensure  => file,
    content => template('nginx_server/index.html.erb'),
    require => Package['nginx'],
  }

  service { 'nginx':
    ensure    => running,
    enable    => true,
    subscribe => File['/var/www/html/index.html'],
  }
}
```

## 3.3 NRPE Monitoring Module (`nrpe_monitoring/manifests/init.pp`)
```puppet
class nrpe_monitoring {
  package { ['nagios-nrpe-server', 'nagios-plugins']:
    ensure => installed,
  }

  file { '/etc/nagios/nrpe.cfg':
    ensure  => file,
    content => template('nrpe_monitoring/nrpe.cfg.erb'),
    notify  => Service['nagios-nrpe-server'],
    require => Package['nagios-nrpe-server'],
  }

  service { 'nagios-nrpe-server':
    ensure => running,
    enable => true,
  }
}
```

---

<div style="page-break-after: always;"></div>

# CHAPTER 4: NAGIOS OBSERVABILITY & NRPE PROBES

## 4.1 Monitored Services
- **Control Plane Probe:** Tests Puppet Master on TCP port `8140` to ensure catalog compiler availability.
- **Web Ingress (`check_http`):** Tests port 80 on Agent 1, alerting if Nginx is stopped.
- **Deep Host Probing via NRPE (`check_nrpe` on port 5666):**
  - `check_disk`: Warns at 80% disk usage, critical at 90%.
  - `check_mem`: Monitors RAM consumption.
  - `check_load`: Tracks CPU load averages.
  - `check_procs`: Verifies both `nginx` and `puppet` agent daemons are active.

---

<div style="page-break-after: always;"></div>

# CHAPTER 5: TESTING STRATEGY & FAULT INJECTION (TC-01 TO TC-05)

| Test Case | Injected Action | Expected System Response | Nagios State | Status |
| :--- | :--- | :--- | :--- | :--- |
| **TC-01** | `puppet agent -t` on unconfigured node | Downloads catalog, installs Nginx & NRPE | All checks initialize OK | **PASS** |
| **TC-02** | Access Agent 1 IP in web browser | Default Puppet website loads successfully | `check_http` reports OK | **PASS** |
| **TC-03** | Stop Nginx manually (`systemctl stop nginx`) | Immediate outage detected; alert triggered | Transitions to CRITICAL | **PASS** |
| **TC-04** | Run Puppet agent (`puppet agent -t`) | Puppet detects stopped service, restarts it | Drift corrected | **PASS** |
| **TC-05** | Re-evaluate Nagios dashboard | Nagios detects restored service | Restores to GREEN OK | **PASS** |

---

<div style="page-break-after: always;"></div>

# CHAPTER 6: CONCLUSION & REFERENCES

1. **Puppet by Perforce.** *Puppet 8 Reference Manual: Architecture, DSL, and Modules.* Puppet Library, 2024.
2. **Nagios Enterprises.** *NRPE Documentation: Monitoring Remote Linux Hosts.* Nagios Library, 2024.
3. **Lovely Professional University.** *INT333 Curriculum: DevOps Advance Configuration Management.* 2026.

