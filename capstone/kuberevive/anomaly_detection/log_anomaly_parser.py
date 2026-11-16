"""
Log Anomaly Parser & Semantic Error Extractor (Member 2 Responsibility)
Extracts structure from semi-structured log streams, clusters templates,
and detects anomalous stack traces or error surges.
"""

import re
import math
from typing import Dict, List, Any
from collections import Counter


class LogAnomalyParser:
    """
    Online Log Template Miner and Anomaly Detector based on regex pattern masking,
    token frequency deviation, Shannon entropy, and security exploit signature scanning.
    """
    def __init__(self):
        # Patterns to mask dynamic variables in logs
        self.ip_regex = re.compile(r"\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b")
        self.uuid_regex = re.compile(r"\b[a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12}\b", re.I)
        self.num_regex = re.compile(r"\b\d+\b")
        self.error_keywords = ["ERROR", "FATAL", "CRITICAL", "Exception", "Timeout", "OOMKilled", "Deadlock", "Refused"]
        
        # Security Threat Patterns (v2.0)
        self.security_patterns = {
            "SQLI": re.compile(r"(\b(union|select|insert|delete|drop)\b.*\b(from|where)\b|'.*--|/\*.*\*/)", re.IGNORECASE),
            "CMD_INJECTION": re.compile(r"(;.*?\b(cat|ls|rm|curl|wget|nc|sh|bash)\b|\|\|.*?\b(sh|bash)\b)", re.IGNORECASE),
            "PATH_TRAVERSAL": re.compile(r"(\.\./\.\./|/etc/passwd|/windows/win\.ini)", re.IGNORECASE),
            "BRUTE_FORCE": re.compile(r"(failed password|authentication failure|invalid user)", re.IGNORECASE)
        }

        self.template_counter: Counter = Counter()
        self.recent_logs: List[Dict[str, Any]] = []

    def compute_entropy(self, s: str) -> float:
        """Computes Shannon Entropy of character sequence to detect encrypted/obfuscated attack vectors."""
        if not s:
            return 0.0
        prob = [float(s.count(c)) / len(s) for c in dict.fromkeys(list(s))]
        return round(-sum([p * math.log(p) / math.log(2.0) for p in prob]), 3)

    def mask_log(self, message: str) -> str:
        """Transforms a raw log message into an abstract template."""
        s = self.ip_regex.sub("<IP>", message)
        s = self.uuid_regex.sub("<UUID>", s)
        s = self.num_regex.sub("<NUM>", s)
        return s.strip()

    def parse_log(self, raw_log: str, service: str = "checkout-service") -> Dict[str, Any]:
        """
        Parses a log line, computes template hash, entropy, security threats, and evaluates log severity.
        """
        is_error = any(keyword.lower() in raw_log.lower() for keyword in self.error_keywords)
        template = self.mask_log(raw_log)
        self.template_counter[template] += 1
        
        entropy = self.compute_entropy(raw_log)
        matched_threats = [threat for threat, pat in self.security_patterns.items() if pat.search(raw_log)]
        is_sec = len(matched_threats) > 0 or entropy > 4.9

        parsed = {
            "service": service,
            "raw": raw_log,
            "template": template,
            "is_error": is_error,
            "occurrence_count": self.template_counter[template],
            "shannon_entropy": entropy,
            "security_threats": matched_threats,
            "is_security_incident": is_sec
        }
        self.recent_logs.append(parsed)
        if len(self.recent_logs) > 500:
            self.recent_logs.pop(0)

        return parsed

    def get_recent_error_summary(self, max_items: int = 10) -> List[Dict[str, Any]]:
        """Returns the most frequent recent error templates."""
        errors = [l for l in self.recent_logs if l["is_error"]]
        templates = Counter(e["template"] for e in errors)
        return [{"template": t, "count": c} for t, c in templates.most_common(max_items)]

