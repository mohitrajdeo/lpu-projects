import os
import sys
from typing import List, Dict, Any, Optional
import numpy as np
from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, PlainTextResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uvicorn

# Setup module path
sys.path.insert(0, os.path.dirname(__file__))
from secops_agent import AutonomousSecOpsSOC
from v2_threat_graph_engine import SemanticLogAnalyzer, ThreatAttackGraphNavigator, AutomatedSOARPlaybook

app = FastAPI(title="Saif Autonomous SOC Threat Hunter Microservice v2.0", version="2.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

model_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'models', 'intrusion_detection_model.pkl'))
secops_engine = AutonomousSecOpsSOC(model_path)
semantic_log_analyzer = SemanticLogAnalyzer()

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

class SecOpsTriageRequest(BaseModel):
    pkt_len: float
    duration: float
    fwd_pkts: float
    syn_flags: int
    port: int
    source_ip: str = "198.51.100.42"

@app.get("/health")
async def health_check():
    return JSONResponse(content={
        "status": "UP",
        "service": "Saif Autonomous SOC Threat Hunter Microservice",
        "port": 5003,
        "model_loaded": os.path.exists(model_path),
        "student": "Saif Siddique (12308813 | Roll: 44)"
    })

@app.get("/metrics")
async def prometheus_metrics():
    metrics_text = f"""# HELP secops_service_up Status of SecOps Microservice
# TYPE secops_service_up gauge
secops_service_up 1
# HELP secops_model_loaded Deep neural network intrusion detection model status
# TYPE secops_model_loaded gauge
secops_model_loaded 1
# HELP secops_port Serving port
# TYPE secops_port gauge
secops_port 5003
"""
    return PlainTextResponse(content=metrics_text, media_type="text/plain; version=0.0.4")

@app.post("/api/secops/triage")
async def triage_cyber_threat(req: SecOpsTriageRequest):
    try:
        triage = secops_engine.triage_network_flow(
            req.pkt_len, req.duration, req.fwd_pkts, req.syn_flags, req.port, req.source_ip
        )
        intel = secops_engine.correlate_threat_intel(triage)
        quarantine = secops_engine.execute_quarantine(triage, intel)
        brief = secops_engine.generate_cti_brief(triage, intel, quarantine)
        return JSONResponse(content=to_safe_json({
            "triage": triage,
            "threat_intelligence": intel,
            "quarantine": quarantine,
            "cti_brief": brief
        }))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

class LogThreatAnalysisRequest(BaseModel):
    log_text: str
    attacker_ip: Optional[str] = "198.51.100.42"

class SOARContainmentRequest(BaseModel):
    attacker_ip: str
    attack_type: Optional[str] = "SQLI"

@app.post("/api/v2/secops/threat-graph")
async def analyze_threat_graph(req: LogThreatAnalysisRequest):
    try:
        log_res = semantic_log_analyzer.analyze_log_entry(req.log_text)
        graph_res = ThreatAttackGraphNavigator.traverse_attack_path(log_res.get("matched_signatures", []))
        soar_res = AutomatedSOARPlaybook.synthesize_containment(
            req.attacker_ip,
            log_res.get("matched_signatures", ["ANOMALY"])[0] if log_res.get("matched_signatures") else "ANOMALY"
        )
        return JSONResponse(content=to_safe_json({
            "status": "SUCCESS",
            "version": "2.0.0",
            "semantic_log_analysis": log_res,
            "mitre_attack_graph": graph_res,
            "automated_soar_playbook": soar_res
        }))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/v2/secops/soar-quarantine")
async def dispatch_soar_quarantine(req: SOARContainmentRequest):
    try:
        playbook = AutomatedSOARPlaybook.synthesize_containment(req.attacker_ip, req.attack_type)
        return JSONResponse(content=to_safe_json({
            "status": "SUCCESS",
            "version": "2.0.0",
            "dispatch_status": "ENFORCED",
            "playbook": playbook
        }))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

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
    uvicorn.run(app, host="0.0.0.0", port=5003)

