"""Define IDS alert types and severity levels.

This module centralizes named constants for alert categories and severity
levels used across detection, logging, and reporting.
"""

# This has all the IDS alerts

class AlertType:
    RPM_SPOOF = "RPM_SPOOF"
    HIGH_RPM = "HIGH_RPM"
    RPM_SPIKE = "RPM_SPIKE"
    FREQ_ANOMALY = "FREQ_ANOMALY"
    BEHAVIOR_ANOMALY = "BEHAVIOR_ANOMALY"


class Severity:
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    CRITICAL = "CRITICAL"
