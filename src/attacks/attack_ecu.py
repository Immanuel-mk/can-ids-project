"""Simulate an attacking ECU that injects spoofed CAN frames.

AttackECU creates protocol-compliant messages that represent spoofed engine
RPM traffic for IDS and gateway validation in the CAN simulation.
"""

import can
import random
import time
from src.ecu.base_ecu import BaseECU

# NEW: canonical protocol import
from src.protocol.can_protocol import CANMessage, MsgType


class AttackECU(BaseECU):
    """
    Attack ECU (Protocol-enabled adversary simulation)

    PURPOSE:
    - Inject malicious CAN traffic
    - Be explicitly identifiable at simulation level
    - Still appear as normal CAN frames on bus
    """

    def __init__(self):
        super().__init__(name="AttackECU")

    def send_messages(self):

        # Simulate attack timing (not constant flooding)
        time.sleep(random.uniform(0.2, 0.6))

        # -----------------------------
        # SPOOFED RPM ATTACK
        # -----------------------------
        spoofed_rpm = random.choice([0xFFFF, 9500, 12000])

        rpm_high = (spoofed_rpm >> 8) & 0xFF
        rpm_low = spoofed_rpm & 0xFF

        data = [
            rpm_high,
            rpm_low,
            120,  # fake temperature
            0, 0, 0, 0, 0
        ]

        # -----------------------------
        # CANONICAL ATTACK MESSAGE
        # -----------------------------
        msg = CANMessage(
            arbitration_id=0x100,  # same ID as EngineECU (spoofing)
            data=data,
            source="AttackECU",
            msg_type=MsgType.ATTACK_RPM_SPOOF
        )

        try:
            self.bus.send(msg.encode())

        except (OSError, can.CanError):
            return

        print("[AttackECU] SPOOF: Fake Engine RPM sent")

    def stop(self):
        print("[AttackECU] Stopping...")
        super().stop()
        print("[AttackECU] Stopped")

