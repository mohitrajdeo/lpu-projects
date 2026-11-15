#!/usr/bin/env python3
"""
Interactive Terminal Demonstration for Akash Autonomous SWE Platform
INT422: Deep Learning & Applied AI
"""

import sys
import os
import time

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))
from swe_agents import AutonomousSWESystem

def main():
    print("=" * 70)
    print(" INT422 AUTONOMOUS SOFTWARE ENGINEERING PLATFORM")
    print(" Student: Akash Choudhary (12301625) | Lovely Professional University")
    print("=" * 70)
    
    model_file = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'models', 'code_defect_classifier.pkl'))
    swe = AutonomousSWESystem(model_file)
    
    user_prompt = "Design and implement a robust sliding-window API Rate Limiter in Python"
    print(f"\n[USER PROMPT]: \"{user_prompt}\"")
    time.sleep(1)

    print("\n[STEP 1] Agent 1 (System Architect) querying RAG Architecture Patterns...")
    spec = swe.decompose_requirements(user_prompt)
    print(f"  Target Module: {spec['module_name']}")
    print(f"  Pattern Retrieved: {spec['recommended_pattern']}")
    print(f"  Security Policy: {spec['security_policy']}")
    time.sleep(1)

    print("\n[STEP 2] Agent 2 (Code Generator) generating implementation...")
    code_info = swe.generate_code(spec)
    print("  Code generated successfully.")
    print("  Code metrics extracted (LOC: {}, Cyclomatic: {}, AST Depth: {})".format(
        code_info["metrics"]["loc"], code_info["metrics"]["cyclomatic_complexity"], code_info["metrics"]["ast_depth"]
    ))
    time.sleep(1)

    print("\n[STEP 3] Agent 3 (ML Defect Reviewer) running Deep Defect Classifier...")
    audit = swe.audit_defect_risk(code_info)
    print(f"  Risk Assessment: {audit['risk_label']}")
    print(f"  Defect Probability Score: {audit['defect_probability']}")
    time.sleep(1)

    print("\n[STEP 4] Agent 4 (Test Engineer) executing automated unit tests in sandbox...")
    test_res = swe.run_tests_and_validate(code_info)
    print(f"  Test Suite Status: {test_res['test_suite_status']} ({test_res['tests_passed']}/{test_res['tests_executed']} passed)")
    print(f"  Code Coverage: {test_res['coverage_pct']}%")
    time.sleep(1)

    print("\n" + "=" * 70)
    print("                    VALIDATED CODE ARTIFACT                        ")
    print("=" * 70)
    print(code_info["code"])
    print("=" * 70)
    print("[SUCCESS] End-to-end multi-agent SWE pipeline completed without human intervention!")

if __name__ == '__main__':
    main()

