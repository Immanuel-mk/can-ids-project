"""Data model for a grouped attack campaign.

AttackCampaign aggregates several attack sessions and tracks combined ECU
involvement, attack types, and cumulative severity.
"""

from dataclasses import dataclass, field
from typing import List, Set


@dataclass
class AttackCampaign:
    campaign_id: str

    sessions: List[object] = field(default_factory=list)

    involved_ecus: Set[str] = field(default_factory=set)
    attack_types: Set[str] = field(default_factory=set)

    total_severity: float = 0.0

    def add_session(self, session):

        self.sessions.append(session)

        self.involved_ecus.update(session.involved_ecus)
        self.attack_types.update(session.attack_types)

        self.total_severity += session.severity_score

    def to_dict(self):
        return {
            "campaign_id": self.campaign_id,
            "session_count": len(self.sessions),
            "involved_ecus": list(self.involved_ecus),
            "attack_types": list(self.attack_types),
            "total_severity": self.total_severity,
        }
