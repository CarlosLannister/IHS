# Start with a basic flask app webpage.
from flask_socketio import SocketIO, emit
from flask import Flask, render_template, Response
from threading import Thread, Event
import sqlite3



app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!' #Generate a personal secret key for production use !!!!!. It should be random and secret. 
app.config['DEBUG'] = True #Do not forget to turnoff debug mode it is a production environment. 

#turn the flask app into a socketio app
socketio = SocketIO(app, async_mode=None, logger=True, engineio_logger=True)

#random number Generator Thread
thread = Thread()
thread_stop_event = Event()


def waterLevels():

    print("Getting waterLevels")
    db = sqlite3.connect('file:swat_s1_db.sqlite?mode=ro', uri=True, timeout=3)
    cursorObj = db.cursor()
    while not thread_stop_event.isSet():
        db = sqlite3.connect('file:swat_s1_db.sqlite?mode=ro', uri=True, timeout=3)
        cursorObj = db.cursor()
        cursorObj.execute('SELECT name, value FROM swat_s1 WHERE name="LIT101"')
        level = cursorObj.fetchall()
        waterLevel = level[0][1]
        cursorObj.execute('SELECT name, value FROM swat_s1 WHERE name="MV001"')
        MV001 = cursorObj.fetchall()[0][1]

        cursorObj.execute('SELECT name, value FROM swat_s1 WHERE name="P201"')
        P201 = cursorObj.fetchall()[0][1]

        db.commit()

        socketio.emit('newnumber', {'number': waterLevel, 'MV001' : MV001, 'P201': P201}, namespace='/test')
        socketio.sleep(1)

    cursorObj.close()
    db.close()
        

def runCommand(mode):
    print("TEST 1")
    db1 = sqlite3.connect('file:hmi_db.sqlite?mode=rw', uri=True, timeout=3)
    cursorObj1 = db1.cursor()
    #cursorObj.execute('INSERT INTO hmi(value) VALUES (2)')
    cursorObj1.execute('UPDATE hmi SET value = ' + str(mode) + ' WHERE name = "MODE"')
    db1.commit()
    db1.close()

@app.route('/')
def index():
    #only by sending this page first will the client be connected to the socketio instance
    return render_template('index.html')

@app.route('/auto', methods=['GET'])
def auto():
    runCommand(1)
    return render_template('index.html')

@app.route('/close1', methods=['GET'])
def close1():
    runCommand(2)
    return render_template('index.html')

@app.route('/open1', methods=['GET'])
def open1():
    runCommand(3)
    return render_template('index.html')

@app.route('/open2', methods=['GET'])
def open2():
    runCommand(4)
    return render_template('index.html')

@app.route('/close2', methods=['GET'])
def close2():
    runCommand(5)
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