"""
Integration Tests for FastAPI Endpoints (Member 1 & 5)
"""

import pytest
from fastapi.testclient import TestClient
from kuberevive.dashboard.app import app

client = TestClient(app)

def test_api_status():
    response = client.get("/api/status")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ONLINE"
    assert "current_telemetry" in data

def test_api_telemetry():
    response = client.get("/api/telemetry")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_chaos_inject_and_stop():
    resp_inject = client.post("/api/chaos/inject", json={"scenario": "cpu_spike"})
    assert resp_inject.status_code == 200
    assert resp_inject.json()["status"] == "SUCCESS"

    resp_stop = client.post("/api/chaos/stop")
    assert resp_stop.status_code == 200
    assert resp_stop.json()["status"] == "SUCCESS"

def test_prometheus_metrics():
    response = client.get("/metrics")
    assert response.status_code == 200
    assert "kuberevive_cpu_usage_pct" in response.text

def test_real_checkout_transaction():
    response = client.post("/api/checkout/process", json={
        "user_id": "test_user_42",
        "item_id": "item_gpu_01",
        "quantity": 1,
        "amount": 799.00
    })
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "COMPLETED"
    assert "order_id" in data
    assert data["processing_time_ms"] > 0


