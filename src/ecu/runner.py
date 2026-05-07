"""
Launch the full CAN ECU simulation with IDS and attack injection.

This runner starts all ECUs, IDS, and attack simulation, and ensures
clean, idempotent shutdown on Ctrl+C.
"""

from src.ecu.engine_ecu import EngineECU
from src.ecu.brake_ecu import BrakeECU
from src.ecu.gateway_ecu import GatewayECU
from src.attacks.attack_ecu import AttackECU
from src.ids.core.can_ids import CANIDS
import time


def main():
    # -----------------------------
    # Instantiate components
    # -----------------------------
    engine_ecu = EngineECU()
    brake_ecu = BrakeECU()
    gateway_ecu = GatewayECU()
    attack_ecu = AttackECU()
    ids = CANIDS()

    # -----------------------------
    # Inject IDS into ECUs
    # -----------------------------
    engine_ecu.ids = ids
    brake_ecu.ids = ids
    gateway_ecu.ids = ids

    # -----------------------------
    # Track shutdown state (FIX)
    # -----------------------------
    shutdown_initiated = False

    def shutdown():
        nonlocal shutdown_initiated

        if shutdown_initiated:
            return  # prevents double stop
        shutdown_initiated = True

        print("\n[SYSTEM] Stopping ECUs...")

        # Stop attack first (important)
        attack_ecu.stop()
        ids.stop()

        engine_ecu.stop()
        brake_ecu.stop()
        gateway_ecu.stop()

        # Join threads safely
        engine_ecu.join()
        brake_ecu.join()
        gateway_ecu.join()

        print("[SYSTEM] Shutdown complete.")

    # -----------------------------
    # Start system
    # -----------------------------
    engine_ecu.start()
    brake_ecu.start()
    gateway_ecu.start()
    ids.start()
    attack_ecu.start()

    print("[SYSTEM] ECU simulation running. Press Ctrl+C to stop.")

    try:
        while True:
            time.sleep(1)

    except KeyboardInterrupt:
        shutdown()

    finally:
        # Safety net in case of unexpected exit
        shutdown()


if __name__ == "__main__":
    main()
