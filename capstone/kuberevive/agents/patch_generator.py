"""
Remediation Planner & Patch Generator (Member 3 Responsibility)
Translates RCA diagnoses into executable, deterministic self-healing plans
equipped with pre-conditions, action sequences, and rollback contingencies.
"""

import ast
import difflib
from typing import Dict, Any, List


class RemediationPlanner:
    """
    Constructs declarative remediation execution specs.
    Enforces safety bounds, AST Code Property Graph validation, and SOAR actions.
    """
    def __init__(self, allowed_actions=None):
        self.allowed_actions = allowed_actions or [
            "restart_service",
            "rollback_deployment",
            "scale_replicas",
            "circuit_breaker_trip",
            "flush_cache",
            "quarantine_threat_ip",
            "bolt_graceful_drain",
            "karpenter_spot_scale"
        ]

    def validate_patch_ast(self, code_str: str) -> Dict[str, Any]:
        """v2.0: Parses patch source with Python AST to verify syntax & cyclomatic complexity."""
        try:
            tree = ast.parse(code_str)
            ast_nodes = sum(1 for _ in ast.walk(tree))
            branches = sum(1 for n in ast.walk(tree) if isinstance(n, (ast.If, ast.For, ast.While, ast.ExceptHandler)))
            return {
                "valid": True,
                "ast_nodes": ast_nodes,
                "cyclomatic_complexity": branches + 1,
                "error": None
            }
        except SyntaxError as e:
            return {
                "valid": False,
                "ast_nodes": 0,
                "cyclomatic_complexity": 0,
                "error": str(e)
            }

    def generate_unified_diff(self, original_config: str, updated_config: str, filepath: str = "config.yaml") -> str:
        """v2.0: Generates standard Git unified diff for automated PR generation."""
        orig_lines = original_config.splitlines(keepends=True)
        updated_lines = updated_config.splitlines(keepends=True)
        diff = difflib.unified_diff(orig_lines, updated_lines, fromfile=f"a/{filepath}", tofile=f"b/{filepath}", n=3)
        return "".join(diff)

    def build_plan(self, diagnosis: Dict[str, Any]) -> Dict[str, Any]:
        """
        Creates an actionable plan dictionary for the Actuators.
        """
        action = diagnosis.get("recommended_action", "scale_replicas")
        if action not in self.allowed_actions:
            action = "scale_replicas"

        plan = {
            "plan_id": f"PLAN-{diagnosis.get('incident_id', 'UNKNOWN')}",
            "incident_id": diagnosis.get("incident_id"),
            "target_service": diagnosis.get("service", "checkout-service"),
            "primary_action": action,
            "confidence": diagnosis.get("confidence_score", 0.8),
            "safety_checks": [
                "Verify replica count does not exceed cluster max (10)",
                "Ensure health probe passes before releasing traffic",
                "Ensure cooldown period (15s) is respected"
            ],
            "parameters": {},
            "verification_criteria": {
                "max_allowed_error_rate_pct": 1.0,
                "max_allowed_latency_ms": 150.0,
                "max_allowed_cpu_pct": 75.0,
                "stabilization_wait_seconds": 3
            }
        }

        if action == "scale_replicas":
            plan["parameters"] = {"scale_factor": 2, "target_replicas": 4}
        elif action == "restart_service":
            plan["parameters"] = {"graceful_timeout_seconds": 5, "rolling": True}
        elif action == "rollback_deployment":
            plan["parameters"] = {"target_version": "v1.0.4-stable", "drain_traffic": True}
        elif action == "circuit_breaker_trip":
            plan["parameters"] = {"shed_traffic_pct": 50, "trip_duration_seconds": 20}
        elif action == "flush_cache":
            plan["parameters"] = {"namespace": "checkout:session", "warmup_enabled": True}
        elif action == "quarantine_threat_ip":
            plan["parameters"] = {"attacker_ip": diagnosis.get("attacker_ip", "198.51.100.42"), "action": "DROP_EGRESS_AND_WAF_BLOCK"}
        elif action == "bolt_graceful_drain":
            plan["parameters"] = {"service_name": plan["target_service"], "drain_seconds": 5}
        elif action == "karpenter_spot_scale":
            plan["parameters"] = {"nodepool": "spot-cost-optimizer", "min_replicas": 4, "max_replicas": 12}

        return plan

