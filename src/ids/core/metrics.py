"""Compute summary metrics for IDS alert data.

This module provides lightweight analytics for persisted alerts, such as
counts by type, severity, ECU, and rule, plus a console summary.
"""

import json
from collections import Counter, defaultdict


class IDSMetrics:

    def __init__(self, log_file="results/alerts.json"):
        self.log_file = log_file
        self.alerts = self._load_alerts()

    # -----------------------------
    # Load alerts
    # -----------------------------
    def _load_alerts(self):
        try:
            with open(self.log_file, "r") as f:
                return json.load(f)
        except Exception:
            return []

    # -----------------------------
    # Total alerts
    # -----------------------------
    def total_alerts(self):
        return len(self.alerts)

    # -----------------------------
    # Alerts by type
    # -----------------------------
    def alerts_by_type(self):
        return Counter(alert["alert_type"] for alert in self.alerts)

    # -----------------------------
    # Alerts by severity
    # -----------------------------
    def alerts_by_severity(self):
        return Counter(alert["severity"] for alert in self.alerts)

    # -----------------------------
    # Alerts by ECU
    # -----------------------------
    def alerts_by_ecu(self):
        return Counter(alert["ecu"] for alert in self.alerts)

    # -----------------------------
    # Rule effectiveness
    # -----------------------------
    def alerts_by_rule(self):
        return Counter(alert["rule"] for alert in self.alerts)

    # -----------------------------
    # Timeline (alerts per second)
    # -----------------------------
    def alerts_over_time(self):
        timeline = defaultdict(int)

        for alert in self.alerts:
            ts = int(alert["timestamp"])
            timeline[ts] += 1

        return dict(sorted(timeline.items()))

    # -----------------------------
    # Pretty summary
    # -----------------------------
    def summary(self):

        print("\n========== IDS METRICS ==========")

        print(f"\nTotal Alerts: {self.total_alerts()}")

        print("\nAlerts by Type:")
        for k, v in self.alerts_by_type().items():
            print(f"  {k}: {v}")

        print("\nAlerts by Severity:")
        for k, v in self.alerts_by_severity().items():
            print(f"  {k}: {v}")

        print("\nAlerts by ECU:")
        for k, v in self.alerts_by_ecu().items():
            print(f"  {k}: {v}")

        print("\nAlerts by Rule:")
        for k, v in self.alerts_by_rule().items():
            print(f"  {k}: {v}")

        print("\n================================\n")
