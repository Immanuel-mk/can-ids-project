"""Enumerate standard attack phases for intelligence analysis.

AttackPhase is used by phase detection and reporting components to provide
higher-level descriptions of attacker behavior.
"""

from enum import Enum


class AttackPhase(Enum):
    RECONNAISSANCE = "RECONNAISSANCE"
    EXPLOITATION = "EXPLOITATION"
    ESCALATION = "ESCALATION"
    PERSISTENCE = "PERSISTENCE"
    UNKNOWN = "UNKNOWN"
