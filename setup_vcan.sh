#!/bin/bash

set -e

echo "[SETUP] Loading vcan module..."
sudo modprobe vcan

echo "[SETUP] Creating vcan0 interface..."
sudo ip link add dev vcan0 type vcan 2>/dev/null || true

echo "[SETUP] Bringing vcan0 up..."
sudo ip link set up vcan0

echo "[SETUP] Verifying interface..."
ip link show vcan0

echo "[SUCCESS] vcan0 is ready."
