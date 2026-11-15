import React, { useState, useEffect, useRef } from 'react';

export default function App() {
  const [cpu, setCpu] = useState(22);
  const [mem, setMem] = useState(41);
  const [lat, setLat] = useState(18);
  const [sock, setSock] = useState(120);

  const [healthIndex, setHealthIndex] = useState(98.2);
  const [isAnomaly, setIsAnomaly] = useState(false);
  const [anomalyScore, setAnomalyScore] = useState(0.152);
  const [matchedRunbook, setMatchedRunbook] = useState('None (System Healthy)');
  const [ragConfidence, setRagConfidence] = useState(95);
  const [mttr, setMttr] = useState(0);
  const [rcaReport, setRcaReport] = useState('Waiting for telemetry ingestion...');
  const [latencyMs, setLatencyMs] = useState(3.4);
  const [copied, setCopied] = useState(false);

  const chartRef = useRef(null);
  const chartInstance = useRef(null);

  useEffect(() => {
    if (window.Chart && chartRef.current) {
      if (!chartInstance.current) {
        chartInstance.current = new window.Chart(chartRef.current, {
          type: 'line',
          data: {
            labels: ['-50s', '-40s', '-30s', '-20s', '-10s', 'Now'],
            datasets: [
              {
                label: 'CPU %',
                data: [20, 22, 21, 24, 22, cpu],
                borderColor: '#2563eb',
                backgroundColor: 'rgba(37, 99, 235, 0.25)',
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
                backgroundColor: 'rgba(124, 58, 237, 0.25)',
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
        const d = chartInstance.current.data.datasets;
        d[0].data.shift();
        d[0].data.push(cpu);
        d[1].data.shift();
        d[1].data.push(mem);
        chartInstance.current.update();
      }
    }
  }, [cpu, mem]);

  const sendTelemetry = async (cVal = cpu, mVal = mem, lVal = lat, sVal = sock) => {
    const t0 = performance.now();
    try {
      const res = await fetch('/api/aiops/telemetry', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ cpu: cVal, memory: mVal, latency: lVal, sockets: sVal })
      });
      const data = await res.json();
      setLatencyMs(Math.round(performance.now() - t0));

      setHealthIndex(data.monitoring.system_health_index || 95.0);
      setIsAnomaly(data.monitoring.is_anomaly);
      setAnomalyScore(data.monitoring.anomaly_score);
      setMatchedRunbook(data.investigation.retrieved_runbook.title);
      setRagConfidence(Math.round((data.investigation.rag_confidence || 0.9) * 100));
      setMttr(data.remediation.estimated_recovery_time_sec || 12);
      setRcaReport(data.rca_report);
    } catch (err) {
      setRcaReport('AIOps Microservice API Error: ' + err.message);
    }
  };

  useEffect(() => {
    sendTelemetry(cpu, mem, lat, sock);
  }, []);

  const handleCopy = () => {
    navigator.clipboard.writeText(rcaReport);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  return (
    <div>
      {/* Header */}
      <header>
        <div style={{ display: 'flex', alignItems: 'center', gap: '14px' }}>
          <div className="brand-badge">Δ</div>
          <div>
            <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
              <h1 style={{ fontSize: '17px', fontWeight: 800 }}>AIOps Cloud Intelligence Platform</h1>
              <span style={{ backgroundColor: 'var(--solid-blue)', color: '#fff', fontSize: '10px', padding: '2px 8px', borderRadius: '4px', fontWeight: 800 }}>
                HARD SOLID v2.0
              </span>
            </div>
            <p style={{ fontSize: '11px', color: 'var(--text-muted)' }}>Student: Mohit Raj Deo (12323329 | Roll: 62) | INT422 Capstone</p>
          </div>
        </div>

        <div style={{ display: 'flex', alignItems: 'center', gap: '12px' }}>
          <div className="chip">PORT: 5001</div>
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
            <div className="pipeline-step">Stage 1: Ingestion</div>
            <div className="pipeline-title">Telemetry Streamer</div>
            <div className="pipeline-desc">Real-time rolling buffer &amp; gradients</div>
          </div>
          <div className="pipeline-node active-node">
            <div className="pipeline-step">Stage 2: Inference</div>
            <div className="pipeline-title">Isolation Forest</div>
            <div className="pipeline-desc">100 iTrees unsupervised anomaly scoring</div>
          </div>
          <div className="pipeline-node active-node">
            <div className="pipeline-step">Stage 3: Vector RAG</div>
            <div className="pipeline-title">Runbook Matcher</div>
            <div className="pipeline-desc">Cosine similarity ranking over SRE SOPs</div>
          </div>
          <div className="pipeline-node active-node">
            <div className="pipeline-step">Stage 4: LLM Action</div>
            <div className="pipeline-title">Auto-Remediation</div>
            <div className="pipeline-desc">Automated SQL/Shell recovery execution</div>
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

        {/* 4 Stat Cards */}
        <div className="grid-4">
          <div className="stat-card">
            <div className="stat-label">System Health Index</div>
            <div className="stat-val" style={{ color: healthIndex < 50 ? 'var(--solid-red)' : (healthIndex < 75 ? 'var(--solid-amber)' : 'var(--solid-green)') }}>
              {Math.round(healthIndex)}%
            </div>
            <div className="stat-sub">{healthIndex < 50 ? 'CRITICAL STATE' : (healthIndex < 75 ? 'DEGRADED PERFORMANCE' : 'OPTIMAL BASELINE')}</div>
          </div>

          <div className="stat-card">
            <div className="stat-label">ML Anomaly Status</div>
            <div className="stat-val" style={{ color: isAnomaly ? 'var(--solid-red)' : 'var(--solid-green)' }}>
              {isAnomaly ? 'ANOMALY DETECTED' : 'NORMAL'}
            </div>
            <div className="stat-sub">Decision Score: <strong style={{ color: '#fff' }}>{anomalyScore}</strong></div>
          </div>

          <div className="stat-card">
            <div className="stat-label">Matched SRE Runbook</div>
            <div className="stat-val" style={{ fontSize: '14px', marginTop: '6px', color: '#38bdf8', lineHeight: 1.3 }}>
              {matchedRunbook}
            </div>
            <div className="stat-sub">Vector RAG Confidence: <strong style={{ color: '#fff' }}>{ragConfidence}%</strong></div>
          </div>

          <div className="stat-card">
            <div className="stat-label">Estimated MTTR</div>
            <div className="stat-val" style={{ color: 'var(--solid-amber)' }}>
              {mttr}s
            </div>
            <div className="stat-sub">Autonomous Self-Healing Loop</div>
          </div>
        </div>

        {/* 2-Column Main Content */}
        <div className="grid-2">
          {/* Controls Column */}
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
              <input type="range" min="1" max="100" value={cpu} onChange={(e) => { const v = Number(e.target.value); setCpu(v); sendTelemetry(v, mem, lat, sock); }} />
            </div>

            <div className="control-group">
              <div className="control-label">
                <span>Memory Consumption</span>
                <span>{mem}%</span>
              </div>
              <input type="range" min="1" max="100" value={mem} onChange={(e) => { const v = Number(e.target.value); setMem(v); sendTelemetry(cpu, v, lat, sock); }} />
            </div>

            <div className="control-group">
              <div className="control-label">
                <span>HTTP / TCP Latency (ms)</span>
                <span>{lat}ms</span>
              </div>
              <input type="range" min="5" max="2500" value={lat} onChange={(e) => { const v = Number(e.target.value); setLat(v); sendTelemetry(cpu, mem, v, sock); }} />
            </div>

            <div className="control-group">
              <div className="control-label">
                <span>Active Sockets</span>
                <span>{sock}</span>
              </div>
              <input type="range" min="10" max="5000" value={sock} onChange={(e) => { const v = Number(e.target.value); setSock(v); sendTelemetry(cpu, mem, lat, v); }} />
            </div>

            {/* Sparkline Canvas */}
            <div className="card-header" style={{ marginTop: '16px', marginBottom: '8px' }}>
              <span className="card-title" style={{ fontSize: '12px' }}>📊 Live Telemetry Stream Trend</span>
            </div>
            <div style={{ position: 'relative', height: '140px', width: '100%', marginBottom: '14px' }}>
              <canvas ref={chartRef}></canvas>
            </div>

            <div className="card-header">
              <span className="card-title" style={{ fontSize: '12px' }}>🚨 Chaos Fault Injection Presets</span>
            </div>
            <div style={{ display: 'grid', gridTemplateColumns: 'repeat(2, 1fr)', gap: '8px' }}>
              <button className="btn btn-solid-dark" onClick={() => { setCpu(22); setMem(41); setLat(18); setSock(120); sendTelemetry(22, 41, 18, 120); }}>
                Normal Baseline
              </button>
              <button className="btn btn-solid-red" onClick={() => { setCpu(94); setMem(95); setLat(450); setSock(420); sendTelemetry(94, 95, 450, 420); }}>
                Memory Leak (RB-104)
              </button>
              <button className="btn btn-solid-red" onClick={() => { setCpu(98); setMem(55); setLat(320); setSock(250); sendTelemetry(98, 55, 320, 250); }}>
                CPU Choke (RB-108)
              </button>
              <button className="btn btn-solid-red" onClick={() => { setCpu(85); setMem(88); setLat(1200); setSock(3200); sendTelemetry(85, 88, 1200, 3200); }}>
                Socket Storm (RB-212)
              </button>
            </div>
          </div>

          {/* Terminal Output */}
          <div className="card">
            <div className="card-header">
              <span className="card-title">AIOps Autonomous Multi-Agent Response Stream</span>
              <div style={{ display: 'flex', gap: '8px' }}>
                <button className="btn btn-solid-dark" onClick={handleCopy}>
                  {copied ? '✓ Copied' : '📋 Copy RCA'}
                </button>
                <button className="btn" onClick={() => sendTelemetry()}>
                  ⚡ Force Cycle
                </button>
              </div>
            </div>
            <div className="terminal-box">{rcaReport}</div>
          </div>
        </div>
      </main>
    </div>
  );
}
