"""CAN protocol helpers and canonical message abstractions.

This module defines standard message types and the canonical wrapper used by
the ECU simulation and IDS components.
"""

import can


class MsgType:
    ENGINE_RPM = "ENGINE_RPM"
    BRAKE_PRESSURE = "BRAKE_PRESSURE"

    ATTACK_RPM_SPOOF = "ATTACK_RPM_SPOOF"
    ATTACK_BUS_FLOOD = "ATTACK_BUS_FLOOD"

    UNKNOWN = "UNKNOWN"


class CANMessage:
    """
    Canonical CAN message wrapper
    """

    def __init__(self, arbitration_id, data, source=None, msg_type=None):
        self.arbitration_id = arbitration_id
        self.data = data
        self.source = source
        self.msg_type = msg_type

    # =========================================================
    # ENCODE → real CAN frame
    # =========================================================
    def encode(self):
        return can.Message(
            arbitration_id=self.arbitration_id,
            data=self.data,
            is_extended_id=False
        )

    # =========================================================
    # DECODE ← real CAN frame (FIXED)
    # =========================================================
    @staticmethod
    def decode(message):
        return {
            "arbitration_id": message.arbitration_id,
            "data": message.data
        }

    # =========================================================
    # RPM DECODER (REQUIRED BY IDS)
    # =========================================================
    @staticmethod
    def decode_rpm(data):
        """
        Assumes RPM encoded in first 2 bytes (big endian)
        """
        try:
            if len(data) < 2:
                return None

            rpm = (data[0] << 8) | data[1]
            return rpm
        except Exception:
            return None

    # =========================================================
    # OPTIONAL SPOOF CHECK (placeholder for later)
    # =========================================================
    @staticmethod
    def is_rpm_spoof(data):
        """
        Placeholder logic — will improve later
        """
        rpm = CANMessage.decode_rpm(data)
        if rpm is None:
            return False

        # unrealistic threshold
        return rpm > 7000

    def __repr__(self):
        return (
            f"CANMessage("
            f"id=0x{self.arbitration_id:X}, "
            f"data={list(self.data)}, "
            f"source={self.source}, "
            f"type={self.msg_type}"
            f")"
        )
