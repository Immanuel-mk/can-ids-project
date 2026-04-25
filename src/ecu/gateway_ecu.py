"""Implement a CAN gateway ECU with replay protection and filtering.

GatewayECU relays approved messages through the bus while dropping self-
forwarded traffic and known spoofed attack frames.
"""

import can
import time
from src.ecu.base_ecu import BaseECU

from src.protocol.can_protocol import CANMessage, MsgType


class GatewayECU(BaseECU):
    """
    Gateway ECU (Secure + Loop-safe)

    FIXES:
    - Prevents self-forwarding (true loop elimination)
    - Deduplication cache (short-term replay protection)
    - Blocks malicious RPM spoof traffic (0xFFFF)
    """

    def __init__(self):
        super().__init__(name="GatewayECU")

        # -----------------------------
        # LOOP + REPLAY PREVENTION
        # -----------------------------
        self.forward_cache = {}
        self.cache_ttl = 0.2  # 200ms window

    def send_messages(self):
        pass

    def on_message_received(self, message):

        # -----------------------------
        # Decode into canonical form
        # -----------------------------
        decoded = CANMessage.decode(message)

        # -----------------------------
        # FIX 1: DROP self-forwarded frames
        # -----------------------------
        if decoded.source == "GatewayECU":
            return

        # -----------------------------
        # FIX 2: BLOCK malicious RPM spoof
        # -----------------------------
        if message.arbitration_id == 0x100:
            if CANValidator.is_rpm_spoof(message.data):
                print("[GatewayECU] BLOCKED spoofed RPM frame")
                return

        # -----------------------------
        # Signature for deduplication
        # -----------------------------
        signature = (
            message.arbitration_id,
            bytes(message.data)
        )

        now = time.time()

        # Clean cache
        self.forward_cache = {
            k: v for k, v in self.forward_cache.items()
            if now - v < self.cache_ttl
        }

        # Drop duplicates
        if signature in self.forward_cache:
            return

        self.forward_cache[signature] = now

        # -----------------------------
        # Wrap and forward
        # -----------------------------
        wrapped = CANMessage(
            arbitration_id=message.arbitration_id,
            data=list(message.data),
            source="GatewayECU",
            msg_type=MsgType.RAW_FORWARD
        )

        try:
            self.bus.send(wrapped.encode())
        except (OSError, can.CanError):
            return

        print(
            f"[GatewayECU] RELAY 0x{message.arbitration_id:X} "
            f"DATA={list(message.data)}"
        )

    def stop(self):
        print("[GatewayECU] Stopping...")
        super().stop()
        print("[GatewayECU] Stopped")

