"""Detect the dominant attack phase from IDS alerts.

PhaseDetector maps detection rules to standard phases and selects the most
likely phase for a session.
"""

from collections import Counter
from .attack_phases import AttackPhase


class PhaseDetector:
    """
    Converts IDS alerts into attack phase sequence.
    """

    def __init__(self):

        # mapping IDS rules → phases
        self.rule_map = {
            "FREQUENCY_THRESHOLD_CHECK": AttackPhase.RECONNAISSANCE,
            "RPM_SPOOF_CHECK": AttackPhase.EXPLOITATION,
            "RPM_SPIKE_DETECTION": AttackPhase.ESCALATION,
            "RPM_RANGE_CHECK": AttackPhase.PERSISTENCE,
        }

    def detect_phase(self, alerts):

        phases = []

        for alert in alerts:
            phase = self.rule_map.get(alert.rule, AttackPhase.UNKNOWN)
            phases.append(phase)

        return phases

    def dominant_phase(self, alerts):

        phases = self.detect_phase(alerts)

        if not phases:
            return AttackPhase.UNKNOWN

        return Counter(phases).most_common(1)[0][0]
