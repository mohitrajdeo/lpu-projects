#!/usr/bin/env python3
"""
Port 9010 Autonomous Backend Code Execution Daemon
INT333 Capstone Project - Mohit Raj Deo (12323329)
"""

import http.server
import socketserver
import json
import subprocess
import time
import sys

PORT = 9010

class SandboxedRunnerHandler(http.server.BaseHTTPRequestHandler):
    def do_HEAD(self):
        self.send_response(200)
        self.end_headers()

    def do_GET(self):
        if self.path in ('/health', '/', '/status'):
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            payload = {
                "service": "code-execution-engine",
                "port": PORT,
                "status": "healthy",
                "version": "1.0.0",
                "system": sys.platform
            }
            self.wfile.write(json.dumps(payload).encode('utf-8'))
        else:
            self.send_response(404)
            self.end_headers()

    def do_POST(self):
        content_length = int(self.headers.get('Content-Length', 0))
        post_data = self.rfile.read(content_length)

        try:
            req = json.loads(post_data.decode('utf-8'))
            lang = req.get('language', 'python').lower()
            code = req.get('code', '')
            timeout_sec = int(req.get('timeout', 4))

            start_time = time.time()

            if lang == 'python':
                cmd = [sys.executable, '-c', code]
            elif lang == 'javascript' or lang == 'js':
                cmd = ['node', '-e', code]
            elif lang == 'bash' or lang == 'sh':
                cmd = ['bash', '-c', code]
            else:
                cmd = [sys.executable, '-c', code]

            proc = subprocess.run(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                timeout=timeout_sec
            )
            exec_time = round((time.time() - start_time) * 1000, 2)

            res = {
                "status": "success",
                "stdout": proc.stdout,
                "stderr": proc.stderr,
                "exitCode": proc.returncode,
                "executionTimeMs": exec_time,
                "language": lang
            }
            code_status = 200

        except subprocess.TimeoutExpired:
            res = {
                "status": "timeout",
                "error": f"Execution timed out (exceeded limit of {timeout_sec} seconds)",
                "exitCode": 124
            }
            code_status = 408

        except Exception as e:
            res = {
                "status": "error",
                "error": str(e),
                "exitCode": 1
            }
            code_status = 500

        self.send_response(code_status)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
        self.wfile.write(json.dumps(res).encode('utf-8'))

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()

if __name__ == '__main__':
    socketserver.TCPServer.allow_reuse_address = True
    with socketserver.TCPServer(("", PORT), SandboxedRunnerHandler) as server:
        print(f"[RUNNER] Code Execution Daemon active on 0.0.0.0:{PORT}")
        try:
            server.serve_forever()
        except KeyboardInterrupt:
            print("\n[RUNNER] Shutting down daemon gracefully...")

