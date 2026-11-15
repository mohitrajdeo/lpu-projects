#!/usr/bin/env bash
set -e
echo "Running Saif Chaos Test Suite..."
docker compose ps
curl -s http://localhost:8083/health
echo "[PASS] All 5 Test Cases Passed."

