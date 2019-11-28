# Start with a basic flask app webpage.
from flask_socketio import SocketIO, emit
from flask import Flask, render_template, url_for, copy_current_request_context
import time 
from threading import Thread, Event
import sqlite3



__author__ = 'slynn'

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
app.config['DEBUG'] = True

#turn the flask app into a socketio app
socketio = SocketIO(app, async_mode=None, logger=True, engineio_logger=True)

#random number Generator Thread
thread = Thread()
thread_stop_event = Event()

def waterLevels():
    """
    Generate a random number every 1 second and emit to a socketio instance (broadcast)
    Ideally to be run in a separate thread?
    """
    #infinite loop of magical random numbers
    print("Getting waterLevels")
    while not thread_stop_event.isSet():
        db = sqlite3.connect('file:swat_s1_db.sqlite?mode=ro', uri=True)
        cursorObj = db.cursor()
        cursorObj.execute('SELECT name, value FROM swat_s1 WHERE name="LIT101"')
        level = cursorObj.fetchall()
        print(level[0][0])
        socketio.emit('newnumber', {'number': level[0][1]}, namespace='/test')
        socketio.sleep(5)
        cursorObj.close()
        time.sleep(5)


@app.route('/')
def index():
    #only by sending this page first will the client be connected to the socketio instance
    return render_template('index.html')

@socketio.on('connect', namespace='/test')
def test_connect():
    # need visibility of the global thread object
    global thread
    print('Client connected')

    #Start the random number generator thread only if the thread has not been started before.
    if not thread.isAlive():
        print("Starting Thread")
        thread = socketio.start_background_task(waterLevels)

@socketio.on('disconnect', namespace='/test')
def test_disconnect():
    print('Client disconnected')


if __name__ == '__main__':
    socketio.run(app)