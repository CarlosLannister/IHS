from flask_socketio import SocketIO, emit
from flask import Flask, render_template
from flask_mqtt import Mqtt
import paho.mqtt.client as mqtt
from utils import MQTT_SERVER, MQTT_PORT

import time

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!' #Generate a personal secret key for production use !!!!!. It should be random and secret. 
app.config['DEBUG'] = True #Do not forget to turnoff debug mode it is a production environment. 

app.config['MQTT_BROKER_URL'] = MQTT_SERVER
app.config['MQTT_BROKER_PORT'] = MQTT_PORT
app.config['MQTT_USERNAME'] = ''
app.config['MQTT_PASSWORD'] = ''
app.config['MQTT_KEEPALIVE'] = 5
app.config['MQTT_TLS_ENABLED'] = False


mqtt = Mqtt(app)
socketio = SocketIO(app, async_mode=None, logger=True, engineio_logger=True)


@app.route('/')
def index():
    #only by sending this page first will the client be connected to the socketio instance
    return render_template('index.html')

@mqtt.on_connect()
def handle_connect(client, userdata, flags, rc):
    mqtt.subscribe("scada")

@mqtt.on_message()
def handle_mqtt_message(client, userdata, message):
    payload = message.payload.decode()
    print(payload)
    socketio.emit('newnumber', {'number': payload['water_level'], 'MV001' : payload['plc0'], 'P201': payload['plc1']}, 
    	namespace='/test')

@mqtt.on_log()
def handle_logging(client, userdata, level, buf):
    print(level, buf)


@socketio.on('connect', namespace='/test')
def test_connect():
    # need visibility of the global thread object
    print('Client connected')

@socketio.on('disconnect', namespace='/test')
def test_disconnect():
    print('Client disconnected')





'''
	def send_action(action):
		# TODO add action parser
		message = {"subnet": 1, "plc": 2, "action": True}
		self.client.publish("actions", message)


        self.client = mqtt.Client()
        self.client.connect(MQTT_SERVER)
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
        self.client.loop_start()
'''




if __name__ == "__main__":

    socketio.run(app)




