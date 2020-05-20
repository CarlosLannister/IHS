
"""
swat-s1 plc2
"""

from minicps.devices import PLC
from utils import PLC2_DATA, STATE, PLC2_PROTOCOL, PLC3_PROTOCOL
from utils import PLC_SAMPLES, PLC_PERIOD_SEC
from utils import IP, RTU_ADDR

import time

PLC2_ADDR = IP['plc2']
RTU_ADDR = IP['rtu_int2'] + ':502'

CO_0_2a = ('CO', 0, '2a')

class SwatPLC2(PLC):

    def pre_loop(self, sleep=0.1):
        print('DEBUG: swat-s1 plc2 enters pre_loop')

        time.sleep(sleep)

    def main_loop(self):
        print('DEBUG: swat-s1 plc3 enters main_loop.')

        while(True):

            aaa = self.receive(CO_0_2a, RTU_ADDR)

            print("DEBUG: PLC3 received coil {}".format(aaa))


            time.sleep(PLC_PERIOD_SEC)

if __name__ == "__main__":

    # notice that memory init is different form disk init
    plc2 = SwatPLC2(
        name='plc2',
        state=STATE,
        protocol=PLC3_PROTOCOL)
