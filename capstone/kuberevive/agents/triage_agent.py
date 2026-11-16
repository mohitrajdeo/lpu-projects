"""
Incident Triage & Alert Deduplication Agent (Member 3 Responsibility)
Suppresses alert storms, clusters related metric violations, and assigns incident severity.
"""

import time
import uuid
from typing import Dict, List, Any, Optional


class IncidentTriageAgent:
    """
    Intelligent Triage Agent that acts as the first line of defense in AIOps:
    1. Deduplicates continuous anomalies from the same service.
    2. Groups co-occurring symptom metrics into a unified incident ticket.
    3. Calculates incident priority (P1 Critical to P4 Low).
    """
    def __init__(self, suppression_window_seconds: int = 30):
        self.suppression_window_seconds = suppression_window_seconds
        self.active_incidents: Dict[str, Dict[str, Any]] = {}
        self.incident_history: List[Dict[str, Any]] = []

    def triage_anomaly(self, anomaly_report: Dict[str, Any], service: str = "checkout-service") -> Optional[Dict[str, Any]]:
        """
        Receives an anomaly report. If an incident is already ongoing for this service
        within the suppression window, updates it. Otherwise, creates a new incident.
        """
        if not anomaly_report.get("is_anomaly", False):
            return None

        now = time.time()
        severity_score = anomaly_report.get("severity_score", 0.5)

        # Map score to P1 - P4
        if severity_score >= 0.85:
            priority = "P1-CRITICAL"
        elif severity_score >= 0.65:
            priority = "P2-HIGH"
        elif severity_score >= 0.40:
            priority = "P3-MEDIUM"
        else:
            priority = "P4-LOW"

        # Check existing active incident for suppression
        if service in self.active_incidents:
            inc = self.active_incidents[service]
            if now - inc["last_seen"] < self.suppression_window_seconds:
                # Update existing incident
                inc["last_seen"] = now
                inc["event_count"] += 1
                inc["max_severity"] = max(inc["max_severity"], severity_score)
                inc["offending_metrics"] = list(set(inc["offending_metrics"] + anomaly_report.get("offending_metrics", [])))
                return None  # Suppress duplicate alert noise

        # Create fresh incident ticket
        incident_id = f"INC-{str(uuid.uuid4())[:8].upper()}"
        incident_ticket = {
            "incident_id": incident_id,
            "service": service,
            "status": "OPEN",
            "priority": priority,
            "created_at": now,
            "last_seen": now,
            "event_count": 1,
            "max_severity": severity_score,
            "offending_metrics": anomaly_report.get("offending_metrics", []),
            "critical_violations": anomaly_report.get("critical_violations", []),
            "raw_anomaly_data": anomaly_report
        }

        self.active_incidents[service] = incident_ticket
        self.incident_history.append(incident_ticket)
        return incident_ticket

    def resolve_incident(self, service: str):
        """Marks an active incident as resolved."""
        if service in self.active_incidents:
            inc = self.active_incidents.pop(service)
            inc["status"] = "RESOLVED"
            inc["resolved_at"] = time.time()
            return inc
        return None

