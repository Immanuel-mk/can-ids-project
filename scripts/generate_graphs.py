"""Generate IDS visualizations from saved alert logs.

This script loads alert history from the results directory and generates
a set of summary graphs for analysis and reporting.
"""

from src.ids.visualization import IDSVisualizer

if __name__ == "__main__":
    viz = IDSVisualizer()
    viz.generate_all()
