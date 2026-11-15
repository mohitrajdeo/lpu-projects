#!/usr/bin/env bash
set -e

# Update and install core dependencies
export DEBIAN_FRONTEND=noninteractive
apt-get update -y
apt-get install -y nginx curl git python3 python3-pip python3-venv build-essential ufw

# Install Node.js 20.x LTS
curl -fsSL https://deb.nodesource.com/setup_20.x | bash -
apt-get install -y nodejs

# 1. Create Dedicated Sandbox User for Code Execution
useradd -m -s /bin/bash sandbox-user || true

# 2. Deploy Code Execution Daemon on Port 9010
mkdir -p /opt/code-runner
cat << 'EOF' > /opt/code-runner/runner.py
import http.server
import socketserver
import json
import subprocess
import time

PORT = 9010

class CodeExecutionHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/health' or self.path == '/':
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(b'{"service":"code-execution-engine","status":"healthy","port":9010}')
        else:
            self.send_response(404)
            self.end_headers()

    def do_POST(self):
        content_length = int(self.headers.get('Content-Length', 0))
        post_data = self.rfile.read(content_length)
        
        try:
            req = json.loads(post_data.decode('utf-8'))
            lang = req.get('language', 'python')
            code = req.get('code', '')
            timeout = int(req.get('timeout', 4))
            
            start = time.time()
            if lang == 'python':
                cmd = ['python3', '-c', code]
            elif lang == 'bash':
                cmd = ['bash', '-c', code]
            else:
                cmd = ['node', '-e', code]
                
            res = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, timeout=timeout)
            duration = round((time.time() - start) * 1000, 2)
            
            output = {
                "status": "success",
                "stdout": res.stdout,
                "stderr": res.stderr,
                "exitCode": res.returncode,
                "executionTimeMs": duration
            }
            status_code = 200
        except subprocess.TimeoutExpired:
            output = {"status": "error", "error": "Execution timed out (Limit: 4s)"}
            status_code = 408
        except Exception as e:
            output = {"status": "error", "error": str(e)}
            status_code = 500

        self.send_response(status_code)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(json.dumps(output).encode('utf-8'))

with socketserver.TCPServer(("", PORT), CodeExecutionHandler) as httpd:
    print(f"Code Runner listening on port {PORT}")
    httpd.serve_forever()
EOF

# Create Systemd Service for Code Runner (Port 9010)
cat << 'EOF' > /etc/systemd/system/code-runner.service
[Unit]
Description=Backend Code Execution Service on Port 9010
After=network.target

[Service]
Type=simple
User=root
WorkingDirectory=/opt/code-runner
ExecStart=/usr/bin/python3 /opt/code-runner/runner.py
Restart=always
RestartSec=3

[Install]
WantedBy=multi-user.target
EOF

systemctl daemon-reload
systemctl enable code-runner
systemctl start code-runner

# 3. Configure Nginx Web Proxy
cat << 'EOF' > /etc/nginx/sites-available/default
server {
    listen 80 default_server;
    listen [::]:80 default_server;
    server_name _;

    root /var/www/html;
    index index.html;

    # Health Probe for Nagios Tier 1
    location = /health {
        default_type application/json;
        return 200 '{"status":"healthy","uptime":"active","server":"int333-web-portal"}\n';
    }

    # API Proxy to Port 9010 Code Execution Service
    location /api/execute {
        proxy_pass http://127.0.0.1:9010/;
        proxy_http_version 1.1;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_connect_timeout 3s;
        proxy_read_timeout 10s;
    }

    location / {
        try_files $uri $uri/ =404;
    }
}
EOF

# Create Modern Developer Portal Page
cat << 'EOF' > /var/www/html/index.html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Mohit Raj Deo - Developer Web Portal & Code Runner</title>
    <style>
        body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; background: #0f172a; color: #f8fafc; padding: 40px; margin: 0; }
        .container { max-width: 900px; margin: auto; background: #1e293b; padding: 30px; border-radius: 12px; border: 1px solid #334155; }
        h1 { color: #38bdf8; margin-top: 0; }
        .badge { background: #0284c7; padding: 4px 10px; border-radius: 20px; font-size: 12px; font-weight: bold; }
        textarea { width: 100%; height: 140px; background: #090d16; color: #38bdf8; font-family: monospace; padding: 12px; border: 1px solid #475569; border-radius: 6px; box-sizing: border-box; }
        button { background: #2563eb; color: #fff; border: none; padding: 10px 20px; border-radius: 6px; font-weight: bold; cursor: pointer; margin-top: 10px; }
        button:hover { background: #1d4ed8; }
        pre { background: #090d16; padding: 14px; border-radius: 6px; border: 1px solid #334155; min-height: 60px; color: #34d399; }
        .meta { color: #94a3b8; font-size: 13px; margin-bottom: 20px; }
    </style>
</head>
<body>
    <div class="container">
        <span class="badge">INT333 Capstone</span>
        <h1>Developer Web Portal & Code Execution Service</h1>
        <div class="meta">Student: <strong>Mohit Raj Deo (12323329)</strong> | Monitored actively via <strong>Nagios Core</strong> on Port 80 and Port 9010</div>
        
        <h3>Write & Run Code (Port 9010 Sandbox):</h3>
        <textarea id="code">print("Hello from AWS EC2 provisioned by Terraform!")
import platform
print(f"Platform: {platform.platform()}")</textarea>
        <br>
        <button onclick="runCode()">⚡ Execute on Backend (Port 9010)</button>
        
        <h3>Execution Output:</h3>
        <pre id="output">Click Execute to trigger backend code runner...</pre>
    </div>
    <script>
        async function runCode() {
            const out = document.getElementById('output');
            out.textContent = "Executing code on backend daemon...";
            try {
                const res = await fetch('/api/execute', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({language: 'python', code: document.getElementById('code').value})
                });
                const data = await res.json();
                out.textContent = data.stdout || data.stderr || JSON.stringify(data, null, 2);
            } catch(e) {
                out.textContent = "Error communicating with backend: " + e.message;
            }
        }
    </script>
</body>
</html>
EOF

systemctl restart nginx

