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
        
        print("Devices started")
        
        if auto:
            plc0, rtu, plc2, s1, scada = self.net.get('plc0', 'rtu', 'plc2', 's1', 'scada')

            print("Running PLCs")
            plc0.cmd('nohup python plc0.py > logs/plc0.log &')
            time.sleep(1)
            plc2.cmd('nohup python plc2.py > logs/plc2.log &')
            time.sleep(2)

            print("Running physical process")
            s1.cmd('nohup python physical_process.py > logs/physical_process.log &')
            time.sleep(2)
            
            print("Running RTU")
            rtu.cmd('nohup python rtu.py > logs/rtu.log &')
            time.sleep(2)

            print("Running SCADA")
            scada.cmd('nohup python scada.py > logs/scada.log &')

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
