"""CAN intrusion detection engine implementation.

This module monitors CAN traffic from a virtual bus, applies anomaly
and rule-based detection, logs alerts, and manages blocking and attack
correlation state.
"""

import time
import threading
import can
import json
import os

from src.ids.detection.alert import IDSAlert
from src.ids.detection.alert_types import AlertType, Severity
from src.ids.explainability.explanation import format_alert
from src.ids.intelligence.attack_correlator import AttackCorrelator


class CANIDS:
    def __init__(self, channel="vcan0"):

        self.bus = can.interface.Bus(channel=channel, bustype="socketcan")

        self.running = False
        self.thread = None

        # Detection thresholds
        self.rpm_max = 6000
        self.spike_threshold = 10000
        self.frequency_threshold = 50

        # State tracking
        self.message_count = {}
        self.last_reset_time = time.time()

        self.last_rpm = None
        self.last_timestamp = None

        # Alert cooldown
        self.last_alert_time = {}
        self.alert_cooldown = 1.0

        # BLOCKING STATE (NEW - STEP 4)
        self.blocked_ids = {}  # msg_id -> unblock_time
        self.block_duration = 3.0  # seconds

        # Alert storage
        self.alert_history = []

        self.log_file = "results/alerts.json"
        self.block_file = "results/blocked_events.json"
        os.makedirs("results", exist_ok=True)

        if not os.path.exists(self.log_file):
            with open(self.log_file, "w") as f:
                json.dump([], f)

        if not os.path.exists(self.block_file):
            with open(self.block_file, "w") as f:
                json.dump([], f)

        self.correlator = AttackCorrelator(time_threshold=5.0)
        self.attack_sessions_file = "results/attack_sessions.json"

        print("[IDS] Initialized")

    # ==============================
    # BLOCKING LOGIC (NEW)
    # ==============================
    def _is_blocked(self, msg_id):
        now = time.time()

        if msg_id in self.blocked_ids:
            if now < self.blocked_ids[msg_id]:
                return True
            else:
                del self.blocked_ids[msg_id]

        return False

    def _block_message(self, msg_id, reason):
        unblock_time = time.time() + self.block_duration
        self.blocked_ids[msg_id] = unblock_time

        event = {
            "timestamp": time.time(),
            "msg_id": hex(msg_id),
            "reason": reason,
            "severity": "HIGH",
            "action": "BLOCKED"
        }

        try:
            with open(self.block_file, "r") as f:
                data = json.load(f)

            data.append(event)

            with open(self.block_file, "w") as f:
                json.dump(data, f, indent=2)

        except Exception as e:
            print(f"[BLOCK LOG ERROR] {e}")

        print(f"""
[🛑 IDS BLOCK]
Message ID : {hex(msg_id)}
Reason     : {reason}
Action     : BLOCKED
""")

    # ==============================
    # COOLDOWN
    # ==============================
    def _should_alert(self, alert_type, msg_id):
        key = f"{alert_type}_{msg_id}"
        now = time.time()

        if key in self.last_alert_time:
            if now - self.last_alert_time[key] < self.alert_cooldown:
                return False

        self.last_alert_time[key] = now
        return True

    # ==============================
    # MAIN PROCESSOR
    # ==============================
    def process_message(self, message):

        try:
            msg_id = message.arbitration_id
            data = message.data
        except Exception as e:
            print(f"[IDS] Invalid CAN message: {e}")
            return

        # ❗ BLOCK CHECK (NEW STEP 4)
        if self._is_blocked(msg_id):
            return

        self.message_count[msg_id] = self.message_count.get(msg_id, 0) + 1

        if msg_id == 0x100:

            if len(data) < 2:
                return

            rpm = int.from_bytes(data[0:2], byteorder="big")
            now = time.time()

            # HIGH RPM CHECK
            if rpm > self.rpm_max:

                if self._should_alert(AlertType.HIGH_RPM, msg_id):

                    alert = IDSAlert(
                        alert_type=AlertType.HIGH_RPM,
                        msg_id=msg_id,
                        ecu="EngineECU",
                        severity=Severity.HIGH,
                        reason=f"RPM exceeds threshold ({rpm})",
                        rule="RPM_RANGE_CHECK",
                        evidence={"rpm": rpm}
                    )

                    print(format_alert(alert))
                    self._log_alert(alert)
                    self.correlator.process_alert(alert)

            # SPIKE DETECTION (with safe timing)
            if self.last_rpm is not None and self.last_timestamp is not None:

                delta_rpm = abs(rpm - self.last_rpm)
                delta_time = now - self.last_timestamp

                if delta_time > 0.05:  # guard
                    rate = delta_rpm / delta_time

                    if rate > self.spike_threshold:

                        if self._should_alert(AlertType.RPM_SPIKE, msg_id):

                            alert = IDSAlert(
                                alert_type=AlertType.RPM_SPIKE,
                                msg_id=msg_id,
                                ecu="EngineECU",
                                severity=Severity.HIGH,
                                reason="Rapid RPM change detected",
                                rule="RPM_SPIKE_DETECTION",
                                evidence={"rate": int(rate)}
                            )

                            print(format_alert(alert))
                            self._log_alert(alert)
                            self.correlator.process_alert(alert)

                            # 🚨 STEP 4: TRIGGER BLOCK ON CONFIRMED PATTERN
                            if rate > self.spike_threshold * 3:
                                self._block_message(msg_id, "Confirmed RPM spoofing attack")

            self.last_rpm = rpm
            self.last_timestamp = now

        self._check_frequency()

    # ==============================
    # FREQUENCY CHECK
    # ==============================
    def _check_frequency(self):

        current_time = time.time()

        if current_time - self.last_reset_time < 1:
            return

        for mid, count in self.message_count.items():

            if count > self.frequency_threshold:

                if self._should_alert(AlertType.FREQ_ANOMALY, mid):

                    alert = IDSAlert(
                        alert_type=AlertType.FREQ_ANOMALY,
                        msg_id=mid,
                        ecu="GatewayECU",
                        severity=Severity.MEDIUM,
                        reason="High message frequency",
                        rule="FREQUENCY_THRESHOLD_CHECK",
                        evidence={"count": count}
                    )

                    print(format_alert(alert))
                    self._log_alert(alert)
                    self.correlator.process_alert(alert)

        self.message_count = {}
        self.last_reset_time = current_time

    # ==============================
    # LOGGING
    # ==============================
    def _log_alert(self, alert):

        self.alert_history.append(alert.to_dict())

        try:
            with open(self.log_file, "r") as f:
                data = json.load(f)

            data.append(alert.to_dict())

            with open(self.log_file, "w") as f:
                json.dump(data, f, indent=2)

        except Exception as e:
            print(f"[IDS LOG ERROR] {e}")

    # ==============================
    # START
    # ==============================
    def start(self):

        if self.running:
            return

        print("[IDS] Monitoring started")
        self.running = True

        def loop():
            while self.running:
                try:
                    msg = self.bus.recv(timeout=1)
                    if msg:
                        self.process_message(msg)
                except Exception as e:
                    print(f"[IDS] Error: {e}")

        self.thread = threading.Thread(target=loop, daemon=True)
        self.thread.start()

    # ==============================
    # STOP
    # ==============================
    def stop(self):

        print("[IDS] Stopping...")
        self.running = False

        if self.thread:
            self.thread.join(timeout=2)

        try:
            self.bus.shutdown()
        except Exception:
            pass

        try:
            sessions = self.correlator.finalize_all()

            with open(self.attack_sessions_file, "w") as f:
                json.dump([s.to_dict() for s in sessions], f, indent=2)

            print(f"[AttackCorrelator] Saved {len(sessions)} attack sessions")

        except Exception as e:
            print(f"[AttackCorrelator ERROR] {e}")

        print("[IDS] Stopped")
