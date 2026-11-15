# DEPARTMENT OF COMPUTER SCIENCE AND ENGINEERING
## School of Computer Science and Engineering
### Lovely Professional University, Punjab

---

# FINAL PROJECT REPORT
### Course Code: INT333 – DevOps Advance Configuration Management

## **Automated AWS Multi-Tier Infrastructure Deployment with Terraform and Real-Time Nagios Observability**

---

### **Submitted By:**
- **Name:** Saif Siddique
- **Registration No:** 12308813
- **Roll No:** 44
- **Program:** B.Tech Computer Science and Engineering (DevOps Specialization)

### **Under the Guidance of:**
- **Supervisor:** Ms. Manpreet Kaur (Assistant Professor)
- **Department:** School of Computer Science and Engineering
- **Institution:** Lovely Professional University, Phagwara, Punjab, India
- **Academic Session:** 2024–2025 / 2026–2027

---

<div style="page-break-after: always;"></div>

## CERTIFICATE

This is to certify that the project entitled **"Automated AWS Multi-Tier Infrastructure Deployment with Terraform and Real-Time Nagios Observability"** submitted by **Saif Siddique (Registration No: 12308813, Roll No: 44)** in partial fulfillment of the requirements for the award of the degree of **Bachelor of Technology in Computer Science and Engineering (DevOps)** for the course **INT333: DevOps Advance Configuration Management** at **Lovely Professional University**, Phagwara, is an authentic record of the candidate's own work carried out under my supervision and guidance.

<br><br>
_________________________________  
**Ms. Manpreet Kaur**  
Assistant Professor (Project Guide)  
School of Computer Science and Engineering  
Lovely Professional University, Punjab  

---

<div style="page-break-after: always;"></div>

## CANDIDATE DECLARATION

I hereby declare that the work presented in this project report entitled **"Automated AWS Multi-Tier Infrastructure Deployment with Terraform and Real-Time Nagios Observability"** submitted to the Department of Computer Science and Engineering, Lovely Professional University, is an authentic record of my original work, design, implementation, and experimental validation under the supervision of **Ms. Manpreet Kaur**, Assistant Professor.

<br><br>
_________________________________  
**Saif Siddique**  
Registration No: 12308813 | Roll No: 44  
School of Computer Science and Engineering  
Lovely Professional University  

---

<div style="page-break-after: always;"></div>

## ABSTRACT

Modern cloud operations require infrastructure to be fully automated, resilient, and observable at all times. In traditional IT environments, multi-tier cloud architectures (load balancers, application servers, network subnets, and firewalls) are manually provisioned via cloud web consoles or command-line scripts. This manual workflow inevitably results in configuration drift, non-reproducible deployments, and critical security group misconfigurations that expose internal application tiers to the public internet. Furthermore, once a multi-tier cloud infrastructure is provisioned, monitoring only the public entry point leaves system administrators completely unaware when backend compute nodes experience memory exhaustion, disk storage overflow, or local service failures.

This project delivers an automated, enterprise-grade cloud DevOps framework combining **Declarative Cloud Automation with Terraform** (Course Unit IV) and **Deep Full-Stack Observability with Nagios Core & NRPE** (Course Unit III). 

The infrastructure provisions an isolated **AWS Virtual Private Cloud (VPC 10.200.0.0/16)** across region `ap-south-1`, encompassing dual-AZ public subnets (`10.200.1.0/24`, `10.200.2.0/24`), dual-AZ private subnets (`10.200.10.0/24`, `10.200.20.0/24`), and a dedicated management subnet. An **AWS Application Load Balancer (ALB)** terminates SSL and distributes public web traffic across redundant backend application compute nodes residing in private subnets with no public IPv4 addresses. 

To provide complete visibility, a dedicated **Nagios Core 4.5** server performs synthetic uptime monitoring of the public load balancer (`check_http`) while simultaneously querying deep internal operating system metrics (CPU load, memory consumption via `check_mem`, root disk space via `check_disk`, and service process counts) across private instances using the **Nagios Remote Plugin Executor (NRPE)** over secure TCP port `5666`. A comprehensive chaos testing plan (`TC-01` through `TC-05`) validates automated multi-tier provisioning, memory stress detection, ALB node health drainage, and automated recovery.

---

<div style="page-break-after: always;"></div>

# CHAPTER 1: ARCHITECTURE & MULTI-TIER NETWORK FLOW

