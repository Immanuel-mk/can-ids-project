"""Create summaries and JSON reports for attack intelligence.

This module consolidates session and campaign analytics into reports for
later review and automated dashboards.
"""

import json
from datetime import datetime


class AttackReporter:

    def __init__(self, sessions, campaigns):

        self.sessions = sessions
        self.campaigns = campaigns

    def generate_summary(self):

        return {
            "generated_at": datetime.utcnow().isoformat(),

            "total_sessions": len(self.sessions),
            "total_campaigns": len(self.campaigns),

            "total_attacks": sum(len(s.alerts) for s in self.sessions),

            "severity_distribution": self._severity_summary(),

            "campaign_overview": [
                c.to_dict() for c in self.campaigns
            ]
        }

    def _severity_summary(self):

        summary = {
            "low": 0,
            "medium": 0,
            "high": 0,
            "critical": 0
        }

        for session in self.sessions:
            score = session.severity_score

            if score <= 2:
                summary["low"] += 1
            elif score <= 5:
                summary["medium"] += 1
            elif score <= 10:
                summary["high"] += 1
            else:
                summary["critical"] += 1

        return summary

    def export_json(self, path="results/attack_report.json"):

        report = self.generate_summary()

        with open(path, "w") as f:
            json.dump(report, f, indent=2)

        return path
