"""
swat-s1 plc1.py
"""

from minicps.devices import PLC
from utils import PLC1_DATA, STATE, PLC1_PROTOCOL
from utils import PLC_PERIOD_SEC, PLC_SAMPLES
from utils import IP, LIT_101_M

import time

PLC0_ADDR = IP['plc0']
PLC1_ADDR = IP['plc1']
PLC2_ADDR = IP['plc2']

FIT101 = ('FIT101', 1)
MV001 = ('MV001', 0)
LIT101 = ('LIT101', 1)
P201 = ('P201', 2)
FLAG = ('flag(estoesunaflag)', 2)
# interlocks to be received from plc2 and plc3
#FIT201_1 = ('FIT201', 1)
#FIT201_2 = ('FIT201', 2)
#MV201_1 = ('MV201', 1)
#MV201_2 = ('MV201', 2)
# SPHINX_SWAT_TUTORIAL PLC1 LOGIC)

# TODO: real value tag where to read/write flow sensor
class SwatPLC1(PLC):

    def pre_loop(self, sleep=0.1):
        print('DEBUG: swat-s1 plc1 enters pre_loop')

        time.sleep(sleep)

    def main_loop(self):
        """plc1 main loop.

            - reads sensors value
            - drives actuators according to the control strategy
            - updates its enip server
        """

        print('DEBUG: swat-s1 plc1 enters main_loop.')
        print()

        count = 0
        while(count <= PLC_SAMPLES):
            # lit101 [meters]
            lit101 = float(self.get(LIT101))
            #self.send(LIT101, lit101, PLC1_ADDR)
        
            print('DEBUG plc1 lit101: %.5f' % lit101)
            # TODO this would go to the SCADA
            self.send(LIT101, lit101, PLC1_ADDR)

            # TODO If it does not work, problem here
            # Remove if working
            ###############################

            # Hit the first overflow threshold
            if lit101 >= LIT_101_M['H']:
                print("INFO PLC1 - lit101 over H -> close mv001 and open p201")
                
                # Overflow!!!    
                if lit101 >= LIT_101_M['HH']:
                    print("WARNING OVERFLOW!! Over HH: %.2f >= %.2f." % (lit101, LIT_101_M['HH']))
                    #TODO overflow flag here?
                
                # PLC1 informs PLC0 to close the valve mv001
                self.send(MV001, 2, PLC0_ADDR)

                # PLC1 informs PLC2 to open the pump p201
                self.send(P201, 1, PLC2_ADDR)
            
            # Hit the first underflow threshold
            elif lit101 <= LIT_101_M['L']:
                print("INFO PLC1 - lit101 over H -> close mv101 and open p201")
                
                # Underflow!!!
                if lit101 <= LIT_101_M['LL']:
                    print("WARNING UNDERFLOW!! Under LL: %.2f <= %.2f." % (lit101, LIT_101_M['LL']))
                    #TODO underflow flag here
                
                # PLC1 informs PLC0 to open the valve mv001
                #self.set(MV101, 1)
                self.send(MV001, 1, PLC0_ADDR)

                # PLC1 informs PLC2 to close the pump p201
                #print("INFO PLC1 - close p101.")
                #self.set(P201, 0)
                self.send(P201, 2, PLC2_ADDR)


            print("************************************")
            self.send(FLAG, 2, PLC2_ADDR)
            time.sleep(PLC_PERIOD_SEC)
            count += 1

        print('DEBUG swat plc1 shutdown')


if __name__ == "__main__":

    # notice that memory init is different form disk init
    plc1 = SwatPLC1(
        name='plc1',
        state=STATE,
        protocol=PLC1_PROTOCOL,
        memory=PLC1_DATA,
        disk=PLC1_DATA)
