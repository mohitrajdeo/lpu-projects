"""
Chaos Engineering Injector (Member 5 Responsibility)
Programmatically injects system anomalies to simulate real-world production outages:
- CPU saturation (infinite loop simulation)
- Memory leak (unbounded heap allocation)
- HTTP 500 error storm (faulty commit / null pointer)
- Latency injection (network jitter / slow dependency)
"""

import time
from typing import Dict, Any


class ChaosInjector:
    """
    Chaos engineering agent designed to test self-healing resilience
    and measure MTTD (Mean Time To Detect) and MTTR (Mean Time To Recover).
    """
    def __init__(self, target_service):
        self.service = target_service
        self.active_chaos = None
        self.injection_log = []

    def inject_fault(self, scenario: str) -> Dict[str, Any]:
        """
        Injects an active fault scenario into the target microservice.
        Allowed scenarios: ['cpu_spike', 'memory_leak', 'http_500_storm', 'latency_burst']
        """
        valid_scenarios = ["cpu_spike", "memory_leak", "http_500_storm", "latency_burst"]
        if scenario not in valid_scenarios:
            raise ValueError(f"Unknown scenario {scenario}. Must be one of {valid_scenarios}")

        self.service.fault_active = scenario
        self.service.fault_start_time = time.time()
        self.active_chaos = scenario

        entry = {
            "scenario": scenario,
            "injected_at": time.time(),
            "target": self.service.service_name,
            "status": "ACTIVE"
        }
        self.injection_log.append(entry)
        return entry

    def stop_chaos(self) -> Dict[str, Any]:
        """Clears active chaos faults."""
        prev = self.active_chaos
        self.service.fault_active = None
        self.active_chaos = None
        return {"scenario": prev, "status": "CLEARED", "stopped_at": time.time()}

