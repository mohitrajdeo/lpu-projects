"""
Temporal Anomaly Detection Engine v2.0 (Deep Learning Track)
Implements a 1D-CNN Temporal Convolutional Autoencoder (TCAE) in PyTorch.
Analyzes sliding sequential metric windows (W=12 time-steps) to catch slow temporal drifts
and multi-variate trajectory anomalies that static thresholding misses.
"""

import os
import torch
import torch.nn as nn
import numpy as np
from typing import Dict, List, Any, Tuple
from collections import deque


class TemporalAutoencoder(nn.Module):
    """
    1D-CNN Temporal Autoencoder for Microservice Telemetry Sequences.
    Input shape: (batch_size, num_features=5, sequence_length=12)
    """
    def __init__(self, num_features: int = 5, seq_len: int = 12, latent_dim: int = 8):
        super(TemporalAutoencoder, self).__init__()
        self.encoder = nn.Sequential(
            nn.Conv1d(in_channels=num_features, out_channels=16, kernel_size=3, padding=1),
            nn.BatchNorm1d(16),
            nn.ReLU(),
            nn.MaxPool1d(kernel_size=2),  # 12 -> 6
            nn.Conv1d(in_channels=16, out_channels=latent_dim, kernel_size=3, padding=1),
            nn.BatchNorm1d(latent_dim),
            nn.ReLU()
        )
        self.decoder = nn.Sequential(
            nn.ConvTranspose1d(in_channels=latent_dim, out_channels=16, kernel_size=2, stride=2), # 6 -> 12
            nn.BatchNorm1d(16),
            nn.ReLU(),
            nn.Conv1d(in_channels=16, out_channels=num_features, kernel_size=3, padding=1),
            nn.Sigmoid()
        )

    def forward(self, x):
        z = self.encoder(x)
        x_rec = self.decoder(z)
        return x_rec, z


class TemporalAnomalyEngine:
    """
    Online Temporal Anomaly Evaluator maintaining rolling historical metric sequences.
    """
    def __init__(self, seq_len: int = 12, threshold: float = 0.022):
        self.device = torch.device("cpu")
        self.seq_len = seq_len
        self.threshold = threshold
        self.feature_names = [
            "cpu_usage_pct",
            "memory_usage_pct",
            "latency_ms",
            "error_rate_pct",
            "request_rate_rps"
        ]
        self.bounds = {
            "cpu_usage_pct": (0.0, 100.0),
            "memory_usage_pct": (0.0, 100.0),
            "latency_ms": (0.0, 2000.0),
            "error_rate_pct": (0.0, 100.0),
            "request_rate_rps": (0.0, 500.0)
        }
        self.model = TemporalAutoencoder(num_features=len(self.feature_names), seq_len=self.seq_len).to(self.device)
        self.sliding_buffer = deque(maxlen=self.seq_len)
        self._initialize_baseline_weights()

    def _normalize(self, sample: Dict[str, float]) -> List[float]:
        norm = []
        for feat in self.feature_names:
            val = float(sample.get(feat, 0.0))
            low, high = self.bounds[feat]
            norm.append(float(np.clip((val - low) / (high - low), 0.0, 1.0)))
        return norm

    def _initialize_baseline_weights(self):
        """Fits baseline normal operational patterns in sub-second CPU time."""
        torch.manual_seed(42)
        np.random.seed(42)
        batches = []
        for _ in range(100):
            seq = []
            base_cpu = np.random.uniform(25, 45)
            base_mem = np.random.uniform(35, 55)
            base_lat = np.random.uniform(30, 80)
            base_err = np.random.uniform(0.0, 0.5)
            base_rps = np.random.uniform(80, 150)
            for t in range(self.seq_len):
                pt = {
                    "cpu_usage_pct": base_cpu + 2.0 * np.sin(t * 0.4) + np.random.normal(0, 1.0),
                    "memory_usage_pct": base_mem + 0.1 * t + np.random.normal(0, 0.4),
                    "latency_ms": base_lat + np.random.normal(0, 3.0),
                    "error_rate_pct": base_err + np.random.exponential(0.05),
                    "request_rate_rps": base_rps + np.random.normal(0, 5.0)
                }
                seq.append(self._normalize(pt))
            batches.append(np.array(seq).T)

        x_train = torch.tensor(np.array(batches), dtype=torch.float32)
        optimizer = torch.optim.Adam(self.model.parameters(), lr=0.01)
        criterion = nn.MSELoss()

        self.model.train()
        for _ in range(25):
            optimizer.zero_grad()
            rec, _ = self.model(x_train)
            loss = criterion(rec, x_train)
            loss.backward()
            optimizer.step()

        self.model.eval()

    def score_temporal_window(self, telemetry_payload: Dict[str, float]) -> Dict[str, Any]:
        """
        Appends latest sample to sliding window and performs temporal autoencoder inference.
        """
        self.sliding_buffer.append(telemetry_payload)
        
        # If buffer is still filling, pad with current sample
        buf_list = list(self.sliding_buffer)
        if len(buf_list) < self.seq_len:
            buf_list = [buf_list[0]] * (self.seq_len - len(buf_list)) + buf_list

        norm_seq = [self._normalize(pt) for pt in buf_list[-self.seq_len:]]
        x_tensor = torch.tensor(np.array(norm_seq).T, dtype=torch.float32).unsqueeze(0).to(self.device)

        with torch.no_grad():
            rec_tensor, latent = self.model(x_tensor)
            mse_per_feature = torch.mean((rec_tensor - x_tensor) ** 2, dim=2).squeeze(0).numpy()
            total_mse = float(torch.mean((rec_tensor - x_tensor) ** 2).item())

        is_anomaly = total_mse > self.threshold
        confidence = float(np.clip(total_mse / (self.threshold * 1.5), 0.0, 1.0) if is_anomaly else 0.0)

        feature_attribution = {
            self.feature_names[i]: round(float(mse_per_feature[i]), 5)
            for i in range(len(self.feature_names))
        }

        return {
            "model": "KubeRevive-v2.0-TemporalAutoencoder",
            "is_anomaly": bool(is_anomaly),
            "temporal_mse": round(total_mse, 5),
            "threshold": self.threshold,
            "anomaly_confidence": round(confidence, 3),
            "feature_attribution": feature_attribution,
            "latent_vector_sample": [round(float(v), 3) for v in latent.squeeze(0).mean(dim=1).tolist()]
        }

