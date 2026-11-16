"""
Mock Microservice Implementation (Member 5 & 1 Responsibility)
Simulates an e-commerce checkout service with stateful health indicators,
traffic degradation, memory growth, and real response to self-healing actions.
"""

import random
import time
from typing import Dict, Any


class MockMicroservice:
    """
    Simulated stateful microservice representing a mission-critical checkout service.
    Exposes metrics, logs, and actuators (restart, rollback, scale).
    """
    def __init__(self, service_name: str = "checkout-service"):
        self.service_name = service_name
        self.version = "v1.0.5-release"
        self.replicas = 2
        self.circuit_breaker_active = False

        # Internal operational states
        self.cpu_usage_pct = 25.0
        self.memory_usage_pct = 35.0
        self.latency_ms = 45.0
        self.error_rate_pct = 0.2
        self.request_rate_rps = 120.0
        
        # Injected fault flags
        self.fault_active = None
        self.fault_start_time = 0.0

    def restart(self):
        """Simulates container restart: clears memory leak, resets transient states."""
        self.memory_usage_pct = 32.0
        self.cpu_usage_pct = 22.0
        self.fault_active = None
        return {"status": "restarted", "service": self.service_name}

    def rollback(self):
        """Simulates git/canary rollback: restores clean previous release."""
        self.version = "v1.0.4-stable"
        self.error_rate_pct = 0.1
        self.latency_ms = 40.0
        self.fault_active = None
        return {"status": "rolled_back", "version": self.version}

    def scale(self, replicas: int = 4):
        """Simulates horizontal autoscaling."""
        self.replicas = replicas
        self.cpu_usage_pct = max(18.0, self.cpu_usage_pct / (replicas / 2))
        self.latency_ms = max(35.0, self.latency_ms * 0.6)
        self.fault_active = None
        return {"status": "scaled", "replicas": self.replicas}

    def trip_circuit_breaker(self):
        """Simulates shedding traffic."""
        self.circuit_breaker_active = True
        self.latency_ms = 50.0
        self.error_rate_pct = 0.4
        return {"status": "circuit_tripped"}

    def flush_cache(self):
        """Simulates cache flush & warm up."""
        self.latency_ms = 42.0
        return {"status": "cache_flushed"}

    def step_tick(self) -> Dict[str, Any]:
        """
        Advances simulation clock by 1 second.
        Simulates natural noise or progression of active faults.
        """
        noise = lambda scale: random.gauss(0, scale)

        if self.fault_active == "cpu_spike":
            self.cpu_usage_pct = min(99.0, self.cpu_usage_pct + 8.0 + noise(1))
            self.latency_ms = min(1500.0, self.latency_ms + 25.0 + noise(5))

        elif self.fault_active == "memory_leak":
            self.memory_usage_pct = min(98.0, self.memory_usage_pct + 4.5)
            if self.memory_usage_pct > 90.0:
                self.error_rate_pct = min(40.0, self.error_rate_pct + 3.0)

        elif self.fault_active == "http_500_storm":
            self.error_rate_pct = min(65.0, self.error_rate_pct + 12.0 + noise(2))
            self.latency_ms = min(800.0, self.latency_ms + 20.0)

        elif self.fault_active == "latency_burst":
            self.latency_ms = min(2800.0, self.latency_ms + 200.0 + noise(10))

        else:
            # Baseline normal state with gentle fluctuations
            self.cpu_usage_pct = max(15.0, min(50.0, self.cpu_usage_pct + noise(0.8)))
            self.memory_usage_pct = max(30.0, min(55.0, self.memory_usage_pct + noise(0.3)))
            self.latency_ms = max(25.0, min(80.0, self.latency_ms + noise(2)))
            self.error_rate_pct = max(0.05, min(0.8, self.error_rate_pct + noise(0.05)))
            self.request_rate_rps = max(80.0, min(250.0, self.request_rate_rps + noise(5)))

        return {
            "service": self.service_name,
            "version": self.version,
            "replicas": self.replicas,
            "cpu_usage_pct": round(self.cpu_usage_pct, 2),
            "memory_usage_pct": round(self.memory_usage_pct, 2),
            "latency_ms": round(self.latency_ms, 2),
            "error_rate_pct": round(self.error_rate_pct, 2),
            "request_rate_rps": round(self.request_rate_rps, 2),
            "circuit_breaker": self.circuit_breaker_active,
            "fault_active": self.fault_active,
            "timestamp": time.time()
        }

