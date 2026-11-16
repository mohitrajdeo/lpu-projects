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
from swe_agents import AutonomousSWESystem
from v2_cpg_engine import CodePropertyGraphAnalyzer, SpeculativeSandboxRunner, AutonomousPRGenerator

app = FastAPI(title="Akash Autonomous SWE Platform Microservice v2.0", version="2.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

model_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'models', 'code_defect_classifier.pkl'))
swe_engine = AutonomousSWESystem(model_path)
cpg_analyzer = CodePropertyGraphAnalyzer()

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

class SWEGenerateRequest(BaseModel):
    prompt: str

@app.get("/health")
async def health_check():
    return JSONResponse(content={
        "status": "UP",
        "service": "Akash Autonomous SWE Platform Microservice",
        "port": 5002,
        "model_loaded": os.path.exists(model_path),
        "student": "Akash Choudhary (12301625 | Roll: 11)"
    })

@app.get("/metrics")
async def prometheus_metrics():
    metrics_text = f"""# HELP swe_service_up Status of SWE Microservice
# TYPE swe_service_up gauge
swe_service_up 1
# HELP swe_model_loaded Machine learning defect classifier model status
# TYPE swe_model_loaded gauge
swe_model_loaded 1
# HELP swe_port Serving port
# TYPE swe_port gauge
swe_port 5002
"""
    return PlainTextResponse(content=metrics_text, media_type="text/plain; version=0.0.4")

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

class CPGAnalysisRequest(BaseModel):
    code: str
    filename: Optional[str] = "service.py"

class SpeculativeVerifyRequest(BaseModel):
    code: str
    assertions: Optional[List[str]] = None
    original_code: Optional[str] = None
    task_description: Optional[str] = "Refactor and optimize algorithm"

@app.post("/api/v2/swe/cpg-analysis")
async def analyze_cpg(req: CPGAnalysisRequest):
    try:
        analysis = cpg_analyzer.analyze_source(req.code)
        return JSONResponse(content=to_safe_json({
            "status": "SUCCESS",
            "version": "2.0.0",
            "cpg_analysis": analysis
        }))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/v2/swe/speculative-verify")
async def speculative_verify_and_diff(req: SpeculativeVerifyRequest):
    try:
        cpg_info = cpg_analyzer.analyze_source(req.code)
        sandbox_res = SpeculativeSandboxRunner.execute_speculative_verification(req.code, req.assertions)
        
        diff_str = ""
        if req.original_code:
            diff_str = AutonomousPRGenerator.generate_unified_diff(req.original_code, req.code)
            
        pr_meta = AutonomousPRGenerator.generate_pr_metadata(
            req.task_description, cpg_info, sandbox_res
        )

        return JSONResponse(content=to_safe_json({
            "status": "SUCCESS",
            "version": "2.0.0",
            "cpg_metrics": cpg_info,
            "speculative_sandbox": sandbox_res,
            "unified_diff": diff_str,
            "pull_request_metadata": pr_meta
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
    uvicorn.run(app, host="0.0.0.0", port=5002)

