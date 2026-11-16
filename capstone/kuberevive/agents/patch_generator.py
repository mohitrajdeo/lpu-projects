"""
Remediation Planner & Patch Generator (Member 3 Responsibility)
Translates RCA diagnoses into executable, deterministic self-healing plans
equipped with pre-conditions, action sequences, and rollback contingencies.
"""

from typing import Dict, Any


class RemediationPlanner:
    """
    Constructs declarative remediation execution specs.
    Enforces safety bounds (e.g., maximum scale limits, rollback commit hashes).
    """
    def __init__(self, allowed_actions=None):
        self.allowed_actions = allowed_actions or [
            "restart_service",
            "rollback_deployment",
            "scale_replicas",
            "circuit_breaker_trip",
            "flush_cache"
        ]

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

        return plan

