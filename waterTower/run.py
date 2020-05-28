"""
swat-s1 run.py
"""

from mininet.net import Mininet
from mininet.cli import CLI
from minicps.mcps import MiniCPS

import re
import sys
from mininet.link import Intf
from mininet.util import quietRun

from topo import ScenarioTopo


def checkIntf( intf ):
        #Make sure intf exists and is not configured.
        config = quietRun( 'ifconfig %s 2>/dev/null' % intf, shell=True )
        print(config)
        if not config:
            print( 'Error:', intf, 'does not exist!\n' )
            sys.exit( 1 )
        ips = re.findall( r'\d+\.\d+\.\d+\.\d+', config )
        if ips:
            print( 'Error:', intf, 'has an IP address, and is probably in use!\n' )
            sys.exit( 1 )

class SwatS1CPS(MiniCPS):

    """Main container used to run the simulation."""
    def __init__(self, name, net):

        # try to get hw intf from the command line; by default, use eth1
        '''
        intfName = 'enp0s3'
        print( '*** Connecting to hw intf: %s' % intfName )

        print( '*** Checking', intfName, '\n' )
        checkIntf( intfName )
        '''
        
        self.name = name
        self.net = net

        net.start()

        net.pingAll()

        # start devices
        self.net.get('plc0', 'rtu', 'plc2', 's1')

        print("Devices started")
        
        CLI(self.net)

        net.stop()

if __name__ == "__main__":

    topo = ScenarioTopo()
    net = Mininet(topo=topo)

    swat_s1_cps = SwatS1CPS(
        name='swat_s1',
        net=net)
