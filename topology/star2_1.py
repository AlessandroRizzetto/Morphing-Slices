from ryu.base import app_manager
from ryu.controller import ofp_event
from ryu.controller.handler import CONFIG_DISPATCHER, MAIN_DISPATCHER
from ryu.controller.handler import set_ev_cls
from ryu.ofproto import ofproto_v1_3
from ryu.lib.packet import packet
from ryu.lib.packet import ethernet

class StarTopo(app_manager.RyuApp):
    avoid_dst =['ff:ff:ff:ff:ff:ff', '33:33:00:00:00:02','33:33:00:00:00:16']
    OFP_VERSIONS = [ofproto_v1_3.OFP_VERSION]
    cutted =[2,3,7]
    def __init__(self, *args, **kwargs):
        super(StarTopo, self).__init__(*args, **kwargs)

        self.mac_to_port = {}

    @set_ev_cls(ofp_event.EventOFPSwitchFeatures, CONFIG_DISPATCHER)
    def switch_features_handler(self, ev):
        datapath = ev.msg.datapath
        ofproto = datapath.ofproto
        parser = datapath.ofproto_parser

        # install the table-miss flow entry.
        match = parser.OFPMatch()
        actions = [parser.OFPActionOutput(ofproto.OFPP_CONTROLLER,
                                          ofproto.OFPCML_NO_BUFFER)]
        self.add_flow(datapath, 0, match, actions)

    def add_flow(self, datapath, priority, match, actions):
        ofproto = datapath.ofproto
        parser = datapath.ofproto_parser


        inst = [parser.OFPInstructionActions(ofproto.OFPIT_APPLY_ACTIONS,
                                             actions)]
        mod = parser.OFPFlowMod(datapath=datapath, priority=priority,
                                match=match, instructions=inst)
        datapath.send_msg(mod)

    @set_ev_cls(ofp_event.EventOFPPacketIn, MAIN_DISPATCHER)
    def _packet_in_handler(self, ev):
        msg = ev.msg
        datapath = msg.datapath
        ofproto = datapath.ofproto
        parser = datapath.ofproto_parser
       
        # SWITCH ID.
        switch_id = datapath.id

        self.mac_to_port.setdefault(switch_id, {})

        # packet analysis
        pkt = packet.Packet(msg.data)
        eth_pkt = pkt.get_protocol(ethernet.ethernet)
        dst = eth_pkt.dst
        src = eth_pkt.src

        # packet ingress port
        in_port = msg.match['in_port']

        for x in datapath.ports:
            conf=datapaath.ports[x].config
            break

        if(dst not in self.avoid_dst):from ryu.base import app_manager
from ryu.controller import ofp_event
from ryu.controller.handler import CONFIG_DISPATCHER, MAIN_DISPATCHER
from ryu.controller.handler import set_ev_cls
from ryu.ofproto import ofproto_v1_3
from ryu.lib.packet import packet
from ryu.lib.packet import ethernet

