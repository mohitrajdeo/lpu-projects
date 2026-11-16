"""
Unit Tests for Agentic Triage & RCA (Member 3 & 5)
"""

import pytest
from kuberevive.agents import IncidentTriageAgent, RootCauseAnalysisAgent, RemediationPlanner


def test_triage_agent_deduplication():
    triage = IncidentTriageAgent(suppression_window_seconds=10)
    report = {
        "is_anomaly": True,
        "severity_score": 0.9,
        "offending_metrics": ["cpu_usage_pct"],
        "critical_violations": ["cpu_usage_pct > 90.0%"]
    }

    # First anomaly triggers incident
    inc1 = triage.triage_anomaly(report, service="checkout-service")
    assert inc1 is not None
    assert inc1["priority"] == "P1-CRITICAL"

    # Rapid second anomaly within window gets suppressed
    inc2 = triage.triage_anomaly(report, service="checkout-service")
    assert inc2 is None


def test_rca_diagnosis_memory():
    rca = RootCauseAnalysisAgent()
    ticket = {
        "incident_id": "TEST-1",
        "service": "checkout-service",
        "offending_metrics": ["memory_usage_pct"],
        "critical_violations": ["memory_usage_pct > 88.0%"]
    }
    diag = rca.diagnose(ticket)
    assert "memory" in diag["probable_root_cause"].lower()
    assert diag["recommended_action"] == "restart_service"


def test_remediation_planner():
    planner = RemediationPlanner()
    diag = {
        "incident_id": "TEST-2",
        "service": "checkout-service",
        "recommended_action": "rollback_deployment",
        "confidence_score": 0.95
    }
    plan = planner.build_plan(diag)
    assert plan["primary_action"] == "rollback_deployment"
    assert "target_version" in plan["parameters"]

