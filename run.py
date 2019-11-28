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
        plc1, plc2, plc3, s1 = self.net.get(
            'plc1', 'plc2', 'plc3', 's1')

        print("Devices started")
        # SPHINX_SWAT_TUTORIAL RUN(
        a = plc2.cmd(sys.executable + ' plc2.py &')
        print(a)
        b=plc3.cmd(sys.executable + ' plc3.py &')
        print(b)
        time.sleep(1)
        c= plc1.cmd(sys.executable + ' plc1.py &')
        print(c)
        s1.cmd(sys.executable + ' physical_process.py &')
        # SPHINX_SWAT_TUTORIAL RUN)

        CLI(self.net)

        net.stop()

if __name__ == "__main__":

    topo = SwatTopo()
    net = Mininet(topo=topo)

    swat_s1_cps = SwatS1CPS(
        name='swat_s1',
        net=net)
