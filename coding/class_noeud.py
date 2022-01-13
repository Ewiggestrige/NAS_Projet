class Interface(object):
         ip_address = 'not defined'
         mask = 'not defined'
         ospf = 'not defined'
         area = 'not defined'
         negotiation_auto = 'not defined'
 
         def __init__(self,port):
                 self.port = port
                 self.json = {}
         def to_json(self):
                 self.json['ip address'] = self.ip_address
                 self.json['mask'] = self.mask
                 self.json['ospf'] = self.ospf
                 self.json['area'] = self.area
                 self.json['negotiation auto'] = self.negotiation_auto
         def to_python(self,info):
                 self.ip_address = info['ip address']
                 self.mask = info['mask']
                 self.ip_ospf = info['ospf']
                 self.area = info['area']
                 self.negotiation_auto = into['negotiation auto']
class Routeur(object):
         ip_forward_protocol = 'not defined'
         ip_server = False
         ip_secure_server = False
         def __init__(self,name,number):
                 self.name = name
                 self.number = number
                 self.neighbors = []
                 self.interfaces = {}
                 self.router_ospf = {}
                 self.router_bgp = {}
                 self.json = {}
         def add_interface(self,port,info):
                 self.interface[port] = info
         def interfaces_to_json(self):
                 for interface in self.interfaces.keys():
                         self.interfaces[interface].to_json()
                         self.interfaces[interface] = self.interfaces[interface].json
         def interfaces_to_python(self):
                 for interface in self.interfaces.keys():
                         new_interface = Interface(interface)
                         new_interface.to_python(interfaces[interface].json)
                         interfaces[interface] = new_interface
         def set_router_ospf(self,process,router_id):
                 self.router_ospf['process'] = process
                 self.router_ospf['router id'] = router_id
         def get_router_bgp(self):
                 print(self.router_bgp) # area,router-id, log-neighbor-changes, neighbor, remote-as, address-family{network,neighbor,activate},exit-address-family
         def to_json(self):
                 self.json['name'] = self.name
                 self.json['number'] = self.number
                 self.json['neighbors'] = self.neighbors
                 self.json['interfaces'] = self.interfaces
                 self.json['router ospf'] = self.router_ospf
                 self.json['router bgp'] = self.router_bgp
                 self.json['ip forward-protocol'] = self.ip_forward_protocol
                 self.json['ip http server'] = self.ip_server
                 self.json['ip http secure-server'] = self.ip_secure_server

         def to_python(self,info):
                 self.name = info['name']
                 self.number = info['number']
                 self.neighbors = info['neighbors']
                 self.interfaces = info['interfaces']
                 self.router_ospf = info['router ospf']
                 self.router_bgp = info['router bgp']
                 self.ip_forward_protocol = info['ip forward-protocol']
                 self.ip_server = info['ip http server']
                 self.ip_secure_server = info['ip http secure-server']
class Client(object):
        ip = 'not defined'
        gateway = 'not defined'
        mask = 'not defined'
        def __init__(self, name, router):
                 self.name = name
                 self.router = router
                 self.json = {}
        def to_json(self):
                 self.json['pcname'] = self.name
                 self.json['router'] = self.router
                 self.json['ip'] = self.ip
                 self.json['gateway'] = self.gateway
                 self.json['mask'] = self.mask
        def to_python(self, info):
                 self.name = info['pcname']
                 self.ip = info['ip']
                 self.router = info['router']
                 self.gateway = info['gateway']
                 self.mask = info['mask']
            

