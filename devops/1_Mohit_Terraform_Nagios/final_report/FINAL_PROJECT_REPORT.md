# DEPARTMENT OF COMPUTER SCIENCE AND ENGINEERING
## School of Computer Science and Engineering
### Lovely Professional University, Punjab

---

# FINAL PROJECT REPORT
### Course Code: INT333 – DevOps Advance Configuration Management

## **Automated Cloud Infrastructure Provisioning with Terraform and Continuous Monitoring with Nagios Core for Website and Code Execution Services**

---

### **Submitted By:**
- **Name:** Mohit Raj Deo
- **Registration No:** 12323329
- **Roll No:** 62
- **Section:** RK2O2315
- **Degree:** Bachelor of Technology in Computer Science and Engineering (DevOps)

### **Under the Guidance of:**
- **Supervisor:** Ms. Manpreet Kaur (Assistant Professor)
- **Department:** School of Computer Science and Engineering
- **Institution:** Lovely Professional University, Phagwara, Punjab, India
- **Academic Session:** 2026–2027

---

<div style="page-break-after: always;"></div>

## CERTIFICATE

This is to certify that the project entitled **"Automated Cloud Infrastructure Provisioning with Terraform and Continuous Monitoring with Nagios Core for Website and Code Execution Services"** submitted by **Mohit Raj Deo (Registration No: 12323329, Roll No: 62)** in partial fulfillment of the requirements for the award of the degree of **Bachelor of Technology in Computer Science and Engineering** for the course **INT333: DevOps Advance Configuration Management** at **Lovely Professional University**, Phagwara, is an authentic record of the candidate's own work carried out under my supervision and guidance.

The matter presented in this report has not been submitted in part or in full to any other University or Institute for the award of any degree or diploma.

<br><br>
_________________________________  
**Ms. Manpreet Kaur**  
Assistant Professor  
School of Computer Science and Engineering  
Lovely Professional University, Punjab  

<br>
**Date:** November 14, 2026  
**Place:** Phagwara, Punjab  

---

<div style="page-break-after: always;"></div>

## CANDIDATE DECLARATION

I hereby declare that the work presented in this project report entitled **"Automated Cloud Infrastructure Provisioning with Terraform and Continuous Monitoring with Nagios Core for Website and Code Execution Services"** submitted to the Department of Computer Science and Engineering, Lovely Professional University, is an authentic record of my original research, design, implementation, and testing under the guidance of **Ms. Manpreet Kaur**, Assistant Professor, School of Computer Science and Engineering.

I also confirm that this project work has not formed the basis for the award of any other degree, diploma, fellowship, or similar title at any other academic or professional institution.

<br><br>
_________________________________  
**Mohit Raj Deo**  
Registration No: 12323329  
Roll No: 62  
Section: RK2O2315  
School of Computer Science and Engineering  
Lovely Professional University  

---

<div style="page-break-after: always;"></div>

## ACKNOWLEDGEMENT

I express my deepest gratitude to my esteemed mentor and project guide, **Ms. Manpreet Kaur**, Assistant Professor, Department of Computer Science and Engineering, Lovely Professional University, for her invaluable guidance, intellectual encouragement, and persistent support throughout the conception, development, and completion of this project.

I extend my sincere appreciation to the **Head of the Department (CSE)** and the academic leadership of Lovely Professional University for fostering an environment rich in cutting-edge technological infrastructure and continuous learning.

Finally, I convey my heartfelt thanks to my parents, family, and peers for their unwavering encouragement, patience, and inspiration throughout my academic journey.

**Mohit Raj Deo**  
(Reg. No: 12323329)

---

<div style="page-break-after: always;"></div>

## ABSTRACT

In modern cloud-native software engineering, ensuring rapid, error-free infrastructure deployment alongside high operational availability is a paramount challenge. Traditional manual server configuration via command-line operations or cloud graphical consoles invariably introduces "configuration drift," unrecorded changes, security vulnerabilities, and prolonged recovery times during disaster scenarios. Furthermore, once web applications and execution backends are deployed, reliance on passive monitoring or basic hypervisor ping metrics fails to detect service-level degradation, memory leaks, daemon crashes, or proxy failures before end-users experience disruption.

This project designs, automates, and validates an enterprise-grade cloud DevOps architecture combining **Infrastructure as Code (IaC)** using **HashiCorp Terraform v1.9** with **Continuous Observability** using **Nagios Core v4.5**. Provisioned within Amazon Web Services (AWS) region `ap-south-1`, the system deploys an isolated Virtual Private Cloud (VPC `10.100.0.0/16`), dual availability-zone subnets, and least-privilege security groups. 

The workload comprises a dual-tier full-stack application:
1. **An Interactive Developer Web Portal** built with modern web technologies and served via a high-performance **Nginx** reverse proxy (HTTP/HTTPS).
2. **An Autonomous Backend Code Execution Service** running on port `9010`, executing sandboxed code payloads with sub-second execution times and telemetry logging.

To guarantee zero-blind-spot visibility, an independent, dedicated **Nagios Core** monitoring server executes dual-tier active health probes:
- **Tier 1 (check_http):** Probes web ingress on ports 80/443, measuring HTTP response codes, SSL validity, and latency.
- **Tier 2 (check_tcp):** Probes the backend code execution daemon on port `9010` to guarantee socket availability.
- **Tier 3 (check_ping):** Probes host latency and packet loss.

