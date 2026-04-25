"""Launch the full CAN ECU simulation with IDS and attack injection.

This runner starts the engine, brake, gateway, and attack ECUs together with
the IDS and coordinates clean shutdown on user interrupt.
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
    # Inject IDS into ECUs (FIXED)
    # -----------------------------
    engine_ecu.ids = ids
    brake_ecu.ids = ids
    gateway_ecu.ids = ids

    # -----------------------------
    # Start all components
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
        print("\n[SYSTEM] Stopping ECUs...")

        # -----------------------------
        # STOP ORDER MATTERS
        # -----------------------------
        attack_ecu.stop()
        ids.stop()

        engine_ecu.stop()
        brake_ecu.stop()
        gateway_ecu.stop()

        # -----------------------------
        # JOIN THREADS
        # -----------------------------
        engine_ecu.join()
        brake_ecu.join()
        gateway_ecu.join()

        print("[SYSTEM] Shutdown complete.")


if __name__ == "__main__":
    main()

