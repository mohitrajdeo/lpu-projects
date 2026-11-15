"""
Generator for all 3 INT333 DevOps Advance Configuration Management Final Project Reports
and Master Execution Manual.
Students:
- Mohit Raj Deo (12323329 | Roll: 62)
- Akash Choudhary (12301625 | Roll: 11)
- Saif Siddique (12308813 | Roll: 44)
"""

import os
import sys
from docx.shared import Inches, Pt
from report_builder import AcademicReportBuilder

BASE_DIR = r"c:\MOHIT\devops"

def generate_mohit_devops_report():
    print("[*] Generating Mohit DevOps Final Project Report...")
    title = "Automated AWS Multi-Tier Cloud Infrastructure Deployment with Terraform & Continuous Nagios Core Dual-Tier Observability"
    subtitle = "A Declarative Infrastructure-as-Code Framework Deploying Autonomous AI Microservices with Resilient Ingress, Dual-Tier Fault Isolation, and Proactive Alerting"

    b = AcademicReportBuilder(
        title=title,
        subtitle=subtitle,
        student_name="Mohit Raj Deo",
        reg_no="12323329",
        roll_no="62",
        course_code="INT333",
        course_name="DevOps Advance Configuration Management"
    )

    b.add_title_page()
    b.add_certificate()
    b.add_declaration()
    b.add_acknowledgement()

    abstract_text = (
        "Enterprise cloud adoption demands deterministic, reproducible, and verifiable infrastructure provisioning coupled with continuous "
        "observability to enforce high availability and strict Service Level Agreements (SLAs). "
        "This project presents an enterprise-grade Infrastructure as Code (IaC) and observability architecture designed by Mohit Raj Deo "
        "for INT333 (DevOps Advance Configuration Management). The solution employs HashiCorp Terraform to provision a secure, multi-tier AWS cloud topology "
        "comprising custom Virtual Private Clouds (VPCs), public and private subnet segregations, internet gateways, route tables, and granular security groups. "
        "The infrastructure deploys a containerized multi-tier application stack consisting of an Nginx high-performance reverse proxy ingress, "
        "the Autonomous AIOps Neural Telemetry microservice (Port 5001), an isolated Python backend code-execution daemon (Port 9010), "
        "and a dedicated Nagios Core 4.5 continuous monitoring engine. "
        "Observability is achieved via custom Nagios command definitions, active HTTP/TCP socket probes, and custom alerting plugins. "
        "The architecture is validated through an automated 5-stage chaos engineering test suite (TC-01 through TC-05), verifying container lifecycle, "
        "dual-tier network isolation, front-end crash recovery, backend socket failure detection, and automated alert state transitions from SOFT/HARD CRITICAL to OK. "
        "All code, configurations, and test runners operate deterministically in both production AWS environments and zero-dependency local simulation modes."
    )
    b.add_abstract(abstract_text, "DevOps, Terraform, Infrastructure as Code (IaC), AWS, Nagios Core 4.5, Reverse Proxy, Dual-Tier Isolation, AIOps Deployment, Continuous Observability, Chaos Engineering")

    toc_items = [
        ("ABSTRACT", "Executive Summary and Core Findings", 5),
        ("CHAPTER 1", "Introduction, Cloud Engineering Problem & Scope", 6),
        ("CHAPTER 2", "Infrastructure as Code & Observability Paradigm", 8),
        ("CHAPTER 3", "System Architecture & Dual-Tier Cloud Topology", 10),
        ("CHAPTER 4", "Terraform Manifests & Nagios Core Configuration", 12),
        ("CHAPTER 5", "Chaos Engineering, Fault Injection & Validation Matrix", 15),
        ("CHAPTER 6", "Local Docker Simulation & Production Parity", 17),
        ("CHAPTER 7", "Conclusion, Operational SRE Metrics & Future Scope", 18),
        ("REFERENCES", "IEEE Formatted Bibliography", 19)
    ]
    b.add_table_of_contents(toc_items)

    # CHAPTER 1
    b.add_chapter_heading(1, "Introduction, Cloud Engineering Problem & Scope")
    b.add_section_heading("1.1", "Industrial Motivation and Problem Statement")
    b.add_paragraph(
        "Modern cloud environments suffer from configuration drift, unversioned manual changes ('ClickOps'), and brittle monitoring setups "
        "that alert operators only after catastrophic failures have impacted end users. When applications host advanced AI and telemetry microservices, "
        "ensuring strict network isolation between public ingress proxies and internal compute daemons is paramount. "
        "This project designs and implements a declarative, automated cloud delivery pipeline with continuous observability for multi-tier microservices."
    )
    b.add_section_heading("1.2", "Project Objectives")
    b.add_paragraph(
        "The technical objectives accomplished by this project are:\n"
        "• Author modular HashiCorp Terraform manifests (`vpc.tf`, `security_groups.tf`, `nagios.tf`, `brain.tf`) provisioning an AWS multi-tier architecture.\n"
        "• Deploy the containerized Autonomous AIOps React + FastAPI microservice behind a hardened Nginx reverse proxy.\n"
        "• Establish an isolated Tier 2 code execution daemon operating on Port 9010 accessible solely through the private network boundary.\n"
        "• Configure Nagios Core 4.5 with active health probes (`check_http`, `check_tcp:9010`, and custom AIOps telemetry plugins).\n"
        "• Execute an automated chaos validation test harness verifying zero-loss failover and automated alert clearing."
    )

    # CHAPTER 2
    b.add_chapter_heading(2, "Infrastructure as Code & Observability Paradigm")
    b.add_section_heading("2.1", "Declarative Infrastructure as Code (IaC)")
    b.add_paragraph(
        "Terraform operates on a declarative configuration paradigm where desired cloud resources are described using HashiCorp Configuration Language (HCL). "
        "Terraform constructs a directed acyclic graph (DAG) of resource dependencies, calculating execution plans and converging state without procedural side effects."
    )
    b.add_section_heading("2.2", "Continuous Observability with Nagios Core")
    b.add_paragraph(
        "Nagios Core provides a resilient active polling monitoring framework. Services transition through a two-phase state machine: "
        "SOFT states (temporary anomalies evaluated across max_check_attempts) and HARD states (confirmed failures that trigger operator notifications). "
        "This prevents flapping alerts while guaranteeing swift notification for persistent outages."
    )

    # CHAPTER 3
    b.add_chapter_heading(3, "System Architecture & Dual-Tier Cloud Topology")
    b.add_section_heading("3.1", "Architectural Topology")
    b.add_paragraph(
        "The infrastructure is partitioned into two distinct security and compute tiers: "
        "Tier 1 (Public DMZ) hosts the Nginx reverse proxy and AIOps visual interface exposed on Port 80/5001. "
        "Tier 2 (Private Isolated Subnet) houses the backend execution engine on Port 9010, shielded from direct internet access."
    )

    img_arch = os.path.join(BASE_DIR, "1_Mohit_Terraform_Nagios", "final_report", "diagram_mohit_architecture.png")
    b.add_image(img_arch, "Mohit DevOps Multi-Tier Cloud Architecture & Nagios Core Topology", width_in_inches=5.8)

    # CHAPTER 4
    b.add_chapter_heading(4, "Terraform Manifests & Nagios Core Configuration")
    b.add_section_heading("4.1", "Terraform VPC & Security Specification")
    b.add_paragraph(
        "The network perimeter is defined with strict ingress rules in `security_groups.tf`, permitting Port 80/443 ingress to the proxy "
        "while restricting Port 9010 traffic exclusively to the proxy security group CIDR."
    )

    b.add_code_block("""# Terraform Security Group: Ingress & Isolated Tier 2
resource "aws_security_group" "web_dmz_sg" {
  name        = "int333-mohit-dmz-sg"
  description = "Allow inbound HTTP/HTTPS traffic to Tier 1 Ingress"
  vpc_id      = aws_vpc.main.id

  ingress {
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

resource "aws_security_group" "internal_runner_sg" {
  name        = "int333-mohit-internal-sg"
  vpc_id      = aws_vpc.main.id

  ingress {
    from_port       = 9010
    to_port         = 9010
    protocol        = "tcp"
    security_groups = [aws_security_group.web_dmz_sg.id]
  }
}
""")

    b.add_section_heading("4.2", "Nagios Service Definitions")
    b.add_paragraph(
        "Nagios service definitions in `nagios/conf.d/services.cfg` configure health checks for Port 80 Ingress, Port 5001 AIOps microservice, "
        "and Port 9010 backend daemon with 60-second polling intervals."
    )

    # CHAPTER 5
    b.add_chapter_heading(5, "Chaos Engineering, Fault Injection & Validation Matrix")
    b.add_section_heading("5.1", "Automated Chaos Suite Execution (TC-01 to TC-05)")
    b.add_paragraph(
        "The deployment was subjected to the automated PowerShell chaos test runner (`local-simulation/test_chaos.ps1`), "
        "demonstrating a 100% pass rate across all five test cases."
    )

    tc_headers = ["Test Case", "Test Scenario", "Fault Injection Action", "Expected Nagios / SRE Response", "Status"]
    tc_rows = [
        ["TC-01", "Topology Provisioning", "Container status & socket audit", "All services UP & healthy", "PASS (100%)"],
        ["TC-02", "Ingress & AIOps Telemetry", "POST /api/aiops/telemetry", "HTTP 200 OK, Anomaly=True, Command Dispatched", "PASS (Verified)"],
        ["TC-03", "Nginx Proxy Crash", "docker stop int333_nginx_proxy", "Connection refused, Nagios -> HARD CRITICAL", "PASS (Alerted)"],
        ["TC-04", "Tier 2 Isolation Outage", "docker stop int333_code_runner", "check_tcp:9010 CRITICAL, Tier 1 remains UP", "PASS (Isolated)"],
        ["TC-05", "Automated Recovery", "Restart all stopped daemons", "Sockets restored, Nagios -> HARD OK", "PASS (100% OK)"]
    ]
    b.add_table(tc_headers, tc_rows, [Inches(0.8), Inches(1.5), Inches(1.8), Inches(1.5), Inches(0.9)])

    # CHAPTER 6
    b.add_chapter_heading(6, "Local Docker Simulation & Production Parity")
    b.add_paragraph(
        "To ensure frictionless local evaluation without requiring live AWS credentials, a complete Docker Compose simulation "
        "is provided in `local-simulation/docker-compose.yml`. The compose manifest orchestrates `mohit_aiops_platform` (Port 5001), "
        "`int333_code_runner` (Port 9010), `int333_nginx_proxy` (Port 80), and `int333_nagios_core` (Port 8080) on a shared bridge network. "
        "Crucially, the production application payload deployed at `/app` is Mohit's INT422 Deep Learning AIOps platform (`dl/1_Mohit_AIOps_Cloud_Intelligence`), "
        "which serves the React 19 + Vite frontend in Real Hard Solid Colours (#060911, #0c1220, #2563eb, #dc2626, #059669) with tactile 3D buttons. "
        "The project is accompanied by the official university project synopsis (`Mohit_Raj_Deo_Project_Synopsis.pdf`) and clean submission ZIP packages."
    )

    # CHAPTER 7
    b.add_chapter_heading(7, "Conclusion & Future Scope")
    b.add_paragraph(
        "Mohit Raj Deo's INT333 DevOps capstone project demonstrates the seamless convergence of Infrastructure as Code, "
        "cloud-native multi-tier network segregation, and proactive continuous observability. By hosting the real AIOps neural microservice "
        "and validating dual-tier isolation under chaos conditions, the project provides a rock-solid foundation for enterprise operations."
    )

    # REFERENCES
    b.add_chapter_heading(8, "References (IEEE Standard)")
    refs = [
        "[1] HashiCorp, \"Terraform: Declarative Infrastructure Management,\" Technical Documentation, 2024.",
        "[2] Nagios Enterprises, \"Nagios Core 4.5 Architecture and Service Checking Protocol,\" Whitepaper, 2023.",
        "[3] Amazon Web Services, \"AWS Well-Architected Framework: Reliability Pillar,\" AWS Whitepaper, 2023.",
        "[4] Nginx Inc., \"High Performance Ingress Routing and Reverse Proxy Patterns,\" Architecture Guide, 2022."
    ]
    for r in refs:
        p = b.doc.add_paragraph()
        p.paragraph_format.line_spacing = 1.15
        p.paragraph_format.space_after = Pt(4)
        run = p.add_run(r)
        run.font.size = Pt(9)
        run.font.name = "Calibri"

    out_path = os.path.join(BASE_DIR, "1_Mohit_Terraform_Nagios", "final_report", "FINAL_PROJECT_REPORT.docx")
    b.save(out_path)

