"""Shared ECU thread base class with safe CAN send and receive behavior.

All ECU implementations inherit from BaseECU to standardize CAN interfacing,
thread lifecycle management, and exception handling.
"""

import can
import threading
import time
import traceback


class BaseECU(threading.Thread):
    """
    Base class for all ECUs.

    FIXES INCLUDED:
    1. Prevent ECU crash from application-level exceptions (e.g., MsgType issues)
    2. Standardized CAN send wrapper for canonical messages
    3. Stronger shutdown safety (no partial states)
    4. Better logging for debugging ECU failures
    """

    def __init__(self, channel='vcan0', bitrate=500000, name="BaseECU"):
        super().__init__(daemon=True)

        self.name = name

        # -----------------------------
        # CAN BUS
        # -----------------------------
        self.bus = can.interface.Bus(
            channel=channel,
            bustype='socketcan'
        )

        self.running = False
        self._lock = threading.Lock()

    # =========================================================
    # THREAD ENTRY POINT
    # =========================================================
    def run(self):

        self.running = True
        print(f"[{self.name}] Started")

        while True:
            try:
                with self._lock:
                    if not self.running:
                        break

                # -----------------------------
                # SAFE ECU EXECUTION LAYER
                # -----------------------------
                try:
                    self.send_messages()
                    self.receive_messages()

                except Exception as e:
                    # FIX 1: DO NOT kill ECU thread on logical errors
                    print(f"[{self.name}] Internal ECU error: {e}")
                    traceback.print_exc()

                time.sleep(0.1)

            except OSError:
                break

            except Exception as e:
                print(f"[{self.name}] Fatal loop error: {e}")
                break

        print(f"[{self.name}] Exiting loop")

    # =========================================================
    # CAN SEND WRAPPER (NEW SAFETY LAYER)
    # =========================================================
    def send_can(self, can_message):
        """
        Unified safe sender for CANMessage objects.
        Prevents invalid MsgType or encoding crashes from breaking ECUs.
        """

        try:
            msg = can_message.encode()
            self.bus.send(msg)

        except Exception as e:
            print(f"[{self.name}] CAN send error: {e}")

    # =========================================================
    # TO BE IMPLEMENTED BY CHILD CLASSES
    # =========================================================
    def send_messages(self):
        pass

    # =========================================================
    # RECEIVE LOOP (UNCHANGED BUT SAFER)
    # =========================================================
    def receive_messages(self):

        if not self.running:
            return

        try:
            message = self.bus.recv(timeout=0.01)

            if message:
                self.on_message_received(message)

        except (OSError, AttributeError):
            return

        except Exception:
            return

    def on_message_received(self, message):
        pass

    # =========================================================
    # CLEAN SHUTDOWN
    # =========================================================
    def stop(self):

        print(f"[{self.name}] Stopping...")

        with self._lock:
            self.running = False

        if self.is_alive():
            self.join(timeout=2.0)

        if hasattr(self, "bus") and self.bus:
            try:
                self.bus.shutdown()
            except Exception:
                pass

        print(f"[{self.name}] Stopped")
