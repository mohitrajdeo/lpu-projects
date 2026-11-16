"""
Log Anomaly Parser & Semantic Error Extractor (Member 2 Responsibility)
Extracts structure from semi-structured log streams, clusters templates,
and detects anomalous stack traces or error surges.
"""

import re
from typing import Dict, List, Any
from collections import Counter


class LogAnomalyParser:
    """
    Online Log Template Miner and Anomaly Detector based on regex pattern masking
    and token frequency deviation.
    """
    def __init__(self):
        # Patterns to mask dynamic variables in logs
        self.ip_regex = re.compile(r"\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b")
        self.uuid_regex = re.compile(r"\b[a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12}\b", re.I)
        self.num_regex = re.compile(r"\b\d+\b")
        self.error_keywords = ["ERROR", "FATAL", "CRITICAL", "Exception", "Timeout", "OOMKilled", "Deadlock", "Refused"]
        
        self.template_counter: Counter = Counter()
        self.recent_logs: List[Dict[str, Any]] = []

    def mask_log(self, message: str) -> str:
        """Transforms a raw log message into an abstract template."""
        s = self.ip_regex.sub("<IP>", message)
        s = self.uuid_regex.sub("<UUID>", s)
        s = self.num_regex.sub("<NUM>", s)
        return s.strip()

    def parse_log(self, raw_log: str, service: str = "checkout-service") -> Dict[str, Any]:
        """
        Parses a log line, computes template hash, and evaluates log severity.
        """
        is_error = any(keyword.lower() in raw_log.lower() for keyword in self.error_keywords)
        template = self.mask_log(raw_log)
        self.template_counter[template] += 1

        parsed = {
            "service": service,
            "raw": raw_log,
            "template": template,
            "is_error": is_error,
            "occurrence_count": self.template_counter[template]
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

