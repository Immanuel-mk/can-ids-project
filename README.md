# CAN Bus Intrusion Detection System (CAN IDS)

![Python](https://img.shields.io/badge/Python-3.11-blue)
![Status](https://img.shields.io/badge/Status-Simulation-orange)
![Domain](https://img.shields.io/badge/Cybersecurity-Automotive-red)

---

## Overview

This project is a **simulated automotive CAN bus intrusion detection system** designed to model, detect, and analyze cyberattacks targeting in-vehicle communication networks.

It integrates:
- ECU-level simulation (Engine, Brake, Gateway)
- Attack injection framework
- Real-time intrusion detection system (IDS)
- Attack correlation and session tracking
- Explainable security decision-making

The system is designed for **cybersecurity research, academic evaluation, and portfolio demonstration** in automotive security domains.

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

## Results Interpretation

The CAN IDS is evaluated based on its ability to detect, correlate, and explain malicious activity across simulated automotive network conditions.

### Detection Performance

The system successfully identifies:

- Sudden RPM anomalies caused by spoofing attacks
- Brake signal inconsistencies under manipulation
- Abnormal message frequency patterns during flooding attacks

### Correlation Capability

Individual suspicious events are aggregated into structured attack campaigns.

This enables the system to:

- Distinguish isolated anomalies from coordinated attacks
- Group related events into attack sessions
- Reconstruct multi-stage intrusion behavior

### Explainability Output

Each detected event includes a human-readable explanation:

- Why the event was flagged
- Which rule or detector triggered it
- Severity classification (low, medium, high)
- Associated ECU and signal source

### System Value

This project demonstrates how traditional automotive CAN systems can be extended with:

- Real-time intrusion detection
- Behavioral anomaly analysis
- Attack lifecycle reconstruction
- Interpretable security decision-making

The architecture is aligned with modern automotive cybersecurity research focusing on explainable and intelligent IDS systems.

## System Architecture Diagram

The system is designed around a modular architecture that separates vehicle simulation, intrusion detection, and attack intelligence layers.

### High-Level Flow

- ECUs generate CAN messages (Engine, Brake, Gateway)
- Attack ECU injects malicious traffic into the CAN bus
- IDS monitors all bus traffic in real-time
- Detection engine identifies anomalies and suspicious patterns
- Intelligence layer correlates events into attack campaigns
- Explainability module generates human-readable alerts
- Visualization module produces analytical graphs

### Planned Visualization

The architecture diagram represents:

- ECU communication flow over CAN bus
- Attack injection points
- IDS monitoring layer placement
- Data flow into detection and correlation engines
- Output pipeline (alerts, graphs, reports)