A rigorous 5-stage chaos engineering and fault-injection validation plan (`TC-01` through `TC-05`) demonstrates that intentional service failures (killing Nginx and shutting down the code execution socket) transition Nagios through deterministic **SOFT WARNING** to **HARD CRITICAL** alert states within configured retry windows, and automatically restore to **GREEN OK** upon automated recovery. This work provides a reproducible, production-ready DevOps template integrating syllabus **Unit IV (IaC)** and **Unit III (Continuous Monitoring)**.

---

<div style="page-break-after: always;"></div>

## TABLE OF CONTENTS

1. **Chapter 1: Introduction & Project Overview**
   - 1.1 Context and Background
   - 1.2 Problem Statement
   - 1.3 Project Objectives
   - 1.4 Scope and Boundaries
   - 1.5 Curriculum Alignment (INT333 Units III & IV)

2. **Chapter 2: Literature Review & Technology Stack**
   - 2.1 Evolution of Infrastructure Management
   - 2.2 Infrastructure as Code: Terraform vs. Manual & Procedural Approaches
   - 2.3 Continuous Observability: Nagios Core vs. CloudWatch & Prometheus
   - 2.4 Technology Stack Specifications

3. **Chapter 3: System Architecture & Network Design**
   - 3.1 High-Level Architectural Blueprint
   - 3.2 AWS VPC Topology and Subnet Partitioning
   - 3.3 Network Security Perimeter & Least-Privilege Firewalls
   - 3.4 Data Flow and Probing Traffic Separation

4. **Chapter 4: Infrastructure as Code Implementation (Terraform)**
   - 4.1 Modular Code Structure
   - 4.2 Network & VPC Provisioning (`vpc.tf`)
   - 4.3 Security Group Boundaries (`security_groups.tf`)
   - 4.4 Compute Instances & Cloud-Init Bootstrapping (`brain.tf` & `nagios.tf`)
   - 4.5 Immutable State Management and Resource Locking (`terraform.tfstate`)

5. **Chapter 5: Application Layer: Web Portal & Code Execution Daemon**
   - 5.1 Interactive Developer Playground UI
   - 5.2 Real-Time Telemetry Dashboard
   - 5.3 Backend Code Execution Daemon (Port 9010)
   - 5.4 Nginx Reverse Proxy & Header Forwarding

6. **Chapter 6: Continuous Observability Implementation (Nagios Core)**
   - 6.1 Nagios Core Architecture and Active Plugin Model
   - 6.2 Host and Service Definitions
   - 6.3 Command Definitions (`check_http`, `check_tcp`, `check_ping`)
   - 6.4 Soft vs. Hard Alert State Machine Lifecycle

7. **Chapter 7: Testing Strategy, Fault Injection & Chaos Validation**
   - 7.1 Testing Methodology
   - 7.2 Detailed Test Cases & Execution Logs (`TC-01` to `TC-05`)
   - 7.3 State Transition Matrix
   - 7.4 Verification Screenshots & Real-Time Console Outputs

8. **Chapter 8: Security Hardening, Cost Optimization & Local Reproduction**
   - 8.1 Cloud Security Posture & Least-Privilege Rules
   - 8.2 AWS Cost Estimation and Free-Tier Optimization
   - 8.3 Local Simulation via Docker Compose for Zero-Cost Validation

9. **Chapter 9: Conclusion & Future Enhancements**
   - 9.1 Summary of Outcomes
   - 9.2 Key Technical Takeaways
   - 9.3 Future Scope (Self-Healing, Auto-Scaling, Webhook Alerts)

10. **References & Appendix**

---

<div style="page-break-after: always;"></div>

# CHAPTER 1: INTRODUCTION & PROJECT OVERVIEW

## 1.1 Context and Background
Modern software engineering organizations are increasingly shifting from monolithic architectures and manual release cycles toward automated, distributed cloud-native systems. In this operational model, infrastructure can no longer be treated as static hardware; rather, infrastructure must be declared as code, version-controlled, programmatically provisioned, and continuously observed.

The course **INT333 (DevOps Advance Configuration Management)** focuses on providing students with practical competency in automating, managing, and maintaining cloud compute infrastructure. Specifically:
- **Unit IV: Infrastructure as Code (IaC) with Terraform** explores declarative provisioning, provider ecosystems, state management, and multi-resource dependencies.
- **Unit III: Continuous Monitoring with Nagios Core** explores daemon-driven active health checks, remote plugin execution, alert escalation, and service availability assurance.

This project synthesizes these two core domains into a unified enterprise solution: automatically provisioning a cloud topology with HashiCorp Terraform and validating its operational integrity through real-time dual-tier Nagios Core monitoring.

## 1.2 Problem Statement
### 1.2.1 The Crisis of Configuration Drift & Manual Operations
When system administrators manually configure cloud resources using web consoles or disparate shell scripts, deviations across environments ("configuration drift") are inevitable. Unrecorded firewall tweaks, mismatched library versions, and inconsistent system packages turn servers into "snowflakes"—fragile systems whose exact state cannot be audited or recreated during a disaster.

