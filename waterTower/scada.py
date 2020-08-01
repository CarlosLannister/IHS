"""
WaterTower scada.py
"""
import sqlite3

from minicps.devices import SCADAServer

from utils import PLC1_DATA, STATE, SCADA_PROTOCOL, SCADA_LOOP 
from utils import SCADA_ADDR, RTU_ADDR

from utils import MQTT_SERVER
import paho.mqtt.client as mqtt
import time


MV001 = ('MV001', 0)
LIT101 = ('LIT101', 1)
P201 = ('P201', 2)

class ScadaServer(SCADAServer):

    # Callback when the client connects to the MQTT broker
    def on_connect(self, client, userdata, flags, rc):
        print("Connected with result code "+str(rc))

        self.client.subscribe("actions")

    # The callback for when a PUBLISH message is received from the server.
    def on_message(self, client, userdata, msg):

        print(msg.topic+" "+str(msg.payload))
        # Here we should execute the methods On/Off to send the message to the RTU
        # This send should be in such way for the switch to understand what to do on which plc
        # self.send(P201, 1, PLC2_ADDR)


    def plcOn(self, subnet, plc_addr):
        #TODO
        #self.send(MV001, 1, PLC0_ADDR)

        pass

    def plcOff(self, plc_addr):
        pass


    def pre_loop(self, sleep=0.5):
        print('DEBUG: SCADA server enters pre_loop')

        #Start MQTT client on background
        
        self.client = mqtt.Client()
        self.client.connect(MQTT_SERVER)
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
        self.client.loop_start()
        

        time.sleep(sleep)

    def main_loop(self):
        """Scada main loop.
            - reads RTU values
            - stores info in database
            - 
        """
        print('DEBUG: SCADA server enters main_loop.\n')

        while(True):
            # Each X seconds gets the data from the RTU
            water_level = float(self.receive(LIT101, SCADA_ADDR))
            
            print("[DEBUG] Water level:", water_level)

            #water_level = self.receive(LIT101, RTU_ADDR)

            plc0 = 1
            plc2 = 1
            #water_level = 600.0
            #Pushes values to the MQTT broken
            print("pushing message")
            message = {'plc0': plc0, 'plc1': plc1, 'water_level': water_level}
            client.publish("scada", message)

            time.sleep(SCADA_LOOP)


if __name__ == "__main__":

    # notice that memory init is different form disk init
    scada = ScadaServer(
        name='scada',
        state=STATE,
        protocol=SCADA_PROTOCOL)
