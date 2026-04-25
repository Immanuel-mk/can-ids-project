"""Visualize attack sessions and campaign intelligence.

This module generates charts showing attack timelines, campaign sizes, and
severity evolution across detected attacks.
"""

import matplotlib.pyplot as plt


class AttackVisualizer:

    def __init__(self, sessions, campaigns):
        self.sessions = sessions
        self.campaigns = campaigns

    # =========================================================
    # 1. SESSION TIMELINE
    # =========================================================
    def plot_session_timeline(self, save_path="results/graphs/session_timeline.png"):

        plt.figure()

        for i, session in enumerate(self.sessions):

            plt.plot(
                [session.start_time, session.end_time],
                [i, i],
                linewidth=4
            )

        plt.title("Attack Session Timeline")
        plt.xlabel("Time")
        plt.ylabel("Session Index")

        plt.savefig(save_path)
        plt.close()

    # =========================================================
    # 2. CAMPAIGN SIZE DISTRIBUTION
    # =========================================================
    def plot_campaign_sizes(self, save_path="results/graphs/campaign_sizes.png"):

        sizes = [len(c.sessions) for c in self.campaigns]

        plt.figure()
        plt.bar(range(len(sizes)), sizes)

        plt.title("Attack Campaign Sizes")
        plt.xlabel("Campaign ID")
        plt.ylabel("Number of Sessions")

        plt.savefig(save_path)
        plt.close()

    # =========================================================
    # 3. SEVERITY EVOLUTION
    # =========================================================
    def plot_severity_over_time(self, save_path="results/graphs/severity_evolution.png"):

        severities = [s.severity_score for s in self.sessions]

        plt.figure()
        plt.plot(severities, marker="o")

        plt.title("Attack Severity Evolution")
        plt.xlabel("Session Index")
        plt.ylabel("Severity Score")

        plt.savefig(save_path)
        plt.close()

    # =========================================================
    # RUN ALL
    # =========================================================
    def generate_all(self):

        self.plot_session_timeline()
        self.plot_campaign_sizes()
        self.plot_severity_over_time()

        print("[Visualizer] Attack intelligence graphs generated.")
