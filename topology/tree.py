from ryu.base import app_manager
from ryu.controller import ofp_event
from ryu.controller.handler import CONFIG_DISPATCHER, MAIN_DISPATCHER
from ryu.controller.handler import set_ev_cls
from ryu.ofproto import ofproto_v1_3
from ryu.lib.packet import packet
from ryu.lib.packet import ethernet

class StarTopo(app_manager.RyuApp):
    avoid_dst =['ff:ff:ff:ff:ff:ff', '33:33:00:00:00:02']
    OFP_VERSIONS = [ofproto_v1_3.OFP_VERSION]

    def __init__(self, *args, **kwargs):
        super(StarTopo, self).__init__(*args, **kwargs)
        # initialize mac address table.
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

        # construct flow_mod message and send it.
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
        dpid = datapath.id
        
        self.mac_to_port.setdefault(dpid, {})

        # analyse the received packets using the packet library.
        pkt = packet.Packet(msg.data)
        eth_pkt = pkt.get_protocol(ethernet.ethernet)
        dst = eth_pkt.dst
        src = eth_pkt.src

        # get the received port number from packet_in message.
        #print(vars(msg))
        in_port = msg.match['in_port']
        #out_port = msg.match['out_port']
        

        for x in datapath.ports:
            conf=datapath.ports[x].config
            break

        if(dst not in self.avoid_dst):
            self.logger.info("input port: P%s IN SWITCH S%s looking for %s",in_port,dpid,dst)
        
        # learn a mac address to avoid FLOOD next time.
        self.mac_to_port[dpid][src] = in_port

        # if the destination mac address is already learned,
        # decide which port to output the packet, otherwise FLOOD.
        if(dpid == 9 and in_port == 4):
            if dst in self.mac_to_port[dpid]:
                out_port = self.mac_to_port[dpid][dst]
            else:
                out_port = ofproto.OFPP_FLOOD
                out_port = 1
        elif(dpid == 9 and in_port == 1):
            if dst in self.mac_to_port[dpid]:
                out_port = self.mac_to_port[dpid][dst]
            else:
                out_port = 4
        elif(dpid == 2 or dpid == 3):
            return
        else:
            if dst in self.mac_to_port[dpid]:
                out_port = self.mac_to_port[dpid][dst]
            else:
                out_port = ofproto.OFPP_FLOOD

        # construct action list.
        actions = [parser.OFPActionOutput(out_port)]

        # install a flow to avoid packet_in next time.
        if out_port != ofproto.OFPP_FLOOD:
            match = parser.OFPMatch(in_port=in_port, eth_dst=dst)
            self.add_flow(datapath, 1, match, actions)

        # construct packet_out message and send it.
        out = parser.OFPPacketOut(datapath=datapath,
                                  buffer_id=ofproto.OFP_NO_BUFFER,
                                  in_port=in_port, actions=actions,
                                  data=msg.data)
        datapath.send_msg(out)

        '''
        >h1 ping h2
        self.logger.info("input port: P%s IN SWITCH S%s looking for %s",in_port,dpid,dst)
        
        cerca h1 partendo da h2 (non so perche` al contrario)
        input port: P1 IN SWITCH S4 looking for 00:00:00:00:00:01
        input port: P1 IN SWITCH S8 looking for 00:00:00:00:00:01
        input port: P1 IN SWITCH S16 looking for 00:00:00:00:00:01
        input port: P4 IN SWITCH S9 looking for 00:00:00:00:00:01
        input port: P2 IN SWITCH S1 looking for 00:00:00:00:00:01
        #lo trova e ora torna in dietro
        input port: P1 IN SWITCH S1 looking for 00:00:00:00:00:04
        input port: P1 IN SWITCH S9 looking for 00:00:00:00:00:04
        input port: P2 IN SWITCH S16 looking for 00:00:00:00:00:04
        input port: P4 IN SWITCH S8 looking for 00:00:00:00:00:04
        input port: P2 IN SWITCH S4 looking for 00:00:00:00:00:04

        pingall:
        mininet> pingall
        *** Ping: testing ping reachability
        h1 -> X X h4 h5 h6 h7 h8
        h2 -> X X X X X X X
        h3 -> X X X X X X X
        h4 -> h1 X X h5 h6 h7 h8
        h5 -> h1 X X h4 h6 h7 h8
        h6 -> h1 X X h4 h5 h7 h8
        h7 -> h1 X X h4 h5 h6 h8
        h8 -> h1 X X h4 h5 h6 h7
        *** Results: 46% dropped (30/56 received)



        '''
