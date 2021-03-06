from typing import Dict

from helpermodules.log import MainLogger
from modules.common.abstract_chargepoint import AbstractChargepoint
from modules.common.component_context import SingleComponentUpdateContext
from modules.common.fault_state import ComponentInfo


def get_default_config() -> Dict:
    return {"id": 0,
            "connection_module": {
                "type": "mqtt",
                "configuration":
                {}
            },
            "power_module": {}}


class ChargepointModule(AbstractChargepoint):
    def __init__(self, id: int, connection_module: dict, power_module: dict) -> None:
        self.id = id
        self.connection_module = connection_module
        self.power_module = power_module
        self.component_info = ComponentInfo(
            self.id,
            "Ladepunkt", "chargepoint")

    def set_current(self, current: float) -> None:
        with SingleComponentUpdateContext(self.component_info):
            MainLogger().debug("MQTT-Ladepunkte subscriben die Daten direkt vom Broker.")

    def get_values(self) -> None:
        with SingleComponentUpdateContext(self.component_info):
            MainLogger().debug("MQTT-Ladepunkte müssen nicht ausgelesen werden.")

    def switch_phases(self, phases_to_use: int, duration: int) -> None:
        MainLogger().warning("Phasenumschaltung für MQTT-Ladepunkte nicht unterstuezt.")
