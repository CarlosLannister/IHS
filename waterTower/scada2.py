"""
WaterTower scada.py
"""
import sqlite3

from minicps.devices import SCADAServer

from utils import STATE3, SCADA_LOOP
from utils import SUBNET_2

from threading import Thread, Event
import sqlite3

import time


#MODE = ('MODE', 1) # 0 error / 1 automatic / 2 manual mode
#COMMAND = ('COMMAND', 0) # 0 error / 1 automatic / 2 -> close plc0 / 3 -> open plc0 / 4 -> close plc0 / 5 -> open plc0 / 
SCADA_ADDR = SUBNET_2['scada']
RTU_ADDR = SUBNET_2['rtu']

MODE = ('MODE', 1) # 0 error / 1 automatic / 2 -> close plc0 / 3 -> open plc0 / 4 -> close plc0 / 5 -> open plc0 / 

MV001 = ('MV001', 0)
LIT101 = ('LIT101', 1)
P201 = ('P201', 2)

class ScadaServer(SCADAServer):

    def plcOn(self, subnet, plc_addr):
        #TODO
        #self.send(MV001, 1, PLC0_ADDR)
        pass

    def plcOff(self, plc_addr):
        pass


    def pre_loop(self, sleep=0.5):
        print('DEBUG: SCADA server enters pre_loop')
        self.thread_stop_event = Event()

        time.sleep(sleep)

    def main_loop(self):
        """Scada main loop.
            - reads RTU values
            - stores info in database
            - 
        """
        print('DEBUG: SCADA server enters main_loop.\n')

        water_level = 0
        last_value = 0

        while(True):
            # Each X seconds gets the data from the RTU

            try:
                water_level = float(self.receive(LIT101, SCADA_ADDR))
                last_value = water_level
            except:
                water_level = last_value

            print("[DEBUG] Water level:", water_level)
            # TODO guarda en la base de datos

            #mira si hay comando
            #check database
            db = sqlite3.connect('file:hmi3_db.sqlite?mode=ro', uri=True, timeout=3)
            cursorObj = db.cursor()
            cursorObj.execute('SELECT name, value FROM hmi3 WHERE name="MODE"')
            mode = cursorObj.fetchall()[0][1]

            db.commit()
            db.close()

            print("MODE === " + str(mode))

            if mode != 0:
                print("SENDING")
                self.send(MODE, int(mode), RTU_ADDR)

            #water_level = self.receive(LIT101, RTU_ADDR)


            time.sleep(SCADA_LOOP)


if __name__ == "__main__":

    SCADA_TAGS = (
        ('LIT101', 1, 'REAL'),
        ('MODE', 1, 'INT')
    )
    SCADA_SERVER = {
        'address': SUBNET_2['scada'],
        'tags': SCADA_TAGS
    }
    PROTOCOL = {
        'name': 'enip',
        'mode': 1,
        'server': SCADA_SERVER
    }


    # notice that memory init is different form disk init
    scada = ScadaServer(
        name='scada',
        state=STATE3,
        protocol=PROTOCOL)
