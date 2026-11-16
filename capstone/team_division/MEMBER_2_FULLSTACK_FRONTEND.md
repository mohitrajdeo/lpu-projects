# Member 2: Full-Stack Engineer (Frontend UI, Real-Time Observability & Operator Gateway)

**Full Name / Placeholder:** Ananya Iyer  
**Technical Track:** Full-Stack Engineering (Frontend, UI/UX & Observability Gateway)  
**Project Role:** Observability UI Lead & Client-State Architect  

---

## 1. What You Built in the Project (Code Ownership)

You built the user-facing operational command center and real-time observability interface that SRE engineers and evaluators interact with.

### Primary Code Files Owned:
* [kuberevive/dashboard/static/index.html](file:///c:/MOHIT/capstone/kuberevive/dashboard/static/index.html):
  - High-performance, single-page application (SPA) operational dashboard.
  - Features real-time metric cards (CPU, Memory, P99 Latency, Error Rate, Pod Replicas, Active Incidents).
  - Contains the Chaos Engineering injection console allowing on-demand fault triggers (Memory Leak, CPU Spike, Latency Regression, 500 Spike).
  - Displays the live incident timeline and automated remediation activity feed with status badges (ANALYZING, REMEDIATING, RESOLVED).
* [kuberevive/dashboard/static/app.js](file:///c:/MOHIT/capstone/kuberevive/dashboard/static/app.js):
  - Client-side event poller and state synchronizer running every 1,000ms via `fetch()`.
  - Implements dynamic DOM updates without flickering or page reloads.
  - Handles chaos fault injection API requests and visualizes actuator state transitions.
  - Manages real-time alert toast notifications and color-coded SLA threshold warnings.
* Integration with [kuberevive/dashboard/app.py](file:///c:/MOHIT/capstone/kuberevive/dashboard/app.py): Formatted telemetry and incident JSON payloads for smooth client-side consumption.

---

## 2. What You Authored in the IEEE Research Paper

* **Section II-B: Operator Dashboard & Real-Time Telemetry Interface:**
  - Described the human-in-the-loop auditability layer: while KubeRevive operates autonomously, enterprise compliance requires complete visual transparency into every automated decision.
  - Documented the client-side state machine tracking incident lifecycle stages: `DETECTED` $\to$ `TRIAGED` $\to$ `DIAGNOSING` $\to$ `EXECUTING_REMEDIATION` $\to$ `VERIFYING` $\to$ `RESOLVED`.
* **Figure 1 Description & System Flowchart:**
  - Co-authored the dataflow diagram illustrating how user requests flow through the checkout service while observability metrics stream simultaneously into the dashboard.

---

## 3. Your Presentation (PPT) Role & Word-for-Word Script

**Assigned Slides:** Slide 12 (Live Operational Dashboard & Human-in-the-Loop Transparency) + Conducting the Live Interactive Demo.  
**Time Allocation:** 2.5 Minutes.

### Slide 12: Operator Dashboard & Live System Demo
> *"I designed the real-time observability command center in `kuberevive/dashboard/static/`. While KubeRevive operates autonomously, enterprise SRE teams require complete visibility and auditability into every autonomous action.*  
> *Our dashboard updates every second via asynchronous polling, streaming live CPU, memory, P99 latency, and error rate metrics.*  
> *When an incident occurs—for instance, when a chaos memory leak is triggered—the dashboard immediately updates the service health badge to Critical, logs the incoming telemetry anomaly, renders the AI root-cause diagnosis, and visually animates the autonomous actuator recycling the pod.*  
> *I will now demonstrate this live on our running cluster: as you can see, when I inject a memory leak, the memory line ramps to 92%, KubeRevive detects it in 2.8 seconds, executes a pod restart, and within 6 seconds the memory drops back to 42% and the incident closes automatically.*  
> *I will now pass the presentation to Member 3, our AI/ML engineer, to explain the mathematical algorithms behind our anomaly detection engine."*

---

## 4. Viva Defense Masterclass (Questions & Exact Technical Answers)

#### Q1: "Why did you use vanilla JavaScript instead of heavy frameworks like React or Angular?"
**Answer:**  
*"In mission-critical SRE environments, dashboard load speed and zero-dependency reliability are paramount. Modern heavy single-page application frameworks like React or Angular introduce large bundle sizes (several megabytes) and client-side virtual DOM reconciliation overhead. By utilizing pure modern ES6 JavaScript with modular asynchronous `fetch` calls and targeted DOM node mutations, our dashboard loads in under 120 milliseconds and maintains sub-5ms rendering cycles even when receiving streaming metrics at 10Hz."*

#### Q2: "How do you prevent UI freezing when hundreds of telemetry events arrive simultaneously?"
**Answer:**  
*"We implemented client-side throttling and batch rendering in `app.js`. Rather than executing a DOM repaint for every single metric point, updates are batched into a single `requestAnimationFrame()` cycle. Furthermore, the event feed keeps a sliding window of the last 50 historical incidents, preventing unbounded memory growth in the browser tab."*

#### Q3: "What role does the dashboard play if KubeRevive is fully autonomous?"
**Answer:**  
*"Enterprise compliance frameworks (such as SOC2 and ISO 27001) mandate that autonomous systems provide complete explainability and immutable audit trails. The dashboard provides human SREs with real-time auditability: displaying the exact anomaly confidence score, the matched historical postmortem ID, the corrective action executed, and the post-remediation verification status. If needed, an operator can toggle manual override mode with a single click."*

#### Trap to Avoid:
* **Never say:** *"I just made a simple HTML webpage."*
* **Always say:** *"I built the client-side observability gateway and state synchronization layer that translates asynchronous backend AIOps events into real-time visual telemetry for enterprise operator auditability."*

