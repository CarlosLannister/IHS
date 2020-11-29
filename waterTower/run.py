"""
swat-s1 run.py
"""

from mininet.net import Mininet
from mininet.cli import CLI
from minicps.mcps import MiniCPS

import argparse
import re
import sys
import time
from mininet.link import Intf
from mininet.util import quietRun

from topo import ScenarioTopo


class SwatS1CPS(MiniCPS):

    """Main container used to run the simulation."""
    def __init__(self, name, net, auto):

        # try to get hw intf from the command line; by default, use eth1
        
        self.name = name
        self.net = net

        net.start()

        net.pingAll()

        # start devices
        plc0, rtu, plc2, s1, scada = self.net.get('plc0', 'rtu', 'plc2', 's1', 'scada')

        print("Devices started")
        
        if auto:
            print("Running PLCs")
            plc0.cmd(sys.executable + ' plc0.py &')
            plc2.cmd(sys.executable + ' plc2.py &')
            time.sleep(2)

            print("Running physical process")
            s1.cmd(sys.executable + ' physical_process.py &')
            time.sleep(2)
            '''
            print("Running RTU")
            rtu.cmd(sys.executable + ' rtu.py &')
            time.sleep(2)

            print("Running SCADA")
            scada.cmd(sys.executable + ' scada.py &')
            '''

        CLI(self.net)

        net.stop()




if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("-a", "--automatic", help="Runs the scenario automatically", action="store_true")
    args = parser.parse_args()

    topo = ScenarioTopo()
    net = Mininet(topo=topo)

    if args.automatic:
        print("Running AUTOMATIC mode")
        swat_s1_cps = SwatS1CPS(name='swat_s1', net=net, auto=True)
    else:
        print("Running MANUAL mode")
        swat_s1_cps = SwatS1CPS(name='swat_s1', net=net, auto=False)
