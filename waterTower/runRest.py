"""
waterTower run.py
"""

from mininet.net import Mininet
from mininet.cli import CLI
from mininet.node import Node
from mininet.util import waitListening
from mininet.log import setLogLevel, info

from flask import Flask, request, render_template, jsonify

from topo import SwatTopo
from subprocess import call, run
import time

import sys


app = Flask(__name__)

running=False

@app.route('/cli', methods=['POST'])
def cli():
    global net
    cmd = request.form['cmd']

    with open('/tmp/webapp-cmd', 'w') as f:
        f.write(cmd)

    try:
        with open('/tmp/webapp-log', 'r') as f:
            old=f.read()
    except:
        with open('/tmp/webapp-log', 'w') as f:
            old=''

    CLI(net, script='/tmp/webapp-cmd')

    try:
        with open('/tmp/webapp-log', 'r') as f:
            new=f.read()
    except:
        with open('/tmp/webapp-log', 'w') as f:
            new=''

    return new[len(old):]


@app.route('/dos', methods=['GET'])
def dos():
    global net

    with open('/tmp/webapp-cmd', 'w') as f:
        f.write('attacker bash ../attacks/plc0-dos.sh')

    try:
        with open('/tmp/webapp-log', 'r') as f:
            old=f.read()
    except:
        with open('/tmp/webapp-log', 'w') as f:
            old=''

    CLI(net, script='/tmp/webapp-cmd')

    try:
        with open('/tmp/webapp-log', 'r') as f:
            new=f.read()
    except:
        with open('/tmp/webapp-log', 'w') as f:
            new=''

    return new[len(old):]



@app.route('/start')
def start():

    global net, attacker, running
    setLogLevel('info')

    run(["sudo", "mn" , "-c"])

    topo = SwatTopo()
    net = Mininet(topo=topo)

    net.start()

    net.pingAll()

    # start devices
    plc0, plc1, plc2, s1 = net.get(
        'plc0', 'plc1', 'plc2', 's1')

    plc0.cmd('while true; do `' + sys.executable + ' plc0.py` && break; done &')
    time.sleep(0.5)
    plc1.cmd('while true; do `' + sys.executable + ' plc1.py` && break; done &')
    time.sleep(0.5)
    plc2.cmd('while true; do `' + sys.executable + ' plc2.py` && break; done &')
    time.sleep(0.5)
    s1.cmd('while true; do `' + sys.executable + ' physical_process.py` && break; done &')

    print("Devices started")

    running = True

    return '\nServer started.\n'   



@app.route('/stop')
def stop():
    global net, attacker, running

    if not running:
        return '\nServer not running.\n'


    net.stop()

    print("*** Running clean")
    run(["sudo", "mn" , "-c"])
    
    running = False


    return '\nServer successfully stopped.\n'

@app.route('/restart')
def restart():

    stop()
    start()

    return '\nServer successfully restarted.\n'


if __name__ == '__main__':
    app.run(host='localhost', port=8080, debug=True, threaded = True)

