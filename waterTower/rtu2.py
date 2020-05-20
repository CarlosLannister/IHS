"""
swat-s1 plc1.py
"""

# TODO edit again
#from minicps.devices import RTU

from minicps.devices import RTU
from utils import PLC1_DATA, STATE, PLC1_PROTOCOL, RTU_PROTOCOL
from utils import PLC_PERIOD_SEC, PLC_SAMPLES
from utils import IP, LIT_101_M

import time

PLC0_ADDR = IP['plc0']
PLC1_ADDR = IP['plc1']
PLC2_ADDR = IP['plc2'] + ':502'

CO_0_2a = ('CO', 0, '2a')

class SubnetRTU(RTU):

    def pre_loop(self, sleep=0.1):
        print('DEBUG: swat-s1 plc1 enters pre_loop')

        time.sleep(sleep)

    def main_loop(self):

        print('DEBUG: swat-s1 plc1 enters main_loop.')
        print()

        while(True):
            
            self.send(CO_0_2a, True, PLC2_ADDR, "modbus")

            print("************************************")
            #self.send(FLAG, 2, PLC2_ADDR, "modbus")
            time.sleep(PLC_PERIOD_SEC)


if __name__ == "__main__":

    # notice that memory init is different form disk init
    rtu = SubnetRTU(
        name='rtu',
        state=STATE,
        protocols=[RTU_PROTOCOL])
