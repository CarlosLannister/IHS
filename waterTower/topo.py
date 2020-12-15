"""
Subnet topology
"""
from mininet.cli import CLI
from mininet.net import Mininet
from mininet.topo import Topo

from utils import IP, MAC, NETMASK, SUBNET_1, SUBNET_2, SUBNET_3, SUBNET_3_MAC, SUBNET_2_MAC, SUBNET_1_MAC
from mininet.link import Intf

class ScenarioTopo(Topo):

    """Topology of the scenario"""

    def subnet1(self):

        switch = self.addSwitch('s1_1')

        plc0 = self.addHost(
            'plc0_1',
            ip=SUBNET_1['plc0'] + NETMASK,
            mac=SUBNET_1_MAC['plc0'])
        self.addLink(plc0, switch)

        rtu = self.addHost(
            'rtu_1',
            ip=SUBNET_1['rtu'] + NETMASK,
            mac=SUBNET_1_MAC['rtu'])
        self.addLink(rtu, switch)

        plc2 = self.addHost(
            'plc2_1',
            ip=SUBNET_1['plc2'] + NETMASK,
            mac=SUBNET_1_MAC['plc2'])
        self.addLink(plc2, switch)

        attacker = self.addHost(
            'attacker_1',
            ip=SUBNET_1['attacker'] + NETMASK,
            mac=SUBNET_1_MAC['attacker'])
        self.addLink(attacker, switch)

        switch2 = self.addSwitch('s2_1')

        scada = self.addHost(
            'scada_1',
            ip=SUBNET_1['scada'] + NETMASK,
            mac=SUBNET_1_MAC['scada'])
        self.addLink(scada, switch2)

        self.addLink(switch2, switch)

    def subnet2(self):

        switch = self.addSwitch('s1_2')

        plc0 = self.addHost(
            'plc0_2',
            ip=SUBNET_2['plc0'] + NETMASK,
            mac=SUBNET_2_MAC['plc0'])
        self.addLink(plc0, switch)

        rtu = self.addHost(
            'rtu_2',
            ip=SUBNET_2['rtu'] + NETMASK,
            mac=SUBNET_2_MAC['rtu'])
        self.addLink(rtu, switch)

        plc2 = self.addHost(
            'plc2_2',
            ip=SUBNET_2['plc2'] + NETMASK,
            mac=SUBNET_2_MAC['plc2'])
        self.addLink(plc2, switch)

        attacker = self.addHost(
            'attacker_2',
            ip=SUBNET_2['attacker'] + NETMASK,
            mac=SUBNET_2_MAC['attacker'])
        self.addLink(attacker, switch)

        switch2 = self.addSwitch('s2_2')

        scada = self.addHost(
            'scada_2',
            ip=SUBNET_2['scada'] + NETMASK,
            mac=SUBNET_2_MAC['scada'])
        self.addLink(scada, switch2)

        self.addLink(switch2, switch)


    def subnet3(self):

        switch = self.addSwitch('s1_3')

        plc0 = self.addHost(
            'plc0_3',
            ip=SUBNET_3['plc0'] + NETMASK,
            mac=SUBNET_3_MAC['plc0'])
        self.addLink(plc0, switch)

        rtu = self.addHost(
            'rtu_3',
            ip=SUBNET_3['rtu'] + NETMASK,
            mac=SUBNET_3_MAC['rtu'])
        self.addLink(rtu, switch)

        plc2 = self.addHost(
            'plc2_3',
            ip=SUBNET_3['plc2'] + NETMASK,
            mac=SUBNET_3_MAC['plc2'])
        self.addLink(plc2, switch)

        attacker = self.addHost(
            'attacker_3',
            ip=SUBNET_3['attacker'] + NETMASK,
            mac=SUBNET_3_MAC['attacker'])
        self.addLink(attacker, switch)

        switch2 = self.addSwitch('s2_3')

        scada = self.addHost(
            'scada_3',
            ip=SUBNET_3['scada'] + NETMASK,
            mac=SUBNET_3_MAC['scada'])
        self.addLink(scada, switch2)

        self.addLink(switch2, switch)


    def build(self):


        self.subnet1()
        

        self.subnet2()

        #switch = self.subnet3()
        #self.addLink(switch2, switch)

        


if __name__ == '__main__':
    """Test MixTopo."""

    topo = ScenarioTopo()
    net = Mininet(topo=topo)
    net.start()

    CLI(net)

    net.stop()