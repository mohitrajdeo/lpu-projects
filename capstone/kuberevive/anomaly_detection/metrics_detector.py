"""
Metric Anomaly Detection Engine (Member 2 Responsibility)
Implements Hybrid Multi-Variate Anomaly Detection combining:
1. Dynamic Rolling Z-Score / EWMA for single-variate threshold violations
2. Isolation Forest (Unsupervised Ensembling) for multi-variate metric correlation anomalies
"""

import numpy as np
import pandas as pd
from typing import Dict, List, Any, Tuple
from collections import deque
from sklearn.ensemble import IsolationForest


class RollingZScoreDetector:
    """
    Online single-variate anomaly detector utilizing rolling statistical moments
    (mean, standard deviation) and EWMA with adjustable z-score bounds.
    """
    def __init__(self, window_size: int = 30, z_threshold: float = 2.75):
        self.window_size = window_size
        self.z_threshold = z_threshold
        self.buffers: Dict[str, deque] = {}

    def update_and_check(self, metric_name: str, value: float) -> Tuple[bool, float, float]:
        """
        Ingests a new metric value and checks if it violates the rolling z-score boundary.
        Returns: (is_anomaly, z_score, deviation_pct)
        """
        if metric_name not in self.buffers:
            self.buffers[metric_name] = deque(maxlen=self.window_size)

        buf = self.buffers[metric_name]
        buf.append(value)

        if len(buf) < 10:
            return False, 0.0, 0.0

        arr = np.array(buf)
        mean = np.mean(arr)
        std = np.std(arr)

        if std < 1e-4:
            std = 1e-4

        z_score = abs(value - mean) / std
        is_anomaly = bool(z_score > self.z_threshold)
        deviation_pct = float(((value - mean) / mean) * 100.0) if abs(mean) > 1e-4 else 0.0

        return is_anomaly, float(z_score), deviation_pct


class MetricAnomalyDetector:
    """
    Multi-variate anomaly detector utilizing Isolation Forest trained on baseline operational metrics.
    Detects complex cross-metric correlations (e.g., normal CPU + normal RPS, but abnormal latency).
    """
    def __init__(self, feature_names: List[str] = None, contamination: float = 0.05):
        self.feature_names = feature_names or [
            "cpu_usage_pct",
            "memory_usage_pct",
            "latency_ms",
            "error_rate_pct",
            "request_rate_rps"
        ]
        self.contamination = contamination
        self.model = IsolationForest(
            contamination=self.contamination,
            n_estimators=100,
            random_state=42
        )
        self.is_fitted = False

    def fit(self, df: pd.DataFrame):
        """Fits the Isolation Forest on historical baseline telemetry dataframe."""
        X = df[self.feature_names].values
        self.model.fit(X)
        self.is_fitted = True
        return self

    def score_sample(self, sample_dict: Dict[str, float]) -> Tuple[bool, float]:
        """
        Scores a single point.
        Returns: (is_anomaly: bool, normalized_anomaly_score: float [0.0 - 1.0])
        """
        if not self.is_fitted:
            # Bootstrap synthetic baseline if not yet fitted
            baseline_data = np.random.normal(loc=[30, 40, 50, 0.5, 100], scale=[5, 5, 10, 0.2, 10], size=(300, len(self.feature_names)))
            self.model.fit(baseline_data)
            self.is_fitted = True

        features = [sample_dict.get(feat, 0.0) for feat in self.feature_names]
        X = np.array(features).reshape(1, -1)
        pred = self.model.predict(X)[0]  # -1 for anomaly, 1 for normal
        decision = self.model.decision_function(X)[0]  # Lower means more abnormal
        
        # Normalize decision function to [0, 1] anomaly score
        # Decision function is typically between -0.5 and +0.5
        norm_score = float(np.clip(0.5 - decision, 0.0, 1.0))
        is_anomaly = bool(pred == -1 or norm_score > 0.65)
        return is_anomaly, norm_score


class HybridAnomalyScorer:
    """
    Ensemble engine reconciling statistical boundary thresholds with
    unsupervised multi-variate isolation forest scores.
    """
    def __init__(self, window_size: int = 30, z_threshold: float = 2.75):
        self.stat_detector = RollingZScoreDetector(window_size=window_size, z_threshold=z_threshold)
        self.ml_detector = MetricAnomalyDetector()

    def evaluate_telemetry(self, telemetry_payload: Dict[str, float]) -> Dict[str, Any]:
        """
        Evaluates an incoming streaming telemetry payload.
        Returns detailed incident diagnosis dictionary.
        """
        stat_flags = {}
        high_z_metrics = []

        for metric, val in telemetry_payload.items():
            if isinstance(val, (int, float)):
                is_anom, z_score, dev = self.stat_detector.update_and_check(metric, float(val))
                stat_flags[metric] = {
                    "is_anomaly": is_anom,
                    "z_score": round(z_score, 2),
                    "deviation_pct": round(dev, 2),
                    "current_value": round(val, 2)
                }
                if is_anom:
                    high_z_metrics.append((metric, z_score, val))

        # ML multi-variate score
        ml_anom, ml_score = self.ml_detector.score_sample(telemetry_payload)

        # Ensemble decision rule:
        # If ML score > 0.70 OR more than one metric has statistically significant z-score
        # OR critical thresholds exceeded (e.g. error rate > 5%, memory > 90%)
        critical_violations = []
        if telemetry_payload.get("error_rate_pct", 0) > 5.0:
            critical_violations.append("error_rate_pct > 5.0%")
        if telemetry_payload.get("memory_usage_pct", 0) > 88.0:
            critical_violations.append("memory_usage_pct > 88.0%")
        if telemetry_payload.get("cpu_usage_pct", 0) > 90.0:
            critical_violations.append("cpu_usage_pct > 90.0%")
        if telemetry_payload.get("latency_ms", 0) > 1000.0:
            critical_violations.append("latency_ms > 1000ms")

        is_overall_anomaly = bool(ml_anom or len(high_z_metrics) >= 2 or len(critical_violations) >= 1)
        
        # Calculate combined severity score [0.0 - 1.0]
        severity = max(
            ml_score,
            min(1.0, len(critical_violations) * 0.35 + (0.3 if len(high_z_metrics) > 0 else 0.0))
        )

        return {
            "is_anomaly": is_overall_anomaly,
            "severity_score": round(float(severity), 3),
            "ml_anomaly_score": round(float(ml_score), 3),
            "critical_violations": critical_violations,
            "stat_metrics": stat_flags,
            "offending_metrics": [m[0] for m in high_z_metrics] + [v.split()[0] for v in critical_violations]
        }

