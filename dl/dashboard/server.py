import os
import sys
import numpy as np
from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uvicorn

# Setup paths to import agent engines from each project
base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, os.path.join(base_dir, '1_Mohit_AIOps_Cloud_Intelligence', 'src'))
sys.path.insert(0, os.path.join(base_dir, '2_Akash_Autonomous_SWE_System', 'src'))
sys.path.insert(0, os.path.join(base_dir, '3_Saif_Cyber_Threat_Intelligence', 'src'))

from aiops_agent import AIOpsMultiAgentSystem
from swe_agents import AutonomousSWESystem
from secops_agent import AutonomousSecOpsSOC

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

app = FastAPI(title="INT422 Deep Learning & Applied AI - Master Production Dashboard", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load trained models
mohit_model_path = os.path.join(base_dir, '1_Mohit_AIOps_Cloud_Intelligence', 'models', 'telemetry_anomaly_detector.pkl')
akash_model_path = os.path.join(base_dir, '2_Akash_Autonomous_SWE_System', 'models', 'code_defect_classifier.pkl')
saif_model_path = os.path.join(base_dir, '3_Saif_Cyber_Threat_Intelligence', 'models', 'intrusion_detection_model.pkl')

aiops_engine = AIOpsMultiAgentSystem(mohit_model_path)
swe_engine = AutonomousSWESystem(akash_model_path)
secops_engine = AutonomousSecOpsSOC(saif_model_path)

# Pydantic Request Models
class TelemetryRequest(BaseModel):
    cpu: float
    memory: float
    latency: float
    sockets: float

class SWEGenerateRequest(BaseModel):
    prompt: str

class SecOpsTriageRequest(BaseModel):
    pkt_len: float
    duration: float
    fwd_pkts: float
    syn_flags: int
    port: int
    source_ip: str = "198.51.100.42"

# 1. Project 1: AIOps Endpoints
@app.post("/api/aiops/telemetry")
async def analyze_telemetry(req: TelemetryRequest):
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

# 2. Project 2: SWE Endpoints
@app.post("/api/swe/generate")
async def generate_and_audit_code(req: SWEGenerateRequest):
    try:
        spec = swe_engine.decompose_requirements(req.prompt)
        code_data = swe_engine.generate_code(spec)
        audit = swe_engine.audit_defect_risk(code_data)
        test_res = swe_engine.run_tests_and_validate(code_data)
        return JSONResponse(content=to_safe_json({
            "specification": spec,
            "code_data": code_data,
            "defect_audit": audit,
            "test_results": test_res
        }))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# 3. Project 3: SecOps Endpoints
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

@app.get("/api/status")
async def get_system_status():
    return JSONResponse(content=to_safe_json({
        "status": "ONLINE",
        "platform": "INT422 Deep Learning & Applied AI Multi-Project Server",
        "active_models": {
            "mohit_aiops": os.path.exists(mohit_model_path),
            "akash_swe": os.path.exists(akash_model_path),
            "saif_secops": os.path.exists(saif_model_path)
        },
        "port": 8000
    }))

# Serve Static Downloads (Reports, Zips, Devops)
static_path = os.path.join(os.path.dirname(__file__), 'static')
app.mount("/static", StaticFiles(directory=static_path), name="static")

# Serve Compiled React 19 + Vite Master Single-Page Application
ui_dist_path = os.path.abspath(os.path.join(os.path.dirname(__file__), 'ui', 'dist'))
if os.path.exists(ui_dist_path):
    assets_path = os.path.join(ui_dist_path, 'assets')
    if os.path.exists(assets_path):
        app.mount("/assets", StaticFiles(directory=assets_path), name="ui-assets")

    @app.get("/")
    async def root():
        return FileResponse(os.path.join(ui_dist_path, 'index.html'))
else:
    @app.get("/")
    async def root():
        return FileResponse(os.path.join(static_path, 'index.html'))

if __name__ == '__main__':
    uvicorn.run("server:app", host="0.0.0.0", port=8000, reload=False)
