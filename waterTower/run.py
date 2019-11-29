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
        plc0, plc1, plc2, s1 = self.net.get(
            'plc0', 'plc1', 'plc2', 's1')

        #plc0.cmd(sys.executable + ' plc0.py &')
        #time.sleep(1)
        #plc1.cmd(sys.executable + ' plc1.py &')
        #time.sleep(1)
        #plc2.cmd(sys.executable + ' plc2.py &')
        #time.sleep(1)
        #s1.cmd(sys.executable + ' physical_process.py &')

        print("Devices started")
        
        CLI(self.net)

        net.stop()

if __name__ == "__main__":

    topo = SwatTopo()
    net = Mininet(topo=topo)

    swat_s1_cps = SwatS1CPS(
        name='swat_s1',
        net=net)