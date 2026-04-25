"""Compute IDS metrics and print a summary report.

This script reads the persisted alerts file and presents a breakdown of
counts by type, severity, ECU, and rule to aid in detection validation.
"""

from src.ids.metrics import IDSMetrics

if __name__ == "__main__":
    metrics = IDSMetrics()
    metrics.summary()
