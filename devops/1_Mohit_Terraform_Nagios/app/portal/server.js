const express = require('express');
const path = require('path');
const http = require('http');

const app = express();
const PORT = process.env.PORT || 3000;
const RUNNER_HOST = process.env.RUNNER_HOST || '127.0.0.1';
const RUNNER_PORT = process.env.RUNNER_PORT || 9010;

app.use(express.json());
app.use(express.static(path.join(__dirname, 'public')));

// Nagios Tier 1 Health Endpoint
app.get('/health', (req, res) => {
    res.status(200).json({
        status: "healthy",
        uptime: process.uptime(),
        service: "web-portal",
        timestamp: new Date().toISOString()
    });
});

// Proxy to Backend Code Runner on Port 9010
app.post('/api/execute', (req, res) => {
    const payload = JSON.stringify(req.body);

    const options = {
        hostname: RUNNER_HOST,
        port: RUNNER_PORT,
        path: '/',
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'Content-Length': Buffer.byteLength(payload)
        },
        timeout: 6000
    };

    const runnerReq = http.request(options, (runnerRes) => {
        let responseData = '';
        runnerRes.on('data', (chunk) => { responseData += chunk; });
        runnerRes.on('end', () => {
            try {
                res.status(runnerRes.statusCode).json(JSON.parse(responseData));
            } catch (e) {
                res.status(500).json({ error: "Invalid JSON from code runner", raw: responseData });
            }
        });
    });

    runnerReq.on('error', (err) => {
        res.status(502).json({
            status: "error",
            error: `Failed to connect to Code Runner daemon at ${RUNNER_HOST}:${RUNNER_PORT}. Is it running? Details: ${err.message}`
        });
    });

    runnerReq.on('timeout', () => {
        runnerReq.destroy();
        res.status(504).json({ status: "error", error: "Gateway Timeout: Backend runner took too long to reply." });
    });

    runnerReq.write(payload);
    runnerReq.end();
});

app.listen(PORT, '0.0.0.0', () => {
    console.log(`[PORTAL] Developer Web Portal running on http://0.0.0.0:${PORT}`);
    console.log(`[PORTAL] Forwarding code execution requests to ${RUNNER_HOST}:${RUNNER_PORT}`);
});

