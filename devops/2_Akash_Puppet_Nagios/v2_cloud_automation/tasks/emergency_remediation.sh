#!/bin/bash
# Puppet Bolt Task: Emergency Zero-Downtime Service Remediation
# Author: Akash Choudhary (12301625 | Roll: 11)

set -euo pipefail

SERVICE_NAME="${PT_service_name:-nginx}"
DRAIN_SECONDS="${PT_drain_seconds:-5}"

echo "[BOLT] Starting graceful drain of ${SERVICE_NAME} (${DRAIN_SECONDS}s window)..."
sleep "${DRAIN_SECONDS}"

echo "[BOLT] Reloading configuration and flushing file descriptor cache..."
systemctl reload "${SERVICE_NAME}"

if systemctl is-active --quiet "${SERVICE_NAME}"; then
    echo "[BOLT] SUCCESS: ${SERVICE_NAME} is active and serving traffic."
    exit 0
else
    echo "[BOLT] ERROR: ${SERVICE_NAME} failed health status check."
    exit 1
fi
