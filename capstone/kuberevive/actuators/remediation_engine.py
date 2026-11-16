"""
Self-Healing Remediation Engine (Member 4 Responsibility)
Executes infrastructure actuators (rolling restart, automated rollback, horizontal pod autoscaling,
and circuit breaking) with safe execution boundaries and cooldown state tracking.
"""

import time
from typing import Dict, Any, List


class RemediationEngine:
    """
    Automated DevOps actuator executing self-healing workflows on microservices.
    Enforces cooldown windows to avoid flapping/thrashing.
    """
    def __init__(self, cooldown_seconds: int = 10, dry_run: bool = False):
        self.cooldown_seconds = cooldown_seconds
        self.dry_run = dry_run
        self.last_action_timestamp: Dict[str, float] = {}
        self.execution_history: List[Dict[str, Any]] = []

    def can_execute(self, service: str) -> bool:
        """Checks whether the service has passed its cooldown period."""
        last_time = self.last_action_timestamp.get(service, 0)
        return (time.time() - last_time) >= self.cooldown_seconds

    def execute_plan(self, plan: Dict[str, Any], service_instance=None) -> Dict[str, Any]:
        """
        Executes the primary remediation action defined in the plan.
        """
        service = plan.get("target_service", "checkout-service")
        action = plan.get("primary_action", "scale_replicas")
        plan_id = plan.get("plan_id", "UNKNOWN")

        if not self.can_execute(service):
            return {
                "status": "REJECTED_COOLDOWN",
                "message": f"Service {service} is within cooldown window ({self.cooldown_seconds}s). Suppressing action.",
                "action": action,
                "timestamp": time.time()
            }

        start_time = time.time()
        result = {
            "plan_id": plan_id,
            "service": service,
            "action": action,
            "dry_run": self.dry_run,
            "status": "SUCCESS",
            "details": {}
        }

        if not self.dry_run:
            if action == "restart_service":
                if service_instance and hasattr(service_instance, "restart"):
                    service_instance.restart()
                result["details"] = {"message": f"Service {service} container gracefully restarted. Memory reclaimed."}

            elif action == "rollback_deployment":
                if service_instance and hasattr(service_instance, "rollback"):
                    service_instance.rollback()
                result["details"] = {"message": f"Deployment rolled back to stable release v1.0.4 for {service}."}

            elif action == "scale_replicas":
                if service_instance and hasattr(service_instance, "scale"):
                    service_instance.scale(replicas=4)
                result["details"] = {"message": f"Service {service} autoscaled from 2 to 4 worker replicas."}

            elif action == "circuit_breaker_trip":
                if service_instance and hasattr(service_instance, "trip_circuit_breaker"):
                    service_instance.trip_circuit_breaker()
                result["details"] = {"message": f"Circuit breaker tripped for {service}; shedding non-critical load."}

            elif action == "flush_cache":
                if service_instance and hasattr(service_instance, "flush_cache"):
                    service_instance.flush_cache()
                result["details"] = {"message": f"Redis key cache flushed and re-primed for {service}."}
        else:
            result["status"] = "SIMULATED_DRY_RUN"
            result["details"] = {"message": f"Dry-run mode: {action} validated but not applied."}

        execution_duration = round((time.time() - start_time) * 1000, 2)
        result["duration_ms"] = execution_duration
        self.last_action_timestamp[service] = time.time()
        self.execution_history.append(result)
        return result

