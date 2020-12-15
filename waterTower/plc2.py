
"""
scenario plc2
"""

from minicps.devices import PLC
from utils import PLC2_DATA, STATE, PLC2_PROTOCOL
from utils import PLC_PERIOD_SEC
from utils import IP

import time

PLC2_ADDR = IP['plc2']

# Pump Tag
P201 = ('P201', 2)

class ScenarioPLC2(PLC):

    def pre_loop(self, sleep=0.1):
        print('[DEBUG] PLC2 - Enters pre loop\n')

        time.sleep(sleep)

    def main_loop(self):
        """plc2 main loop.

            - read engine value from the network 
            - opens or closes the engine
        """

        print('[DEBUG] PLC2 - Enters main loop\n')

        while True:
            try:
                p201 = int(self.receive(P201, PLC2_ADDR))
            except:
                p201 = 0
            
            if p201 != 0:
                self.set(P201, p201)
                if p201 == 1:
                    print("[DEBUG] PLC2 - Open pump")
                if p201 == 2:
                    print("[DEBUG] PLC2 - Close pump")

            time.sleep(PLC_PERIOD_SEC)

if __name__ == "__main__":

    # notice that memory init is different form disk init
    plc2 = ScenarioPLC2(
        name='plc2',
        state=STATE,
        protocol=PLC2_PROTOCOL,
        memory=PLC2_DATA,
        disk=PLC2_DATA)
