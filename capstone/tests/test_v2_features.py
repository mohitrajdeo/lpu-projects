"""
KubeRevive v2.0 Enterprise Feature Test Suite
Tests:
1. PyTorch Temporal Convolutional Autoencoder (TCAE) sliding window anomaly evaluation
2. Semantic Log Anomaly & Shannon Entropy calculation
3. Local SLM Chain-of-Thought (CoT) RCA reasoning synthesis
4. Code Property Graph (CPG) AST validation & unified diff generation
5. Multi-Cloud SOAR Containment Actuator
"""

import pytest
from kuberevive.anomaly_detection.temporal_detector import TemporalAnomalyEngine
from kuberevive.anomaly_detection.log_anomaly_parser import LogAnomalyParser
from kuberevive.agents.rca_agent import RootCauseAnalysisAgent
from kuberevive.agents.patch_generator import RemediationPlanner
from kuberevive.actuators.remediation_engine import RemediationEngine
from kuberevive.actuators.verification_sandbox import VerificationSandbox


def test_temporal_autoencoder_evaluation():
    engine = TemporalAnomalyEngine(seq_len=12)
    normal_sample = {
        "cpu_usage_pct": 35.0,
        "memory_usage_pct": 45.0,
        "latency_ms": 40.0,
        "error_rate_pct": 0.1,
        "request_rate_rps": 120.0
    }
    res = engine.score_temporal_window(normal_sample)
    assert "temporal_mse" in res
    assert "feature_attribution" in res
    assert isinstance(res["is_anomaly"], bool)


def test_semantic_log_entropy_and_threats():
    parser = LogAnomalyParser()
    normal_log = "2026-11-16 10:00:00 INFO User checkout session created id=1024"
    p_norm = parser.parse_log(normal_log)
    assert p_norm["is_security_incident"] is False
    assert p_norm["shannon_entropy"] > 0.0

    sqli_log = "2026-11-16 10:01:00 WARNING Invalid input detected: ' UNION SELECT null, password FROM users--"
    p_sqli = parser.parse_log(sqli_log)
    assert p_sqli["is_security_incident"] is True
    assert "SQLI" in p_sqli["security_threats"]


def test_slm_chain_of_thought_rca():
    rca = RootCauseAnalysisAgent()
    ticket = {
        "incident_id": "INC-TEST-001",
        "service": "order-processor",
        "symptoms": ["Memory leak escalating", "Socket exhaustion"]
    }
    mock_rca = {
        "probable_root_cause": "Node.js circular closure memory buildup",
        "recommended_action": "restart_service",
        "confidence": 0.92
    }
    cot = rca.synthesize_slm_chain_of_thought(ticket, mock_rca)
    assert cot["slm_engine"] == "KubeRevive-SLM-CoT-v2.0"
    assert len(cot["chain_of_thought"]) == 4
    assert cot["recommended_action"] == "restart_service"


def test_cpg_ast_and_unified_diff():
    planner = RemediationPlanner()
    valid_code = "def handle_event(e):\n    if e.is_valid():\n        return True\n    return False"
    val = planner.validate_patch_ast(valid_code)
    assert val["valid"] is True
    assert val["cyclomatic_complexity"] == 2

    invalid_code = "def syntax_broken(\n"
    val_bad = planner.validate_patch_ast(invalid_code)
    assert val_bad["valid"] is False

    diff = planner.generate_unified_diff("replicas: 2\n", "replicas: 4\n", "deploy.yaml")
    assert "-replicas: 2" in diff
    assert "+replicas: 4" in diff


def test_soar_containment_actuation():
    engine = RemediationEngine(cooldown_seconds=0, dry_run=False)
    plan = {
        "plan_id": "PLAN-SOAR-01",
        "target_service": "ingress-balancer",
        "primary_action": "quarantine_threat_ip",
        "parameters": {"attacker_ip": "203.0.113.88"}
    }
    res = engine.execute_plan(plan)
    assert res["status"] == "SUCCESS"
    assert "203.0.113.88" in res["details"]["message"]


def test_speculative_sandbox_execution():
    sandbox = VerificationSandbox()
    test_script = "x = 10\ny = 20\nassert x + y == 30\nprint('SUCCESS')"
    res = sandbox.execute_speculative_verification(test_script, timeout_sec=2.0)
    assert res["success"] is True
    assert "SUCCESS" in res["stdout"]

