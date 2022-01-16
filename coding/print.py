import json
filename = 'topologie.json'

with open(filename) as f:
	file = f.read()

noeuds = file.split('!')
routers = json.loads(noeuds[0])
pcs = json.loads(noeuds[1])

#create router files
for router_key in routers.keys():
	router = routers[router_key]
	fc = open('./config/%s_startup_config.cfg' %router['name'],'w')
	fc.write('!\n\n!\n')
	fc.write('version 15.2\n')
	fc.write('service timestamps debug datetime msec\n')
	fc.write('service timestamps log datetime msec\n!\n')
	fc.write('hostname %s\n!\n' %router['name'])
	fc.write('boot-start-marker\nboot-end-marker\n!\n!\n!\n')
	fc.write('no aaa new-model\nno ip icmp rate-limit unreachable\nip cef\n!\n!\n!\n!\n!\n!\n')
	fc.write('no ip domain lookup\nno ipv6 cef\n!\n!\n')
	fc.write('multilink bundle-name authenticated\n!\n!\n!\n!\n!\n!\n!\n!\n!\n')
	fc.write('ip tcp synwait-time 5\n!\n!\n!\n!\n!\n!\n!\n!\n!\n!\n!\n!\n')
	
	#interfaces
	interfaces = router['interfaces']
	for interface in interfaces.keys():
		info = interfaces[interface]
		fc.write('interface %s\n' %interface)
		fc.write(' ip address %s %s\n' %(info['ip address'],info['mask']))
		if info['ospf'] != 'not defined':
			fc.write(' ip ospf %s area %s\n' %(info['ospf'],info['area']))
		if info['negotiation auto'] != 'not defined':
			fc.write(' negotiation auto\n')
		if info['mpls'] != 'not defined':
			fc.write(' mpls ip\n')
		fc.write('!\n')
	
	#ospf
	if router['router ospf'] != {}:
		ospf = router['router ospf']
		fc.write('router ospf %s\n' %ospf['process'])
		fc.write(' router-id %s\n' %ospf['router id'])
		for port in ospf['passive']:
			fc.write(' passive-interface %s\n' %port)
		fc.write('!\n')
	
	#bgp
	if router['router bgp'] !={}:
		bgp = router['router bgp']
		fc.write('router bgp %s\n' %bgp['area'])
		fc.write(' bgp router-id %s\n' %bgp['router_id'])
		fc.write(' bpg log-neighbor-changes\n')
		for neighbor in bgp['neighbors']:
			fc.write(' neighbor %s remote-as %s\n' %(neighbor['ip'],neighbor['area']))
			if neighbor['loopback'] == True:
				fc.write(' neighbor %s update-source Loopback0\n' %(neighbor['ip']))
		if bgp['address_family']!=[]:
			fc.write(' !\n')
			fc.write(' address-family ipv4\n')
		for address in bgp['address_family']:
			if address['activate'] == True:
				fc.write('  neighbor %s activate\n' %address['ip'])
			if address['send_community'] == True:
				fc.write('  neighbor %s send-community\n' %address['ip'])
			if address['route map'] != None:
				fc.write('  neighbor %s route-map %s in\n' %(address['ip'],address['route map']))
				#out to be added
		fc.write(' exit-address-family\n')
		fc.write('!\n')
		
	#constant
	fc.write('ip forward-protocol nd\n!\n!\n')
	fc.write('no ip http server\n')
	fc.write('no ip http secure-server\n!\n')
	
	#access list
	
	#
	fc.write('control-plane\n!\n!\n')
	fc.write('line con 0\n')
	fc.write(' exec-timeout 0 0\n')
	fc.write(' privilege level 15\n')
	fc.write(' logging synchronous\n')
	fc.write(' stopbits 1\n')
	fc.write('line aux 0')
	fc.write(' exec-timeout 0 0\n')
	fc.write(' privilege level 15\n')
	fc.write(' logging synchronous\n')
	fc.write(' stopbits 1\n')
	fc.write('line vty 0 4\n')
	fc.write(' login\n')
	fc.write('!\n!\nend\n')
			
	fc.close()
	