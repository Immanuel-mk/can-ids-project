"""Engine ECU simulation that emits periodic RPM and temperature frames.

EngineECU models mileage behavior and produces canonical CAN frames used
by the IDS and gateway for anomaly detection.
"""

import random
from src.ecu.base_ecu import BaseECU
from src.protocol.can_protocol import CANMessage, MsgType


class EngineECU(BaseECU):
    """
    Fixed Engine ECU

    FIXES:
    1. Uses BaseECU.send_can() (critical fix)
    2. Enforces strict integer casting
    3. Prevents invalid payload structures
    4. Removes any unsafe CAN encode paths
    """

    def __init__(self):
        super().__init__(name="EngineECU")

        self.rpm = 800
        self.temperature = 70.0

    def send_messages(self):

        # -----------------------------
        # ENGINE SIMULATION
        # -----------------------------
        self.rpm += random.randint(-40, 60)
        self.rpm = max(700, min(self.rpm, 5000))

        self.temperature += random.uniform(-0.3, 0.6)
        self.temperature = max(60, min(self.temperature, 120))

        # -----------------------------
        # STRICT CAN PAYLOAD (FIX)
        # -----------------------------
        rpm = int(self.rpm)
        temp = int(self.temperature)

        rpm_high = (rpm >> 8) & 0xFF
        rpm_low = rpm & 0xFF

        data = [
            int(rpm_high),
            int(rpm_low),
            temp,
            0, 0, 0, 0, 0
        ]

        # HARD VALIDATION (prevents invalid encode)
        if not isinstance(data, list) or len(data) != 8:
            print(f"[EngineECU] Invalid payload structure, skipping")
            return

        # -----------------------------
        # CAN MESSAGE
        # -----------------------------
        msg = CANMessage(
            arbitration_id=0x100,
            data=data,
            source="EngineECU",
            msg_type=MsgType.ENGINE_RPM
        )

        # -----------------------------
        # SAFE SEND PATH (CRITICAL FIX)
        # -----------------------------
        try:
            self.send_can(msg)

        except Exception as e:
            print(f"[EngineECU] Send failed: {e}")
            return

        print(f"[EngineECU] RPM={rpm} Temp={temp:.1f}")

    def stop(self):
        print("[EngineECU] Stopping...")
        super().stop()
        print("[EngineECU] Stopped")

