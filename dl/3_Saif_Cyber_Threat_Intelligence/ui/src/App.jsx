import React, { useState, useEffect } from 'react';

export default function App() {
  const [ip, setIp] = useState('203.0.113.88');
  const [pkt, setPkt] = useState(450);
  const [pps, setPps] = useState(600);
  const [syn, setSyn] = useState(75);
  const [port, setPort] = useState(80);

  const [attackType, setAttackType] = useState('DDoS');
  const [confidence, setConfidence] = useState(100.0);
  const [threatRiskScore, setThreatRiskScore] = useState(95);
  const [techniqueId, setTechniqueId] = useState('T1498.001');
  const [tactic, setTactic] = useState('Impact');
  const [quarantineStatus, setQuarantineStatus] = useState('BLOCKED & ISOLATED');
  const [ctiBrief, setCtiBrief] = useState('Waiting for threat triage trigger...');
  const [latencyMs, setLatencyMs] = useState(3.8);
  const [copied, setCopied] = useState(false);

  const executeTriage = async (pLen = pkt, pRate = pps, sCount = syn, tPort = port, sIp = ip) => {
    const t0 = performance.now();
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
      setLatencyMs(Math.round(performance.now() - t0));

      const isThreat = data.triage.is_threat;
      setAttackType(data.triage.attack_type);
      setConfidence(Number((data.triage.confidence_score * 100).toFixed(1)));
      setThreatRiskScore(Math.round(data.triage.threat_risk_score || (isThreat ? 95 : 5)));
      setTechniqueId(data.threat_intelligence.technique_id || '--');
      setTactic(data.threat_intelligence.tactic || '--');
      setQuarantineStatus(isThreat ? 'BLOCKED & ISOLATED' : 'ACTIVE MONITORING');
      setCtiBrief(data.cti_brief);
    } catch (err) {
      setCtiBrief('SecOps Microservice API Error: ' + err.message);
    }
  };

  useEffect(() => {
    executeTriage();
  }, []);

  const setPreset = (pLen, pRate, sCount, tPort) => {
    setPkt(pLen);
    setPps(pRate);
    setSyn(sCount);
    setPort(tPort);
    executeTriage(pLen, pRate, sCount, tPort, ip);
  };

  const handleCopy = () => {
    navigator.clipboard.writeText(ctiBrief);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  const isMalicious = attackType !== 'Normal Traffic';

  return (
    <div>
      {/* Header */}
      <header>
        <div style={{ display: 'flex', alignItems: 'center', gap: '14px' }}>
          <div className="brand-badge">🔒</div>
          <div>
            <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
              <h1 style={{ fontSize: '17px', fontWeight: 800 }}>SOC Cyber Threat Hunter</h1>
              <span style={{ backgroundColor: 'var(--solid-red)', color: '#fff', fontSize: '10px', padding: '2px 8px', borderRadius: '4px', fontWeight: 800 }}>
                HARD SOLID v2.0
              </span>
            </div>
            <p style={{ fontSize: '11px', color: 'var(--text-muted)' }}>Student: Saif Siddique (12308813 | Roll: 44) | INT422 Capstone</p>
          </div>
        </div>

        <div style={{ display: 'flex', alignItems: 'center', gap: '12px' }}>
          <div className="chip">PORT: 5003</div>
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
            <div className="pipeline-step">Stage 1: Triage</div>
            <div className="pipeline-title">Flow Ingestion</div>
            <div className="pipeline-desc">Real-time packet feature extraction &amp; buffer</div>
          </div>
          <div className="pipeline-node active-node">
            <div className="pipeline-step">Stage 2: Deep MLP Net</div>
            <div className="pipeline-title">Intrusion Classifier</div>
            <div className="pipeline-desc">Multi-class flow classification neural net</div>
          </div>
          <div className="pipeline-node active-node">
            <div className="pipeline-step">Stage 3: MITRE ATT&amp;CK</div>
            <div className="pipeline-title">Threat Intel RAG</div>
            <div className="pipeline-desc">Adversary technique &amp; IOC correlation</div>
          </div>
          <div className="pipeline-node active-node">
            <div className="pipeline-step">Stage 4: Active Defense</div>
            <div className="pipeline-title">Zero Trust Containment</div>
            <div className="pipeline-desc">Linux Netfilter, nftables &amp; AWS security rules</div>
          </div>
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

        {/* Metric Cards Row */}
        <div className="grid-4">
          <div className="stat-card">
            <div className="stat-label">Threat Classification</div>
            <div className="stat-val" style={{ color: isMalicious ? 'var(--solid-red)' : 'var(--solid-green)' }}>
              {attackType}
            </div>
            <div className="stat-sub">Neural Confidence: <span style={{ color: '#fff' }}>{confidence}%</span></div>
          </div>

          <div className="stat-card">
            <div className="stat-label">Threat Risk Score</div>
            <div style={{ display: 'flex', alignItems: 'center', gap: '16px', margin: '8px 0' }}>
              <div style={{ position: 'relative', width: '74px', height: '74px' }}>
                <svg style={{ transform: 'rotate(-90deg)', width: '74px', height: '74px' }}>
                  <circle cx="37" cy="37" r="30" fill="none" stroke="#1e293b" strokeWidth="7" />
                  <circle
                    cx="37"
                    cy="37"
                    r="30"
                    fill="none"
                    stroke={threatRiskScore > 50 ? 'var(--solid-red)' : 'var(--solid-green)'}
                    strokeWidth="7"
                    strokeDasharray="188.5"
                    strokeDashoffset={188.5 - (188.5 * (threatRiskScore / 100))}
                    strokeLinecap="round"
                    style={{ transition: 'stroke-dashoffset 0.4s ease, stroke 0.3s ease' }}
                  />
                </svg>
                <div style={{ position: 'absolute', top: '50%', left: '50%', transform: 'translate(-50%, -50%)', fontFamily: 'JetBrains Mono', fontSize: '14px', fontWeight: 800 }}>
                  {threatRiskScore}
                </div>
              </div>
              <div>
                <div style={{ fontSize: '13px', fontWeight: 800, color: threatRiskScore > 50 ? 'var(--solid-red)' : 'var(--solid-green)' }}>
                  {threatRiskScore > 50 ? 'CRITICAL RISK' : 'LOW RISK'}
                </div>
                <div className="stat-sub">Blast Radius Index</div>
              </div>
            </div>
          </div>

          <div className="stat-card">
            <div className="stat-label">MITRE Technique ID</div>
            <div className="stat-val" style={{ fontSize: '16px', marginTop: '6px', color: 'var(--solid-blue)' }}>
              {techniqueId}
            </div>
            <div className="stat-sub">Tactic: <span style={{ color: '#fff' }}>{tactic}</span></div>
          </div>

          <div className="stat-card">
            <div className="stat-label">Perimeter Quarantine</div>
            <div className="stat-val" style={{ color: isMalicious ? 'var(--solid-red)' : 'var(--solid-green)', fontSize: '16px', marginTop: '6px' }}>
              {quarantineStatus}
            </div>
            <div className="stat-sub">Zero-Trust Packet Filtering</div>
          </div>
        </div>

        {/* 2-Column Main Content */}
        <div className="grid-2">
          {/* Controls Column */}
          <div>
            <div className="card">
              <div className="card-header">
                <span className="card-title">Network Packet Flow Synthesizer</span>
                <span className="chip" style={{ fontSize: '10px' }}>Flow Vector</span>
              </div>

              <div className="control-group">
                <div className="control-label">
                  <span>Adversary Source IP</span>
                  <span>Attacker Origin</span>
                </div>
                <input
                  type="text"
                  value={ip}
                  onChange={(e) => setIp(e.target.value)}
                  style={{ width: '100%', background: '#000000', border: '2px solid var(--border-solid)', borderRadius: '6px', padding: '8px 12px', color: '#fff', fontFamily: 'JetBrains Mono', fontSize: '12px' }}
                />
              </div>

              <div className="control-group">
                <div className="control-label">
                  <span>Packet Length (Bytes)</span>
                  <span>{pkt} B</span>
                </div>
                <input type="range" min="40" max="9000" value={pkt} onChange={(e) => { setPkt(Number(e.target.value)); executeTriage(Number(e.target.value), pps, syn, port, ip); }} />
              </div>

              <div className="control-group">
                <div className="control-label">
                  <span>Packets Per Second (PPS)</span>
                  <span>{pps} PPS</span>
                </div>
                <input type="range" min="5" max="25000" value={pps} onChange={(e) => { setPps(Number(e.target.value)); executeTriage(pkt, Number(e.target.value), syn, port, ip); }} />
              </div>

              <div className="control-group">
                <div className="control-label">
                  <span>TCP SYN Flags Count</span>
                  <span>{syn}</span>
                </div>
                <input type="range" min="0" max="2500" value={syn} onChange={(e) => { setSyn(Number(e.target.value)); executeTriage(pkt, pps, Number(e.target.value), port, ip); }} />
              </div>

              <div className="card-header" style={{ marginTop: '16px', marginBottom: '8px' }}>
                <span className="card-title" style={{ fontSize: '12px' }}>🚨 Adversarial Attack Presets</span>
              </div>
              <div className="btn-group">
                <button className="btn btn-solid-dark" onClick={() => setPreset(400, 15, 1, 443)}>Normal Enterprise</button>
                <button className="btn" onClick={() => setPreset(450, 750, 85, 80)}>🚨 SYN Flood (DDoS)</button>
                <button className="btn" onClick={() => setPreset(60, 45, 2, 22)}>🚨 PortScan (T1046)</button>
                <button className="btn" onClick={() => setPreset(1450, 30, 1, 80)}>🚨 SQL Injection (T1190)</button>
              </div>

              <button className="btn btn-solid-blue" style={{ marginTop: '16px', width: '100%', justifyContent: 'center' }} onClick={() => executeTriage()}>
                ⚡ Ingest &amp; Mitigate Live Flow
              </button>
            </div>
          </div>

          {/* Terminal Output */}
          <div>
            <div className="card">
              <div className="card-header">
                <span className="card-title">Autonomous SOC Threat Intelligence Brief</span>
                <div style={{ display: 'flex', gap: '8px' }}>
                  <button className="btn btn-solid-dark" onClick={handleCopy}>
                    {copied ? '✓ Copied!' : '📋 Copy CTI Brief'}
                  </button>
                </div>
              </div>
              <div className="terminal-box">{ctiBrief}</div>
            </div>
          </div>
        </div>
      </main>
    </div>
  );
}
