
"""
swat-s1 plc2
"""

from minicps.devices import PLC
from utils import PLC2_DATA, STATE, PLC2_PROTOCOL
from utils import PLC_SAMPLES, PLC_PERIOD_SEC
from utils import IP

import time

PLC0_ADDR = IP['plc0']
PLC1_ADDR = IP['plc1']
PLC2_ADDR = IP['plc2']

P201 = ('P201', 2)


class SwatPLC2(PLC):

    def pre_loop(self, sleep=0.1):
        print('DEBUG: swat-s1 plc2 enters pre_loop')
        print()

        time.sleep(sleep)

    def main_loop(self):
        """plc2 main loop.

            - read engine value from the network 
            - opens or closes the engine
        """

        print('DEBUG: swat-s1 plc2 enters main_loop.')
        print()

        count = 0
        while(count <= PLC_SAMPLES):

            p201 = int(self.receive(P201, PLC2_ADDR))
            if p201 != 0:
                self.set(P201, p201)
                print("DEBUG PLC2 - received p201: %f" % p201)

            time.sleep(PLC_PERIOD_SEC)
            count += 1

if __name__ == "__main__":

    # notice that memory init is different form disk init
    plc2 = SwatPLC2(
        name='plc2',
        state=STATE,
        protocol=PLC2_PROTOCOL,
        memory=PLC2_DATA,
        disk=PLC2_DATA)
