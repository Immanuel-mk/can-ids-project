#!/bin/bash

set -e

echo "[RUN] Starting CAN IDS Simulation..."

# Ensure vcan0 exists
if ! ip link show vcan0 >/dev/null 2>&1; then
    echo "[RUN] vcan0 not found. Setting up..."
    bash setup_vcan.sh
fi

echo "[RUN] Launching system..."
python -m src.ecu.runner
