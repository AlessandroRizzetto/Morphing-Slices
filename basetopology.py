from mininet.topo import Topo
from mininet.net import Mininet
from mininet.log import setLogLevel
from mininet.cli import CLI
from mininet.node import OVSKernelSwitch, Controller, RemoteController

class RoutingTopo(Topo):
    def __init__(self):
        # Initialize topology
        Topo.__init__(self)

        # Create template host, switch, and link
        host_config = dict(inNamespace=True)
        host_link_config = dict()

        # Create switch nodes
        for i in range(10):
            #sconfig = {"dpid": "%016x" % (i + 1)}
            sconfig = {"dpid": "00:00:00:00:00:"+str(i + 1)}
            self.addSwitch("s%d" % (i + 1), **sconfig)

        # Create host (not the 5 & 7, for not possible)
        for i in range(8):
            host_config = {"dpid": "00:00:00:00:00:0"+str(i+1)}
            self.addHost("h%d" % (1+i), **host_config)

        # Add host links
        self.addLink("h1", "s1", **host_link_config)
        self.addLink("h2", "s2", **host_link_config)
        self.addLink("h3", "s3", **host_link_config)
        self.addLink("h4", "s4", **host_link_config)
        self.addLink("h5", "s5", **host_link_config)
        self.addLink("h6", "s6", **host_link_config)
        self.addLink("h7", "s7", **host_link_config)
        self.addLink("h8", "s7", **host_link_config)

        # Add switch links        
        self.addLink("s1", "s9", **host_link_config)
        self.addLink("s2", "s9", **host_link_config)
        self.addLink("s3", "s9", **host_link_config)
        self.addLink("s9", "s10", **host_link_config)
        self.addLink("s10", "s8", **host_link_config)
        self.addLink("s8", "s4", **host_link_config)
        self.addLink("s8", "s5", **host_link_config)
        self.addLink("s8", "s6", **host_link_config)
        self.addLink("s6", "s7", **host_link_config)




        '''
        h1 - eth0 <-> s1 - eth1  
        h2 - eth0 <-> s2 - eth1  
        h3 - eth0 <-> s3 - eth1  
        h4 - eth0 <-> s4 - eth1  
        h5 - eth0 <-> s5 - eth1  
        h6 - eth0 <-> s6 - eth1  
        s1 - eth2 <-> s6 - eth2  
        s2 - eth2 <-> s5 - eth2  
        s3 - eth2 <-> s5 - eth3  
        s4 - eth2 <-> s6 - eth3  
        s5 - eth4 <-> s6 - eth4 
        '''


topos = {'RoutingTopo': (lambda: RoutingTopo() )}     
        
if __name__ == "__main__":
    topo = RoutingTopo()
    net = Mininet(topo=topo,switch=OVSKernelSwitch, controller=RemoteController, build=False,autoSetMacs=True)
    controller = RemoteController("c1", ip="127.0.0.1")
    net.start()

    CLI(net)
    net.stop()

