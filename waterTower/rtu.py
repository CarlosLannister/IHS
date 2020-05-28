"""
rtu
"""

#from minicps.devices import RTU

from minicps.devices import RTU
from utils import PLC1_DATA, STATE, PLC1_PROTOCOL, RTU_PROTOCOL
from utils import PLC_PERIOD_SEC, PLC_SAMPLES
from utils import IP, LIT_101_M
from utils import SCADA_ADDR, PLC0_ADDR, PLC2_ADDR, RTU_ADDR

import time

ManualMode = ('MM', 0)

MV001 = ('MV001', 0)
LIT101 = ('LIT101', 1)
P201 = ('P201', 2)
FLAG = ('flag(thisisaflag)', 2)

CO_0_2a = ('CO', 0, '2a')

class ScenarioRTU(RTU):

    def pre_loop(self, sleep=0.1):
        print('[DEBUG] RTU - Enters pre loop\n')

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

            # TODO this would go to the SCADA
            self.send(LIT101, water_level, SCADA_ADDR, "enip")

            # Hit the first overflow threshold
            if water_level >= LIT_101_M['H']:
                print("[WARNING] Water level over soft high -> close mv001 and open p201")
                
                # Overflow!!!    
                if water_level >= LIT_101_M['HH']:
                    print("[WARNING] OVERFLOW!! %.2f >= %.2f." % (water_level, LIT_101_M['HH']))
                    #TODO overflow flag here?
                
                # PLC1 informs PLC0 to close the valve mv001
                self.send(MV001, 2, PLC0_ADDR, "enip")

                # PLC1 informs PLC2 to open the pump p201
                self.send(P201, 1, PLC2_ADDR, "enip")
            
            # Hit the first underflow threshold
            elif water_level <= LIT_101_M['L']:
                print("[WARNING] Water level under soft low -> open mv101 and close p201")
                
                # Underflow!!!
                if water_level <= LIT_101_M['LL']:
                    print("[WARNING] UNDERFLOW!! %.2f <= %.2f." % (water_level, LIT_101_M['LL']))
                    #TODO underflow flag here
                
                # PLC1 informs PLC0 to open the valve mv001
                self.send(MV001, 1, PLC0_ADDR, "enip")

                # PLC1 informs PLC2 to close the pump p201
                self.send(P201, 2, PLC2_ADDR, "enip")



            #self.send(FLAG, 2, PLC2_ADDR, "modbus")
            time.sleep(PLC_PERIOD_SEC)


if __name__ == "__main__":

    # notice that memory init is different form disk init
    rtu = ScenarioRTU(
        name='rtu',
        state=STATE,
        protocols=[RTU_PROTOCOL],
        memory=PLC1_DATA,
        disk=PLC1_DATA)
