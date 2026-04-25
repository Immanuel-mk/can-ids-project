"""Brake ECU simulation for pressure and engine RPM reaction behavior.

BrakeECU emits brake pressure frames and optionally processes engine RPM
messages for reactive behavior without performing IDS logic itself.
"""

import can
import random
from src.ecu.base_ecu import BaseECU
from src.protocol.can_protocol import CANMessage, MsgType


class BrakeECU(BaseECU):
    """
    Brake ECU (clean separation version)

    - Sends brake pressure signals
    - Reacts to engine RPM
    - Does NOT perform IDS logic (IDS is authority)
    """

    def __init__(self):
        super().__init__(name="BrakeECU")
        self.brake_pressure = 0

    # -----------------------------
    # PERIODIC MESSAGE SENDER
    # -----------------------------
    def send_messages(self):

        if not self.running:
            return

        self.brake_pressure = random.randint(0, 100)

        data = [self.brake_pressure] + [0] * 7

        try:
            # Canonical CAN message wrapper (consistent with system design)
            msg = CANMessage(
                arbitration_id=0x200,
                data=data,
                source="BrakeECU",
                msg_type=MsgType.BRAKE_PRESSURE
            )

            # Send actual CAN frame
            self.bus.send(msg.encode())

        except (OSError, can.CanError):
            return

        print(f"[BrakeECU] Pressure={self.brake_pressure}")

    # -----------------------------
    # MESSAGE HANDLER
    # -----------------------------
    def on_message_received(self, message):

        # Optional IDS hook (safe guard)
        if hasattr(self, "ids") and self.ids:
            if not self.ids.is_valid_message(message):
                print("[BrakeECU] Ignoring invalid CAN frame (IDS filtered)")
                return

        # Only process engine RPM frames
        if message.arbitration_id != 0x100:
            return

        if len(message.data) < 2:
            return

        rpm = (message.data[0] << 8) | message.data[1]

        # Brake response logic (domain behavior only)
        if rpm > 3000:
            print("[BrakeECU] High RPM detected → braking adjustment needed")

    # -----------------------------
    # CLEAN SHUTDOWN
    # -----------------------------
    def stop(self):

        if not self.running:
            return

        print("[BrakeECU] Stopping...")

        self.running = False

        super().stop()

        print("[BrakeECU] Stopped")
