# Member 3: AI/ML Engineer 1 (Time-Series Anomaly Detection & Isolation Forest Ensemble)

**Full Name / Placeholder:** Aarav Gupta  
**Technical Track:** Artificial Intelligence & Machine Learning (Time-Series & Unsupervised ML)  
**Project Role:** Anomaly Detection Lead & Mathematical Modeling Specialist  

---

## 1. What You Built in the Project (Code Ownership)

You formulated and implemented the mathematical core of the anomaly detection engine that identifies multi-variate metric failures in streaming cloud telemetry.

### Primary Code Files Owned:
* [kuberevive/anomaly_detection/metrics_detector.py](file:///c:/MOHIT/capstone/kuberevive/anomaly_detection/metrics_detector.py):
  - Formulated the **Dynamic Rolling Z-Score & EWMA Detector**: maintains sliding windows ($W=30$) dynamically updating mean $\mu_{j,t}$ and sample standard deviation $\sigma_{j,t}$.
  - Engineered the **Multi-Variate Isolation Forest Ensemble**: an unsupervised ensemble of $T=100$ isolation trees (`sklearn.ensemble.IsolationForest`) trained over normalized telemetry vectors (CPU, Memory, P99 Latency, Error Rate, RPS).
  - Formulated the **Hybrid Anomaly Scorer**: combining single-variate statistical bounds with multi-variate isolation tree depths to suppress false alarms during traffic surges.
* [tests/test_anomaly_detection.py](file:///c:/MOHIT/capstone/tests/test_anomaly_detection.py):
  - Comprehensive unit test suite verifying mathematical edge cases (e.g., zero-variance divisions, sudden spikes, multi-variate drift).

---

## 2. What You Authored in the IEEE Research Paper

* **Section III-A: Hybrid Telemetry Anomaly Detection:**
  - Formulated Equations (1) and (2) for dynamic sliding window mean and sample variance:
    $$\mu_{j,t} = \frac{1}{W} \sum_{k=0}^{W-1} x_{j,t-k}, \quad \sigma_{j,t} = \sqrt{\frac{1}{W-1} \sum_{k=0}^{W-1} (x_{j,t-k} - \mu_{j,t})^2}$$
  - Formulated the standardized Z-Score deviation with variance floor $\epsilon = 10^{-6}$:
    $$z_{j,t} = \frac{|x_{j,t} - \mu_{j,t}|}{\max(\sigma_{j,t}, \epsilon)}$$
  - Formulated Equation (3) and (4) for Isolation Forest anomaly score $s(\mathbf{x}_t, n)$ and Binary Search Tree average path length $c(n)$ incorporating the Euler-Mascheroni constant ($\gamma \approx 0.5772156649$):
    $$s(\mathbf{x}_t, n) = 2^{-\frac{\mathbb{E}(h(\mathbf{x}_t))}{c(n)}}, \quad c(n) = 2\left(\ln(n - 1) + 0.5772156649\right) - \frac{2(n - 1)}{n}$$
* **Figure 2 & Table I (Ablation Study):**
  - Proved that the Hybrid Ensemble outperforms standalone Z-Score ($F1 = 79.8\%$) and standalone Isolation Forest ($F1 = 86.7\%$), reaching **$F1 = 93.0\%$ with $94.2\%$ precision**.

---

## 3. Your Presentation (PPT) Role & Word-for-Word Script

**Assigned Slides:** Slide 4 (Anomaly Detection Engine: Z-Score + Isolation Forest Ensemble).  
**Time Allocation:** 3 Minutes.

### Slide 4: Hybrid Anomaly Detection Engine
> *"I designed and formulated the anomaly detection engine in `kuberevive/anomaly_detection/metrics_detector.py`.*  
> *In production microservices, anomaly detection faces two fundamental hurdles: first, diurnal traffic fluctuations trigger false alarms in static threshold systems; second, complex distributed failures often exhibit normal individual metrics while their joint distribution is broken—such as normal CPU accompanied by an explosive latency spike.*  
> *To solve this, I designed a **two-tier Hybrid Ensemble** combining statistical time-series tracking with unsupervised machine learning:*  
> *1. Tier 1 is a dynamic Rolling Z-Score with Exponential Weighted Moving Average across a sliding window of 30 observations. This immediately isolates rapid, sharp single-metric boundary leaps within 1 tick.*  
> *2. Tier 2 is an unsupervised **Isolation Forest** comprising 100 isolation trees. Rather than calculating normal data clusters, it exploits the fact that anomalies are few and different, isolating them at shallow tree depths.*  
> *In our paper, we normalized the path length using the Binary Search Tree average unsuccessful search formula $c(n)$ with the Euler-Mascheroni constant.*  
> *In our empirical ablation study, neither model alone is sufficient: Z-Score alone produced 36% false alarms during benign traffic surges, while Isolation Forest alone had higher latency on sharp single-metric spikes. Our Hybrid Ensemble achieved 94.2% precision and 91.8% recall.*  
> *I now invite Member 4, our GenAI and NLP lead, to explain how our agentic triage and dense RAG engine deduces the root cause."*

---

## 4. Viva Defense Masterclass (Questions & Exact Technical Answers)

#### Q1: "Why use Isolation Forest instead of an LSTM or Autoencoder neural network?"
**Answer:**  
*"While LSTMs and Deep Autoencoders can model sequential patterns, they have major drawbacks in online cloud operations: high training latency, substantial GPU compute costs, and vulnerability to catastrophic forgetting when traffic regimes shift. In contrast, Isolation Forest has $O(T \cdot \psi \log \psi)$ linear time complexity (where $\psi=256$ is the sub-sampling size). It executes inference in under 15 milliseconds on a single standard CPU core without GPU requirements, making it ideal for edge and containerized AIOps."*

#### Q2: "What is the purpose of $c(n)$ in the Isolation Forest equation?"
**Answer:**  
*"In Equation (4), $c(n)$ represents the average path length of unsuccessful searches in a Binary Search Tree constructed over $n$ instances. It acts as an equivalent normalization denominator for the tree depth $h(x)$. When the average path length $\mathbb{E}(h(x)) \to 0$, the anomaly score $s \to 2^0 = 1$, indicating an anomaly that was isolated close to the root of the tree. When $\mathbb{E}(h(x)) \to c(n)$, $s \to 0.5$, indicating a normal observation."*

#### Q3: "How does your rolling Z-score handle cold-start when a service just booted up?"
**Answer:**  
*"During the warm-up period (when the window size $k < 10$), the detector relies on a pre-calibrated baseline variance and enforces an epsilon floor ($\epsilon = 10^{-6}$) in the denominator to avoid division-by-zero errors. As live streaming metrics populate the sliding buffer, it dynamically shifts to purely localized online variance."*

#### Trap to Avoid:
* **Never say:** *"Isolation Forest finds anomalies by clustering data."*
* **Always say:** *"Isolation Forest isolates anomalies rather than profiling normal data; because anomalies are few and structurally distinct, they are isolated at significantly shallower tree depths."*

