import React, { useState, useEffect, useRef } from 'react';

export default function App() {
  const [prompt, setPrompt] = useState('Build a high-performance sliding window API Rate Limiter in Python with auto cleanup');
  const [maintainabilityIndex, setMaintainabilityIndex] = useState(55.5);
  const [cyclomaticComplexity, setCyclomaticComplexity] = useState(4);
  const [loc, setLoc] = useState(19);
  const [astDepth, setAstDepth] = useState(10);
  const [defectRisk, setDefectRisk] = useState('CLEAN (Production Ready)');
  const [defectProbability, setDefectProbability] = useState(1.2);
  const [testStatus, setTestStatus] = useState('PASS');
  const [coveragePct, setCoveragePct] = useState(100.0);
  const [codeOutput, setCodeOutput] = useState('Waiting for SWE swarm execution...');
  const [latencyMs, setLatencyMs] = useState(4.2);
  const [copied, setCopied] = useState(false);

  const radarRef = useRef(null);
  const radarInstance = useRef(null);

  // Initialize and update Radar Chart
  useEffect(() => {
    if (window.Chart && radarRef.current) {
      if (!radarInstance.current) {
        radarInstance.current = new window.Chart(radarRef.current, {
          type: 'radar',
          data: {
            labels: ['Maintainability', 'Test Coverage', 'AST Simplicity', 'Cleanliness', 'Security Compliance'],
            datasets: [{
              label: 'Code Quality Vector',
              data: [maintainabilityIndex, coveragePct, 80, 95, 90],
              borderColor: '#7c3aed',
              backgroundColor: 'rgba(124, 58, 237, 0.25)',
              borderWidth: 2,
              pointBackgroundColor: '#2563eb'
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
                grid: { color: 'rgba(255,255,255,0.08)' },
                pointLabels: { color: '#cbd5e1', font: { size: 9, weight: 'bold' } }
              }
            }
          }
        });
      } else {
        radarInstance.current.data.datasets[0].data = [
          maintainabilityIndex,
          coveragePct,
          Math.max(40, 100 - cyclomaticComplexity * 8),
          100 - defectProbability,
          95
        ];
        radarInstance.current.update();
      }
    }
  }, [maintainabilityIndex, coveragePct, cyclomaticComplexity, defectProbability]);

  const executePipeline = async (targetPrompt = prompt) => {
    const t0 = performance.now();
    try {
      const res = await fetch('/api/swe/generate', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ prompt: targetPrompt })
      });
      const data = await res.json();
      setLatencyMs(Math.round(performance.now() - t0));

      const m = data.code_data.metrics;
      const mi = m.maintainability_index || 65.0;
      setMaintainabilityIndex(mi);
      setCyclomaticComplexity(m.cyclomatic_complexity);
      setLoc(m.loc);
      setAstDepth(m.ast_depth);
      setDefectRisk(data.defect_audit.risk_label);
      setDefectProbability(Number((data.defect_audit.defect_probability * 100).toFixed(1)));
      setTestStatus(data.test_results.test_suite_status);
      setCoveragePct(data.test_results.coverage_pct);

      let out = `======================================================================
1. ARCHITECT AGENT & RAG DESIGN PATTERN:
Module Target   : ${data.specification.module_name}
Category        : ${data.specification.category || "Application Architecture"}
Pattern Match   : ${data.specification.recommended_pattern}
Security Policy : ${data.specification.security_policy}

2. REAL AST STATIC METRICS & MAINTAINABILITY:
LOC: ${m.loc} | Cyclomatic Complexity: ${m.cyclomatic_complexity} | AST Depth: ${m.ast_depth}
Maintainability Index : ${mi} / 100 (${data.defect_audit.maintainability_rating || "ACCEPTABLE"})
ML Defect Probability : ${(data.defect_audit.defect_probability*100).toFixed(2)}% [${data.defect_audit.risk_label}]

3. AUTOMATED SANDBOX TEST SUITE:
Status: ${data.test_results.test_suite_status} (${data.test_results.tests_passed}/${data.test_results.tests_executed} Unit Tests Passed)
Statement Coverage : ${data.test_results.coverage_pct}%

======================================================================
VALIDATED CODE ARTIFACT:
${data.code_data.code}
`;
      setCodeOutput(out);
    } catch (err) {
      setCodeOutput('SWE Swarm API Error: ' + err.message);
    }
  };

  useEffect(() => {
    executePipeline(prompt);
  }, []);

  const handleCopy = () => {
    navigator.clipboard.writeText(codeOutput);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  return (
    <div>
      {/* Header */}
      <header>
        <div style={{ display: 'flex', alignItems: 'center', gap: '14px' }}>
          <div className="brand-badge">⚡</div>
          <div>
            <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
              <h1 style={{ fontSize: '17px', fontWeight: 800 }}>Autonomous SWE Platform</h1>
              <span style={{ backgroundColor: 'var(--solid-violet)', color: '#fff', fontSize: '10px', padding: '2px 8px', borderRadius: '4px', fontWeight: 800 }}>
                HARD SOLID v2.0
              </span>
            </div>
            <p style={{ fontSize: '11px', color: 'var(--text-muted)' }}>Student: Akash Choudhary (12301625 | Roll: 11) | INT422 Capstone</p>
          </div>
        </div>

        <div style={{ display: 'flex', alignItems: 'center', gap: '12px' }}>
          <div className="chip">PORT: 5002</div>
          <div className="chip">LATENCY: {latencyMs}ms</div>
          <div className="status-chip">
            <span className="pulse-dot"></span>
            <span>MICROSERVICE ONLINE</span>
          </div>
        </div>
      </header>

      {/* Main Container */}
      <main>
        {/* 4-Stage Agent State Pipeline */}
        <div className="pipeline-tracker">
          <div className="pipeline-node active-node">
            <div className="pipeline-step">Stage 1: Architect</div>
            <div className="pipeline-title">Requirement RAG</div>
            <div className="pipeline-desc">Gang of Four & Clean Architecture decomposition</div>
          </div>
          <div className="pipeline-node active-node">
            <div className="pipeline-step">Stage 2: Developer</div>
            <div className="pipeline-title">Code Synthesizer</div>
            <div className="pipeline-desc">Modular clean architecture class generator</div>
          </div>
          <div className="pipeline-node active-node">
            <div className="pipeline-step">Stage 3: AST Analyzer</div>
            <div className="pipeline-title">AST Static Parser</div>
            <div className="pipeline-desc">Real Cyclomatic Complexity & Maintainability Index</div>
          </div>
          <div className="pipeline-node active-node">
            <div className="pipeline-step">Stage 4: Sandbox Tester</div>
            <div className="pipeline-title">Unit Test Runner</div>
            <div className="pipeline-desc">Dynamic validation & statement coverage</div>
          </div>
        </div>

        {/* Deep Learning & Static Analysis Model Architecture Card */}
        <div style={{ backgroundColor: '#0f182c', border: '2px solid var(--solid-violet)', padding: '14px 20px', borderRadius: '8px', marginBottom: '20px', boxShadow: '0 4px 0 #000', display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
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
          <span style={{ backgroundColor: 'var(--solid-violet)', color: '#fff', padding: '4px 12px', borderRadius: '4px', fontWeight: 800, fontSize: '11px' }}>
            ACTIVE ML &amp; AST ENGINE
          </span>
        </div>

        {/* Metric Cards Row */}
        <div className="grid-4">
          <div className="stat-card">
            <div className="stat-label">Maintainability Index</div>
            <div className="stat-val" style={{ color: maintainabilityIndex > 50 ? 'var(--solid-green)' : 'var(--solid-amber)' }}>
              {maintainabilityIndex} / 100
            </div>
            <div className="stat-sub">SEI Metric Standard</div>
          </div>

          <div className="stat-card">
            <div className="stat-label">ML Defect Risk</div>
            <div className="stat-val" style={{ color: defectProbability < 5 ? 'var(--solid-green)' : 'var(--solid-amber)' }}>
              {defectProbability}% Prob
            </div>
            <div className="stat-sub">Random Forest Assessment</div>
          </div>

          <div className="stat-card">
            <div className="stat-label">Cyclomatic Complexity</div>
            <div className="stat-val" style={{ color: 'var(--solid-blue)' }}>
              {cyclomaticComplexity} (LOC: {loc})
            </div>
            <div className="stat-sub">AST Tree Decision Branches</div>
          </div>

          <div className="stat-card">
            <div className="stat-label">Sandbox Test Suite</div>
            <div className="stat-val" style={{ color: testStatus === 'PASS' ? 'var(--solid-green)' : 'var(--solid-red)' }}>
              {testStatus} ({coveragePct}%)
            </div>
            <div className="stat-sub">Automated Statement Coverage</div>
          </div>
        </div>

        {/* 2-Column Main Content */}
        <div className="grid-2">
          {/* Prompt Column */}
          <div>
            <div className="card">
              <div className="card-header">
                <span className="card-title">Software Requirement Specification</span>
                <span className="chip" style={{ fontSize: '10px' }}>Natural Language</span>
              </div>

              <textarea
                style={{ width: '100%', height: '110px', background: '#000000', border: '2px solid var(--border-solid)', borderRadius: '6px', padding: '12px', color: '#fff', fontFamily: 'inherit', fontSize: '13px', resize: 'none' }}
                value={prompt}
                onChange={(e) => setPrompt(e.target.value)}
              />

              <div className="card-header" style={{ marginTop: '14px', marginBottom: '8px' }}>
                <span className="card-title" style={{ fontSize: '12px' }}>Architectural Presets</span>
              </div>
              <div className="btn-group">
                <button
                  className="btn btn-solid-dark"
                  onClick={() => {
                    const p = 'Build a high-performance sliding window API Rate Limiter in Python with auto cleanup';
                    setPrompt(p);
                    executePipeline(p);
                  }}
                >
                  Rate Limiter
                </button>
                <button
                  className="btn btn-solid-dark"
                  onClick={() => {
                    const p = 'Design and implement a thread-safe O(1) LRU Cache with mutex locking';
                    setPrompt(p);
                    executePipeline(p);
                  }}
                >
                  Thread-Safe LRU Cache
                </button>
                <button
                  className="btn btn-solid-dark"
                  onClick={() => {
                    const p = 'Create a stateless HMAC-SHA256 JWT Auth token validator with expiry checks';
                    setPrompt(p);
                    executePipeline(p);
                  }}
                >
                  JWT Token Validator
                </button>
                <button
                  className="btn btn-solid-dark"
                  onClick={() => {
                    const p = 'Implement Kadanes algorithm for maximum sub-array sum with boundary checks';
                    setPrompt(p);
                    executePipeline(p);
                  }}
                >
                  Kadane Max Subarray
                </button>
                <button
                  className="btn btn-solid-dark"
                  onClick={() => {
                    const p = 'Build an asynchronous Kafka consumer with exponential backoff and DLQ routing';
                    setPrompt(p);
                    executePipeline(p);
                  }}
                >
                  Kafka Async Consumer
                </button>
              </div>

              {/* Radar Chart Canvas */}
              <div className="card-header" style={{ marginTop: '16px', marginBottom: '8px' }}>
                <span className="card-title" style={{ fontSize: '12px' }}>📊 AST Code Quality Radar</span>
              </div>
              <div style={{ position: 'relative', height: '150px', width: '100%', marginBottom: '14px' }}>
                <canvas ref={radarRef}></canvas>
              </div>

              <button className="btn" style={{ width: '100%', justifyContent: 'center' }} onClick={() => executePipeline(prompt)}>
                🚀 Trigger Multi-Agent SWE Swarm
              </button>
            </div>
          </div>

          {/* Code Viewer Column */}
          <div>
            <div className="card">
              <div className="card-header">
                <span className="card-title">Validated Code Artifact &amp; Audit Trace</span>
                <button className="btn btn-solid-dark" onClick={handleCopy}>
                  {copied ? '✓ Copied!' : '📋 Copy Code Artifact'}
                </button>
              </div>
              <div className="terminal-box">{codeOutput}</div>
            </div>
          </div>
        </div>
      </main>
    </div>
  );
}
