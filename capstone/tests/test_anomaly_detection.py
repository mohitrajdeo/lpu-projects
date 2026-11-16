"""
Unit Tests for Anomaly Detection (Member 2 & 5)
"""

import pytest
import pandas as pd
from kuberevive.anomaly_detection import RollingZScoreDetector, MetricAnomalyDetector, HybridAnomalyScorer, LogAnomalyParser


def test_rolling_z_score_detector():
    detector = RollingZScoreDetector(window_size=20, z_threshold=2.5)
    # Feed 15 normal values
    for _ in range(15):
        is_anom, _, _ = detector.update_and_check("cpu", 30.0)
        assert not is_anom

    # Feed an extreme spike
    is_anom, z, dev = detector.update_and_check("cpu", 99.0)
    assert is_anom
    assert z > 2.5


def test_metric_anomaly_detector_isolation_forest():
    detector = MetricAnomalyDetector()
    df_normal = pd.DataFrame({
        "cpu_usage_pct": [20, 22, 25, 23, 24] * 20,
        "memory_usage_pct": [35, 36, 34, 35, 37] * 20,
        "latency_ms": [40, 42, 45, 41, 43] * 20,
        "error_rate_pct": [0.1, 0.2, 0.15, 0.1, 0.2] * 20,
        "request_rate_rps": [100, 105, 98, 102, 101] * 20
    })
    detector.fit(df_normal)

    # Test normal sample
    normal_sample = {"cpu_usage_pct": 23, "memory_usage_pct": 35, "latency_ms": 42, "error_rate_pct": 0.1, "request_rate_rps": 100}
    is_anom, score = detector.score_sample(normal_sample)
    assert not is_anom

    # Test extreme anomaly sample
    anom_sample = {"cpu_usage_pct": 98, "memory_usage_pct": 95, "latency_ms": 1500, "error_rate_pct": 35.0, "request_rate_rps": 300}
    is_anom, score = detector.score_sample(anom_sample)
    assert is_anom
    assert score > 0.5


def test_log_anomaly_parser():
    parser = LogAnomalyParser()
    res = parser.parse_log("ERROR [checkout-service] OutOfMemoryError in worker thread 42")
    assert res["is_error"] is True
    assert "NUM" in res["template"] or "ERROR" in res["template"]

