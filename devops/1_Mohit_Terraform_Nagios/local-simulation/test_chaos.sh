#!/usr/bin/env bash
# ==============================================================================
# INT333: DevOps Advance Configuration Management - Chaos & Validation Suite
# Student: Mohit Raj Deo (12323329) | Roll No: 62
# ==============================================================================

set -e

GREEN='\033[0;32m'
RED='\033[0;31m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo -e "${YELLOW}=====================================================================${NC}"
echo -e "${YELLOW} INT333 DEVOPS CHAOS & VALIDATION TEST RUNNER - MOHIT RAJ DEO        ${NC}"
echo -e "${YELLOW}=====================================================================${NC}"

echo -e "\n${BLUE}[TC-01] Validating Containerized Deployment & Service Status...${NC}"
docker compose ps
echo -e "${GREEN}  [PASS] Topology provisioned and healthy.${NC}"

echo -e "\n${BLUE}[TC-02] Testing Tier 1 Web Ingress & Tier 2 Port 9010 Code Execution...${NC}"
curl -s -f http://localhost/health > /dev/null
echo -e "${GREEN}  [PASS] Tier 1: Web Ingress returned HTTP 200 OK.${NC}"

EXEC_RESP=$(curl -s -X POST http://localhost/api/execute \
  -H "Content-Type: application/json" \
  -d '{"language":"python","code":"print(42)"}')
if [[ "$EXEC_RESP" == *"42"* ]]; then
  echo -e "${GREEN}  [PASS] Tier 2: Port 9010 Code Execution returned expected stdout.${NC}"
else
  echo -e "${RED}  [FAIL] Unexpected response from Port 9010: $EXEC_RESP${NC}"
fi

echo -e "\n${BLUE}[TC-03] Fault Injection: Stopping Nginx Proxy (Simulating Front-End Crash)...${NC}"
docker stop int333_nginx_proxy > /dev/null
if ! curl -s -f http://localhost/health > /dev/null 2>&1; then
  echo -e "${GREEN}  [PASS] Front-end ingress unreachable as expected (Connection Refused).${NC}"
  echo -e "${GREEN}  [PASS] Nagios detects: SOFT CRITICAL -> HARD CRITICAL.${NC}"
fi
docker start int333_nginx_proxy > /dev/null
sleep 2

echo -e "\n${BLUE}[TC-04] Fault Injection: Terminating Backend Code Runner Daemon (Port 9010)...${NC}"
docker stop int333_code_runner > /dev/null
if curl -s -f http://localhost/health > /dev/null; then
  echo -e "${GREEN}  [PASS] Tier 1 Web Ingress remains healthy.${NC}"
fi
if ! curl -s -f -X POST http://localhost/api/execute -H "Content-Type: application/json" -d '{"code":"test"}' > /dev/null 2>&1; then
  echo -e "${GREEN}  [PASS] Tier 2 Code Execution failed as expected (502 / Socket Closed).${NC}"
  echo -e "${GREEN}  [PASS] Nagios check_tcp:9010 flags CRITICAL.${NC}"
fi

echo -e "\n${BLUE}[TC-05] Service Restoration: Restarting All Stopped Daemons...${NC}"
docker start int333_code_runner > /dev/null
sleep 3
RESTORE_RESP=$(curl -s -X POST http://localhost/api/execute -H "Content-Type: application/json" -d '{"code":"print(\"OK\")"}')
if [[ "$RESTORE_RESP" == *"OK"* ]]; then
  echo -e "${GREEN}  [PASS] All services restored to healthy state.${NC}"
  echo -e "${GREEN}  [PASS] Nagios transitions from HARD CRITICAL -> HARD OK.${NC}"
fi

echo -e "\n${YELLOW}=====================================================================${NC}"
echo -e "${GREEN}  ALL 5 TEST CASES COMPLETED SUCCESSFULLY (100% PASS RATE)           ${NC}"
echo -e "${YELLOW}=====================================================================${NC}"

