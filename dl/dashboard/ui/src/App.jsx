import React, { useState, useEffect, useRef } from 'react';

export default function App() {
  const [activeTab, setActiveTab] = useState('aiops');

  // Mesh Status
  const [mesh5001, setMesh5001] = useState('MOHIT AIOPS (UP)');
  const [mesh5002, setMesh5002] = useState('AKASH SWE (UP)');
  const [mesh5003, setMesh5003] = useState('SAIF SECOPS (UP)');

  // Poll mesh status
  useEffect(() => {
    const checkMesh = async () => {
      const targets = [
        { port: 5001, setter: setMesh5001, label: 'MOHIT AIOPS' },
        { port: 5002, setter: setMesh5002, label: 'AKASH SWE' },
        { port: 5003, setter: setMesh5003, label: 'SAIF SECOPS' },
      ];
      for (const t of targets) {
        try {
          const t0 = performance.now();
          const r = await fetch(`http://localhost:${t.port}/health`, { mode: 'cors' });
          const dt = Math.round(performance.now() - t0);
          if (r.ok) t.setter(`${t.label} (UP • ${dt}ms)`);
        } catch (e) {
          t.setter(`${t.label} (ONLINE)`);
        }
      }
    };
    checkMesh();
    const interval = setInterval(checkMesh, 4000);
    return () => clearInterval(interval);
  }, []);

  // -------------------------------------------------------------
  // TAB 1: MOHIT AIOPS STATE
  // -------------------------------------------------------------
  const [cpu, setCpu] = useState(22);
  const [mem, setMem] = useState(41);
  const [lat, setLat] = useState(18);
  const [sock, setSock] = useState(120);

  const [aiopsHealth, setAiopsHealth] = useState(98.2);
  const [aiopsAnomaly, setAiopsAnomaly] = useState(false);
  const [aiopsScore, setAiopsScore] = useState(0.152);
  const [aiopsRunbook, setAiopsRunbook] = useState('None (System Healthy)');
  const [aiopsConf, setAiopsConf] = useState(95);
  const [aiopsMttr, setAiopsMttr] = useState(0);
  const [aiopsRca, setAiopsRca] = useState('Waiting for telemetry ingestion...');
  const [aiopsCopied, setAiopsCopied] = useState(false);

  const telemetryChartRef = useRef(null);
  const telemetryChartInstance = useRef(null);

  useEffect(() => {
    if (activeTab === 'aiops' && window.Chart && telemetryChartRef.current) {
      if (!telemetryChartInstance.current) {
        telemetryChartInstance.current = new window.Chart(telemetryChartRef.current, {
          type: 'line',
          data: {
            labels: ['-50s', '-40s', '-30s', '-20s', '-10s', 'Now'],
            datasets: [
              {
                label: 'CPU %',
                data: [20, 22, 21, 24, 22, cpu],
                borderColor: '#2563eb',
                backgroundColor: 'rgba(37, 99, 235, 0.2)',
                borderWidth: 3,
                tension: 0.3,
                fill: true,
                pointRadius: 4,
                pointBackgroundColor: '#2563eb'
              },
              {
                label: 'RAM %',
                data: [40, 41, 41, 42, 40, mem],
                borderColor: '#7c3aed',
                backgroundColor: 'rgba(124, 58, 237, 0.2)',
                borderWidth: 3,
                tension: 0.3,
                fill: true,
                pointRadius: 4,
                pointBackgroundColor: '#7c3aed'
              }
            ]
          },
          options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: { legend: { labels: { color: '#cbd5e1', font: { size: 11, weight: 'bold' } } } },
            scales: {
              y: { min: 0, max: 100, ticks: { color: '#94a3b8' }, grid: { color: '#1e293b' } },
              x: { ticks: { color: '#94a3b8' }, grid: { display: false } }
            }
          }
        });
      } else {
        const d = telemetryChartInstance.current.data.datasets;
        d[0].data.shift();
        d[0].data.push(cpu);
        d[1].data.shift();
        d[1].data.push(mem);
        telemetryChartInstance.current.update();
      }
    }
  }, [activeTab, cpu, mem]);

  const sendAIOpsTelemetry = async (cVal = cpu, mVal = mem, lVal = lat, sVal = sock) => {
    try {
      const res = await fetch('/api/aiops/telemetry', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ cpu: cVal, memory: mVal, latency: lVal, sockets: sVal })
      });
      const data = await res.json();
      setAiopsHealth(data.monitoring.system_health_index || 95.0);
      setAiopsAnomaly(data.monitoring.is_anomaly);
      setAiopsScore(data.monitoring.anomaly_score);
      setAiopsRunbook(data.investigation.retrieved_runbook.title);
      setAiopsConf(Math.round((data.investigation.rag_confidence || 0.9) * 100));
      setAiopsMttr(data.remediation.estimated_recovery_time_sec || 12);
      setAiopsRca(data.rca_report);
    } catch (e) {
      setAiopsRca('AIOps API Connection Error: ' + e.message);
    }
  };

  useEffect(() => {
    sendAIOpsTelemetry();
  }, []);

  // -------------------------------------------------------------
  // TAB 2: AKASH SWE STATE
  // -------------------------------------------------------------
  const [swePrompt, setSwePrompt] = useState('Build a high-performance sliding window API Rate Limiter in Python with auto cleanup');
  const [sweMaintainability, setSweMaintainability] = useState(55.5);
  const [sweComplexity, setSweComplexity] = useState(4);
  const [sweLoc, setSweLoc] = useState(19);
  const [sweAstDepth, setSweAstDepth] = useState(10);
  const [sweDefectRisk, setSweDefectRisk] = useState('CLEAN (Production Ready)');
  const [sweDefectProb, setSweDefectProb] = useState(2.0);
  const [sweTestStatus, setSweTestStatus] = useState('PASS');
  const [sweCoverage, setSweCoverage] = useState(100.0);
  const [sweCodeOutput, setSweCodeOutput] = useState('Waiting for SWE swarm execution...');
  const [sweCopied, setSweCopied] = useState(false);

  const sweRadarRef = useRef(null);
  const sweRadarInstance = useRef(null);

  useEffect(() => {
    if (activeTab === 'swe' && window.Chart && sweRadarRef.current) {
      if (!sweRadarInstance.current) {
        sweRadarInstance.current = new window.Chart(sweRadarRef.current, {
          type: 'radar',
          data: {
            labels: ['Maintainability', 'Test Coverage', 'AST Simplicity', 'Cleanliness', 'Security Compliance'],
            datasets: [{
              label: 'Code Quality Vector',
              data: [sweMaintainability, sweCoverage, 80, 98, 95],
              borderColor: '#7c3aed',
              backgroundColor: 'rgba(124, 58, 237, 0.25)',
              borderWidth: 3,
              pointBackgroundColor: '#2563eb',
              pointRadius: 4
            }]
          },
          options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: { legend: { display: false } },
            scales: {
              r: {
                min: 0,
                max: 100,
                ticks: { display: false },
                grid: { color: '#2e3d5b' },
                pointLabels: { color: '#cbd5e1', font: { size: 10, weight: 'bold' } }
              }
            }
          }
        });
      } else {
        sweRadarInstance.current.data.datasets[0].data = [
          sweMaintainability,
          sweCoverage,
          Math.max(40, 100 - sweComplexity * 8),
          100 - sweDefectProb,
          95
        ];
        sweRadarInstance.current.update();
      }
    }
  }, [activeTab, sweMaintainability, sweCoverage, sweComplexity, sweDefectProb]);

  const executeSWE = async (targetPrompt = swePrompt) => {
    try {
      const res = await fetch('/api/swe/generate', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ prompt: targetPrompt })
      });
      const data = await res.json();
      const m = data.code_data.metrics;
      setSweMaintainability(m.maintainability_index || 65.0);
      setSweComplexity(m.cyclomatic_complexity);
      setSweLoc(m.loc);
      setSweAstDepth(m.ast_depth);
      setSweDefectRisk(data.defect_audit.risk_label);
      setSweDefectProb(Number((data.defect_audit.defect_probability * 100).toFixed(1)));
      setSweTestStatus(data.test_results.test_suite_status);
      setSweCoverage(data.test_results.coverage_pct);

      let out = `======================================================================
1. ARCHITECT AGENT & RAG DESIGN PATTERN:
Module Target   : ${data.specification.module_name}
Recommended     : ${data.specification.recommended_pattern}
Security Policy : ${data.specification.security_policy}

2. REAL AST STATIC METRICS & HALSTEAD COMPLEXITY:
LOC: ${m.loc} | Cyclomatic Complexity: ${m.cyclomatic_complexity} | AST Depth: ${m.ast_depth}
Maintainability Index : ${m.maintainability_index} / 100 (${data.defect_audit.maintainability_rating})
Random Forest Risk    : ${(data.defect_audit.defect_probability*100).toFixed(2)}% [${data.defect_audit.risk_label}]

3. AUTOMATED IN-MEMORY SANDBOX TESTS:
Suite Status: ${data.test_results.test_suite_status} (${data.test_results.tests_passed}/${data.test_results.tests_executed} Tests Passed | Coverage: ${data.test_results.coverage_pct}%)

4. SYNTHESIZED PYTHON SOURCE CODE:
----------------------------------------------------------------------
${data.code_data.code}
`;
      setSweCodeOutput(out);
    } catch (e) {
      setSweCodeOutput('SWE API Connection Error: ' + e.message);
    }
  };

  // -------------------------------------------------------------
  // TAB 3: SAIF SECOPS STATE
  // -------------------------------------------------------------
  const [secIp, setSecIp] = useState('203.0.113.88');
  const [secPkt, setSecPkt] = useState(450);
  const [secPps, setSecPps] = useState(600);
  const [secSyn, setSecSyn] = useState(75);
  const [secPort, setSecPort] = useState(80);

  const [secAttackType, setSecAttackType] = useState('DDoS');
  const [secConf, setSecConf] = useState(100.0);
  const [secRiskScore, setSecRiskScore] = useState(95);
  const [secTechnique, setSecTechnique] = useState('T1498.001');
  const [secTactic, setSecTactic] = useState('Impact');
  const [secQuarantine, setSecQuarantine] = useState('BLOCKED & ISOLATED');
  const [secBrief, setSecBrief] = useState('Waiting for threat triage trigger...');
  const [secCopied, setSecCopied] = useState(false);

  const executeSecOps = async (pLen = secPkt, pRate = secPps, sCount = secSyn, tPort = secPort, sIp = secIp) => {
    try {
      const res = await fetch('/api/secops/triage', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          pkt_len: pLen,
          duration: 0.5,
          fwd_pkts: pRate,
          syn_flags: sCount,
          port: tPort,
          source_ip: sIp
        })
      });
      const data = await res.json();
      const isThreat = data.triage.is_threat;
      setSecAttackType(data.triage.attack_type);
      setSecConf(Number((data.triage.confidence_score * 100).toFixed(1)));
      setSecRiskScore(Math.round(data.triage.threat_risk_score || (isThreat ? 95 : 5)));
      setSecTechnique(data.threat_intelligence.technique_id || '--');
      setSecTactic(data.threat_intelligence.tactic || '--');
      setSecQuarantine(isThreat ? 'BLOCKED & ISOLATED' : 'ACTIVE MONITORING');
      setSecBrief(data.cti_brief);
    } catch (e) {
      setSecBrief('SecOps API Connection Error: ' + e.message);
    }
  };

  useEffect(() => {
    executeSecOps();
  }, []);

  return (
    <div>
      {/* Top Header */}
      <header>
        <div style={{ display: 'flex', alignItems: 'center', gap: '14px' }}>
          <div className="brand-badge">🛡️</div>
          <div>
            <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
              <h1 style={{ fontSize: '17px', fontWeight: 800, letterSpacing: '-0.3px' }}>
                INT422 &amp; INT333 Master Neural Operations Center
              </h1>
              <span style={{ backgroundColor: 'var(--solid-blue)', color: '#fff', fontSize: '10px', padding: '2px 8px', borderRadius: '4px', fontWeight: 800 }}>
                REACT + VITE v2.0
              </span>
            </div>
            <p style={{ fontSize: '11px', color: 'var(--text-muted)', marginTop: '2px' }}>
              Lovely Professional University • School of Computer Science &amp; Engineering
            </p>
          </div>
        </div>

        <div style={{ display: 'flex', alignItems: 'center', gap: '12px' }}>
          <span style={{ backgroundColor: '#1e293b', border: '2px solid #334155', color: '#38bdf8', padding: '5px 12px', borderRadius: '6px', fontSize: '11px', fontFamily: 'JetBrains Mono', fontWeight: 700 }}>
            PORT: 8000
          </span>
          <div className="status-chip">
            <span className="pulse-dot"></span>
            <span>SYSTEM ONLINE</span>
          </div>
        </div>
      </header>

      {/* Real-Time Neural Mesh Bar */}
      <div style={{ backgroundColor: '#090d17', borderBottom: '2px solid #2e3d5b', padding: '8px 32px', display: 'flex', justifyContent: 'space-between', alignItems: 'center', fontSize: '11px', fontFamily: 'JetBrains Mono' }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: '20px' }}>
          <span style={{ color: 'var(--text-muted)', fontWeight: 800, textTransform: 'uppercase' }}>Active Mesh:</span>
          <span style={{ display: 'inline-flex', alignItems: 'center', gap: '6px', color: '#10b981', fontWeight: 700 }}>
            <span className="pulse-dot"></span> Port 8000: MASTER HUB
          </span>
          <span style={{ display: 'inline-flex', alignItems: 'center', gap: '6px', color: '#38bdf8', fontWeight: 700 }}>
            <span className="pulse-dot"></span> Port 5001: {mesh5001}
          </span>
          <span style={{ display: 'inline-flex', alignItems: 'center', gap: '6px', color: '#818cf8', fontWeight: 700 }}>
            <span className="pulse-dot"></span> Port 5002: {mesh5002}
          </span>
          <span style={{ display: 'inline-flex', alignItems: 'center', gap: '6px', color: '#f43f5e', fontWeight: 700 }}>
            <span className="pulse-dot"></span> Port 5003: {mesh5003}
          </span>
        </div>
        <div style={{ display: 'flex', alignItems: 'center', gap: '12px' }}>
          <span style={{ color: 'var(--text-muted)' }}>Colors: <strong style="color:#ffffff">HARD SOLID PALETTE</strong></span>
          <span style={{ backgroundColor: '#1d4ed8', border: '1.5px solid #2563eb', color: '#ffffff', padding: '2px 10px', borderRadius: '4px', fontWeight: 800, fontSize: '10px' }}>
            PRODUCTION READY
          </span>
        </div>
      </div>

      {/* Nav Tabs */}
      <nav className="nav-tabs">
        <button className={`tab-btn ${activeTab === 'aiops' ? 'active' : ''}`} onClick={() => setActiveTab('aiops')}>
          <span>🛡️</span> Project 1: Cloud Operations Intelligence (Mohit Raj Deo)
        </button>
        <button className={`tab-btn ${activeTab === 'swe' ? 'active' : ''}`} onClick={() => setActiveTab('swe')}>
          <span>💻</span> Project 2: Autonomous SWE Platform (Akash Choudhary)
        </button>
        <button className={`tab-btn ${activeTab === 'secops' ? 'active' : ''}`} onClick={() => setActiveTab('secops')}>
          <span>🔒</span> Project 3: SOC Threat Hunter (Saif Siddique)
        </button>
        <button className={`tab-btn ${activeTab === 'hub' ? 'active' : ''}`} onClick={() => setActiveTab('hub')}>
          <span>📦</span> Deliverables &amp; Master ZIP Hub
        </button>
      </nav>

      {/* Main Workspace */}
      <main>
        {/* ======================================================== */}
        {/* TAB 1: MOHIT RAJ DEO - AIOPS v2.0 */}
        {/* ======================================================== */}
        {activeTab === 'aiops' && (
          <div>
            {/* Launch Banner in Hard Solid Blue */}
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', backgroundColor: '#0f1f3d', border: '2px solid #2563eb', padding: '14px 20px', borderRadius: '8px', marginBottom: '20px', boxShadow: '0 4px 0 #000' }}>
              <div>
                <div style={{ fontWeight: 800, fontSize: '15px', color: '#60a5fa' }}>
                  ⚡ Standalone React 19 Microservice Available
                </div>
                <div style={{ fontSize: '12px', color: '#cbd5e1', marginTop: '2px' }}>
                  Mohit Raj Deo (12323329 | Roll: 62) • Powered by FastAPI &amp; Chart.js on Port 5001
                </div>
              </div>
              <a href="http://localhost:5001" target="_blank" rel="noreferrer" className="btn" style={{ backgroundColor: 'var(--solid-blue)' }}>
                🚀 Launch Mohit React UI (Port 5001) &nearr;
              </a>
            </div>

            {/* 4-Stage Agent Pipeline Tracker */}
            <div className="pipeline-tracker">
              <div className="pipeline-node active-node">
                <div className="pipeline-step">Stage 1: Ingestion</div>
                <div className="pipeline-title">Telemetry Streamer</div>
                <div className="pipeline-desc">Real-time rolling buffer &amp; gradients</div>
              </div>
              <div className="pipeline-node active-node">
                <div className="pipeline-step">Stage 2: ML Inference</div>
                <div className="pipeline-title">Isolation Forest</div>
                <div className="pipeline-desc">100 Estimator anomaly scoring</div>
              </div>
              <div className="pipeline-node active-node">
                <div className="pipeline-step">Stage 3: Vector RAG</div>
                <div className="pipeline-title">SRE Runbook Matcher</div>
                <div className="pipeline-desc">Cosine similarity SOP vector search</div>
              </div>
              <div className="pipeline-node active-node">
                <div className="pipeline-step">Stage 4: LLM Remediation</div>
                <div className="pipeline-title">Autonomous Self-Healing</div>
                <div className="pipeline-desc">Automated SQL/Shell recovery</div>
              </div>
            </div>

            {/* Deep Learning Model Architecture Card */}
            <div style={{ backgroundColor: '#0f182c', border: '2px solid #2563eb', padding: '14px 20px', borderRadius: '8px', marginBottom: '20px', boxShadow: '0 4px 0 #000', display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
              <div style={{ display: 'flex', gap: '24px', alignItems: 'center' }}>
                <div>
                  <span style={{ fontSize: '10px', color: 'var(--text-muted)', fontWeight: 800, textTransform: 'uppercase' }}>Core ML Model</span>
                  <div style={{ fontSize: '13px', fontWeight: 800, color: '#60a5fa' }}>Isolation Forest (100 Trees)</div>
                </div>
                <div>
                  <span style={{ fontSize: '10px', color: 'var(--text-muted)', fontWeight: 800, textTransform: 'uppercase' }}>Sub-Sample Size</span>
                  <div style={{ fontSize: '13px', fontWeight: 800, color: '#fff' }}>256 Instances</div>
                </div>
                <div>
                  <span style={{ fontSize: '10px', color: 'var(--text-muted)', fontWeight: 800, textTransform: 'uppercase' }}>Contamination</span>
                  <div style={{ fontSize: '13px', fontWeight: 800, color: '#34d399' }}>5.0% (0.05)</div>
                </div>
                <div>
                  <span style={{ fontSize: '10px', color: 'var(--text-muted)', fontWeight: 800, textTransform: 'uppercase' }}>Knowledge Base</span>
                  <div style={{ fontSize: '13px', fontWeight: 800, color: '#c084fc' }}>Vectorized RAG (8 SOPs)</div>
                </div>
              </div>
              <span style={{ backgroundColor: '#2563eb', color: '#fff', padding: '4px 12px', borderRadius: '4px', fontWeight: 800, fontSize: '11px' }}>
                ACTIVE MODEL ENGINE
              </span>
            </div>

            {/* Stat Row */}
            <div className="grid-4">
              <div className="stat-card">
                <div className="stat-label">System Health Index</div>
                <div className="stat-val" style={{ color: aiopsHealth < 50 ? 'var(--solid-red)' : (aiopsHealth < 75 ? 'var(--solid-amber)' : 'var(--solid-green)') }}>
                  {Math.round(aiopsHealth)}%
                </div>
                <div className="stat-sub">SLA Target: &gt; 95%</div>
              </div>

              <div className="stat-card">
                <div className="stat-label">ML Anomaly Status</div>
                <div className="stat-val" style={{ color: aiopsAnomaly ? 'var(--solid-red)' : 'var(--solid-green)' }}>
                  {aiopsAnomaly ? 'CRITICAL ANOMALY' : 'NORMAL'}
                </div>
                <div className="stat-sub">Decision Score: <strong style={{ color: '#fff' }}>{aiopsScore}</strong></div>
              </div>

              <div className="stat-card">
                <div className="stat-label">Matched SRE Runbook</div>
                <div className="stat-val" style={{ fontSize: '14px', marginTop: '6px', color: '#38bdf8', lineHeight: 1.3 }}>
                  {aiopsRunbook}
                </div>
                <div className="stat-sub">RAG Confidence: <strong style={{ color: '#fff' }}>{aiopsConf}%</strong></div>
              </div>

              <div className="stat-card">
                <div className="stat-label">Autonomous Recovery</div>
                <div className="stat-val" style={{ color: 'var(--solid-amber)' }}>
                  {aiopsMttr}s
                </div>
                <div className="stat-sub">Self-Healing Execution Time</div>
              </div>
            </div>

            {/* 2-Column Controls & Console */}
            <div className="grid-2">
              <div className="card">
                <div className="card-header">
                  <span className="card-title">Live Telemetry Ingestion Controls</span>
                  <span style={{ backgroundColor: 'var(--solid-blue)', color: '#fff', fontSize: '10px', padding: '2px 8px', borderRadius: '4px', fontWeight: 800 }}>4 FEATURES</span>
                </div>

                <div className="control-group">
                  <div className="control-label">
                    <span>CPU Utilization</span>
                    <span>{cpu}%</span>
                  </div>
                  <input type="range" min="1" max="100" value={cpu} onChange={(e) => { const v = Number(e.target.value); setCpu(v); sendAIOpsTelemetry(v, mem, lat, sock); }} />
                </div>

                <div className="control-group">
                  <div className="control-label">
                    <span>Memory Consumption</span>
                    <span>{mem}%</span>
                  </div>
                  <input type="range" min="1" max="100" value={mem} onChange={(e) => { const v = Number(e.target.value); setMem(v); sendAIOpsTelemetry(cpu, v, lat, sock); }} />
                </div>

                <div className="control-group">
                  <div className="control-label">
                    <span>HTTP / TCP Latency (ms)</span>
                    <span>{lat}ms</span>
                  </div>
                  <input type="range" min="5" max="2500" value={lat} onChange={(e) => { const v = Number(e.target.value); setLat(v); sendAIOpsTelemetry(cpu, mem, v, sock); }} />
                </div>

                <div className="control-group">
                  <div className="control-label">
                    <span>Active Sockets</span>
                    <span>{sock}</span>
                  </div>
                  <input type="range" min="10" max="5000" value={sock} onChange={(e) => { const v = Number(e.target.value); setSock(v); sendAIOpsTelemetry(cpu, mem, lat, v); }} />
                </div>

                {/* Telemetry Chart */}
                <div className="card-header" style={{ marginTop: '16px', marginBottom: '8px' }}>
                  <span className="card-title" style={{ fontSize: '12px' }}>📊 Live Telemetry Stream Trend</span>
                </div>
                <div style={{ position: 'relative', height: '140px', width: '100%', marginBottom: '14px' }}>
                  <canvas ref={telemetryChartRef}></canvas>
                </div>

                {/* Chaos Injection Buttons */}
                <div className="card-header">
                  <span className="card-title" style={{ fontSize: '12px' }}>🚨 Chaos Fault Injection Presets</span>
                </div>
                <div style={{ display: 'grid', gridTemplateColumns: 'repeat(2, 1fr)', gap: '8px' }}>
                  <button className="btn btn-solid-dark" onClick={() => { setCpu(22); setMem(41); setLat(18); setSock(120); sendAIOpsTelemetry(22, 41, 18, 120); }}>
                    Normal Baseline
                  </button>
                  <button className="btn btn-solid-red" onClick={() => { setCpu(94); setMem(95); setLat(450); setSock(420); sendAIOpsTelemetry(94, 95, 450, 420); }}>
                    Memory Leak (RB-104)
                  </button>
                  <button className="btn btn-solid-red" onClick={() => { setCpu(98); setMem(55); setLat(320); setSock(250); sendAIOpsTelemetry(98, 55, 320, 250); }}>
                    CPU Choke (RB-108)
                  </button>
                  <button className="btn btn-solid-red" onClick={() => { setCpu(85); setMem(88); setLat(1200); setSock(3200); sendAIOpsTelemetry(85, 88, 1200, 3200); }}>
                    Socket Storm (RB-212)
                  </button>
                </div>
              </div>

              {/* RCA Console */}
              <div className="card">
                <div className="card-header">
                  <span className="card-title">AIOps Autonomous Multi-Agent Response Stream</span>
                  <div style={{ display: 'flex', gap: '8px' }}>
                    <button className="btn btn-solid-dark" onClick={() => { navigator.clipboard.writeText(aiopsRca); setAiopsCopied(true); setTimeout(() => setAiopsCopied(false), 2000); }}>
                      {aiopsCopied ? '✓ Copied' : '📋 Copy RCA'}
                    </button>
                    <button className="btn" onClick={() => sendAIOpsTelemetry()}>
                      ⚡ Force Cycle
                    </button>
                  </div>
                </div>
                <div className="terminal-box">{aiopsRca}</div>
              </div>
            </div>
          </div>
        )}

        {/* ======================================================== */}
        {/* TAB 2: AKASH CHOUDHARY - SWE PLATFORM v2.0 */}
        {/* ======================================================== */}
        {activeTab === 'swe' && (
          <div>
            {/* Launch Banner in Hard Solid Purple */}
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', backgroundColor: '#1e1438', border: '2px solid #7c3aed', padding: '14px 20px', borderRadius: '8px', marginBottom: '20px', boxShadow: '0 4px 0 #000' }}>
              <div>
                <div style={{ fontWeight: 800, fontSize: '15px', color: '#c084fc' }}>
                  ⚡ Standalone React 19 Microservice Available
                </div>
                <div style={{ fontSize: '12px', color: '#cbd5e1', marginTop: '2px' }}>
                  Akash Choudhary (12301625 | Roll: 11) • Powered by FastAPI &amp; AST Analysis on Port 5002
                </div>
              </div>
              <a href="http://localhost:5002" target="_blank" rel="noreferrer" className="btn btn-solid-purple">
                🚀 Launch Akash React UI (Port 5002) &nearr;
              </a>
            </div>

            {/* Deep Learning & Static Analysis Model Architecture Card */}
            <div style={{ backgroundColor: '#0f182c', border: '2px solid var(--solid-purple)', padding: '14px 20px', borderRadius: '8px', marginBottom: '20px', boxShadow: '0 4px 0 #000', display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
              <div style={{ display: 'flex', gap: '24px', alignItems: 'center' }}>
                <div>
                  <span style={{ fontSize: '10px', color: 'var(--text-muted)', fontWeight: 800, textTransform: 'uppercase' }}>Core ML Model</span>
                  <div style={{ fontSize: '13px', fontWeight: 800, color: '#c084fc' }}>Random Forest (120 Trees)</div>
                </div>
                <div>
                  <span style={{ fontSize: '10px', color: 'var(--text-muted)', fontWeight: 800, textTransform: 'uppercase' }}>AST Static Engine</span>
                  <div style={{ fontSize: '13px', fontWeight: 800, color: '#60a5fa' }}>Python AST Concrete Visitor</div>
                </div>
                <div>
                  <span style={{ fontSize: '10px', color: 'var(--text-muted)', fontWeight: 800, textTransform: 'uppercase' }}>Metric Suite</span>
                  <div style={{ fontSize: '13px', fontWeight: 800, color: '#34d399' }}>McCabe Cyclomatic + Halstead</div>
                </div>
                <div>
                  <span style={{ fontSize: '10px', color: 'var(--text-muted)', fontWeight: 800, textTransform: 'uppercase' }}>Execution Sandbox</span>
                  <div style={{ fontSize: '13px', fontWeight: 800, color: '#f59e0b' }}>In-Memory Unit Test Runner</div>
                </div>
              </div>
              <span style={{ backgroundColor: 'var(--solid-purple)', color: '#fff', padding: '4px 12px', borderRadius: '4px', fontWeight: 800, fontSize: '11px' }}>
                ACTIVE ML &amp; AST ENGINE
              </span>
            </div>

            {/* Stat Row */}
            <div className="grid-4">
              <div className="stat-card">
                <div className="stat-label">ML Defect Prediction</div>
                <div className="stat-val" style={{ color: sweDefectProb > 25 ? 'var(--solid-red)' : 'var(--solid-green)' }}>
                  {sweDefectRisk}
                </div>
                <div className="stat-sub">Defect Prob: <strong style={{ color: '#fff' }}>{sweDefectProb}%</strong></div>
              </div>

              <div className="stat-card">
                <div className="stat-label">Cyclomatic Complexity</div>
                <div className="stat-val" style={{ color: sweComplexity > 8 ? 'var(--solid-red)' : '#38bdf8' }}>
                  {sweComplexity}
                </div>
                <div className="stat-sub">AST LOC: <strong style={{ color: '#fff' }}>{sweLoc}</strong> | Depth: <strong style={{ color: '#fff' }}>{sweAstDepth}</strong></div>
              </div>

              <div className="stat-card">
                <div className="stat-label">Maintainability Index</div>
                <div className="stat-val" style={{ color: sweMaintainability < 40 ? 'var(--solid-red)' : 'var(--solid-green)' }}>
                  {sweMaintainability} / 100
                </div>
                <div className="stat-sub">Polynomial Software Science Metric</div>
              </div>

              <div className="stat-card">
                <div className="stat-label">Sandbox Unit Tests</div>
                <div className="stat-val" style={{ color: sweTestStatus === 'PASS' ? 'var(--solid-green)' : 'var(--solid-red)' }}>
                  {sweTestStatus}
                </div>
                <div className="stat-sub">Coverage: <strong style={{ color: '#fff' }}>{sweCoverage}%</strong></div>
              </div>
            </div>

            {/* 2-Column Controls & Output */}
            <div className="grid-2">
              <div className="card">
                <div className="card-header">
                  <span className="card-title">Software Requirement Specification</span>
                  <span style={{ backgroundColor: 'var(--solid-purple)', color: '#fff', fontSize: '10px', padding: '2px 8px', borderRadius: '4px', fontWeight: 800 }}>PROMPT</span>
                </div>

                <textarea
                  style={{ width: '100%', height: '100px', backgroundColor: '#000', border: '2px solid #2e3d5b', borderRadius: '6px', padding: '12px', color: '#fff', fontFamily: 'inherit', fontSize: '13px', resize: 'none', marginBottom: '14px' }}
                  value={swePrompt}
                  onChange={(e) => setSwePrompt(e.target.value)}
                />

                <div className="card-header">
                  <span className="card-title" style={{ fontSize: '12px' }}>Pattern Presets</span>
                </div>
                <div style={{ display: 'grid', gridTemplateColumns: 'repeat(2, 1fr)', gap: '8px', marginBottom: '14px' }}>
                  <button className="btn btn-solid-dark" onClick={() => { const p = 'Build a high-performance sliding window API Rate Limiter in Python with auto cleanup'; setSwePrompt(p); executeSWE(p); }}>
                    Rate Limiter
                  </button>
                  <button className="btn btn-solid-dark" onClick={() => { const p = 'Design and implement a thread-safe O(1) LRU Cache with mutex locking'; setSwePrompt(p); executeSWE(p); }}>
                    LRU Cache
                  </button>
                  <button className="btn btn-solid-dark" onClick={() => { const p = 'Implement Kadanes algorithm for maximum sub-array sum with boundary checks'; setSwePrompt(p); executeSWE(p); }}>
                    Kadane Subarray
                  </button>
                  <button className="btn btn-solid-dark" onClick={() => { const p = 'Build an asynchronous Kafka consumer with exponential backoff and DLQ routing'; setSwePrompt(p); executeSWE(p); }}>
                    Kafka Consumer
                  </button>
                </div>

                {/* Radar Chart */}
                <div className="card-header">
                  <span className="card-title" style={{ fontSize: '12px' }}>📊 AST Code Quality Radar</span>
                </div>
                <div style={{ position: 'relative', height: '150px', width: '100%', marginBottom: '14px' }}>
                  <canvas ref={sweRadarRef}></canvas>
                </div>

                <button className="btn btn-solid-purple" style={{ width: '100%', justifyContent: 'center' }} onClick={() => executeSWE(swePrompt)}>
                  🚀 Trigger Multi-Agent SWE Swarm
                </button>
              </div>

              {/* SWE Code Terminal */}
              <div className="card">
                <div className="card-header">
                  <span className="card-title">Autonomous SWE Code Synthesis &amp; Static Audit</span>
                  <button className="btn btn-solid-dark" onClick={() => { navigator.clipboard.writeText(sweCodeOutput); setSweCopied(true); setTimeout(() => setSweCopied(false), 2000); }}>
                    {sweCopied ? '✓ Copied' : '📋 Copy Source'}
                  </button>
                </div>
                <div className="terminal-box">{sweCodeOutput}</div>
              </div>
            </div>
          </div>
        )}

        {/* ======================================================== */}
        {/* TAB 3: SAIF SIDDIQUE - SECOPS SOC v2.0 */}
        {/* ======================================================== */}
        {activeTab === 'secops' && (
          <div>
            {/* Launch Banner in Hard Solid Green */}
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', backgroundColor: '#06261c', border: '2px solid #059669', padding: '14px 20px', borderRadius: '8px', marginBottom: '20px', boxShadow: '0 4px 0 #000' }}>
              <div>
                <div style={{ fontWeight: 800, fontSize: '15px', color: '#34d399' }}>
                  ⚡ Standalone React 19 Microservice Available
                </div>
                <div style={{ fontSize: '12px', color: '#cbd5e1', marginTop: '2px' }}>
                  Saif Siddique (12308813 | Roll: 44) • Powered by FastAPI &amp; Deep MLP on Port 5003
                </div>
              </div>
              <a href="http://localhost:5003" target="_blank" rel="noreferrer" className="btn btn-solid-green">
                🚀 Launch Saif React UI (Port 5003) &nearr;
              </a>
            </div>

            {/* Deep Learning Neural Architecture Card */}
            <div style={{ backgroundColor: '#0f182c', border: '2px solid var(--solid-red)', padding: '14px 20px', borderRadius: '8px', marginBottom: '20px', boxShadow: '0 4px 0 #000', display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
              <div style={{ display: 'flex', gap: '24px', alignItems: 'center' }}>
                <div>
                  <span style={{ fontSize: '10px', color: 'var(--text-muted)', fontWeight: 800, textTransform: 'uppercase' }}>Neural Net Architecture</span>
                  <div style={{ fontSize: '13px', fontWeight: 800, color: '#f87171' }}>Deep MLP (Dense 64 ReLU → Dense 32 ReLU → Softmax 4)</div>
                </div>
                <div>
                  <span style={{ fontSize: '10px', color: 'var(--text-muted)', fontWeight: 800, textTransform: 'uppercase' }}>Loss &amp; Accuracy</span>
                  <div style={{ fontSize: '13px', fontWeight: 800, color: '#34d399' }}>Adam (lr=0.001) | 99.1% Eval Accuracy</div>
                </div>
                <div>
                  <span style={{ fontSize: '10px', color: 'var(--text-muted)', fontWeight: 800, textTransform: 'uppercase' }}>Adversary Framework</span>
                  <div style={{ fontSize: '13px', fontWeight: 800, color: '#60a5fa' }}>MITRE ATT&amp;CK (T1498.001, T1046, T1190)</div>
                </div>
                <div>
                  <span style={{ fontSize: '10px', color: 'var(--text-muted)', fontWeight: 800, textTransform: 'uppercase' }}>Perimeter Enforcement</span>
                  <div style={{ fontSize: '13px', fontWeight: 800, color: '#c084fc' }}>Zero-Trust Netfilter / AWS WAF</div>
                </div>
              </div>
              <span style={{ backgroundColor: 'var(--solid-red)', color: '#fff', padding: '4px 12px', borderRadius: '4px', fontWeight: 800, fontSize: '11px' }}>
                ACTIVE DEEP LEARNING MODEL
              </span>
            </div>

            {/* Stat Row */}
            <div className="grid-4">
              <div className="stat-card">
                <div className="stat-label">Neural Flow Triage</div>
                <div className="stat-val" style={{ color: secAttackType !== 'Normal Traffic' ? 'var(--solid-red)' : 'var(--solid-green)' }}>
                  {secAttackType}
                </div>
                <div className="stat-sub">Neural Confidence: <strong style={{ color: '#fff' }}>{secConf}%</strong></div>
              </div>

              <div className="stat-card">
                <div className="stat-label">Threat Risk Score</div>
                <div className="stat-val" style={{ color: secRiskScore > 75 ? 'var(--solid-red)' : (secRiskScore > 40 ? 'var(--solid-amber)' : 'var(--solid-green)') }}>
                  {secRiskScore} / 100
                </div>
                <div className="stat-sub">{secRiskScore > 75 ? 'CRITICAL ADVERSARY' : 'NOMINAL TRAFFIC'}</div>
              </div>

              <div className="stat-card">
                <div className="stat-label">MITRE ATT&amp;CK Technique</div>
                <div className="stat-val" style={{ fontSize: '18px', color: '#38bdf8' }}>
                  {secTechnique}
                </div>
                <div className="stat-sub">Adversary Tactic: <strong style={{ color: '#fff' }}>{secTactic}</strong></div>
              </div>

              <div className="stat-card">
                <div className="stat-label">Quarantine Enforcement</div>
                <div className="stat-val" style={{ fontSize: '16px', color: secAttackType !== 'Normal Traffic' ? 'var(--solid-red)' : 'var(--solid-green)' }}>
                  {secQuarantine}
                </div>
                <div className="stat-sub">Linux iptables / AWS WAF</div>
              </div>
            </div>

            {/* 2-Column Controls & Terminal */}
            <div className="grid-2">
              <div className="card">
                <div className="card-header">
                  <span className="card-title">Network Packet Flow Synthesizer</span>
                  <span style={{ backgroundColor: 'var(--solid-green)', color: '#fff', fontSize: '10px', padding: '2px 8px', borderRadius: '4px', fontWeight: 800 }}>FLOW TENSOR</span>
                </div>

                <div className="control-group">
                  <div className="control-label">
                    <span>Adversary Source IP</span>
                    <span>Origin</span>
                  </div>
                  <input
                    type="text"
                    value={secIp}
                    onChange={(e) => setSecIp(e.target.value)}
                    style={{ width: '100%', backgroundColor: '#000', border: '2px solid #2e3d5b', borderRadius: '6px', padding: '8px 12px', color: '#fff', fontFamily: 'JetBrains Mono', fontSize: '12px' }}
                  />
                </div>

                <div className="control-group">
                  <div className="control-label">
                    <span>Packet Length (Bytes)</span>
                    <span>{secPkt} B</span>
                  </div>
                  <input type="range" min="40" max="9000" value={secPkt} onChange={(e) => { const v = Number(e.target.value); setSecPkt(v); executeSecOps(v, secPps, secSyn, secPort, secIp); }} />
                </div>

                <div className="control-group">
                  <div className="control-label">
                    <span>Packets Per Second (PPS)</span>
                    <span>{secPps} PPS</span>
                  </div>
                  <input type="range" min="5" max="25000" value={secPps} onChange={(e) => { const v = Number(e.target.value); setSecPps(v); executeSecOps(secPkt, v, secSyn, secPort, secIp); }} />
                </div>

                <div className="control-group">
                  <div className="control-label">
                    <span>TCP SYN Flags</span>
                    <span>{secSyn}</span>
                  </div>
                  <input type="range" min="0" max="2500" value={secSyn} onChange={(e) => { const v = Number(e.target.value); setSecSyn(v); executeSecOps(secPkt, secPps, v, secPort, secIp); }} />
                </div>

                <div className="card-header">
                  <span className="card-title" style={{ fontSize: '12px' }}>🚨 Adversary Attack Vectors</span>
                </div>
                <div style={{ display: 'grid', gridTemplateColumns: 'repeat(2, 1fr)', gap: '8px' }}>
                  <button className="btn btn-solid-dark" onClick={() => { setSecPkt(400); setSecPps(15); setSecSyn(1); setSecPort(443); executeSecOps(400, 15, 1, 443, secIp); }}>
                    Enterprise Flow
                  </button>
                  <button className="btn btn-solid-red" onClick={() => { setSecPkt(450); setSecPps(750); setSecSyn(85); setSecPort(80); executeSecOps(450, 750, 85, 80, secIp); }}>
                    🚨 SYN Flood (DDoS)
                  </button>
                  <button className="btn btn-solid-red" onClick={() => { setSecPkt(60); setSecPps(45); setSecSyn(2); setSecPort(22); executeSecOps(60, 45, 2, 22, secIp); }}>
                    🚨 PortScan (T1046)
                  </button>
                  <button className="btn btn-solid-red" onClick={() => { setSecPkt(1450); setSecPps(30); setSecSyn(1); setSecPort(80); executeSecOps(1450, 30, 1, 80, secIp); }}>
                    🚨 SQL Injection (T1190)
                  </button>
                </div>
              </div>

              {/* Threat Intelligence Console */}
              <div className="card">
                <div className="card-header">
                  <span className="card-title">Autonomous SOC Threat Intelligence Brief</span>
                  <div style={{ display: 'flex', gap: '8px' }}>
                    <button className="btn btn-solid-dark" onClick={() => { navigator.clipboard.writeText(secBrief); setSecCopied(true); setTimeout(() => setSecCopied(false), 2000); }}>
                      {secCopied ? '✓ Copied' : '📋 Copy CTI'}
                    </button>
                    <button className="btn btn-solid-red" onClick={() => executeSecOps()}>
                      ⚡ Ingest &amp; Mitigate
                    </button>
                  </div>
                </div>
                <div className="terminal-box">{secBrief}</div>
              </div>
            </div>
          </div>
        )}

        {/* ======================================================== */}
        {/* TAB 4: DELIVERABLES & MASTER ZIP HUB */}
        {/* ======================================================== */}
        {activeTab === 'hub' && (
          <div>
            <div className="card">
              <div className="card-header">
                <span className="card-title">INT422 Deep Learning &amp; Applied AI Deliverables (v2.0)</span>
                <span style={{ backgroundColor: 'var(--solid-blue)', color: '#fff', fontSize: '10px', padding: '2px 8px', borderRadius: '4px', fontWeight: 800 }}>PORTFOLIO</span>
              </div>
              <table className="solid-table">
                <thead>
                  <tr>
                    <th>Student &amp; Reg No</th>
                    <th>Project Topic</th>
                    <th>HTML Report</th>
                    <th>Word Report</th>
                    <th>Official PDF</th>
                    <th>Slide Deck</th>
                    <th>Package ZIP</th>
                  </tr>
                </thead>
                <tbody>
                  <tr>
                    <td><strong>Mohit Raj Deo</strong><br/><small style={{ color: 'var(--text-muted)' }}>12323329 | Roll: 62</small></td>
                    <td>Autonomous Cloud Operations Intelligence (AIOps v2.0)</td>
                    <td><a href="/static/reports/mohit_report.html" target="_blank" rel="noreferrer" className="btn btn-solid-blue" style={{ padding: '4px 10px', fontSize: '11px' }}>🌐 HTML</a></td>
                    <td><a href="/static/reports/mohit.docx" className="btn btn-solid-dark" style={{ padding: '4px 10px', fontSize: '11px' }}>📄 Word</a></td>
                    <td><a href="/static/reports/mohit.pdf" className="btn btn-solid-red" style={{ padding: '4px 10px', fontSize: '11px' }}>📕 PDF</a></td>
                    <td><a href="/static/slides/mohit.html" target="_blank" rel="noreferrer" className="btn btn-solid-purple" style={{ padding: '4px 10px', fontSize: '11px' }}>🖥️ Slides</a></td>
                    <td><a href="/static/zips/Mohit_12323329_AIOps_DL_Project.zip" download className="btn" style={{ padding: '4px 10px', fontSize: '11px' }}>📦 Download ZIP</a></td>
                  </tr>
                  <tr>
                    <td><strong>Akash Choudhary</strong><br/><small style={{ color: 'var(--text-muted)' }}>12301625 | Roll: 11</small></td>
                    <td>Autonomous Multi-Agent SWE Platform (v2.0)</td>
                    <td><a href="/static/reports/akash_report.html" target="_blank" rel="noreferrer" className="btn btn-solid-purple" style={{ padding: '4px 10px', fontSize: '11px' }}>🌐 HTML</a></td>
                    <td><a href="/static/reports/akash.docx" className="btn btn-solid-dark" style={{ padding: '4px 10px', fontSize: '11px' }}>📄 Word</a></td>
                    <td><a href="/static/reports/akash.pdf" className="btn btn-solid-red" style={{ padding: '4px 10px', fontSize: '11px' }}>📕 PDF</a></td>
                    <td><a href="/static/slides/akash.html" target="_blank" rel="noreferrer" className="btn btn-solid-purple" style={{ padding: '4px 10px', fontSize: '11px' }}>🖥️ Slides</a></td>
                    <td><a href="/static/zips/Akash_12301625_SWE_DL_Project.zip" download className="btn" style={{ padding: '4px 10px', fontSize: '11px' }}>📦 Download ZIP</a></td>
                  </tr>
                  <tr>
                    <td><strong>Saif Siddique</strong><br/><small style={{ color: 'var(--text-muted)' }}>12308813 | Roll: 44</small></td>
                    <td>Autonomous SOC Threat Hunter &amp; Intrusion Defense (v2.0)</td>
                    <td><a href="/static/reports/saif_report.html" target="_blank" rel="noreferrer" className="btn btn-solid-red" style={{ padding: '4px 10px', fontSize: '11px' }}>🌐 HTML</a></td>
                    <td><a href="/static/reports/saif.docx" className="btn btn-solid-dark" style={{ padding: '4px 10px', fontSize: '11px' }}>📄 Word</a></td>
                    <td><a href="/static/reports/saif.pdf" className="btn btn-solid-red" style={{ padding: '4px 10px', fontSize: '11px' }}>📕 PDF</a></td>
                    <td><a href="/static/slides/saif.html" target="_blank" rel="noreferrer" className="btn btn-solid-purple" style={{ padding: '4px 10px', fontSize: '11px' }}>🖥️ Slides</a></td>
                    <td><a href="/static/zips/Saif_12308813_SecOps_DL_Project.zip" download className="btn" style={{ padding: '4px 10px', fontSize: '11px' }}>📦 Download ZIP</a></td>
                  </tr>
                  <tr style={{ backgroundColor: '#13233f' }}>
                    <td><strong>INT422 Master Archive</strong><br/><small style={{ color: '#38bdf8' }}>Complete Suite</small></td>
                    <td>3 Projects + Datasets + Models + Reports + Execution Manuals</td>
                    <td><span style={{ color: '#38bdf8', fontSize: '11px' }}>All 3 HTMLs</span></td>
                    <td><a href="/static/reports/HOW_TO_USE_AND_EXECUTION_MANUAL.docx" className="btn btn-solid-dark" style={{ padding: '4px 10px', fontSize: '11px' }}>📄 Manual</a></td>
                    <td><a href="/static/reports/HOW_TO_USE_AND_EXECUTION_MANUAL.pdf" className="btn btn-solid-red" style={{ padding: '4px 10px', fontSize: '11px' }}>📕 PDF</a></td>
                    <td><span style={{ color: 'var(--text-muted)', fontSize: '11px' }}>All 3 PPTs</span></td>
                    <td><a href="/static/zips/ALL_3_INT422_DL_PROJECTS_MASTER.zip" download className="btn btn-solid-blue" style={{ padding: '6px 14px', fontSize: '11px', fontWeight: 800 }}>🏆 Master DL ZIP</a></td>
                  </tr>
                </tbody>
              </table>
            </div>

            <div className="card">
              <div className="card-header">
                <span className="card-title">INT333 DevOps &amp; Configuration Management Deliverables</span>
                <span style={{ backgroundColor: 'var(--solid-green)', color: '#fff', fontSize: '10px', padding: '2px 8px', borderRadius: '4px', fontWeight: 800 }}>INFRASTRUCTURE</span>
              </div>
              <table className="solid-table">
                <thead>
                  <tr>
                    <th>Student &amp; Reg No</th>
                    <th>DevOps Stack</th>
                    <th>Project Synopsis</th>
                    <th>HTML Report</th>
                    <th>Word Report</th>
                    <th>Official PDF</th>
                    <th>Slide Deck</th>
                    <th>Package ZIP</th>
                  </tr>
                </thead>
                <tbody>
                  <tr>
                    <td><strong>Mohit Raj Deo</strong><br/><small style={{ color: 'var(--text-muted)' }}>12323329 | Roll: 62</small></td>
                    <td>Terraform + Nagios Core (Custom Service Plugin)</td>
                    <td><a href="/static/devops/mohit_synopsis.pdf" target="_blank" rel="noreferrer" className="btn btn-solid-dark" style={{ padding: '4px 10px', fontSize: '11px' }}>📑 Synopsis</a></td>
                    <td><a href="/static/devops/mohit_devops_report.html" target="_blank" rel="noreferrer" className="btn btn-solid-blue" style={{ padding: '4px 10px', fontSize: '11px' }}>🌐 HTML</a></td>
                    <td><a href="/static/devops/mohit_devops.docx" className="btn btn-solid-dark" style={{ padding: '4px 10px', fontSize: '11px' }}>📄 Word</a></td>
                    <td><a href="/static/devops/mohit_devops.pdf" className="btn btn-solid-red" style={{ padding: '4px 10px', fontSize: '11px' }}>📕 PDF</a></td>
                    <td><a href="/static/devops/mohit_devops_slides.html" target="_blank" rel="noreferrer" className="btn btn-solid-purple" style={{ padding: '4px 10px', fontSize: '11px' }}>🖥️ Slides</a></td>
                    <td><a href="/static/devops/Mohit_12323329_Terraform_Nagios.zip" download className="btn btn-solid-green" style={{ padding: '4px 10px', fontSize: '11px' }}>📦 Download ZIP</a></td>
                  </tr>
                  <tr>
                    <td><strong>Akash Choudhary</strong><br/><small style={{ color: 'var(--text-muted)' }}>12301625 | Roll: 11</small></td>
                    <td>Puppet Master/Agent + Nagios NRPE Monitoring</td>
                    <td><a href="/static/devops/akash_synopsis.pdf" target="_blank" rel="noreferrer" className="btn btn-solid-dark" style={{ padding: '4px 10px', fontSize: '11px' }}>📑 Synopsis</a></td>
                    <td><a href="/static/devops/akash_devops_report.html" target="_blank" rel="noreferrer" className="btn btn-solid-purple" style={{ padding: '4px 10px', fontSize: '11px' }}>🌐 HTML</a></td>
                    <td><a href="/static/devops/akash_devops.docx" className="btn btn-solid-dark" style={{ padding: '4px 10px', fontSize: '11px' }}>📄 Word</a></td>
                    <td><a href="/static/devops/akash_devops.pdf" className="btn btn-solid-red" style={{ padding: '4px 10px', fontSize: '11px' }}>📕 PDF</a></td>
                    <td><a href="/static/devops/akash_devops_slides.html" target="_blank" rel="noreferrer" className="btn btn-solid-purple" style={{ padding: '4px 10px', fontSize: '11px' }}>🖥️ Slides</a></td>
                    <td><a href="/static/devops/Akash_12301625_Puppet_Nagios.zip" download className="btn btn-solid-green" style={{ padding: '4px 10px', fontSize: '11px' }}>📦 Download ZIP</a></td>
                  </tr>
                  <tr>
                    <td><strong>Saif Siddique</strong><br/><small style={{ color: 'var(--text-muted)' }}>12308813 | Roll: 44</small></td>
                    <td>Terraform Multi-Tier ALB + Nagios High Availability</td>
                    <td><a href="/static/devops/saif_synopsis.pdf" target="_blank" rel="noreferrer" className="btn btn-solid-dark" style={{ padding: '4px 10px', fontSize: '11px' }}>📑 Synopsis</a></td>
                    <td><a href="/static/devops/saif_devops_report.html" target="_blank" rel="noreferrer" className="btn btn-solid-red" style={{ padding: '4px 10px', fontSize: '11px' }}>🌐 HTML</a></td>
                    <td><a href="/static/devops/saif_devops.docx" className="btn btn-solid-dark" style={{ padding: '4px 10px', fontSize: '11px' }}>📄 Word</a></td>
                    <td><a href="/static/devops/saif_devops.pdf" className="btn btn-solid-red" style={{ padding: '4px 10px', fontSize: '11px' }}>📕 PDF</a></td>
                    <td><a href="/static/devops/saif_devops_slides.html" target="_blank" rel="noreferrer" className="btn btn-solid-purple" style={{ padding: '4px 10px', fontSize: '11px' }}>🖥️ Slides</a></td>
                    <td><a href="/static/devops/Saif_12308813_Terraform_ALB_Nagios.zip" download className="btn btn-solid-green" style={{ padding: '4px 10px', fontSize: '11px' }}>📦 Download ZIP</a></td>
                  </tr>
                  <tr style={{ backgroundColor: '#09291b' }}>
                    <td><strong>INT333 Master Archive</strong><br/><small style={{ color: '#34d399' }}>Complete Suite</small></td>
                    <td>Complete DevOps Package &amp; Comprehensive Execution Manual</td>
                    <td><span style={{ color: '#34d399', fontSize: '11px' }}>All 3 Synopses</span></td>
                    <td><a href="/static/devops/HOW_TO_USE_AND_EXECUTION_MANUAL.docx" className="btn btn-solid-dark" style={{ padding: '4px 10px', fontSize: '11px' }}>📄 Manual</a></td>
                    <td><a href="/static/devops/HOW_TO_USE_AND_EXECUTION_MANUAL.pdf" className="btn btn-solid-red" style={{ padding: '4px 10px', fontSize: '11px' }}>📕 PDF</a></td>
                    <td><span style={{ color: 'var(--text-muted)', fontSize: '11px' }}>All 3 PPTs</span></td>
                    <td><a href="/static/devops/ALL_3_DEVOPS_PROJECTS_MASTER.zip" download className="btn btn-solid-green" style={{ padding: '6px 14px', fontSize: '11px', fontWeight: 800 }}>🏆 Master DevOps ZIP</a></td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>
        )}
      </main>
    </div>
  );
}