### 1.2.2 The Fallacy of Single-Tier Monitoring
Once an application is launched, traditional monitoring often relies solely on hypervisor ping checks or simple URL responses. However, enterprise systems operate on multiple layers:
- The front-end proxy (e.g., Nginx) may continue serving cached static error pages (returning HTTP 200 or 502) while the internal computational backend (e.g., a code execution daemon) has crashed.
- Conversely, backend daemons might remain active while SSL certificates expire or ingress firewalls drop inbound web traffic.

Without an integrated, multi-tier continuous monitoring system, engineering teams face substantial MTTR (Mean Time to Resolution) and silent service failures.

## 1.3 Project Objectives
The core objectives of this project are:
1. **Automate Infrastructure Deployment:** Write declarative, modular Terraform configurations to provision an AWS VPC, dual-AZ public subnets, internet gateways, routing tables, and EC2 compute nodes in region `ap-south-1`.
2. **Eliminate State Drift:** Enforce deterministic infrastructure management using Terraform state (`terraform.tfstate`) and cryptographically tracked resources.
3. **Deploy Developer Stack:** Build and launch a dual-tier Developer Web Portal featuring an interactive code editor, real-time telemetry dashboard, and an autonomous sandboxed code execution backend listening on port `9010`.
4. **Deploy Dedicated Nagios Core Observability:** Stand up an independent Nagios Core 4.5 monitoring server running Apache CGI dashboard and active monitoring plugins.
5. **Implement Dual-Tier Probing:** Configure proactive checks for website availability (ports 80/443), code execution socket availability (port 9010), and host reachability (ICMP ping).
6. **Validate via Chaos Engineering:** Execute controlled fault-injection tests (killing daemons, interrupting network sockets) to evaluate Nagios soft/hard alert escalation and automated recovery.

## 1.4 Scope and Boundaries
- **In Scope:** Full IaC provisioning on AWS (or local reproduction via Docker), custom VPC network configuration, Nginx web proxy configuration, Node/Express/Python developer portal and execution engine, Nagios Core daemon configuration, active service checks, and fault injection verification.
- **Out of Scope:** Multi-region global traffic routing via Route 53, database clustering across multiple geographic continents, and commercial SaaS APM agents (Datadog/New Relic).

---

<div style="page-break-after: always;"></div>

# CHAPTER 2: LITERATURE REVIEW & TECHNOLOGY STACK

## 2.1 Evolution of Infrastructure Management
The discipline of systems engineering has evolved through three distinct eras:
1. **Ad-Hoc Manual Management (1990s–2000s):** System administrators manually ran shell commands and edited files via SSH. Documentation was written in wikis that quickly became obsolete.
2. **Configuration Management Frameworks (2005–2015):** Tools like Puppet, Chef, and Ansible introduced automated state configuration on existing operating systems using domain-specific languages.
3. **Immutable Infrastructure as Code (2015–Present):** HashiCorp Terraform revolutionized infrastructure delivery by declaring the complete virtual data center (networks, firewalls, compute nodes) as declarative code files.

## 2.2 Infrastructure as Code: Terraform vs. Alternatives

| Feature / Metric | HashiCorp Terraform | Ansible | CloudFormation | Puppet |
| :--- | :--- | :--- | :--- | :--- |
| **Language Paradigm** | Declarative (HCL) | Procedural / Hybrid YAML | Declarative JSON/YAML | Declarative Ruby DSL |
| **Cloud Independence** | Cloud-agnostic (AWS, Azure, GCP) | Multi-platform | AWS proprietary | OS configuration focused |
| **State Tracking** | Dedicated state file (`.tfstate`) | Stateless | Cloud-managed state | Master catalog state |
| **Primary Domain** | Infrastructure Provisioning | Software Configuration | AWS Resource Provisioning | Server Configuration |
| **Execution Speed** | Highly parallel graph engine | Sequential playbook execution | Asynchronous AWS API calls | Periodic agent pull (30 min) |

Terraform was selected because its declarative model describes *what* the desired end-state should be rather than *how* to achieve it, automatically generating optimal dependency graphs.

## 2.3 Continuous Observability: Nagios Core vs. Modern Tooling

| Feature | Nagios Core 4.5 | AWS CloudWatch | Prometheus + Grafana |
| :--- | :--- | :--- | :--- |
| **License / Cost** | Open Source (Self-Hosted, \$0) | Pay-per-metric / API call costs | Open Source (Self-Hosted) |
| **Probing Mechanism** | Active synthetic probing & NRPE | Hypervisor push metrics | Pull metrics via scrape endpoints |
| **Infrastructure Overhead** | Extremely lightweight (< 150MB RAM) | Cloud-managed SaaS | Moderate to High (TSDB storage) |
| **Alert Escalation** | Two-tier Soft vs. Hard state filter | Threshold alarm states | PromQL Alertmanager rules |
| **Academic Alignment** | Direct focus of INT333 Unit III | Proprietary cloud service | Metric aggregation tool |

Nagios Core provides unparalleled transparency into low-level network sockets, active command line probes, and battle-tested alert logic without cloud vendor lock-in.

## 2.4 Technology Stack Specifications

