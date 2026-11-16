"""
Prometheus Metrics Exporter (Member 4 Responsibility)
Standardizes system observability with Prometheus Gauge and Counter formats
compatible with Grafana and Prometheus scraping.
"""

from typing import Dict, Any


class PrometheusMetricsExporter:
    """
    Exposes metrics in standard Prometheus text format.
    Allows easy integration with Prometheus daemon and Grafana dashboards.
    """
    def __init__(self):
        self.metrics: Dict[str, float] = {
            "kuberevive_cpu_usage_pct": 25.0,
            "kuberevive_memory_usage_pct": 35.0,
            "kuberevive_latency_ms": 45.0,
            "kuberevive_error_rate_pct": 0.2,
            "kuberevive_request_rate_rps": 100.0,
            "kuberevive_active_incidents": 0.0,
            "kuberevive_remediations_total": 0.0
        }

    def update_metrics(self, telemetry: Dict[str, Any]):
        """Updates internal exporter state."""
        for k, v in telemetry.items():
            if isinstance(v, (int, float)):
                metric_key = f"kuberevive_{k}"
                self.metrics[metric_key] = float(v)

    def generate_prometheus_payload(self) -> str:
        """Renders Prometheus line format string."""
        lines = []
        for key, value in self.metrics.items():
            lines.append(f"# HELP {key} Metric exported by KubeRevive Agent")
            lines.append(f"# TYPE {key} gauge")
            lines.append(f"{key} {value}")
        return "\n".join(lines) + "\n"

