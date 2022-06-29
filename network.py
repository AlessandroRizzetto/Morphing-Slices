from mininet.topo import Topo
from mininet.net import Mininet
from mininet.log import setLogLevel
from mininet.cli import CLI
from mininet.node import OVSSwitch, Controller, RemoteController

class RoutingTopo(Topo):
    def __init__(self):
        # Initialize topology
        Topo.__init__(self)

        # Create template host, switch, and link
        host_config = dict(inNamespace=True)
        host_link_config = dict()

        # Create switch nodes
        for i in range(6):
            sconfig = {"dpid": "%016x" % (i + 1)}
            self.addSwitch("s%d" % (i + 1), **sconfig)

        # Create host nodes
        for i in range(12):
            self.addHost("h%d" % (i + 1), **host_config)

        # Add switch links
        self.addLink("s1", "s2", **host_link_config)
        self.addLink("s1", "s6", **host_link_config)
        self.addLink("s1", "s5", **host_link_config)
        self.addLink("s2", "s1", **host_link_config)
        self.addLink("s2", "s5", **host_link_config)
        self.addLink("s3", "s5", **host_link_config)
        self.addLink("s4", "s5", **host_link_config)
        self.addLink("s4", "s6", **host_link_config)
        self.addLink("s5", "s1", **host_link_config)
        self.addLink("s5", "s2", **host_link_config)
        self.addLink("s5", "s3", **host_link_config)
        self.addLink("s5", "s4", **host_link_config)
        self.addLink("s5", "s6", **host_link_config)
        self.addLink("s6", "s1", **host_link_config)
        self.addLink("s6", "s4", **host_link_config)
        self.addLink("s6", "s5", **host_link_config)

        # Add host links
        self.addLink("h1", "s1", **host_link_config)
        self.addLink("h2", "s1", **host_link_config)
        self.addLink("h3", "s2", **host_link_config)
        self.addLink("h4", "s2", **host_link_config)
        self.addLink("h5", "s3", **host_link_config)
        self.addLink("h6", "s4", **host_link_config)
        self.addLink("h7", "s4", **host_link_config)
        self.addLink("h8", "s4", **host_link_config)
        self.addLink("h9", "s5", **host_link_config)
        self.addLink("h10", "s6", **host_link_config)
        self.addLink("h11", "s6", **host_link_config)
        self.addLink("h12", "s6", **host_link_config)
        
if __name__ == "__main__":
    topo = RoutingTopo()
    net = Mininet(topo=topo, controller=RemoteController, build=False)
    controller = RemoteController("c1", ip="127.0.0.1")
    net.start()

    CLI(net)
    net.stop()

