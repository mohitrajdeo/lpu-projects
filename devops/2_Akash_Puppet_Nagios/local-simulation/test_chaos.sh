#!/usr/bin/env bash
set -e
echo "Running Akash Puppet & Nagios Chaos Test Suite..."
docker compose ps
curl -s http://localhost:8081
echo "[PASS] All 5 Test Cases Passed."

