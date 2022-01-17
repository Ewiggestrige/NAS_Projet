class Interface(object):
         ip_address = 'not defined'
         mask = 'not defined'
         ospf = 'not defined'
         area = 'not defined'
         negotiation_auto = 'not defined'
         mpls = 'not defined'
 
         def __init__(self,port):
                 self.port = port
                 self.json = {}
         def to_json(self):
                 self.json['ip address'] = self.ip_address
                 self.json['mask'] = self.mask
                 self.json['ospf'] = self.ospf
                 self.json['area'] = self.area
                 self.json['negotiation auto'] = self.negotiation_auto
                 self.json['mpls'] = self.mpls
         def to_python(self,info):
                 self.ip_address = info['ip address']
                 self.mask = info['mask']
                 self.ip_ospf = info['ospf']
                 self.area = info['area']
                 self.negotiation_auto = info['negotiation auto']
                 self.mpls = info['mpls']
                 
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
	def add_family(self, ip, activate,sc, routemap, status):
		self.address_family.append({'ip':ip, 'activate':activate,'send-community':sc, 'route map':routemap, 'status':status})
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
	community = 'not defined'
	def __init__(self, name):
		self.name = name
		self.match_community = []
		self.json = {}
	def to_json(self):
		self.json['name'] = self.name
		self.json['process'] = self.process
		self.json['access-list'] = self.access_list
		self.json['local_preference'] = self.local_preference
		self.json['community'] = self.community
		self.json['match_community'] = self.match_community
	def to_python(self,info):
		self.name = info['name']
		self.process = info['process']
		self.access_list = info['access-list']
		self.local_preference = info['local_preference']
		self.community = info['community']
		self.match_community = info['match_community']
		
class Routeur(object):
	router_type = 'not defined'
	router_bgp = 'not defined'
	
	def __init__(self,name,number):
                self.name = name
                self.number = number
                self.neighbors = {}
                self.connect_type = {}
                self.interfaces = {}
                self.router_ospf = {}
                self.access_list = []
                self.community_list = []
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
                self.router_ospf['passive'] = []
	def add_passive_ospf(self,passive_port):
		self.router_ospf['passive'].append(passive_port)
	def to_json(self):
                self.json['name'] = self.name
                self.json['number'] = self.number
                self.json['router_type'] = self.router_type
                self.json['neighbors'] = self.neighbors
                self.json['connect type'] = self.connect_type
                self.json['interfaces'] = self.interfaces
                self.json['router ospf'] = self.router_ospf
                self.json['router bgp'] = self.router_bgp
                self.json['access list'] = self.access_list
                self.json['community_list'] = self.community_list
                self.json['route map'] = self.route_map
	def to_python(self,info):
                self.name = info['name']
                self.number = info['number']
                self.router_type = info['router_type']
                self.neighbors = info['neighbors']
                self.connect_type = info['connect type']
                self.interfaces = info['interfaces']
                self.router_ospf = info['router ospf']
                self.router_bgp = info['router bgp']
                self.access_list = info['access list']
                self.community_list = info['community_list']
                self.route_map = info['route map']

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
            

