
"""
scenario plc0
"""

from minicps.devices import PLC
from utils import PLC0_DATA, STATE, PLC0_PROTOCOL
from utils import PLC_PERIOD_SEC
from utils import SUBNET_1

import time

PLC0_ADDR = SUBNET_1['plc0']

# Motorized Valve Tag
MV001 = ('MV001', 0)


class ScenarioPLC0(PLC):

    def pre_loop(self, sleep=0.1):
        print('[DEBUG] PLC0 - Enters pre loop\n')

        time.sleep(sleep)

    def main_loop(self):
        """plc2 main loop.

            - reads the valve value from the network 
            - opens or closes the valve
        """

        print('[DEBUG] PLC0 - Enters main loop\n')

        while True:
            try:
                mv001 = int(self.receive(MV001, PLC0_ADDR))
            except:
                mv001 = 0

            if mv001 != 0:      # receives 0 when error
                self.set(MV001, mv001)
                if mv001 == 1:
                    print("[DEBUG] PLC0 - Open valve")
                if mv001 == 2:
                    print("[DEBUG] PLC0 - Close valve")

            time.sleep(PLC_PERIOD_SEC)


if __name__ == "__main__":

    # notice that memory init is different form disk init
    plc0 = ScenarioPLC0(
        name='plc0',
        state=STATE,
        protocol=PLC0_PROTOCOL,
        memory=PLC0_DATA,
        disk=PLC0_DATA)
