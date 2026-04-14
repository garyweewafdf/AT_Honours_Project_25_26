from mininet.topo import Topo
from mininet.net import Mininet
from mininet.node import RemoteController, OVSSwitch
from mininet.link import Intf
from mininet.log import setLogLevel


class MyTopo(Topo):
    def build(self):
        h1 = self.addHost("h1", ip="192.168.100.200/24")
        s1 = self.addSwitch("s1")
        s2 = self.addSwitch("s2") # Switch Attacker VM (192.168.100.200) is connected to
        self.addLink(h1, s1)
        self.addLink(s1, s2)

def run():
    topo = MyTopo()

    net = Mininet(
        topo=topo,
        switch=lambda name, **kwargs: OVSSwitch(name, protocols="OpenFlow13", **kwargs), # use OpenFlow v1.3 for switch communications
        controller=None, # do not use provided internal switches
        autoSetMacs=True
    )

    ryu = RemoteController('ryu', ip='10.0.0.105', port=6653) # 10.0.0.105 (RYU VM) used for SDN controller (port 6653 is RYU listening port)
    net.addController(ryu)

    net.start()
    Intf('enp0s8', node=net.get('s2')) # attach enp0s8 (layer 2 link) to switch 2 (connecting s2 to Attacker VM)
    net.interact() # Enter Mininet CLI

if __name__ == '__main__':
    setLogLevel('info')
    run()
