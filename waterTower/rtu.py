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

FIT101 = ('FIT101', 1)
MV001 = ('MV001', 0)
LIT101 = ('LIT101', 1)
P201 = ('P201', 2)
FLAG = ('flag(estoesunaflag)', 2)

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
        print()

        while True:
            # lit101 [meters]
            lit101 = float(self.get(LIT101))
            #self.send(LIT101, lit101, PLC1_ADDR)
        
            print('DEBUG plc1 lit101: %.5f' % lit101)

            # TODO this would go to the SCADA
            self.send(LIT101, lit101, PLC1_ADDR, "enip")

            # Hit the first overflow threshold
            if lit101 >= LIT_101_M['H']:
                print("INFO PLC1 - lit101 over H -> close mv001 and open p201")
                
                # Overflow!!!    
                if lit101 >= LIT_101_M['HH']:
                    print("WARNING OVERFLOW!! Over HH: %.2f >= %.2f." % (lit101, LIT_101_M['HH']))
                    #TODO overflow flag here?
                
                # PLC1 informs PLC0 to close the valve mv001
                self.send(MV001, 2, PLC0_ADDR, "enip")

                # PLC1 informs PLC2 to open the pump p201
                self.send(P201, True, PLC2_ADDR, "enip")
            
            # Hit the first underflow threshold
            elif lit101 <= LIT_101_M['L']:
                print("INFO PLC1 - lit101 over H -> close mv101 and open p201")
                
                # Underflow!!!
                if lit101 <= LIT_101_M['LL']:
                    print("WARNING UNDERFLOW!! Under LL: %.2f <= %.2f." % (lit101, LIT_101_M['LL']))
                    #TODO underflow flag here
                
                # PLC1 informs PLC0 to open the valve mv001
                #self.set(MV101, 1)
                self.send(MV001, 1, PLC0_ADDR, "enip")

                # PLC1 informs PLC2 to close the pump p201
                #print("INFO PLC1 - close p101.")
                #self.set(P201, 0)
                self.send(P201, True, PLC2_ADDR, "enip")


            print("************************************")
            #self.send(FLAG, 2, PLC2_ADDR, "modbus")
            time.sleep(PLC_PERIOD_SEC)

        print('DEBUG swat plc1 shutdown')


if __name__ == "__main__":

    # notice that memory init is different form disk init
    rtu = ScenarioRTU(
        name='rtu',
        state=STATE,
        protocols=[PLC1_PROTOCOL, RTU_PROTOCOL],
        memory=PLC1_DATA,
        disk=PLC1_DATA)