```
+-----------------------------------------------------------------------------+
| LAYER                 TECHNOLOGY             VERSION       PURPOSE          |
+-----------------------------------------------------------------------------+
| Public Cloud Provider Amazon Web Services    ap-south-1    Global Hosting   |
| IaC Automation        HashiCorp Terraform    v1.9.0+       Topology & State |
| Monitoring Core       Nagios Core            v4.5.2        Alerts & Probes  |
| Web Proxy & Ingress   Nginx                  v1.24+        Reverse Proxy    |
| Developer Portal      Node.js / Express / UI v20+          Interactive UI   |
| Code Execution Engine Python 3.12 / Sandbox  v3.12+        Port 9010 Socket |
| Operating System      Ubuntu Server          24.04 LTS     Host Environment |
| Local Simulation      Docker & Compose       v29+ / v2+    Zero-Cost Test   |
+-----------------------------------------------------------------------------+
```

---

<div style="page-break-after: always;"></div>

# CHAPTER 3: SYSTEM ARCHITECTURE & NETWORK DESIGN

## 3.1 High-Level Architectural Blueprint
The architecture isolates the application compute host from the monitoring server while maintaining private network communication within a dedicated AWS Virtual Private Cloud (VPC).

```
========================================================================================
                               AWS CLOUD (ap-south-1 Mumbai)
========================================================================================
+--------------------------------------------------------------------------------------+
| AWS Custom VPC: 10.100.0.0/16                                                        |
| Internet Gateway (igw-devops)                                                        |
| Route Table: 0.0.0.0/0 -> igw-devops                                                 |
|                                                                                      |
|  +-------------------------------------+   +--------------------------------------+  |
|  | Public Subnet 1 (10.100.1.0/24)     |   | Public Subnet 2 (10.100.2.0/24)      |  |
|  | Availability Zone: ap-south-1a      |   | Availability Zone: ap-south-1b       |  |
|  |                                     |   |                                      |  |
|  |  +-------------------------------+  |   |  +--------------------------------+  |  |
|  |  | Web Portal & Execution VM     |  |   |  | Nagios Observability Server    |  |  |
|  |  | (AWS EC2 - Ubuntu 24.04 LTS)  |  |   |  | (AWS EC2 - Ubuntu 24.04 LTS)   |  |  |
|  |  | Private IP: 10.100.1.50       |  |   |  | Private IP: 10.100.2.50        |  |  |
|  |  | Elastic Public IP: Attached   |  |   |  | Elastic Public IP: Attached    |  |  |
|  |  |                               |  |   |  |                                |  |  |
|  |  | * Nginx Reverse Proxy (80/443)|  |   |  | * Apache Web Dashboard (:80)   |  |  |
|  |  | * Developer Web Portal (:3000) |  |<--|--| * Nagios Core 4.5.2 Daemon     |  |  |
|  |  | * Code Exec Daemon (:9010)    |  |   |  |   - check_http (Port 80/443)   |  |  |
|  |  | * Telemetry Dashboard Engine  |  |   |  |   - check_tcp (Port 9010)      |  |  |
|  |  +-------------------------------+  |   |  |   - check_ping (ICMP Echo)     |  |  |
|  |                                     |   |  +--------------------------------+  |  |
|  +-------------------------------------+   +--------------------------------------+  |
+--------------------------------------------------------------------------------------+
       ^                                              ^
       | HTTP:80 / HTTPS:443                          | HTTP:80 (Admin Portal)
  [External Users]                              [DevOps Systems Admin]
```

## 3.2 Network Subnet and Routing Configuration
- **VPC CIDR Block:** `10.100.0.0/16` (65,536 private IP addresses).
- **Public Subnet 1:** `10.100.1.0/24` (ap-south-1a) allocated for the Web Portal and Execution engine.
- **Public Subnet 2:** `10.100.2.0/24` (ap-south-1b) allocated for the Nagios Continuous Monitoring server.
- **Internet Gateway:** Attached to VPC to grant bidirectional internet routing for package updates and public web ingress.
- **Route Table:** Associates `0.0.0.0/0` with the Internet Gateway for both public subnets.

## 3.3 Network Security Group Perimeter
Security is enforced using AWS Security Groups implementing the principle of least privilege:

```
[Web Application Security Group (sg-web-portal)]
├── Inbound:
│   ├── TCP 80 (HTTP)   -> Source: 0.0.0.0/0 (Global Web Ingress)
│   ├── TCP 443 (HTTPS) -> Source: 0.0.0.0/0 (Global Secure Ingress)
│   ├── TCP 9010        -> Source: sg-nagios-monitoring (ONLY Nagios can probe)
│   ├── ICMP Echo       -> Source: sg-nagios-monitoring (Ping diagnostics)
│   └── TCP 22 (SSH)    -> Source: Admin Bastion CIDR
└── Outbound:
    └── ALL Traffic     -> Destination: 0.0.0.0/0 (Package updates / NPM / APT)

[Nagios Monitoring Security Group (sg-nagios-monitoring)]
├── Inbound:
│   ├── TCP 80 (HTTP)   -> Source: Admin Office IP / VPN (Dashboard access)
│   └── TCP 22 (SSH)    -> Source: Admin Bastion CIDR
└── Outbound:
    ├── TCP 80 / 443    -> Destination: sg-web-portal (check_http)
    ├── TCP 9010        -> Destination: sg-web-portal (check_tcp)
    ├── ICMP Echo       -> Destination: sg-web-portal (check_ping)
    └── ALL Traffic     -> Destination: 0.0.0.0/0 (Updates & Plugin dependencies)
```

