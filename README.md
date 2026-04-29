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

## System Architecture

The simulated automotive environment consists of multiple Electronic Control Units (ECUs) communicating over a virtual CAN bus.

### Core Components

### Engine ECU
Simulates engine telemetry including RPM and temperature values.

### Brake ECU
Simulates braking pressure and braking-state messages.

### Gateway ECU
Acts as the routing and communication coordination layer between simulated subsystems.

### Attack ECU
Injects malicious CAN traffic to simulate cyberattack scenarios such as spoofing and anomalous signal manipulation.

### CAN IDS Core
Monitors all bus traffic and performs anomaly detection.

### Detection Engine
Identifies:

- RPM spikes
- Frequency anomalies
- Message irregularities
- Coordinated suspicious event sequences

### Attack Intelligence Layer
Provides:

- Attack correlation
- Campaign tracking
- Phase detection
- Session analysis

### Explainability Engine
Generates interpretable reasoning for every detected anomaly.

### Defensive Response Layer
Handles:

- Alert generation
- Event logging
- Blocking malicious activity

## Detection Capabilities

The IDS analyzes CAN traffic for malicious patterns using multiple detection strategies.

### RPM Spike Detection
Detects sudden abnormal increases or decreases in engine RPM that indicate spoofed engine telemetry.

### Frequency-Based Anomaly Detection
Monitors CAN message transmission frequency to identify:

- Flooding attacks
- Message injection attempts
- Timing irregularities

### Attack Correlation
Correlates multiple suspicious events into larger attack campaigns.

This enables detection of:

- Multi-stage attacks
- Coordinated spoofing behavior
- Escalating attack sequences

### Session Tracking
Groups related anomalies into attack sessions for forensic analysis.

### Explainable Alerts
Every alert includes reasoning describing:

- Trigger condition
- Detection logic
- Severity classification
- Recommended interpretation

## How to Run the System

### Step 1: Setup Virtual CAN Interface

Initialize the simulated CAN bus environment:

```bash
bash scripts/start_vcan.sh

To stop the virtual CAN interface:

bash scripts/stop_vcan.sh


## Step 2: Install Dependencies

### Install required Python packages:

    pip install -r scripts/requirements.txt


## Step 3: Start the CAN Simulation

### Run the ECU simulation and IDS monitoring system:

    python src/ecu/runner.py

## Step 4: Launch Attack Simulation

### Start malicious CAN traffic injection:
    python src/attacks/attack_ecu.py

## Step 5: Analyze IDS Output

### Generate and review system results:
    python scripts/generate_graphs.py
    python scripts/analyze_alerts.py

## Output Artifacts

### After execution, the system generates:

    results/alerts.json → detected intrusion events
    results/attack_sessions.json → correlated attack campaigns
    results/graphs/ → visualization of system behavior
    
## Attack Scenarios

The system simulates multiple CAN bus attack vectors to evaluate IDS effectiveness under realistic automotive threat conditions.

### 1. RPM Spoofing Attack
The Attack ECU injects falsified engine RPM values to simulate signal spoofing.

- Target: Engine ECU
- Effect: False engine state representation
- Detection: Spike anomaly detection in RPM signal

---

### 2. Brake Pressure Manipulation
Malicious messages modify brake pressure readings to simulate unsafe braking conditions.

- Target: Brake ECU
- Effect: Incorrect braking system state
- Detection: Frequency + value deviation analysis

---

### 3. CAN Bus Flooding
High-frequency message injection overwhelms the CAN network.

- Target: Entire CAN bus
- Effect: Message congestion and denial-of-service behavior
- Detection: Frequency threshold violation

---

### 4. Coordinated Multi-Stage Attack
Sequential injection of multiple anomalies across ECUs to simulate advanced persistent attack behavior.

- Stage 1: Reconnaissance traffic injection
- Stage 2: Signal spoofing (RPM / Brake)
- Stage 3: Persistent flooding
- Detection: Attack correlation engine + session tracking
