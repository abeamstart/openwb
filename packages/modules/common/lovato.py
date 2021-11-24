#!/usr/bin/env python3

from typing import List, Tuple

try:
    from ..common import modbus
    from ..common.modbus import ModbusDataType
    from ..common.fault_state import FaultState, FaultStateLevel
except (ImportError, ValueError, SystemError):
    # for 1.9 compatibility
    from modules.common import modbus
    from modules.common.modbus import ModbusDataType
    from modules.common.fault_state import FaultState, FaultStateLevel


class Lovato:
    def __init__(self, modbus_id: int, client: modbus.ModbusClient) -> None:
        self.client = client
        self.id = modbus_id

    def __process_error(self, e):
        if isinstance(e, FaultState):
            raise
        else:
            raise FaultState(__name__+" "+str(type(e))+" "+str(e), FaultStateLevel.ERROR) from e

    def get_voltage(self) -> List[float]:
        try:
            return [val / 100 for val in self.client.read_input_registers(
                0x0001, [ModbusDataType.FLOAT_32]*3, unit=self.id)]
        except Exception as e:
            self.__process_error(e)

    def get_imported(self) -> float:
        try:
            return self.client.read_input_registers(0x0048, ModbusDataType.FLOAT_32, unit=self.id) * 1000
        except Exception as e:
            self.__process_error(e)

    def get_power(self) -> Tuple[List[float], float]:
        try:
            power_per_phase = [val / 100 for val in self.client.read_input_registers(
                0x0013, [ModbusDataType.FLOAT_32]*3, unit=self.id
            )]
            power_all = self.client.read_input_registers(0x000C, ModbusDataType.FLOAT_32, unit=self.id)
            return power_per_phase, power_all
        except Exception as e:
            self.__process_error(e)

    def get_exported(self) -> float:
        try:
            return self.client.read_input_registers(0x004a, ModbusDataType.FLOAT_32, unit=self.id) * 1000
        except Exception as e:
            self.__process_error(e)

    def get_power_factor(self) -> List[float]:
        try:
            return [val / 10000 for val in self.client.read_input_registers(
                0x0025, [ModbusDataType.FLOAT_32]*3, unit=self.id)]
        except Exception as e:
            self.__process_error(e)

    def get_frequency(self) -> float:
        try:
            frequency = self.client.read_input_registers(0x0031, ModbusDataType.FLOAT_32, unit=self.id) / 100
            if frequency > 100:
                frequency = frequency / 10
            return frequency
        except Exception as e:
            self.__process_error(e)

    def get_current(self) -> List[float]:
        try:
            return [val / 10000 for val in self.client.read_input_registers(
                0x0007, [ModbusDataType.FLOAT_32]*3, unit=self.id)]
        except Exception as e:
            self.__process_error(e)

    def get_counter(self) -> float:
        try:
            finalbezug1 = self.client.read_input_registers(0x1a1f, ModbusDataType.FLOAT_32, unit=self.id)
            finalbezug2 = self.client.read_input_registers(0x1a21, ModbusDataType.FLOAT_32, unit=self.id)
            return max(finalbezug1, finalbezug2)
        except Exception as e:
            self.__process_error(e)
