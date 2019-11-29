
"""
swat-s1 plc0
"""

from minicps.devices import PLC
from utils import PLC0_DATA, STATE, PLC0_PROTOCOL
from utils import PLC_SAMPLES, PLC_PERIOD_SEC
from utils import IP

import time

PLC0_ADDR = IP['plc0']
PLC1_ADDR = IP['plc1']
PLC2_ADDR = IP['plc2']

# Motorized Valve
MV001 = ('MV001', 0)


class SwatPLC0(PLC):

    def pre_loop(self, sleep=0.1):
        print('DEBUG: swat-s1 plc0 enters pre_loop')
        print()

        time.sleep(sleep)

    def main_loop(self):
        """plc2 main loop.

            - reads the valve value from the network 
            - opens or closes the valve
        """

        print('DEBUG: swat-s1 plc0 enters main_loop.')
        print()

        count = 0
        while(count <= PLC_SAMPLES):

            mv001 = int(self.receive(MV001, PLC0_ADDR))
            print("DEBUG PLC0 - received mv001: %f" % mv001)
            if mv001 != 0:
                self.set(MV001, mv001)

            time.sleep(PLC_PERIOD_SEC)
            count += 1

if __name__ == "__main__":

    # notice that memory init is different form disk init
    plc0 = SwatPLC0(
        name='plc0',
        state=STATE,
        protocol=PLC0_PROTOCOL,
        memory=PLC0_DATA,
        disk=PLC0_DATA)