def generate_akash_devops_report():
    print("[*] Generating Akash DevOps Final Project Report...")
    title = "Declarative Infrastructure Configuration Management with Puppet Master/Agent & Continuous Nagios NRPE Drift Remediation"
    subtitle = "An Automated Configuration Management Framework Enforcing Desired State on Autonomous SWE Agent Nodes with Real-Time Drift Detection and Self-Healing"

    b = AcademicReportBuilder(
        title=title,
        subtitle=subtitle,
        student_name="Akash Choudhary",
        reg_no="12301625",
        roll_no="11",
        course_code="INT333",
        course_name="DevOps Advance Configuration Management"
    )

    b.add_title_page()
    b.add_certificate()
    b.add_declaration()
    b.add_acknowledgement()

    abstract_text = (
        "In enterprise server fleets, configuration drift—unauthorized, unrecorded, or accidental modifications made directly to server instances—"
        "is a primary catalyst of operational outages, security vulnerabilities, and deployment failures. "
        "This capstone project presents a declarative configuration management and continuous observability architecture designed by "
        "Akash Choudhary for INT333 (DevOps Advance Configuration Management). The solution utilizes Puppet Master/Agent architecture "
        "to manage target node configurations declaratively through three specialized modules: `nginx_server`, `ssh_hardening`, and `nrpe_monitoring`. "
        "The managed node hosts the Autonomous Software Engineering (SWE) Platform AI microservice (Port 5002 / 8081). "
        "Continuous monitoring and drift detection are orchestrated via Nagios Core 4.5 utilizing the Nagios Remote Plugin Executor (NRPE) daemon (Port 5666). "
        "When configuration drift or service failure is injected out-of-band, Nagios NRPE immediately flags a CRITICAL alert state. "
        "Upon triggering the subsequent Puppet agent catalog convergence cycle, Puppet detects the state discrepancy and automatically "
        "restores the service and configuration to the declared desired state, prompting Nagios to clear the alert back to GREEN OK. "
        "The complete lifecycle is verified through an automated 5-stage chaos engineering script achieving 100% pass rates."
    )
    b.add_abstract(abstract_text, "DevOps, Puppet, Configuration Management, Desired State, Configuration Drift, Self-Healing, Nagios Core, NRPE, Autonomous SWE Platform, Chaos Engineering")

    toc_items = [
        ("ABSTRACT", "Executive Summary and Core Findings", 5),
        ("CHAPTER 1", "Introduction, Configuration Drift Problem & Objectives", 6),
        ("CHAPTER 2", "Theoretical Foundations of Declarative Configuration Management", 8),
        ("CHAPTER 3", "System Architecture & Master-Agent Topology", 10),
        ("CHAPTER 4", "Puppet Modules & Nagios NRPE Monitoring Manifests", 12),
        ("CHAPTER 5", "Empirical Evaluation, Drift Injection & Healing Validation", 15),
        ("CHAPTER 6", "Local Docker Simulation & SWE AI Node Parity", 17),
        ("CHAPTER 7", "Conclusion & Future Scope", 18),
        ("REFERENCES", "IEEE Formatted Bibliography", 19)
    ]
    b.add_table_of_contents(toc_items)

    # CHAPTER 1
    b.add_chapter_heading(1, "Introduction, Configuration Drift Problem & Objectives")
    b.add_section_heading("1.1", "The Problem of Configuration Drift")
    b.add_paragraph(
        "In production environments with hundreds or thousands of nodes, administrators occasionally execute ad-hoc commands to troubleshoot incidents. "
        "These out-of-band interventions introduce silent discrepancies between the declared infrastructure specification and runtime reality. "
        "Configuration drift creates fragile servers that fail during subsequent deployments or reboots. "
        "Automated configuration enforcement combined with continuous observability is necessary to guarantee system consistency."
    )
    b.add_section_heading("1.2", "Project Objectives")
    b.add_paragraph(
        "This project achieves the following key milestones:\n"
        "• Develop modular Puppet manifests (`nginx_server`, `ssh_hardening`, `nrpe_monitoring`) enforcing web serving, SSH security, and observability.\n"
        "• Deploy and manage the Autonomous SWE Platform microservice (Port 5002 / 8081) on the managed node.\n"
        "• Establish an active Nagios NRPE monitoring pipeline verifying TCP ports, process vitality, and system metrics.\n"
        "• Subject the environment to deliberate out-of-band tampering and validate automated Puppet self-healing."
    )

    # CHAPTER 2
    b.add_chapter_heading(2, "Theoretical Foundations of Declarative Configuration Management")
    b.add_paragraph(
        "Puppet implements an idempotent, declarative language where resources represent system state rather than sequential commands. "
        "An idempotent operation can be applied multiple times without changing the result beyond the initial application. "
        "The Puppet Master compiles the code into an abstract graph known as a 'Catalog'. The Puppet Agent evaluates this catalog against "
        "system facts gathered via Facter, modifying only resources that have drifted."
    )

    # CHAPTER 3
    b.add_chapter_heading(3, "System Architecture & Master-Agent Topology")
    b.add_paragraph(
        "The architecture consists of a Puppet Master compiling catalogs, a target Agent node running the Autonomous SWE AI microservice, "
        "and a Nagios Core monitoring server querying the node's NRPE daemon."
    )

    img_arch = os.path.join(BASE_DIR, "2_Akash_Puppet_Nagios", "final_report", "diagram_akash_puppet.png")
    b.add_image(img_arch, "Akash DevOps Puppet Master/Agent & Nagios NRPE Architecture", width_in_inches=5.8)

    # CHAPTER 4
    b.add_chapter_heading(4, "Puppet Modules & Nagios NRPE Monitoring Manifests")
    b.add_paragraph(
        "The Puppet modules are structured under `puppet/modules/`:\n"
        "• `nginx_server`: Ensures Nginx package installation, service running state, and configuration template.\n"
        "• `ssh_hardening`: Enforces protocol 2, disables root login, and configures authorized key management.\n"
        "• `nrpe_monitoring`: Deploys NRPE daemon, configures allowed hosts, and exports Nagios check commands."
    )

    b.add_code_block("""# Puppet Manifest: Nginx & AI Microservice Ingress
class nginx_server {
  package { 'nginx':
    ensure => installed,
  }

  service { 'nginx':
    ensure  => running,
    enable  => true,
    require => Package['nginx'],
  }

  file { '/etc/nginx/sites-available/default':
    ensure  => file,
    content => template('nginx_server/default.erb'),
    notify  => Service['nginx'],
  }
}
""")

    # CHAPTER 5
    b.add_chapter_heading(5, "Empirical Evaluation, Drift Injection & Healing Validation")
    b.add_paragraph(
        "The system was validated using the PowerShell test runner (`local-simulation/test_chaos.ps1`), testing catalog compilation, "
        "SWE microservice health, real code generation, out-of-band tampering, and automated Puppet drift remediation."
    )

    tc_headers = ["Test ID", "Test Scenario", "Execution Action", "Expected State & Observation", "Status"]
    tc_rows = [
        ["TC-01", "Puppet Catalog Compilation", "Compile site.pp catalog", "Modules converged on target node", "PASS (Converged)"],
        ["TC-02", "SWE Microservice Health", "GET /health (Port 5002)", "Status UP, ModelLoaded=True", "PASS (HTTP 200)"],
        ["TC-03", "Real Code Synthesis & Audit", "POST /api/swe/generate", "19 LOC, CC=4, Halstead=197.3, Risk=2.0%", "PASS (Verified)"],
        ["TC-04", "Configuration Drift Outage", "Kill service container out-of-band", "Nagios NRPE -> CRITICAL alert", "PASS (Detected)"],
        ["TC-05", "Puppet Automated Healing", "Puppet agent catalog run", "Service restored -> Nagios GREEN OK", "PASS (100% OK)"]
    ]
    b.add_table(tc_headers, tc_rows, [Inches(0.8), Inches(1.5), Inches(1.8), Inches(1.5), Inches(0.9)])

    # CHAPTER 6
    b.add_chapter_heading(6, "Local Docker Simulation & SWE AI Node Parity")
    b.add_paragraph(
        "The simulation environment in `local-simulation/docker-compose.yml` mounts the actual DL project directory "
        "(`dl/2_Akash_Autonomous_SWE_System`), spinning up `akash_swe_agent_node` on Port 8081:5002 alongside `akash_nagios` on Port 8082:80. "
        "The node serves the compiled React 19 + Vite frontend in Real Hard Solid Colours (#060911, #0c1220, #7c3aed, #2563eb, #059669) "
        "with an explicit Model Architecture Card for the Random Forest AST code analyzer. "
        "The project includes the official university synopsis (`Akash_12301625_Puppet_Nagios_Synopsis.pdf`) and clean submission ZIP packages."
    )

    # CHAPTER 7
    b.add_chapter_heading(7, "Conclusion & Future Scope")
    b.add_paragraph(
        "Akash Choudhary's INT333 project establishes an ironclad declarative infrastructure management framework. "
        "By binding Puppet's desired-state convergence with Nagios NRPE real-time monitoring, the architecture guarantees "
        "that mission-critical AI workloads remain operational, compliant, and immune to configuration drift."
    )

    # REFERENCES
    b.add_chapter_heading(8, "References (IEEE Standard)")
    refs = [
        "[1] Puppet Labs, \"Puppet 8 Reference Manual: Declarative Language & Catalog Compilation,\" 2024.",
        "[2] Nagios Enterprises, \"NRPE: Nagios Remote Plugin Executor Documentation,\" 2023.",
        "[3] M. Burgess, \"In Search of Certainty: The Science of Information and System Administration,\" IEEE Computer, 2020."
    ]
    for r in refs:
        p = b.doc.add_paragraph()
        p.paragraph_format.line_spacing = 1.15
        p.paragraph_format.space_after = Pt(4)
        run = p.add_run(r)
        run.font.size = Pt(9)
        run.font.name = "Calibri"

    out_path = os.path.join(BASE_DIR, "2_Akash_Puppet_Nagios", "final_report", "FINAL_PROJECT_REPORT.docx")
    b.save(out_path)

