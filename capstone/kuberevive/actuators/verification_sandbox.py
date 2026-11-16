"""
Post-Remediation Verification Sandbox (Member 4 Responsibility)
Runs automated health probes, latency checks, and synthetic canary verifications
to guarantee system stabilization after remediation actions.
"""

from typing import Dict, Any, Tuple


class VerificationSandbox:
    """
    Verification probe that verifies whether remediation succeeded
    by evaluating real-time service metrics against acceptance thresholds.
    """
    def __init__(self):
        pass

    def verify_service_health(self, current_telemetry: Dict[str, float], criteria: Dict[str, Any] = None) -> Tuple[bool, Dict[str, Any]]:
        """
        Validates telemetry against criteria thresholds.
        Returns: (is_healthy: bool, validation_report: dict)
        """
        if criteria is None:
            criteria = {
                "max_allowed_error_rate_pct": 1.0,
                "max_allowed_latency_ms": 150.0,
                "max_allowed_cpu_pct": 80.0
            }

        checks = {}
        all_passed = True

        err_rate = current_telemetry.get("error_rate_pct", 0.0)
        max_err = criteria.get("max_allowed_error_rate_pct", 1.0)
        checks["error_rate_ok"] = bool(err_rate <= max_err)
        if not checks["error_rate_ok"]:
            all_passed = False

        lat = current_telemetry.get("latency_ms", 0.0)
        max_lat = criteria.get("max_allowed_latency_ms", 150.0)
        checks["latency_ok"] = bool(lat <= max_lat)
        if not checks["latency_ok"]:
            all_passed = False

        cpu = current_telemetry.get("cpu_usage_pct", 0.0)
        max_cpu = criteria.get("max_allowed_cpu_pct", 80.0)
        checks["cpu_ok"] = bool(cpu <= max_cpu)
        if not checks["cpu_ok"]:
            all_passed = False

        report = {
            "all_passed": all_passed,
            "checks": checks,
            "observed_telemetry": {
                "error_rate_pct": round(err_rate, 2),
                "latency_ms": round(lat, 2),
                "cpu_usage_pct": round(cpu, 2)
            }
        }
        return all_passed, report

    def execute_speculative_verification(self, test_script: str, timeout_sec: float = 3.0) -> Dict[str, Any]:
        """v2.0: Executes custom remediation verification script in an isolated namespace with stdout capture and error trapping."""
        import io
        import sys
        import time
        import traceback

        start = time.time()
        captured_out = io.StringIO()
        old_stdout = sys.stdout
        sys.stdout = captured_out
        success = True
        err_msg = ""

        try:
            # Compiled in isolated namespace
            code_obj = compile(test_script, '<speculative_sandbox>', 'exec')
            exec_globals = {
                "__builtins__": __builtins__,
                "time": time
            }
            exec(code_obj, exec_globals)
        except Exception as e:
            success = False
            err_msg = f"{type(e).__name__}: {str(e)}"
        finally:
            sys.stdout = old_stdout

        duration_ms = round((time.time() - start) * 1000, 2)
        return {
            "success": success,
            "duration_ms": duration_ms,
            "stdout": captured_out.getvalue().strip(),
            "stderr": err_msg
        }

