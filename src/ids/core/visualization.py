"""Graph IDS alert data for visualization and reporting.

This module generates charts that show alert trends, severity, and ECU
coverage from the stored IDS alert log.
"""

import json
import os
from collections import Counter, defaultdict
import matplotlib.pyplot as plt


class IDSVisualizer:

    def __init__(self, log_file="results/alerts.json"):
        self.log_file = log_file
        self.alerts = self._load_alerts()

        os.makedirs("results/graphs", exist_ok=True)

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
    # 1. Alerts over time
    # -----------------------------
    def plot_timeline(self):

        timeline = defaultdict(int)

        for alert in self.alerts:
            t = int(alert["timestamp"])
            timeline[t] += 1

        x = sorted(timeline.keys())
        y = [timeline[i] for i in x]

        plt.figure()
        plt.plot(x, y, marker="o")
        plt.title("IDS Alerts Over Time")
        plt.xlabel("Time (s)")
        plt.ylabel("Number of Alerts")
        plt.tight_layout()
        plt.savefig("results/graphs/timeline.png")
        plt.close()

    # -----------------------------
    # 2. Alert type distribution
    # -----------------------------
    def plot_alert_types(self):

        counts = Counter(a["alert_type"] for a in self.alerts)

        plt.figure()
        plt.bar(counts.keys(), counts.values())
        plt.title("Alert Type Distribution")
        plt.xlabel("Alert Type")
        plt.ylabel("Count")
        plt.xticks(rotation=30)
        plt.tight_layout()
        plt.savefig("results/graphs/alert_types.png")
        plt.close()

    # -----------------------------
    # 3. Severity distribution
    # -----------------------------
    def plot_severity(self):

        counts = Counter(a["severity"] for a in self.alerts)

        plt.figure()
        plt.bar(counts.keys(), counts.values())
        plt.title("Alert Severity Distribution")
        plt.xlabel("Severity")
        plt.ylabel("Count")
        plt.tight_layout()
        plt.savefig("results/graphs/severity.png")
        plt.close()

    # -----------------------------
    # 4. ECU targeting analysis
    # -----------------------------
    def plot_ecu_distribution(self):

        counts = Counter(a["ecu"] for a in self.alerts)

        plt.figure()
        plt.bar(counts.keys(), counts.values())
        plt.title("ECU Targeting Distribution")
        plt.xlabel("ECU")
        plt.ylabel("Alerts")
        plt.tight_layout()
        plt.savefig("results/graphs/ecu_distribution.png")
        plt.close()

    # -----------------------------
    # Run all plots
    # -----------------------------
    def generate_all(self):

        if not self.alerts:
            print("[VISUALIZER] No alerts found.")
            return

        self.plot_timeline()
        self.plot_alert_types()
        self.plot_severity()
        self.plot_ecu_distribution()

        print("[VISUALIZER] Graphs saved to results/graphs/")