class TreeTopo(app_manager.RyuApp):
    avoid_dst =['ff:ff:ff:ff:ff:ff', '33:33:00:00:00:02','33:33:00:00:00:16']
    save_dst =['00:00:00:00:00:01','00:00:00:00:00:02','00:00:00:00:00:03','00:00:00:00:00:04' ,'00:00:00:00:00:05' ,'00:00:00:00:00:06' ,'00:00:00:00:00:07' ,'00:00:00:00:00:08' ]
    OFP_VERSIONS = [ofproto_v1_3.OFP_VERSION]
    cutted =[2,3,7]
    def __init__(self, *args, **kwargs):
        super(TreeTopo, self).__init__(*args, **kwargs)

        self.mac_to_port = {}

    @set_ev_cls(ofp_event.EventOFPSwitchFeatures, CONFIG_DISPATCHER)
    def switch_features_handler(self, ev):
        datapath = ev.msg.datapath
        ofproto = datapath.ofproto
        parser = datapath.ofproto_parser

        # install the table-miss flow entry.
        match = parser.OFPMatch()
        actions = [parser.OFPActionOutput(ofproto.OFPP_CONTROLLER,
                                          ofproto.OFPCML_NO_BUFFER)]
        self.add_flow(datapath, 0, match, actions)

    def add_flow(self, datapath, priority, match, actions):
        ofproto = datapath.ofproto
        parser = datapath.ofproto_parser


        inst = [parser.OFPInstructionActions(ofproto.OFPIT_APPLY_ACTIONS,
                                             actions)]
        mod = parser.OFPFlowMod(datapath=datapath, priority=priority,
                                match=match, instructions=inst)
        datapath.send_msg(mod)

    @set_ev_cls(ofp_event.EventOFPPacketIn, MAIN_DISPATCHER)
    def _packet_in_handler(self, ev):
        msg = ev.msg
        datapath = msg.datapath
        ofproto = datapath.ofproto
        parser = datapath.ofproto_parser

        # SWITCH ID.
        switch_id = datapath.id

        self.mac_to_port.setdefault(switch_id, {})

        # packet analysis
        pkt = packet.Packet(msg.data)
        eth_pkt = pkt.get_protocol(ethernet.ethernet)
        dst = eth_pkt.dst
        src = eth_pkt.src

        # packet ingress port
        #print(vars(msg))
        in_port = msg.match['in_port']
        #out_port = msg.match['out_port']


        for x in datapath.ports:
            conf=datapath.ports[x].config
            break

        if(dst not in self.avoid_dst and switch_id not in self.cutted):
            self.logger.info("input port: P%s IN SWITCH S%s looking for %s",in_port,switch_id,dst)

        # learn a mac address to avoid FLOOD next time.
        self.mac_to_port[switch_id][src] = in_port

        # if the destination mac address is already learned,
        # decide which port to output the packet, otherwise FLOOD.
        # if the destination mac address is already learned,
        # decide which port to output the packet, otherwise FLOOD.
        x = 1
        y = 4
        a = 3
        b = 1
        
        if(switch_id in self.cutted):#removed branches, dropping the packet
            return
            


        if(switch_id == 1 and in_port != y):#s1
                if dst in self.mac_to_port[switch_id]:
                    out_port = self.mac_to_port[switch_id][dst]
                    print (self.mac_to_port[switch_id][dst])
                else:
                    out_port = y

        elif((switch_id == 4 or switch_id == 5 or switch_id == 6) and in_port != a):#s4 s5 s6
                if dst in self.mac_to_port[switch_id]:
                    out_port = self.mac_to_port[switch_id][dst]
                else:
                    out_port = a
            

       
        elif (switch_id == 8):#central switch rules      
            out_port = ofproto.OFPP_FLOOD
            if (out_port == in_port):
                if (in_port == y):
                    z = x
                    x = y
                    y = z
                else:
                    c = a
                    a = b
                    b = c
        
        else:
                out_port = ofproto.OFPP_FLOOD





        actions = [parser.OFPActionOutput(out_port)]

        # install a flow to avoid packet_in next time.
        if out_port != ofproto.OFPP_FLOOD and  dst in self.save_dst:
            match = parser.OFPMatch(in_port=in_port, eth_dst=dst)
            self.add_flow(datapath, 1, match, actions)

        # building the packet out
        out = parser.OFPPacketOut(datapath=datapath,
                                  buffer_id=ofproto.OFP_NO_BUFFER,
                                  in_port=in_port, actions=actions,
                                  data=msg.data)
        datapath.send_msg(out)
            self.logger.info("input port: P%s IN SWITCH S%s looking for %s",in_port,switch_id,dst)

        # learn a mac address to avoid FLOOD next time.
        self.mac_to_port[switch_id][src] = in_port

        # if the destination mac address is already learned,
        # decide which port to output the packet, otherwise FLOOD.
        
        x = 1
        y = 4
        a = 3
        b = 1
        
	if(switch_id in self.cutted):#removed branches, dropping the packet
            return
        


	if(switch_id == 1 and in_port != y):#s1
            if dst in self.mac_to_port[switch_id]:
                out_port = self.mac_to_port[switch_id][dst]
                print (self.mac_to_port[switch_id][dst])
            else:
                out_port = y

        elif((switch_id == 4 or switch_id == 5 or switch_id == 6) and in_port != a):#s4 s5 s6
            if dst in self.mac_to_port[switch_id]:
                out_port = self.mac_to_port[switch_id][dst]
            else:
                out_port = a
        
        
        
'''
        if(switch_id > 8 and in_port != 1):#added switch
            if dst in self.mac_to_port[switch_id]:
                out_port = self.mac_to_port[switch_id][dst]
            else:
                out_port = 1

'''        
        elif (switch_id == 8):#central switch rules
            if dst in self.mac_to_port[switch_id]:
                out_port = self.mac_to_port[switch_id][dst]
            else:
                out_port = ofproto.OFPP_FLOOD
                if (out_port == in_port):
                    if (in_port == y):
                        z = x
                        x = y
                        y = z
                    else:
                        c = a
                        a = b
                        b = c
        
        else:
                out_port = ofproto.OFPP_FLOOD
        

        actions = [parser.OFPActionOutput(out_port)]

        # install a flow to avoid packet_in next time.
        if out_port != ofproto.OFPP_FLOOD:
            match = parser.OFPMatch(in_port=in_port, eth_dst=dst)
            self.add_flow(datapath, 1, match, actions)

        # building the packet out
        out = parser.OFPPacketOut(datapath=datapath,
                                  buffer_id=ofproto.OFP_NO_BUFFER,
                                  in_port=in_port, actions=actions,
                                  data=msg.data)
        datapath.send_msg(out)
