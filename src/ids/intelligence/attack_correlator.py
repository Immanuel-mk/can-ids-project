"""Correlate IDS alerts into sessions and attack campaigns.

This module identifies contiguous alert activity as sessions, classifies
attack types, and groups related sessions into campaigns.
"""

import uuid
from typing import List, Optional
from .attack_session import AttackSession


# ==============================
# ATTACK PHASE CLASSIFIER (NEW)
# ==============================
def classify_phase(session):

    attack_types = session.attack_types

    if "RPM_RANGE_CHECK" in attack_types and "RPM_SPIKE_DETECTION" in attack_types:
        return "INJECTION_ATTACK"

    if "FREQUENCY_THRESHOLD_CHECK" in attack_types:
        return "FLOODING_ATTACK"

    return "UNKNOWN"


class AttackCorrelator:
    def __init__(self, time_threshold: float = 5.0):
        """
        time_threshold: max seconds between alerts in same attack session
        """
        self.time_threshold = time_threshold

        self.sessions: List[AttackSession] = []
        self.current_session: Optional[AttackSession] = None

    def process_alert(self, alert):
        """
        Accepts IDSAlert objects directly
        """

        # First alert → create session
        if self.current_session is None:
            self._start_new_session(alert)
            return

        time_gap = alert.timestamp - self.current_session.end_time

        # Gap detected → close session and start new one
        if time_gap > self.time_threshold:
            self._finalize_session()
            self._start_new_session(alert)
        else:
            self.current_session.add_alert(alert)

    def _start_new_session(self, alert):
        session = AttackSession(
            session_id=str(uuid.uuid4()),
            start_time=alert.timestamp,
            end_time=alert.timestamp,
        )
        session.add_alert(alert)
        self.current_session = session

    def _finalize_session(self):
        if self.current_session:
            # Ensure end_time reflects last alert
            # (AttackSession.add_alert should already update it,
            # but we enforce safety here)
            
            # ✅ CLASSIFY PHASE HERE (CRITICAL)
            self.current_session.phase = classify_phase(self.current_session)

            self.sessions.append(self.current_session)
            self.current_session = None

    def finalize_all(self):
        """Call at end of simulation"""
        self._finalize_session()
        return self.sessions
