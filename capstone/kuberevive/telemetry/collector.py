"""
Telemetry Ring Buffer & Metric Stream Ingestion (Member 1 Responsibility)
High-throughput circular buffer for incoming telemetry metrics.
"""

from collections import deque
from typing import Dict, List, Any
import time


class TelemetryRingBuffer:
    """
    Fixed-size FIFO ring buffer storing streaming telemetry events.
    """
    def __init__(self, capacity: int = 200):
        self.capacity = capacity
        self.buffer = deque(maxlen=capacity)

    def push(self, metrics: Dict[str, Any]):
        """Pushes metric packet with timestamp."""
        payload = dict(metrics)
        if "timestamp" not in payload:
            payload["timestamp"] = time.time()
        self.buffer.append(payload)

    def get_latest(self, n: int = 50) -> List[Dict[str, Any]]:
        """Returns the most recent n telemetry snapshots."""
        items = list(self.buffer)
        return items[-n:] if len(items) >= n else items

    def get_current(self) -> Dict[str, Any]:
        """Returns the single most recent metric snapshot."""
        if self.buffer:
            return self.buffer[-1]
        return {
            "cpu_usage_pct": 25.0,
            "memory_usage_pct": 35.0,
            "latency_ms": 45.0,
            "error_rate_pct": 0.2,
            "request_rate_rps": 100.0,
            "timestamp": time.time()
        }

