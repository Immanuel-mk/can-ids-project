"""Explain IDS alerts in human-readable and structured formats.

This module supports converting IDSAlert objects to console-friendly text,
JSON-compatible dictionaries, and higher-level explanations.
"""

from typing import Dict, Any
from src.ids.detection.alert import IDSAlert


def format_alert(alert: IDSAlert) -> str:
    """
    Converts an IDSAlert into a structured human-readable string.
    Used for logs, CLI output, and debugging.
    """

    return (
        f"\n[🚨 IDS ALERT]\n"
        f"Type      : {alert.alert_type}\n"
        f"ECU       : {alert.ecu}\n"
        f"Msg ID    : {hex(alert.msg_id)}\n"
        f"Severity  : {alert.severity}\n"
        f"Rule      : {alert.rule}\n"
        f"Reason    : {alert.reason}\n"
        f"Evidence  : {alert.evidence}\n"
        f"Timestamp : {alert.timestamp}\n"
    )


def format_alert_json(alert: IDSAlert) -> Dict[str, Any]:
    """
    Returns structured JSON-style output.
    Useful for logging, dashboards, or later ML analysis.
    """

    return alert.to_dict()


def explain_alert(alert: IDSAlert) -> str:
    """
    Higher-level explanation wrapper.
    You can extend this later for natural-language explanations.
    """

    explanation = f"""
The IDS detected a {alert.alert_type} event.

Why this matters:
- Rule triggered: {alert.rule}
- Severity level: {alert.severity}

What happened:
{alert.reason}

Supporting evidence:
{alert.evidence}
"""

    return explanation.strip()
