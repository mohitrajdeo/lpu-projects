# INT333: DevOps Advance Configuration Management
# Comprehensive Student & Evaluator Execution Manual
## How to Run, Test, Present, and Evaluate All 3 Capstone Projects

**Institution:** Department of Computer Science and Engineering, Lovely Professional University  
**Course Code:** INT333 – DevOps Advance Configuration Management  
**Faculty Guide:** Ms. Manpreet Kaur, Assistant Professor  

---

## 📑 Table of Contents
1. [Project Overview & Folder Structure](#1-project-overview--folder-structure)
2. [How to View and Submit the Final Reports (.docx & .pdf)](#2-how-to-view-and-submit-the-final-reports)
3. [How to Present the Slide Decks (PPT via HTML)](#3-how-to-present-the-slide-decks)
4. [Project 1 (Mohit Raj Deo) - Step-by-Step Execution Guide](#4-project-1-mohit-raj-deo---execution-guide)
5. [Project 2 (Akash Choudhary) - Step-by-Step Execution Guide](#5-project-2-akash-choudhary---execution-guide)
6. [Project 3 (Saif Siddique) - Step-by-Step Execution Guide](#6-project-3-saif-siddique---execution-guide)
7. [Submitting and Pushing (Zip Archives & Git)](#7-submitting-and-pushing)

---

## 1. Project Overview & Folder Structure

The workspace is organized into three completely autonomous, self-contained folders:

```
c:\MOHIT\devops\
│
├── 1_Mohit_Terraform_Nagios/         # Mohit Raj Deo (12323329, Roll: 62)
│   ├── final_report/                 # FINAL_PROJECT_REPORT.docx & .pdf + Architecture Diagram
│   ├── presentation/                 # Interactive HTML5 16:9 Slide Deck
│   ├── terraform/                    # AWS ap-south-1 IaC manifests
│   ├── app/                          # Developer Portal UI + Port 9010 Code Runner
│   ├── nagios/                       # Nagios Core 4.5.2 Dual-Tier Probing configs
│   ├── local-simulation/             # Local Docker test cluster + test_chaos.ps1
│   ├── HOW_TO_RUN_AND_USE.md         # Detailed project guide
│   └── Mohit_Raj_Deo_...pdf          # Approved university synopsis
│
├── 2_Akash_Puppet_Nagios/            # Akash Choudhary (12301625, Roll: 11)
│   ├── final_report/                 # FINAL_PROJECT_REPORT.docx & .pdf + Architecture Diagram
│   ├── presentation/                 # Interactive HTML5 16:9 Slide Deck
│   ├── puppet/                       # Puppet Master site.pp & Custom Modules (Nginx, SSH, NRPE)
│   ├── nagios/                       # Nagios Core & NRPE Monitoring configs
│   ├── local-simulation/             # Local Docker cluster + test_chaos.ps1
│   ├── HOW_TO_RUN_AND_USE.md         # Detailed project guide
│   └── Akash_12301625_...pdf         # Approved university synopsis
│
└── 3_Saif_Terraform_ALB_Nagios/      # Saif Siddique (12308813, Roll: 44)
    ├── final_report/                 # FINAL_PROJECT_REPORT.docx & .pdf + Architecture Diagram
    ├── presentation/                 # Interactive HTML5 16:9 Slide Deck
    ├── terraform/                    # Multi-Tier AWS ALB & Private Subnet manifests
    ├── nagios/                       # Nagios Core & NRPE Telemetry configs
    ├── local-simulation/             # Local Docker ALB cluster + test_chaos.ps1
    ├── HOW_TO_RUN_AND_USE.md         # Detailed project guide
    └── Saif_12308813_...pdf          # Approved university synopsis
```

---

## 2. How to View and Submit the Final Reports

Each folder contains an academic final report ready for grading and submission:

- **Microsoft Word Format (`.docx`):** Fully editable, standard academic typography, cover page, certificate of original work, declaration, abstract, and **embedded high-resolution architecture diagrams**.
- **Adobe PDF Format (`.pdf`):** Converted directly from Microsoft Word, preserving all layout, pagination, tables, and color diagrams.

### Direct File Paths:
- **Mohit:**
  - `c:\MOHIT\devops\1_Mohit_Terraform_Nagios\final_report\FINAL_PROJECT_REPORT.docx`
  - `c:\MOHIT\devops\1_Mohit_Terraform_Nagios\final_report\FINAL_PROJECT_REPORT.pdf`
- **Akash:**
  - `c:\MOHIT\devops\2_Akash_Puppet_Nagios\final_report\FINAL_PROJECT_REPORT.docx`
  - `c:\MOHIT\devops\2_Akash_Puppet_Nagios\final_report\FINAL_PROJECT_REPORT.pdf`
- **Saif:**
  - `c:\MOHIT\devops\3_Saif_Terraform_ALB_Nagios\final_report\FINAL_PROJECT_REPORT.docx`
  - `c:\MOHIT\devops\3_Saif_Terraform_ALB_Nagios\final_report\FINAL_PROJECT_REPORT.pdf`

---

## 3. How to Present the Slide Decks (PPT via HTML)

Each project includes an interactive 16:9 presentation slide deck:

1. Double-click `presentation\index.html` in your browser (Chrome, Edge, Firefox).
2. **Keyboard Controls:**
   - **`→` or `Space`**: Next slide
   - **`←`**: Previous slide
   - **`F`**: Toggle Fullscreen presentation mode
   - **`Home` / `End`**: First / Last slide
3. **Export to PDF Presentation:**
   - Press **`Ctrl + P`** (or click the **🖨️ PDF** button on the bottom bar).
   - Destination: **Save as PDF**
   - Layout: **Landscape**
   - Background Graphics: **Checked**
   - Margins: **None**

---

## 4. Project 1 (Mohit Raj Deo) - Step-by-Step Execution Guide

### Option A: 1-Click Local Simulation & Chaos Testing (Zero Cloud Cost)
1. Open PowerShell and navigate to the local simulation directory:
   ```powershell
   cd c:\MOHIT\devops\1_Mohit_Terraform_Nagios\local-simulation
   ```
2. Start the multi-container cluster:
   ```powershell
   docker compose up -d
   ```
3. Open the web interfaces in your browser:
   - **Developer Web Portal:** [http://localhost](http://localhost) (Try running Python or JS code in the interactive playground)
   - **Nagios Observability Console:** [http://localhost:8080](http://localhost:8080)
     - Username: `nagiosadmin`
     - Password: `int333devopspassword`
4. Run the automated Chaos Test Runner:
   ```powershell
   .\test_chaos.ps1
   ```
   *This automatically executes test cases TC-01 through TC-05 (normal ingress, front-end crash detection, port 9010 failure isolation, and automated restoration).*

### Option B: Deploying to Real AWS Cloud via Terraform
1. Configure your AWS credentials (`aws configure`).
2. Navigate to `terraform/`:
   ```powershell
   cd c:\MOHIT\devops\1_Mohit_Terraform_Nagios\terraform
   terraform init
   terraform plan
   terraform apply -auto-approve
   ```
3. Terraform will output the public Elastic IP and Nagios console URL upon completion.

---

## 5. Project 2 (Akash Choudhary) - Step-by-Step Execution Guide

### Local Drift Remediation & Chaos Testing
1. Navigate to the local simulation directory:
   ```powershell
   cd c:\MOHIT\devops\2_Akash_Puppet_Nagios\local-simulation
   ```
2. Start the containers:
   ```powershell
   docker compose up -d
   ```
3. Open web interfaces:
   - **Agent 1 Web Server:** [http://localhost:8081](http://localhost:8081)
   - **Nagios Monitoring Console:** [http://localhost:8082](http://localhost:8082) (`nagiosadmin` / `akash12301625`)
4. Run the Chaos & Drift Test Runner:
   ```powershell
   .\test_chaos.ps1
   ```
   *Demonstrates manual sabotage of Nginx, Nagios alert escalation, and automated Puppet catalog remediation.*

---

## 6. Project 3 (Saif Siddique) - Step-by-Step Execution Guide

### Local Load Balancer & Chaos Testing
1. Navigate to the local simulation directory:
   ```powershell
   cd c:\MOHIT\devops\3_Saif_Terraform_ALB_Nagios\local-simulation
   ```
2. Start the cluster:
   ```powershell
   docker compose up -d
   ```
3. Open web interfaces:
   - **ALB Ingress Endpoint:** [http://localhost:8083](http://localhost:8083) (Refresh to observe round-robin distribution between Node 1 and Node 2)
   - **Nagios Monitoring Console:** [http://localhost:8084](http://localhost:8084) (`nagiosadmin` / `saif12308813`)
4. Run the Chaos Test Runner:
   ```powershell
   .\test_chaos.ps1
   ```
   *Demonstrates memory stress injection, node failure drainage, and target group recovery.*

---

## 7. Submitting and Pushing (Zip Archives & Git)

### Ready-Made Zip Archives:
In the root directory `c:\MOHIT\devops\`, pre-packaged zip archives are available for instant submission:
1. `Mohit_12323329_Terraform_Nagios.zip` (Mohit's complete project package)
2. `Akash_12301625_Puppet_Nagios.zip` (Akash's complete project package)
3. `Saif_12308813_Terraform_ALB_Nagios.zip` (Saif's complete project package)
4. `ALL_3_DEVOPS_PROJECTS_MASTER.zip` (Master bundle of all three projects)

### Pushing to GitHub:
```powershell
cd c:\MOHIT\devops
git init
git add .
git commit -m "Complete INT333 Capstone Projects: Reports, PPTs, Terraform, Puppet, and Chaos Suites"
git branch -M main
git remote add origin <your-github-repo-url>
git push -u origin main
```

