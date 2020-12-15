
"""
scenario plc2
"""

from minicps.devices import PLC
from utils import STATE_2
from utils import PLC_PERIOD_SEC
from utils import SUBNET_2

import time

PLC2_ADDR = SUBNET_2['plc2']

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

    DATA = {
        'TODO': 'TODO',
    }

    PLC2_TAGS = (
        ('P201', 2, 'INT'),
        ('FIT201', 2, 'REAL')
        # no interlocks
    )
    PLC2_SERVER = {
        'address': SUBNET_2['plc2'],
        'tags': PLC2_TAGS
    }
    PROTOCOL = {
        'name': 'enip',
        'mode': 1,
        'server': PLC2_SERVER
    }

    # notice that memory init is different form disk init
    plc2 = ScenarioPLC2(
        name='plc2',
        state=STATE_2,
        protocol=PROTOCOL,
        memory=DATA,
        disk=DATA)