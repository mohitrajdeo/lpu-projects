"""
Unit Tests for Actuators & Verification Sandbox (Member 4 & 5)
"""

import pytest
from kuberevive.actuators import RemediationEngine, VerificationSandbox
from kuberevive.simulation import MockMicroservice


def test_remediation_engine_restart():
    engine = RemediationEngine(cooldown_seconds=1, dry_run=False)
    service = MockMicroservice()
    service.memory_usage_pct = 95.0

    plan = {
        "plan_id": "P-1",
        "target_service": "checkout-service",
        "primary_action": "restart_service"
    }

    result = engine.execute_plan(plan, service_instance=service)
    assert result["status"] == "SUCCESS"
    assert service.memory_usage_pct < 40.0


def test_verification_sandbox():
    sandbox = VerificationSandbox()
    good_telemetry = {"error_rate_pct": 0.2, "latency_ms": 45.0, "cpu_usage_pct": 30.0}
    bad_telemetry = {"error_rate_pct": 12.0, "latency_ms": 450.0, "cpu_usage_pct": 95.0}

    passed, report = sandbox.verify_service_health(good_telemetry)
    assert passed is True

    passed, report = sandbox.verify_service_health(bad_telemetry)
    assert passed is False
    assert report["checks"]["error_rate_ok"] is False