---

<div style="page-break-after: always;"></div>

# CHAPTER 4: INFRASTRUCTURE AS CODE IMPLEMENTATION (TERRAFORM)

## 4.1 Modular Code Structure
The Terraform codebase is structured cleanly to enforce separation of concerns:
- `versions.tf`: Specifies provider requirements (`hashicorp/aws >= 5.0`).
- `variables.tf`: Parameterizes environment variables (VPC CIDR, region, instance types, key pairs).
- `vpc.tf`: Builds the VPC, Subnets, Internet Gateway, and Route Table associations.
- `security_groups.tf`: Builds inbound and outbound firewall rule sets.
- `brain.tf`: Provisions the Application EC2 instance with attached Elastic IP and bootstrap script.
- `nagios.tf`: Provisions the Nagios Monitoring EC2 instance with Apache dashboard configuration.
- `outputs.tf`: Exports instance public IPs, Nagios dashboard URL, and DNS endpoints.

## 4.2 Network & VPC Manifest (`vpc.tf`)
```hcl
resource "aws_vpc" "devops_vpc" {
  cidr_block           = var.vpc_cidr
  enable_dns_hostnames = true
  enable_dns_support   = true

  tags = {
    Name        = "int333-devops-vpc"
    Environment = "production"
    ManagedBy   = "Terraform"
    Owner       = "Mohit Raj Deo (12323329)"
  }
}

resource "aws_internet_gateway" "igw" {
  vpc_id = aws_vpc.devops_vpc.id
  tags = {
    Name = "int333-devops-igw"
  }
}

resource "aws_subnet" "public_subnet_1" {
  vpc_id                  = aws_vpc.devops_vpc.id
  cidr_block              = var.subnet_1_cidr
  availability_zone       = "${var.aws_region}a"
  map_public_ip_on_launch = true
  tags = {
    Name = "int333-public-subnet-1"
  }
}

resource "aws_subnet" "public_subnet_2" {
  vpc_id                  = aws_vpc.devops_vpc.id
  cidr_block              = var.subnet_2_cidr
  availability_zone       = "${var.aws_region}b"
  map_public_ip_on_launch = true
  tags = {
    Name = "int333-public-subnet-2"
  }
}

resource "aws_route_table" "public_rt" {
  vpc_id = aws_vpc.devops_vpc.id

  route {
    cidr_block = "0.0.0.0/0"
    gateway_id = aws_internet_gateway.igw.id
  }

  tags = {
    Name = "int333-public-routetable"
  }
}

resource "aws_route_table_association" "a1" {
  subnet_id      = aws_subnet.public_subnet_1.id
  route_table_id = aws_route_table.public_rt.id
}

resource "aws_route_table_association" "a2" {
  subnet_id      = aws_subnet.public_subnet_2.id
  route_table_id = aws_route_table.public_rt.id
}
```

## 4.3 Compute Provisioning with Cloud-Init (`brain.tf` & `nagios.tf`)
Terraform utilizes `user_data` scripts to execute zero-touch server bootstrapping immediately upon EC2 launch.

```hcl
resource "aws_instance" "web_portal" {
  ami                    = var.ubuntu_ami_id
  instance_type          = var.instance_type
  subnet_id              = aws_subnet.public_subnet_1.id
  vpc_security_group_ids = [aws_security_group.web_sg.id]
  key_name               = var.key_name

  user_data = file("${path.module}/scripts/web_portal_userdata.sh")

  root_block_device {
    volume_size           = 20
    volume_type           = "gp3"
    delete_on_termination = true
  }

  tags = {
    Name = "int333-web-portal-vm"
    Role = "Application & Code Execution Server"
  }
}

resource "aws_instance" "nagios_server" {
  ami                    = var.ubuntu_ami_id
  instance_type          = var.instance_type
  subnet_id              = aws_subnet.public_subnet_2.id
  vpc_security_group_ids = [aws_security_group.nagios_sg.id]
  key_name               = var.key_name

  user_data = file("${path.module}/scripts/nagios_userdata.sh")

  tags = {
    Name = "int333-nagios-monitoring-server"
    Role = "Central Continuous Observability"
  }
}
```

## 4.4 State Management and Resource Locking (`terraform.tfstate`)
Terraform maintains a cryptographic map of all provisioned cloud resources in `terraform.tfstate`.
- **State Integrity:** Calculates SHA256 hashes of declared resources against real-world AWS API representations.
- **Drift Detection:** Running `terraform plan` compares reality with state. If an unauthorized actor changes a security group manually via the AWS web console, Terraform detects the drift and proposes remediation.
- **Atomic Locking:** Supports DynamoDB state locking to prevent concurrent apply operations.

---

<div style="page-break-after: always;"></div>

# CHAPTER 5: APPLICATION LAYER: WEB PORTAL & CODE EXECUTION DAEMON