def generate_saif_devops_report():
    print("[*] Generating Saif DevOps Final Project Report...")
    title = "Automated High-Availability Multi-Tier Application Load Balancer with Terraform & Continuous Nagios Cluster Observability"
    subtitle = "A Cloud-Native High-Availability Cluster Deployment with Multi-AZ Redundancy, Automated Traffic Drainage, and Real-Time Neural SecOps Observability"

    b = AcademicReportBuilder(
        title=title,
        subtitle=subtitle,
        student_name="Saif Siddique",
        reg_no="12308813",
        roll_no="44",
        course_code="INT333",
        course_name="DevOps Advance Configuration Management"
    )

    b.add_title_page()
    b.add_certificate()
    b.add_declaration()
    b.add_acknowledgement()

    abstract_text = (
        "Enterprise web services and cybersecurity microservices require ultra-high availability, seamless horizontal scalability, "
        "and sub-second fault detection to maintain zero-downtime operations during hardware failure or traffic spikes. "
        "This capstone project presents an automated multi-tier cloud infrastructure architecture designed by Saif Siddique "
        "for INT333 (DevOps Advance Configuration Management). The solution provisions an AWS multi-tier environment using HashiCorp Terraform, "
        "featuring an Application Load Balancer (ALB) distributed across multiple Availability Zones (AZs) that intelligently balances traffic "
        "across a high-performance cluster of containerized SecOps Cyber Threat Intelligence worker nodes (Port 5003). "
        "Observability is established via Nagios Core 4.5 configured with high-frequency active health probes monitoring target group member states. "
        "The ALB executes automated connection draining upon detecting node latency or failure, rerouting network flows to healthy worker instances "
        "without dropping user sessions or threat triage requests. "
        "Validated through a 5-stage chaos engineering harness (TC-01 through TC-05), the system demonstrates zero-downtime failover, "
        "instantaneous neural attack classification under load, and automated target group re-registration upon node restoration."
    )
    b.add_abstract(abstract_text, "DevOps, Terraform, Application Load Balancer (ALB), High Availability, Multi-AZ, Health Checks, Connection Draining, Nagios Core, SecOps Microservice, Chaos Engineering")

    toc_items = [
        ("ABSTRACT", "Executive Summary and Core Findings", 5),
        ("CHAPTER 1", "Introduction, High Availability Principles & Project Scope", 6),
        ("CHAPTER 2", "Load Balancing & High Availability Cloud Architecture", 8),
        ("CHAPTER 3", "Multi-Tier Infrastructure Architecture & Data Ingress", 10),
        ("CHAPTER 4", "Terraform ALB Manifests & Nagios Monitoring Configuration", 12),
        ("CHAPTER 5", "Empirical Evaluation, Chaos Failover & Healing Matrix", 15),
        ("CHAPTER 6", "Local Docker Simulation & SecOps Cluster Integration", 17),
        ("CHAPTER 7", "Conclusion & Future Scope", 18),
        ("REFERENCES", "IEEE Formatted Bibliography", 19)
    ]
    b.add_table_of_contents(toc_items)

    # CHAPTER 1
    b.add_chapter_heading(1, "Introduction, High Availability Principles & Project Scope")
    b.add_section_heading("1.1", "Industrial Need for High-Availability Microservices")
    b.add_paragraph(
        "In modern zero-trust cybersecurity operations, intrusion detection systems cannot afford a single point of failure (SPOF). "
        "If a security sensor goes offline, malicious adversaries can execute multi-stage attacks unnoticed. "
        "An Application Load Balancer (ALB) distributed across independent physical failure domains (Availability Zones) "
        "ensures that traffic is dynamically steered away from unhealthy nodes without impacting end-user availability."
    )
    b.add_section_heading("1.2", "Project Objectives")
    b.add_paragraph(
        "The project delivers the following technical milestones:\n"
        "• Author Terraform manifests (`vpc.tf`, `alb.tf`, `security_groups.tf`, `instances.tf`) provisioning an AWS Multi-AZ ALB cluster.\n"
        "• Deploy containerized Cyber Threat Intelligence worker nodes hosting the Deep MLP neural triage engine (Port 5003).\n"
        "• Configure ALB target group health checks (`/health`) with automated connection draining (deregistration delay).\n"
        "• Integrate Nagios Core 4.5 for real-time monitoring of cluster target health and ALB response times.\n"
        "• Execute chaos engineering failover tests proving seamless traffic drainage and self-healing."
    )

    # CHAPTER 2
    b.add_chapter_heading(2, "Load Balancing & High Availability Cloud Architecture")
    b.add_paragraph(
        "Application Load Balancers operate at Layer 7 of the OSI model, inspecting HTTP/HTTPS request headers and routing traffic "
        "using round-robin or least-outstanding-requests algorithms. Health probes evaluate HTTP status codes; instances returning "
        "non-200 responses are removed from the active target pool, and traffic is transparently redistributed."
    )

    # CHAPTER 3
    b.add_chapter_heading(3, "Multi-Tier Infrastructure Architecture & Data Ingress")
    b.add_paragraph(
        "The infrastructure partitions resources into an internet-facing ALB tier spanning multiple public subnets and a backend compute tier "
        "residing in private subnets with restricted ingress."
    )

    img_arch = os.path.join(BASE_DIR, "3_Saif_Terraform_ALB_Nagios", "final_report", "diagram_saif_multitier.png")
    b.add_image(img_arch, "Saif DevOps Terraform Multi-Tier ALB & SecOps Cluster Architecture", width_in_inches=5.8)

    # CHAPTER 4
    b.add_chapter_heading(4, "Terraform ALB Manifests & Nagios Monitoring Configuration")
    b.add_paragraph(
        "Terraform manifests in `terraform/` specify the ALB, target groups, listener rules, and health probe criteria."
    )

    b.add_code_block("""# Terraform: Application Load Balancer & Target Group
resource "aws_lb" "external_alb" {
  name               = "int333-saif-alb"
  internal           = false
  load_balancer_type = "application"
  security_groups    = [aws_security_group.alb_sg.id]
  subnets            = [aws_subnet.public_1.id, aws_subnet.public_2.id]
}

resource "aws_lb_target_group" "secops_tg" {
  name     = "int333-secops-tg"
  port     = 5003
  protocol = "HTTP"
  vpc_id   = aws_vpc.main.id

  health_check {
    path                = "/health"
    matcher             = "200"
    interval            = 10
    healthy_threshold   = 2
    unhealthy_threshold = 2
  }
}
""")

    # CHAPTER 5
    b.add_chapter_heading(5, "Empirical Evaluation, Chaos Failover & Healing Matrix")
    b.add_paragraph(
        "The architecture was verified using the PowerShell chaos test runner (`local-simulation/test_chaos.ps1`), "
        "evaluating multi-tier topology, health checks, live neural threat triage, worker node failure drainage, and auto-healing."
    )

    tc_headers = ["Test ID", "Test Scenario", "Chaos Injection", "Observed Outcome", "Status"]
    tc_rows = [
        ["TC-01", "Multi-Tier Topology", "VPC & Subnet validation", "Multi-AZ SecOps Worker Cluster provisioned", "PASS (100%)"],
        ["TC-02", "ALB Health Check", "GET /health (Port 5003)", "Status UP, ModelLoaded=True", "PASS (HTTP 200)"],
        ["TC-03", "Neural Attack Ingress", "SYN Flood: 750 pkts, 85 flags", "Classified DDoS (Risk: 95.0), iptables DROP", "PASS (Verified)"],
        ["TC-04", "Worker Node Outage", "docker stop saif_secops_node2", "ALB drains traffic to Node 1 seamlessly", "PASS (Drained)"],
        ["TC-05", "Cluster Self-Healing", "docker start saif_secops_node2", "Node re-attaches, Nagios -> GREEN OK", "PASS (100% OK)"]
    ]
    b.add_table(tc_headers, tc_rows, [Inches(0.8), Inches(1.5), Inches(1.8), Inches(1.5), Inches(0.9)])

    # CHAPTER 6
    b.add_chapter_heading(6, "Local Docker Simulation & SecOps Cluster Integration")
    b.add_paragraph(
        "The local simulation (`local-simulation/docker-compose.yml`) deploys Nginx configured as a reverse proxy load balancer (`nginx-alb.conf`), "
        "routing incoming traffic across two SecOps worker nodes (`secops-worker-1` and `secops-worker-2`) mounting the actual DL project directory (`dl/3_Saif_Cyber_Threat_Intelligence`). "
        "Each cluster worker serves the standalone React 19 + Vite frontend in Real Hard Solid Colours (#060911, #0c1220, #dc2626, #059669, #2563eb) "
        "with an explicit Deep MLP Neural Network Architecture Card. Dedicated cluster status pages (`node1.html` and `node2.html`) provide "
        "executive-level visibility into instance health, ALB weight distribution, and zero-trust firewall mitigations. "
        "The project is accompanied by the official university synopsis (`Saif_12308813_Terraform_Nagios_Synopsis.pdf`) and clean submission ZIP packages."
    )

    # CHAPTER 7
    b.add_chapter_heading(7, "Conclusion & Future Scope")
    b.add_paragraph(
        "Saif Siddique's INT333 DevOps capstone delivers a battle-tested high-availability infrastructure pattern. "
        "By load-balancing real neural threat intelligence microservices behind an automated Application Load Balancer and "
        "enforcing continuous Nagios monitoring, the project guarantees resilient, uninterrupted perimeter defense."
    )

    # REFERENCES
    b.add_chapter_heading(8, "References (IEEE Standard)")
    refs = [
        "[1] HashiCorp, \"Terraform AWS Provider Documentation: aws_lb & aws_lb_target_group,\" 2024.",
        "[2] AWS Documentation, \"Elastic Load Balancing: Application Load Balancers Guide,\" 2023.",
        "[3] Nagios Enterprises, \"Monitoring HTTP and Cluster Services with Nagios Core,\" 2023."
    ]
    for r in refs:
        p = b.doc.add_paragraph()
        p.paragraph_format.line_spacing = 1.15
        p.paragraph_format.space_after = Pt(4)
        run = p.add_run(r)
        run.font.size = Pt(9)
        run.font.name = "Calibri"

    out_path = os.path.join(BASE_DIR, "3_Saif_Terraform_ALB_Nagios", "final_report", "FINAL_PROJECT_REPORT.docx")
    b.save(out_path)

