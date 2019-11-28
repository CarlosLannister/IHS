"""
swat-s1 run.py
"""

from mininet.net import Mininet
from mininet.cli import CLI
from minicps.mcps import MiniCPS

from topo import SwatTopo
import time

import sys


class SwatS1CPS(MiniCPS):

    """Main container used to run the simulation."""

    def __init__(self, name, net):

        self.name = name
        self.net = net

        net.start()

        net.pingAll()

        # start devices
        plc1, plc2, s1 = self.net.get(
            'plc1', 'plc2', 's1')

        print("Devices started")
        #pidplc2 = plc2.cmd(sys.executable + ' plc2.py &')
        #print("PLC2 Running with PID " + pidplc2)
        #time.sleep(2)
        #pidplc1= plc1.cmd(sys.executable + ' plc1.py &')
        #print("PLC1 Running with PID " + pidplc1)
        #time.sleep(2)
        # pidphysical=s1.cmd(sys.executable + ' physical_process.py &')
        # print("physical_process running with PID " + pidphysical)

        CLI(self.net)

        net.stop()

if __name__ == "__main__":

    topo = SwatTopo()
    net = Mininet(topo=topo)

    swat_s1_cps = SwatS1CPS(
        name='swat_s1',
        net=net)