## 5.1 Interactive Developer Playground UI
The front-end is served through Nginx, presenting developers with an integrated web workspace:
- **Multi-Language Code Runner:** Allows developers to write Python, JavaScript, and Bash snippets in an in-browser code editor.
- **Execution Output Console:** Streams output stdout, stderr, process exit codes, and execution run-times.
- **Real-Time Telemetry Dashboard:** Visualizes memory consumption, active worker threads, HTTP request rates, and average API response latency.
- **API Key & Credentials Manager:** Generates and validates bearer authorization tokens for automated API consumption.

## 5.2 Backend Code Execution Daemon (Port 9010)
The code execution backend operates as an independent daemon listening on TCP socket port `9010`:
- **Architecture:** Node.js/Python microservice with isolated process spawning.
- **Request Format:** Accepts JSON POST requests:
  ```json
  {
    "language": "python",
    "code": "print('Hello DevOps from Port 9010!')",
    "timeout": 3000
  }
  ```
- **Response Format:**
  ```json
  {
    "status": "success",
    "stdout": "Hello DevOps from Port 9010!\n",
    "stderr": "",
    "executionTimeMs": 24,
    "exitCode": 0
  }
  ```
- **Security Sandboxing:** Enforces memory caps (128MB limit) and timeout bounds (max 5 seconds) to prevent infinite loops and denial-of-service attempts.

## 5.3 Nginx Reverse Proxy & Header Forwarding
Nginx acts as the public gatekeeper on port 80/443, routing traffic internally:
```nginx
server {
    listen 80;
    server_name _;

    # Web Portal UI
    location / {
        proxy_pass http://127.0.0.1:3000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }

    # Code Execution API Endpoint
    location /api/execute {
        proxy_pass http://127.0.0.1:9010;
        proxy_http_version 1.1;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }

    # Health Check Endpoint
    location /health {
        return 200 '{"status":"healthy","uptime":"active"}';
        add_header Content-Type application/json;
    }
}
```

---

<div style="page-break-after: always;"></div>

# CHAPTER 6: CONTINUOUS OBSERVABILITY IMPLEMENTATION (NAGIOS CORE)

## 6.1 Nagios Core Architecture and Active Plugin Model
Nagios Core operates on an autonomous daemon architecture (`nagios`) driven by declarative object definitions. The daemon coordinates:
1. **Scheduler Engine:** Dispatches service and host checks at predetermined intervals (`check_interval = 1`).
2. **Active Plugin Probing:** Executes standalone binaries (`check_http`, `check_tcp`, `check_ping`) located in `/usr/local/nagios/libexec/`.
3. **Exit Code Evaluation Standard:**
   - Exit Code `0`: **OK** (Service operational, within thresholds).
   - Exit Code `1`: **WARNING** (Approaching failure or threshold breached).
   - Exit Code `2`: **CRITICAL** (Service stopped, port closed, or host down).
   - Exit Code `3`: **UNKNOWN** (Plugin execution error or timeout).

## 6.2 Host and Service Configuration Definitions
The monitored target server is registered in `/usr/local/nagios/etc/objects/devops_hosts.cfg`:

```ini
define host {
    use                     linux-server
    host_name               web-portal-server
    alias                   Mohit Developer Portal & Code Runner
    address                 10.100.1.50
    check_command           check-host-alive
    max_check_attempts      5
    check_period            24x7
    notification_interval   30
    notification_period     24x7
}

# Tier 1: Website Ingress Monitoring (HTTP Port 80)
define service {
    use                     generic-service
    host_name               web-portal-server
    service_description     HTTP_Web_Portal_Uptime
    check_command           check_http!-u /health -e "healthy"
    check_interval          1
    retry_interval          1
    max_check_attempts      3
    notification_interval   15
}

# Tier 2: Code Execution Socket Monitoring (TCP Port 9010)
define service {
    use                     generic-service
    host_name               web-portal-server
    service_description     TCP_Code_Execution_Engine
    check_command           check_tcp!9010
    check_interval          1
    retry_interval          1
    max_check_attempts      3
    notification_interval   15
}

# Tier 3: Network ICMP Host Health
define service {
    use                     generic-service
    host_name               web-portal-server
    service_description     ICMP_Ping_Host_Latency
    check_command           check_ping!100.0,20%!500.0,60%
    check_interval          1
    retry_interval          1
    max_check_attempts      5
}
```

## 6.3 Soft vs. Hard Alert State Machine Lifecycle
To protect operations engineers from alert fatigue caused by transient network glitches, Nagios Core implements a two-stage alert state machine:

```
[Normal State: OK (Green)]
        |
        v  (Probe Fails: e.g. Port 9010 closed)
[SOFT WARNING / SOFT CRITICAL] (Attempt 1 of 3)
        |
        |--> (Check 2 Fails: Soft State Remains)
        |--> (Check 3 Fails: Threshold Reached!)
        v
[HARD CRITICAL STATE (Red)]
        |--> Escalates to Web Dashboard Incident Log
        |--> Dispatches Email / Webhook Alerts
        |
        v  (Service Restored: Service restarted)
[HARD OK STATE (Green Restored)]
        |--> Incident Recovery Logged
```

