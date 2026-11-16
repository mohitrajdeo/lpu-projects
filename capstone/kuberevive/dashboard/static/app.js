// KubeRevive Dashboard Frontend JavaScript (Chart.js & Live Polling)

let telemetryChart;
const maxDataPoints = 30;
const chartLabels = [];
const cpuData = [];
const memData = [];
const latData = [];

function initChart() {
    const ctx = document.getElementById('telemetryChart').getContext('2d');
    telemetryChart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: chartLabels,
            datasets: [
                {
                    label: 'CPU Usage (%)',
                    data: cpuData,
                    borderColor: '#6366f1',
                    backgroundColor: 'rgba(99, 102, 241, 0.1)',
                    borderWidth: 2,
                    tension: 0.3,
                    fill: false
                },
                {
                    label: 'Memory Usage (%)',
                    data: memData,
                    borderColor: '#06b6d4',
                    backgroundColor: 'rgba(6, 182, 212, 0.1)',
                    borderWidth: 2,
                    tension: 0.3,
                    fill: false
                },
                {
                    label: 'Latency (ms / 10)',
                    data: latData,
                    borderColor: '#f59e0b',
                    backgroundColor: 'rgba(245, 158, 11, 0.1)',
                    borderWidth: 2,
                    tension: 0.3,
                    fill: false
                }
            ]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            animation: false,
            scales: {
                x: {
                    display: false
                },
                y: {
                    min: 0,
                    max: 120,
                    grid: {
                        color: 'rgba(51, 65, 85, 0.4)'
                    },
                    ticks: {
                        color: '#94a3b8',
                        font: { family: 'JetBrains Mono', size: 10 }
                    }
                }
            },
            plugins: {
                legend: {
                    labels: {
                        color: '#cbd5e1',
                        font: { size: 11 }
                    }
                }
            }
        }
    });
}

async function fetchStatus() {
    try {
        const res = await fetch('/api/status');
        if (!res.ok) return;
        const data = await res.json();
        updateUI(data);
    } catch (err) {
        console.error("Fetch status failed:", err);
    }
}

function updateUI(data) {
    const t = data.current_telemetry || {};
    const evalRes = data.anomaly_evaluation || {};

    // 1. Update metric values
    const cpu = t.cpu_usage_pct || 0;
    const mem = t.memory_usage_pct || 0;
    const lat = t.latency_ms || 0;
    const err = t.error_rate_pct || 0;

    document.getElementById('cpuValue').innerText = cpu.toFixed(1) + ' %';
    document.getElementById('cpuBar').style.width = Math.min(cpu, 100) + '%';
    document.getElementById('cpuBadge').innerText = cpu > 80 ? 'CRITICAL' : (cpu > 60 ? 'HIGH' : 'Normal');
    document.getElementById('cpuBadge').className = cpu > 80 ? 'text-rose-400 font-bold' : (cpu > 60 ? 'text-amber-400 font-bold' : 'text-emerald-400');

    document.getElementById('memValue').innerText = mem.toFixed(1) + ' %';
    document.getElementById('memBar').style.width = Math.min(mem, 100) + '%';
    document.getElementById('memBadge').innerText = mem > 85 ? 'LEAK DETECTED' : 'Normal';
    document.getElementById('memBadge').className = mem > 85 ? 'text-rose-400 font-bold' : 'text-emerald-400';

    document.getElementById('latValue').innerText = lat.toFixed(0) + ' ms';
    document.getElementById('latBar').style.width = Math.min(lat / 10, 100) + '%';
    document.getElementById('latBadge').innerText = lat > 500 ? 'DEGRADED' : 'Optimal';
    document.getElementById('latBadge').className = lat > 500 ? 'text-rose-400 font-bold' : 'text-emerald-400';

    document.getElementById('errValue').innerText = err.toFixed(2) + ' %';
    document.getElementById('errBar').style.width = Math.min(err * 2, 100) + '%';
    document.getElementById('errBadge').innerText = err > 5.0 ? 'ELEVATED' : 'Healthy';
    document.getElementById('errBadge').className = err > 5.0 ? 'text-rose-400 font-bold' : 'text-emerald-400';

    // 2. Push to Chart
    const nowTime = new Date().toLocaleTimeString();
    if (chartLabels.length >= maxDataPoints) {
        chartLabels.shift();
        cpuData.shift();
        memData.shift();
        latData.shift();
    }
    chartLabels.push(nowTime);
    cpuData.push(cpu);
    memData.push(mem);
    latData.push(lat / 10);
    telemetryChart.update();

    // 3. Update Remediation Timeline
    const timelineEl = document.getElementById('remediationTimeline');
    if (data.remediation_timeline && data.remediation_timeline.length > 0) {
        timelineEl.innerHTML = data.remediation_timeline.map(r => `
            <div class="p-2.5 bg-slate-800/80 rounded border border-slate-700/80 flex items-start justify-between">
                <div>
                    <span class="px-1.5 py-0.5 rounded text-[10px] bg-indigo-900 text-indigo-300 font-bold">${r.action}</span>
                    <p class="text-slate-300 text-xs mt-1">${r.details}</p>
                </div>
                <span class="text-[10px] text-emerald-400 font-bold">${r.status}</span>
            </div>
        `).reverse().join('');
    }

    // 4. Update Agent Logs
    const logEl = document.getElementById('agentLogStream');
    if (data.recent_logs && data.recent_logs.length > 0) {
        logEl.innerHTML = data.recent_logs.map(log => {
            let color = 'text-slate-300';
            if (log.includes('🚨')) color = 'text-rose-400 font-bold';
            if (log.includes('🧠')) color = 'text-indigo-300';
            if (log.includes('🛠️')) color = 'text-emerald-400 font-bold';
            if (log.includes('⚡')) color = 'text-amber-400';
            return `<div class="${color}">${log}</div>`;
        }).join('');
        logEl.scrollTop = logEl.scrollHeight;
    }

    // 5. Update Toggle button
    const toggleBtn = document.getElementById('toggleRemediationBtn');
    if (data.auto_remediation_active) {
        toggleBtn.innerText = "Autonomous Healing: ON";
        toggleBtn.className = "px-3 py-1.5 rounded-md text-xs font-semibold bg-emerald-600 hover:bg-emerald-500 text-white transition shadow";
    } else {
        toggleBtn.innerText = "Autonomous Healing: OFF";
        toggleBtn.className = "px-3 py-1.5 rounded-md text-xs font-semibold bg-slate-700 hover:bg-slate-600 text-slate-300 transition shadow";
    }
}

async function triggerChaos(scenario) {
    try {
        await fetch('/api/chaos/inject', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ scenario })
        });
        fetchStatus();
    } catch (e) {
        alert("Chaos trigger failed: " + e);
    }
}

async function stopChaos() {
    try {
        await fetch('/api/chaos/stop', { method: 'POST' });
        fetchStatus();
    } catch (e) {
        alert("Stop chaos failed: " + e);
    }
}

async function toggleRemediation() {
    try {
        await fetch('/api/toggle-auto-remediation', { method: 'POST' });
        fetchStatus();
    } catch (e) {
        alert("Toggle failed: " + e);
    }
}

window.addEventListener('DOMContentLoaded', () => {
    initChart();
    fetchStatus();
    setInterval(fetchStatus, 1000);
});

