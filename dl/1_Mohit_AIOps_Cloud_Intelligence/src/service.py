import os
import sys
from typing import List, Dict, Any
import numpy as np
from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, PlainTextResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uvicorn

# Setup module path
sys.path.insert(0, os.path.dirname(__file__))
from aiops_agent import AIOpsMultiAgentSystem
from v2_temporal_engine import AIOpsTemporalEngineV2

app = FastAPI(title="Mohit AIOps Cloud Intelligence Microservice v2.0", version="2.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

model_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'models', 'telemetry_anomaly_detector.pkl'))
aiops_engine = AIOpsMultiAgentSystem(model_path)
temporal_engine_v2 = AIOpsTemporalEngineV2()

def to_safe_json(obj):
    if isinstance(obj, dict):
        return {str(k): to_safe_json(v) for k, v in obj.items()}
    elif isinstance(obj, (list, tuple)):
        return [to_safe_json(v) for v in obj]
    elif isinstance(obj, np.generic):
        return obj.item()
    elif isinstance(obj, np.ndarray):
        return [to_safe_json(v) for v in obj.tolist()]
    return obj

class TelemetryRequest(BaseModel):
    cpu: float
    memory: float
    latency: float
    sockets: float

@app.get("/health")
async def health_check():
    return JSONResponse(content={
        "status": "UP",
        "service": "Mohit AIOps Microservice",
        "port": 5001,
        "model_loaded": os.path.exists(model_path),
        "student": "Mohit Raj Deo (12323329 | Roll: 62)"
    })

@app.get("/metrics")
async def prometheus_metrics():
    # Return Prometheus text exposition format
    metrics_text = f"""# HELP aiops_service_up Status of AIOps Microservice
# TYPE aiops_service_up gauge
aiops_service_up 1
# HELP aiops_model_loaded Machine learning anomaly detector model status
# TYPE aiops_model_loaded gauge
aiops_model_loaded 1
# HELP aiops_port Serving port
# TYPE aiops_port gauge
aiops_port 5001
"""
    return PlainTextResponse(content=metrics_text, media_type="text/plain; version=0.0.4")

@app.post("/api/aiops/telemetry")
async def process_telemetry(req: TelemetryRequest):
    try:
        mon = aiops_engine.monitor_telemetry(req.cpu, req.memory, req.latency, req.sockets)
        inv = aiops_engine.investigate_incident(mon)
        rem = aiops_engine.execute_remediation(inv)
        rca = aiops_engine.synthesize_rca_report(mon, inv, rem)
        return JSONResponse(content=to_safe_json({
            "monitoring": mon,
            "investigation": inv,
            "remediation": rem,
            "rca_report": rca
        }))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

class TemporalWindowRequest(BaseModel):
    window: List[TelemetryRequest]
    scenario: str = "normal"

@app.post("/api/v2/telemetry/temporal-anomaly")
async def evaluate_temporal_v2(req: TemporalWindowRequest):
    try:
        dict_window = [pt.dict() for pt in req.window]
        anomaly_res = temporal_engine_v2.evaluate_temporal_window(dict_window)
        ebpf_res = temporal_engine_v2.simulate_ebpf_stream(req.scenario)
        slm_res = temporal_engine_v2.generate_slm_rca(anomaly_res, ebpf_res)
        return JSONResponse(content=to_safe_json({
            "status": "SUCCESS",
            "version": "2.0.0",
            "temporal_anomaly_detection": anomaly_res,
            "ebpf_kernel_probe": ebpf_res,
            "slm_chain_of_thought_rca": slm_res
        }))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/v2/telemetry/ebpf-stream")
async def get_ebpf_stream(scenario: str = "normal"):
    stream = temporal_engine_v2.simulate_ebpf_stream(scenario)
    return JSONResponse(content=to_safe_json(stream))

# Mount React UI production distribution
ui_dist_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'ui', 'dist'))
if os.path.exists(ui_dist_path):
    assets_path = os.path.join(ui_dist_path, 'assets')
    if os.path.exists(assets_path):
        app.mount("/assets", StaticFiles(directory=assets_path), name="assets")

    @app.get("/")
    async def serve_react_app():
        return FileResponse(os.path.join(ui_dist_path, 'index.html'))

if __name__ == '__main__':
    uvicorn.run(app, host="0.0.0.0", port=5001)