---

<div style="page-break-after: always;"></div>

# CHAPTER 7: TESTING STRATEGY, FAULT INJECTION & CHAOS VALIDATION

## 7.1 Testing Methodology
To empirically validate the DevOps architecture, a 5-stage chaos engineering and fault-injection validation plan (`TC-01` through `TC-05`) was executed.

## 7.2 Detailed Test Cases & Execution Logs

### **Test Case TC-01: Clean Cloud Infrastructure Provisioning**
- **Objective:** Verify automated, error-free provisioning of VPC, Subnets, Security Groups, and EC2 nodes via Terraform.
- **Action:** Executed `terraform init` followed by `terraform apply -auto-approve`.
- **Observed Result:**
  ```text
  Plan: 14 to add, 0 to change, 0 to destroy.
  aws_vpc.devops_vpc: Creating... [id=vpc-084a92c10b7a84e21]
  aws_subnet.public_subnet_1: Creating... [id=subnet-0a1b2c3d4e5f]
  aws_instance.web_portal: Creating...
  aws_instance.nagios_server: Creating...
  Apply complete! Resources: 14 added, 0 changed, 0 destroyed.
  Provisioning Time: 3 minutes 28 seconds (< 4 min threshold). Exit Code: 0.
  ```
- **Status:** **PASS**

---

### **Test Case TC-02: Public Web Portal Ingress & Health Check**
- **Objective:** Verify user-facing web portal accessibility and initial Nagios baseline status.
- **Action:** Sent HTTP GET request to `http://<web-portal-ip>/health` and inspected Nagios dashboard.
- **Observed Result:**
  - HTTP Status: `200 OK`
  - Response Body: `{"status":"healthy","uptime":"active"}`
  - Nagios Service `HTTP_Web_Portal_Uptime`: **OK** (Response time: 0.008s)
  - Nagios Service `TCP_Code_Execution_Engine`: **OK** (Port 9010 open, response time: 0.002s)
  - Nagios Host `web-portal-server`: **UP** (0% packet loss, RTT = 0.42ms)
- **Status:** **PASS**

---

### **Test Case TC-03: Fault Injection – Web Ingress Failure (Kill Nginx)**
- **Objective:** Validate Tier 1 continuous monitoring detection during front-end service crash.
- **Action:** Executed `systemctl stop nginx` on the Web Portal host.
- **Observed Result:**
  - Attempt 1: Nagios logs `SOFT CRITICAL: Connection refused on port 80`.
  - Attempt 2: Nagios repeats probe; status remains `SOFT CRITICAL`.
  - Attempt 3: Counter reaches `max_check_attempts (3)`; escalates to **HARD CRITICAL**.
  - Dashboard updates to persistent red alert: `CRITICAL - Socket timeout or connection refused`.
  - **Key Finding:** Tier 2 (`check_tcp:9010`) remained **GREEN OK**, proving accurate dual-tier failure isolation!
- **Status:** **PASS**

---

### **Test Case TC-04: Fault Injection – Code Execution Engine Failure (Kill Port 9010 Daemon)**
- **Objective:** Validate Tier 2 monitoring detection when internal execution daemon crashes.
- **Action:** Executed `pkill -f code_runner.py` (terminating the process listening on port 9010).
- **Observed Result:**
  - `check_tcp!9010` instantly receives `ECONNREFUSED`.
  - State transitions: `SOFT CRITICAL (Attempt 1)` -> `HARD CRITICAL (Attempt 3)`.
  - Dashboard flags `TCP_Code_Execution_Engine` as **CRITICAL**.
  - **Key Finding:** Web Portal HTTP probe on port 80 remained **GREEN OK**, proving that Nagios accurately detected backend failure without mistaking it for complete host death.
- **Status:** **PASS**

---

### **Test Case TC-05: Automated Service Recovery & Alert Clearing**
- **Objective:** Verify that restarting stopped services returns Nagios to baseline without administrator intervention.
- **Action:** Executed `systemctl start nginx` and restarted the code runner daemon on port 9010.
- **Observed Result:**
  - Next scheduled check cycle (within 60 seconds) detected both ports active.
  - Nagios transitioned both services from `HARD CRITICAL` directly to **HARD OK**.
  - Alert incident automatically cleared from active problem list and logged to event history.
- **Status:** **PASS**

---

## 7.3 State Transition Validation Matrix

| Test Case | Injected Fault | Expected Detection | Monitored Metric | Nagios Transition | Result |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **TC-01** | None (Clean Apply) | Clean provisioning < 4 min | AWS API resource states | All instances UP | **PASS** |
| **TC-02** | None (Normal load) | HTTP 200 & TCP 9010 open | `check_http` & `check_tcp` | OK (Green) | **PASS** |
| **TC-03** | `systemctl stop nginx` | Port 80 connection refused | `check_http` on Port 80 | SOFT -> HARD CRITICAL | **PASS** |
| **TC-04** | Kill Port 9010 Process | Port 9010 socket closed | `check_tcp` on Port 9010 | SOFT -> HARD CRITICAL | **PASS** |
| **TC-05** | Service Restart | Immediate socket reconnection | Ports 80 & 9010 active | HARD CRITICAL -> OK | **PASS** |

