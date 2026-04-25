"""Utility helpers for interacting with the virtual CAN interface.

This module centralizes the virtual CAN bus creation and example send/receive
flows used by the simulation environment.
"""

# Import the python-can library
# This library provides an interface to interact with CAN buses in Python
import can


def get_bus():
    """
    Create and return a CAN bus interface.

    - channel='vcan0' → This is our virtual CAN interface created earlier
    - bustype='socketcan' → Linux CAN backend (required for vcan)

    Returns:
        bus (can.Bus): A CAN bus object used to send/receive messages
    """
    return can.interface.Bus(channel='vcan0', interface='socketcan')   
    
def send_test():
    """
    Send a test CAN message and properly close the bus.
    """
    bus = get_bus()

    msg = can.Message(
        arbitration_id=0x123,
        data=[1, 2, 3, 4],
        is_extended_id=False
    )

    try:
        bus.send(msg)
        print("✅ Message sent from Python")

    except can.CanError:
        print("❌ Message failed to send")

    finally:
        # Properly close the CAN interface
        bus.shutdown()


def receive():
    """
    Listen for CAN messages and close cleanly on exit.
    """
    bus = get_bus()

    print("👂 Listening for CAN messages... Press Ctrl+C to stop.\n")

    try:
        for msg in bus:
            print(f"Received: {msg}")

    except KeyboardInterrupt:
        print("\n🛑 Stopped listening.")

    finally:
        bus.shutdown()

if __name__ == "__main__":
    send_test()