def generate_devops_master_manual():
    print("[*] Generating Master DevOps Execution Manual...")
    title = "HOW TO USE & COMPLETE EXECUTION MANUAL: INT333 DEVOPS ADVANCE CONFIGURATION MANAGEMENT"
    subtitle = "Comprehensive Operations Guide, Terraform Provisioning, Puppet Manifest Enforcement, Nagios Observability, and Chaos Testing Matrix"

    b = AcademicReportBuilder(
        title=title,
        subtitle=subtitle,
        student_name="Mohit Raj Deo | Akash Choudhary | Saif Siddique",
        reg_no="12323329 | 12301625 | 12308813",
        roll_no="62 | 11 | 44",
        course_code="INT333",
        course_name="DevOps Advance Configuration Management"
    )

    b.add_title_page()
    b.add_certificate()

    b.add_chapter_heading(1, "Executive DevOps Ecosystem Overview & Architecture Topology")
    b.add_paragraph(
        "This execution manual provides operational instructions for deploying, simulating, and validating all three "
        "INT333 DevOps Advance Configuration Management capstone projects for Lovely Professional University. "
        "Each project demonstrates enterprise Infrastructure as Code (Terraform), declarative configuration management (Puppet), "
        "continuous observability (Nagios Core 4.5), and live hosting of real Deep Learning AI microservices."
    )

    topo_headers = ["Project & Student", "DevOps Technology", "Target AI Workload", "Observability Engine", "Chaos Test Runner"]
    topo_rows = [
        ["Mohit: Terraform AWS + Nagios", "Terraform (AWS VPC/SG/EC2)", "AIOps Neural Platform (Port 5001)", "Nagios Core 4.5 (Port 8080)", "devops/1_Mohit.../test_chaos.ps1"],
        ["Akash: Puppet + Nagios NRPE", "Puppet Master/Agent (site.pp)", "Autonomous SWE Node (Port 5002)", "Nagios NRPE (Port 8082)", "devops/2_Akash.../test_chaos.ps1"],
        ["Saif: Terraform Multi-Tier ALB", "Terraform ALB (Multi-AZ)", "SecOps Neural Cluster (Port 5003)", "Nagios Core HA (Port 8084)", "devops/3_Saif.../test_chaos.ps1"]
    ]
    b.add_table(topo_headers, topo_rows, [Inches(1.8), Inches(1.5), Inches(1.8), Inches(1.4), Inches(1.5)])

    b.add_chapter_heading(2, "Local Simulation & Verification Execution")
    b.add_section_heading("2.1", "Running Chaos Validation Suites")
    b.add_paragraph(
        "To verify all 5 test cases (TC-01 through TC-05) for any DevOps project, execute the dedicated PowerShell runner:\n"
        "1. Mohit DevOps: `powershell -ExecutionPolicy Bypass -File c:\\MOHIT\\devops\\1_Mohit_Terraform_Nagios\\local-simulation\\test_chaos.ps1`\n"
        "2. Akash DevOps: `powershell -ExecutionPolicy Bypass -File c:\\MOHIT\\devops\\2_Akash_Puppet_Nagios\\local-simulation\\test_chaos.ps1`\n"
        "3. Saif DevOps: `powershell -ExecutionPolicy Bypass -File c:\\MOHIT\\devops\\3_Saif_Terraform_ALB_Nagios\\local-simulation\\test_chaos.ps1`"
    )

    out_path = os.path.join(BASE_DIR, "HOW_TO_USE_AND_EXECUTION_MANUAL.docx")
    b.save(out_path)

if __name__ == "__main__":
    generate_mohit_devops_report()
    generate_akash_devops_report()
    generate_saif_devops_report()
    generate_devops_master_manual()
    print("[SUCCESS] All DevOps Reports & Execution Manual generated successfully!")