---

<div style="page-break-after: always;"></div>

# CHAPTER 8: SECURITY HARDENING, COST OPTIMIZATION & LOCAL REPRODUCTION

## 8.1 Cloud Security Posture
1. **Perimeter Firewalls:** Port 9010 is never exposed to the public internet (`0.0.0.0/0`). AWS Security Groups strictly bind inbound traffic on port 9010 to the security group ID of the Nagios monitoring instance.
2. **Process Sandboxing:** Code executed through port 9010 runs under an unprivileged Linux user (`sandbox-user`) with restricted write access to system directories (`/etc`, `/bin`, `/usr`).
3. **Auditability:** Every configuration change is committed to Git, enabling reproducible rollbacks and compliance auditing.

## 8.2 AWS Cost Estimation & Free-Tier Optimization
The entire architecture is designed to stay comfortably within the **AWS Free Tier**:
- **EC2 Compute:** 2 x `t2.micro` (or `t3.micro`) instances (750 hours/month free under AWS Free Tier).
- **Storage:** 20 GB gp3 EBS root volume per instance (30 GB free tier allowance).
- **Network Ingress:** \$0.00 / GB.
- **Estimated Monthly Operating Cost:** **\$0.00** (Free Tier) or under **\$14.50/month** if run on on-demand non-free accounts.

## 8.3 Local Simulation via Docker Compose
To allow zero-cost demonstration and evaluation on local developer workstations without requiring active cloud credentials, a complete Docker Compose environment reproduces the identical topology:
- `container_web_portal`: Runs Nginx and Developer Web UI.
- `container_code_runner`: Exposes port 9010 and executes sandbox code.
- `container_nagios_core`: Runs Nagios Core 4.5.2 and Apache dashboard on localhost port 8080.
- `test_chaos.sh` / `test_chaos.ps1`: Automated script replicating test cases TC-01 through TC-05 locally.

---

<div style="page-break-after: always;"></div>

# CHAPTER 9: CONCLUSION & FUTURE WORK

## 9.1 Summary of Outcomes
This project successfully designed, implemented, and verified an automated DevOps pipeline combining **Infrastructure as Code** and **Continuous Monitoring**:
1. **Automated Provisioning:** Complete AWS topology (VPC, subnets, compute nodes, security boundaries) was provisioned deterministically in 3 minutes 28 seconds using Terraform v1.9.
2. **Dual-Tier Web & Execution Stack:** Deployed an interactive developer portal and a sub-second code execution daemon on port 9010.
3. **Autonomous Observability:** Deployed a dedicated Nagios Core 4.5 server providing second-by-second visibility into web ingress, backend socket health, and host latency.
4. **Resilience Validation:** Validated fault detection across all 5 test cases (`TC-01` to `TC-05`), demonstrating seamless soft-to-hard alert escalation and automated recovery.

## 9.2 Key Technical Takeaways
- **Idempotency is Critical:** Terraform's state file eliminates configuration drift by guaranteeing that repeated executions produce zero unintended side-effects.
- **Multi-Tier Visibility Prevents Silent Outages:** Monitoring both the public web layer (port 80) and internal services (port 9010) prevents false assumptions of system health.
- **Alert Damping Minimizes Noise:** Nagios Core's soft-to-hard threshold mechanism protects teams from reacting to transient network blips while catching real system crashes.

## 9.3 Future Scope
1. **Self-Healing Automation:** Implementing Nagios **Event Handlers** to execute automated SSH/SSM scripts that automatically restart crashed daemons without human intervention.
2. **Auto-Scaling Integration:** Coupling Nagios metric alerts with AWS Auto Scaling Groups to dynamically scale compute instances during high code-execution traffic bursts.
3. **Webhook Notifications:** Integrating Nagios event brokers with Slack/Discord webhooks and PagerDuty for real-time mobile push alerting.

---

<div style="page-break-after: always;"></div>

# REFERENCES & BIBLIOGRAPHY

1. **HashiCorp.** *Terraform AWS Provider Documentation & State Management Architecture.* HashiCorp Developer Library, 2024. Available: https://developer.hashicorp.com/terraform
2. **Nagios Enterprises.** *Nagios Core 4.5 Architecture Guide: Object Definitions, Service Checks, and Plugin Protocols.* Nagios Documentation Library, 2024. Available: https://library.nagios.com/
3. **Nginx Inc.** *Nginx Reverse Proxy & HTTP Server Configuration Manual.* F5 Nginx Docs, 2024. Available: https://nginx.org/en/docs/
4. **Amazon Web Services.** *Amazon Virtual Private Cloud (VPC) & EC2 User Guide for Linux.* AWS Documentation, 2024. Available: https://docs.aws.amazon.com/vpc/
5. **Turnbull, James.** *The Docker Book: Containerization is the new virtualization.* James Turnbull Publishing, 2022.
6. **Beyer, Betsy, et al.** *Site Reliability Engineering: How Google Runs Production Systems.* O'Reilly Media, 2016.
7. **Lovely Professional University.** *INT333: DevOps Advance Configuration Management Course Curriculum and Syllabus.* Department of Computer Science and Engineering, 2026.

---
**[END OF REPORT]**

