"""
rtu
"""

#from minicps.devices import RTU

from minicps.devices import PLC
from utils import STATE_2
from utils import PLC_PERIOD_SEC, PLC_SAMPLES
from utils import LIT_101_M
from utils import SCADA_ADDR, SUBNET_2

import time

PLC2_ADDR = SUBNET_2['plc2']
PLC0_ADDR = SUBNET_2['plc0']
RTU_ADDR = SUBNET_2['rtu']

MODE = ('MODE', 1) # 0 error / 1 automatic / 2 -> close plc0 / 3 -> open plc0 / 4 -> close plc0 / 5 -> open plc0 / 

MV001 = ('MV001', 0)
LIT101 = ('LIT101', 1)
P201 = ('P201', 2)
FLAG = ('flag(thisisaflag)', 2)

class ScenarioRTU(PLC):

    def pre_loop(self, sleep=0.1):
        print('[DEBUG] RTU - Enters pre loop\n')
        self.auto = True
        self.mode = 1
        time.sleep(sleep)

    def main_loop(self):
        """plc1 main loop.

            - reads sensors value
            - drives actuators according to the control strategy
            - updates its enip server
        """

        print('[DEBUG] RTU - Enters main loop\n')

        while True:
            # reads water level
            water_level = float(self.get(LIT101))

            print('[DEBUG] Water level: %.5f' % water_level)

            # Sends water level to scada
            self.send(LIT101, water_level, SCADA_ADDR)

            #Checks mode
            try:
                self.mode = int(self.receive(MODE, RTU_ADDR))
            except:
                self.mode = 0

            print("MODE ==== " + str(self.mode))

            if self.mode != 0:
                if self.mode == 1:
                   self.auto = True
                else:
                    self.auto = False
            
            #Manual mode
            if not self.auto:
                # OPEN PLC1
                if self.mode == 2:
                    self.send(MV001, 2, PLC0_ADDR)
                # CLOSE PLC1
                elif self.mode == 3:
                    self.send(MV001, 1, PLC0_ADDR)
                # OPEN PLC2
                elif self.mode == 4:
                    self.send(P201, 1, PLC2_ADDR)
                # CLOSE PLC2
                elif self.mode == 5:
                    self.send(P201, 2, PLC2_ADDR)

            # Automatic mode 
            else:
                # Hit the first OVERFLOW threshold
                if water_level >= LIT_101_M['H']:
                    print("[WARNING] Water level over soft high -> close mv001 and open p201")
                    # OVERFLOW!!!    
                    if water_level >= LIT_101_M['HH']:
                        print("[WARNING] OVERFLOW!! %.2f >= %.2f." % (water_level, LIT_101_M['HH']))
                        #TODO overflow flag here?
                    

                    # PLC1 informs PLC0 to close the valve mv001
                    self.send(MV001, 2, PLC0_ADDR)
                    # PLC1 informs PLC2 to open the pump p201
                    self.send(P201, 1, PLC2_ADDR)
                
                # Hit the first underflow threshold
                elif water_level <= LIT_101_M['L']:
                    print("[WARNING] Water level under soft low -> open mv101 and close p201")
                    
                    # Underflow!!!
                    if water_level <= LIT_101_M['LL']:
                        print("[WARNING] UNDERFLOW!! %.2f <= %.2f." % (water_level, LIT_101_M['LL']))
                        #TODO underflow flag here
                    
                    # PLC1 informs PLC0 to open the valve mv001
                    self.send(MV001, 1, PLC0_ADDR)

                    # PLC1 informs PLC2 to close the pump p201
                    self.send(P201, 2, PLC2_ADDR)



            #self.send(FLAG, 2, PLC2_ADDR, "modbus")
            time.sleep(PLC_PERIOD_SEC)


if __name__ == "__main__":

    RTU_TAGS = (
        ('LIT101', 1, 'REAL'),
        ('MODE', 1, 'INT')
    )
    RTU_SERVER = {
        'address': SUBNET_2['rtu'],
        'tags': RTU_TAGS
    }
    PROTOCOL = {
        'name': 'enip',
        'mode': 1,
        'server': RTU_SERVER
    }

    # notice that memory init is different form disk init
    rtu = ScenarioRTU(
        name='rtu',
        state=STATE_2,
        protocol=PROTOCOL)
