from ryu.base import app_manager
from ryu.controller import ofp_event
from ryu.controller.handler import CONFIG_DISPATCHER, MAIN_DISPATCHER
from ryu.controller.handler import set_ev_cls
from ryu.ofproto import ofproto_v1_3
from ryu.lib.packet import packet
from ryu.lib.packet import ethernet

class RingTopo(app_manager.RyuApp):
    avoid_dst =['ff:ff:ff:ff:ff:ff', '33:33:00:00:00:02']
    cutted=[6,7]
    OFP_VERSIONS = [ofproto_v1_3.OFP_VERSION]

    def __init__(self, *args, **kwargs):
        super(RingTopo, self).__init__(*args, **kwargs)
        # initialize mac address table.
        self.mac_to_port = {}
    
    #extends switch_fetaures_handler= set_ev_cls(extends switch_fetaures_handler)
    #So whenever you use a decorator, you actually pass a function into another function that returns a new version of it. Then you assign the new function to the original one.
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
        switch_id = datapath.id
        
        self.mac_to_port.setdefault(switch_id, {})

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
            self.logger.info("input port: P%s IN SWITCH S%s looking for %s",in_port,switch_id,dst)
        
        # learn a mac address to avoid FLOOD next time.
        self.mac_to_port[switch_id][src] = in_port


        # if the destination mac address is already learned,
        # decide which port to output the packet, otherwise FLOOD.
        
        #primo arco
        if(switch_id == 9 and in_port == 1):#se mi arriva da s1 (port 1) -> 
                out_port = 2
        elif(switch_id == 2 and in_port == 2):#same concept but backwards
            if dst == "00:00:00:00:00:02" or dst in self.avoid_dst:
                out_port = 1
            else:
                out_port = 2

        elif(switch_id == 1 and in_port == 1):#same concept but backwards
                out_port = 2
        
        #secondo arco
        elif(switch_id == 2 and in_port == 1):#same concept but backwards
                out_port = 2
        elif(switch_id == 9 and in_port == 2):#same concept but backwards
                out_port = 4
        elif(switch_id == 10 and in_port == 2):#same concept but backwards
                out_port = 1
        elif(switch_id == 8 and in_port == 4):#same concept but backwards
                out_port = 1
        elif(switch_id == 4 and in_port == 2):#same concept but backwards
            if dst == "00:00:00:00:00:04" or dst in self.avoid_dst:
                out_port = 1
            else:
                out_port = 2


        
        #terzo arco
        elif(switch_id == 4 and in_port == 1):#same concept but backwards
                out_port = 2
        elif(switch_id == 8 and in_port == 1):#same concept but backwards
                out_port = 2
        elif(switch_id == 5 and in_port == 2):#same concept but backwards
            if dst == "00:00:00:00:00:05" or dst in self.avoid_dst:
                out_port = 1
            else:
                out_port = 2




        #quarto arco
        elif(switch_id == 5 and in_port == 1):#same concept but backwards
                out_port = 2
        elif(switch_id == 8 and in_port == 2):#same concept but backwards
                out_port = 4
        elif(switch_id == 10 and in_port == 1):#same concept but backwards
                out_port = 2
        elif(switch_id == 9 and in_port == 4):#same concept but backwards
                out_port = 3
        elif(switch_id == 3 and in_port == 2):#same concept but backwards
            if dst == "00:00:00:00:00:03" or dst in self.avoid_dst:
                out_port = 1
            else:
                out_port = 2



         #quinto arco
        elif(switch_id == 3 and in_port == 1):#same concept but backwards
                out_port = 2
        elif(switch_id == 9 and in_port == 3):#same concept but backwards
                out_port = 1
        elif(switch_id == 1 and in_port == 2):#same concept but backwards
            if dst == "00:00:00:00:00:01" or dst in self.avoid_dst:
                out_port = 1
            else:
                out_port = 2
    
        #taglio il resto
        else:
            return
        


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
        mininet> pingall
        *** Ping: testing ping reachability
        h1 -> h2 h3 h4 h5 X X X
        h2 -> h1 h3 h4 h5 X X X
        h3 -> h1 h2 h4 h5 X X X
        h4 -> h1 h2 h3 h5 X X X
        h5 -> h1 h2 h3 h4 X X X
        h6 -> X X X X X X X
        h7 -> X X X X X X X
        h8 -> X X X X X X X
        *** Results: 64% dropped (20/56 received)
        '''
