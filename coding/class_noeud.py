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
                 
class BGP(object):
	area = 'not defined'
	router_id = 'not defined'
	#bgp log-neighbor-changes
	
	def __init__(self):
		self.neighbors = []
		self.address_family = []
		self.json = {}
	def add_neighbor(self, ip, area, loopback):
		self.neighbors.append({'ip':ip,'area':area, 'loopback': loopback})
	def add_family(self, ip, activate, routemap):
		self.address_family.append({'ip':ip, 'activate':activate, 'route map':routemap})
	def to_json(self):
		self.json['neighbors'] = self.neighbors
		self.json['address_family'] = self.address_family
		self.json['area'] = self.area
		self.json['router_id'] = self.router_id
	def to_python(self,info):
		self.neighbors = info['neighbors']
		self.address_family = info['address_family']
		self.area = info['area']
		self.router_id = info['router_id']
                 
class RouteMap(object):
	process = 'not defined'
	access_list = 'not defined'
	local_preference = 'not defined'
	def __init__(self, name):
		self.name = name
		self.json = {}
	def to_json(self):
		self.json['name'] = self.name
		self.json['process'] = self.process
		self.json['access-list'] = self.access_list
		self.json['local_preference'] = self.local_preference
	def to_python(self,info):
		self.name = info['name']
		self.process = info['process']
		self.access_list = info['access-list']
		self.local_preference = info['local_preference']
		
class Routeur(object):
	router_bgp = 'not defined'
	ip_forward_protocol = 'not defined'
	ip_server = False
	ip_secure_server = False
	
	def __init__(self,name,number):
                self.name = name
                self.number = number
                self.neighbors = []
                self.interfaces = {}
                self.router_ospf = {}
                self.access_list = []
                self.route_map = []
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
                        new_interface.to_python(interfaces[interface])
                        interfaces[interface] = new_interface
	def bgp_to_json(self):
        	self.router_bgp.to_json()
        	self.router_bgp = self.router_bgp.json
	def bgp_to_python(self):
         	new_bgp = BGP()
         	new_bgp.to_json(self.router_bgp)
         	self.router_bgp = new_bgp
	def route_map_to_json(self):
		for map in range(len(self.route_map)):
        		self.route_map[map].to_json()
        		self.route_map[map] = self.route_map[map].json
	def route_map_to_python(self):
		for map in range(len(self.route_map)):
         		new_route_map = RouteMap(self.route_map[map]['name'])
         		new_route_map.to_python(self.route_map[map])
         		self.route_map[map] = new_route_map
	def set_router_ospf(self,process,router_id):
                self.router_ospf['process'] = process
                self.router_ospf['router id'] = router_id
	def to_json(self):
                self.json['name'] = self.name
                self.json['number'] = self.number
                self.json['neighbors'] = self.neighbors
                self.json['interfaces'] = self.interfaces
                self.json['router ospf'] = self.router_ospf
                self.json['router bgp'] = self.router_bgp
                self.json['access list'] = self.access_list
                self.json['route map'] = self.route_map
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
                self.access_list = info['access list']
                self.route_map = info['route map']
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
            

