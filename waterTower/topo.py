"""
Subnet topology
"""
from mininet.cli import CLI
from mininet.net import Mininet
from mininet.topo import Topo

from utils import IP, MAC, NETMASK
from mininet.link import Intf

class ScenarioTopo(Topo):

    """SWaT 3 plcs + attacker + private dirs."""

    def build(self):

        switch = self.addSwitch('s1')

        switch2 = self.addSwitch('s2')
        self.addLink(switch2, switch)
        
        plc0 = self.addHost(
            'plc0',
            ip=IP['plc0'] + NETMASK,
            mac=MAC['plc0'])
        self.addLink(plc0, switch)

        rtu = self.addHost(
            'rtu',
            ip=IP['rtu'] + NETMASK,
            mac=MAC['rtu'])
        self.addLink(rtu, switch)

        plc2 = self.addHost(
            'plc2',
            ip=IP['plc2'] + NETMASK,
            mac=MAC['plc2'])
        self.addLink(plc2, switch)

        attacker = self.addHost(
            'attacker',
            ip=IP['attacker'] + NETMASK,
            mac=MAC['attacker'])
        self.addLink(attacker, switch)

        # Remove when using distributed system
        scada = self.addHost(
            'scada',
            ip=IP['scada'] + NETMASK,
            mac=MAC['scada'])
        self.addLink(scada, switch2)


if __name__ == '__main__':
    """Test MixTopo."""

    topo = ScenarioTopo()
    net = Mininet(topo=topo)
    net.start()

    CLI(net)

    net.stop()