```
AWS CLOUD (ap-south-1)
+-----------------------------------------------------------------------------+
| Custom VPC (10.200.0.0/16)                                                  |
|                                                                             |
| +---------------------------------+ +---------------------------------+     |
| | Public Subnets (10.200.1.0/24)  | | Management Subnet               |     |
| |                                 | |                                 |     |
| | +---------------------------+   | | +---------------------------+   |     |
| | | AWS Application Load      |   | | | Nagios Monitoring Server  |   |     |
| | | Balancer (ALB)            |   | | | (AWS EC2 Instance)        |   |     |
| | | * Public Ingress (80/443) |   | | +---------------------------+   |     |
| | | * Target Group Forwarding |   | | | * Apache Web Dashboard    |   |     |
| | +-------------+-------------+   | | | * check_http (ALB Uptime) |   |     |
| +---------------|-----------------+ | | * check_nrpe (Agent Probes|   |     |
|                 |                   | | * Alert & Incident Logs   |   |     |
| +---------------v-----------------+ | +-------------+-------------+   |     |
| | Private Subnet (10.200.10.0/24) | +---------------|-----------------+     |
| |                                 |                 |                       |
| | +---------------------------+   |                 |                       |
| | | Application Node 1 (EC2)  |   |                 |                       |
| | | * Web Service (Port 80)   |<--+-----------------+ (NRPE Port 5666)      |
| | | * NRPE Agent (check_nrpe) |   |                 |                       |
| | +---------------------------+   |                 |                       |
| |                                 |                 |                       |
| | +---------------------------+   |                 |                       |
| | | Application Node 2 (EC2)  |   |                 |                       |
| | | * Web Service (Port 80)   |<--+-----------------+ (NRPE Port 5666)      |
| | | * NRPE Agent (check_nrpe) |   |                                         |
| | +---------------------------+   |                                         |
| +---------------------------------+                                         |
+-----------------------------------------------------------------------------+
```

---

<div style="page-break-after: always;"></div>

# CHAPTER 2: TERRAFORM MULTI-TIER IMPLEMENTATION

## 2.1 VPC & Subnet Manifests (`vpc.tf`)
```hcl
resource "aws_vpc" "multi_tier_vpc" {
  cidr_block           = "10.200.0.0/16"
  enable_dns_hostnames = true
  enable_dns_support   = true
  tags = { Name = "int333-saif-vpc", Owner = "Saif Siddique (12308813)" }
}

resource "aws_subnet" "public_1" {
  vpc_id            = aws_vpc.multi_tier_vpc.id
  cidr_block        = "10.200.1.0/24"
  availability_zone = "ap-south-1a"
}

resource "aws_subnet" "private_1" {
  vpc_id            = aws_vpc.multi_tier_vpc.id
  cidr_block        = "10.200.10.0/24"
  availability_zone = "ap-south-1a"
}
```

## 2.2 Application Load Balancer (`alb.tf`)
```hcl
resource "aws_lb" "external_alb" {
  name               = "int333-alb"
  internal           = false
  load_balancer_type = "application"
  security_groups    = [aws_security_group.alb_sg.id]
  subnets            = [aws_subnet.public_1.id, aws_subnet.public_2.id]
}

resource "aws_lb_target_group" "app_tg" {
  name     = "int333-app-tg"
  port     = 80
  protocol = "HTTP"
  vpc_id   = aws_vpc.multi_tier_vpc.id

  health_check {
    path                = "/health"
    healthy_threshold   = 2
    unhealthy_threshold = 3
    timeout             = 3
    interval            = 15
  }
}
```

---

<div style="page-break-after: always;"></div>

# CHAPTER 3: NAGIOS OBSERVABILITY & NRPE PROBES

## 3.1 Probing Tiers
- **Tier 1 (check_http):** Probes external ALB endpoint; verifies response time < 500ms and HTTP 200 codes.
- **Tier 2 (check_nrpe over Port 5666):**
  - Memory consumption (`check_mem`): Alerts if active RAM exceeds 80%.
  - Root disk space (`check_disk`): Alerts if free disk falls below 20%.
  - CPU load average (`check_load`).
  - Active web process count (`check_procs`).
- **Tier 3 (check_ping):** Internal ICMP reachability.

---

<div style="page-break-after: always;"></div>

# CHAPTER 4: TESTING STRATEGY & FAULT INJECTION (TC-01 TO TC-05)

| Test Case | Injected Fault | Expected Detection | Observed System Response | Status |
| :--- | :--- | :--- | :--- | :--- |
| **TC-01** | `terraform apply` on clean account | Complete multi-tier topology in < 4 min | All resources created without errors | **PASS** |
| **TC-02** | Send HTTP requests to ALB DNS | Traffic balanced; Nagios reports OK | `check_http` OK; 50/50 distribution | **PASS** |
| **TC-03** | Trigger memory stress (`stress-ng`) | NRPE `check_mem` flags warning/critical | Soft WARNING escalates to HARD CRITICAL | **PASS** |
| **TC-04** | Terminate web service on Node 2 | Nagios flags node CRITICAL; ALB detaches | ALB drains Node 2; traffic routed to Node 1 | **PASS** |
| **TC-05** | Restart service & release stress | Nagios detects restoration via NRPE | All indicators return to green OK | **PASS** |

---

<div style="page-break-after: always;"></div>

# CHAPTER 5: CONCLUSION & REFERENCES

1. **HashiCorp.** *Terraform AWS Provider Documentation & Multi-Tier Architecture.* 2024.
2. **Nagios Enterprises.** *NRPE Documentation: Monitoring Remote Linux Hosts.* 2024.
3. **Amazon Web Services.** *AWS Elastic Load Balancing and VPC User Guide.* 2024.
4. **Lovely Professional University.** *INT333 Curriculum: DevOps Advance Configuration Management.* 2026.

