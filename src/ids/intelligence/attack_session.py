"""Track a single attack session and associated IDS alerts.

AttackSession aggregates alert events over a contiguous time window and
computes severity, involved ECUs, and attack type metadata.
"""

from dataclasses import dataclass, field
from typing import List, Set


@dataclass
class AttackSession:
    session_id: str
    start_time: float
    end_time: float

    alerts: List[object] = field(default_factory=list)

    involved_ecus: Set[str] = field(default_factory=set)
    attack_types: Set[str] = field(default_factory=set)

    severity_score: float = 0.0
    phase: str = "UNKNOWN"

    def add_alert(self, alert):
        """
        Accepts IDSAlert directly from src/ids/alert.py
        """

        self.alerts.append(alert)
        self.end_time = alert.timestamp

        self.involved_ecus.add(alert.ecu)
        self.attack_types.add(alert.rule)

        # -----------------------------
        # FIXED: proper severity mapping
        # -----------------------------
        severity_map = {
            "CRITICAL": 5,
            "HIGH": 3,
            "MEDIUM": 2,
            "LOW": 1
        }

        sev = getattr(alert.severity, "name", str(alert.severity))
        self.severity_score += severity_map.get(sev, 1)

    def analyze_phase(self):
        from .phase_detector import PhaseDetector

        detector = PhaseDetector()
        self.phase = detector.dominant_phase(self.alerts).value

    def to_dict(self):
        return {
            "session_id": self.session_id,
            "start_time": self.start_time,
            "end_time": self.end_time,
            "involved_ecus": list(self.involved_ecus),
            "attack_types": list(self.attack_types),
            "severity_score": self.severity_score,
            "alert_count": len(self.alerts),
            "phase": self.phase,
        }
