# CAN Bus Intrusion Detection System (CAN IDS)

A Python-based automotive cybersecurity project that simulates Controller Area Network (CAN) communication between Electronic Control Units (ECUs) and detects malicious activity using anomaly detection, attack correlation, explainability, and response mechanisms.

## Project Overview

Modern vehicles rely heavily on CAN bus communication for coordination between critical ECUs such as engine control, braking systems, and gateway modules. While efficient, CAN lacks native security controls, making it vulnerable to spoofing, replay, injection, and coordinated cyberattacks.

This project implements a simulated automotive CAN environment with an intelligent Intrusion Detection System capable of:

- Monitoring real-time ECU traffic
- Detecting RPM spike anomalies
- Identifying suspicious message frequency patterns
- Correlating attack campaigns across multiple events
- Generating alerts with explainable reasoning
- Triggering defensive response mechanisms

The system is designed to demonstrate practical automotive IDS concepts used in modern vehicular cybersecurity research.
