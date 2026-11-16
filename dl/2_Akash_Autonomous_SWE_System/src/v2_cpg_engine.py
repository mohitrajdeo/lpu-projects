"""
Akash Autonomous SWE System v2.0 - Code Property Graph (CPG) & Speculative Sandbox Engine
INT422 Applied Deep Learning & Software Intelligence
Author: Akash Choudhary (Reg No: 12301625 | Roll No: 11)

Key Innovations:
1. Code Property Graph (CPG) static semantic graph analyzer combining AST, CFG branches, and Data Dependency.
2. Speculative Sandboxed Execution Runner: verifies generated code patches against runtime test harnesses in sub-second isolation.
3. Automated GitHub Unified Diff and Pull Request Synthesis Engine.
"""

import os
import sys
import ast
import time
import subprocess
import tempfile
from typing import Dict, List, Any

class CodePropertyGraphAnalyzer:
    """
    Constructs a lightweight Code Property Graph representation directly from Python source code:
    - Abstract Syntax Tree (AST) hierarchy
    - Control Flow Graph (CFG) decision points (if/for/while/try)
    - Data Dependency Graph (DDG) variable reads and writes
    """
    def __init__(self):
        pass

    def analyze_source(self, code_str: str) -> Dict[str, Any]:
        try:
            tree = ast.parse(code_str)
        except SyntaxError as e:
            return {
                "parse_success": False,
                "syntax_error": str(e),
                "line": e.lineno,
                "cpg_metrics": {}
            }

        ast_nodes = 0
        cfg_branches = 0
        variables_written = set()
        variables_read = set()
        functions_defined = []
        classes_defined = []
        code_smells = []

        for node in ast.walk(tree):
            ast_nodes += 1
            if isinstance(node, (ast.If, ast.For, ast.While, ast.ExceptHandler, ast.With)):
                cfg_branches += 1
            elif isinstance(node, ast.FunctionDef):
                functions_defined.append(node.name)
            elif isinstance(node, ast.ClassDef):
                classes_defined.append(node.name)
            elif isinstance(node, ast.Name):
                if isinstance(node.ctx, ast.Store):
                    variables_written.add(node.id)
                elif isinstance(node, ast.Load):
                    variables_read.add(node.id)
            elif isinstance(node, ast.Try):
                for handler in node.handlers:
                    if handler.type is None:
                        code_smells.append({
                            "type": "BARE_EXCEPT",
                            "line": handler.lineno,
                            "severity": "HIGH",
                            "recommendation": "Catch specific exception types rather than bare 'except:'"
                        })

        # Check for unused variables (written but never read)
        unused_vars = list(variables_written - variables_read - {"_", "__name__", "self", "cls"})
        if unused_vars:
            code_smells.append({
                "type": "UNUSED_VARIABLE",
                "variables": unused_vars[:5],
                "severity": "LOW",
                "recommendation": "Remove or refactor unused variables to reduce memory footprint."
            })

        # Calculate Cyclomatic Complexity (M = E - N + 2P approximated by CFG decision points + 1)
        cyclomatic_complexity = cfg_branches + 1
        halstead_volume_estimate = round(ast_nodes * 2.8, 1)

        return {
            "parse_success": True,
            "cpg_metrics": {
                "ast_node_count": ast_nodes,
                "cfg_decision_branches": cfg_branches,
                "cyclomatic_complexity": cyclomatic_complexity,
                "data_dependency_variables_tracked": len(variables_written.union(variables_read)),
                "classes_count": len(classes_defined),
                "functions_count": len(functions_defined),
                "halstead_volume_estimate": halstead_volume_estimate
            },
            "detected_code_smells": code_smells,
            "semantic_graph_signature": f"CPG-AST{ast_nodes}-CFG{cfg_branches}-DDG{len(variables_written)}"
        }

class SpeculativeSandboxRunner:
    """
    Executes generated code patches in an isolated temporary Python environment
    with strict time boundaries and assertion validation.
    """
    @staticmethod
    def execute_speculative_verification(code_str: str, test_assertions: List[str] = None) -> Dict[str, Any]:
        harness_code = code_str + "\n\n"
        harness_code += "# Speculative Verification Test Suite\n"
        if test_assertions:
            harness_code += "\n".join(test_assertions)
        else:
            harness_code += "# Default sanity assertion\nassert True\nprint('SANITARY_CHECK_PASSED')"

        start_time = time.time()
        with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as tf:
            tf.write(harness_code)
            temp_path = tf.name

        try:
            res = subprocess.run(
                [sys.executable, temp_path],
                capture_output=True,
                text=True,
                timeout=3.0  # 3-second hard timeout
            )
            duration_ms = round((time.time() - start_time) * 1000, 2)
            passed = (res.returncode == 0)

            return {
                "sandbox_passed": passed,
                "execution_duration_ms": duration_ms,
                "exit_code": res.returncode,
                "stdout": res.stdout.strip()[:500],
                "stderr": res.stderr.strip()[:500] if not passed else "",
                "isolation_boundary": "Process-Isolation-Subprocess"
            }
        except subprocess.TimeoutExpired:
            return {
                "sandbox_passed": False,
                "execution_duration_ms": 3000.0,
                "exit_code": -1,
                "stdout": "",
                "stderr": "EXECUTION_TIMEOUT_EXCEEDED (Max 3000ms allowed - potential infinite loop detected)",
                "isolation_boundary": "Process-Isolation-Subprocess"
            }
        finally:
            if os.path.exists(temp_path):
                try:
                    os.remove(temp_path)
                except Exception:
                    pass

class AutonomousPRGenerator:
    """Generates unified diffs and Git Pull Request markdown templates."""
    @staticmethod
    def generate_unified_diff(original_code: str, patched_code: str, filename: str = "service.py") -> str:
        orig_lines = original_code.splitlines(keepends=True)
        patch_lines = patched_code.splitlines(keepends=True)
        import difflib
        diff = difflib.unified_diff(
            orig_lines,
            patch_lines,
            fromfile=f"a/{filename}",
            tofile=f"b/{filename}",
            n=3
        )
        return "".join(diff)

    @staticmethod
    def generate_pr_metadata(task_description: str, cpg_info: Dict[str, Any], test_res: Dict[str, Any]) -> Dict[str, Any]:
        return {
            "pr_title": f"fix(autocode): autonomous patch for '{task_description[:50]}'",
            "branch_name": f"swe-autonomous-patch-{int(time.time())}",
            "pr_body": f"""### Autonomous SWE Multi-Agent System v2.0
**Lead Engineer:** Akash Choudhary (12301625 | Roll: 11)

#### 🔍 Code Property Graph (CPG) Analysis:
- **AST Nodes:** {cpg_info.get('cpg_metrics', {}).get('ast_node_count', 0)}
- **Cyclomatic Complexity:** {cpg_info.get('cpg_metrics', {}).get('cyclomatic_complexity', 0)}
- **Smells Detected:** {len(cpg_info.get('detected_code_smells', []))}

#### ⚡ Speculative Sandbox Verification:
- **Status:** {'✅ PASSED' if test_res.get('sandbox_passed') else '❌ FAILED'}
- **Execution Latency:** {test_res.get('execution_duration_ms', 0)} ms
- **Exit Code:** {test_res.get('exit_code', 0)}

*Auto-generated and validated via speculative execution sandbox.*
"""
        }

