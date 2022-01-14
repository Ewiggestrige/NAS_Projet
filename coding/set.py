import os
import json
from class_noeud import *

def define_port(noeud):	
	#Define Loopback
	port = Interface('Loopback0')
	num = noeud.number
	port.ip_address = '%d.%d.%d.%d' % (num,num,num,num)
	port.mask = '255.255.255.255'
	noeud.interfaces[port.port] = port
	
	#Define other ports
	n_port = 1
	if noeud.name[:2] == 'CE':
		#Between PC and CE
		port = Interface('GigabitEthernet%d/0' %n_port)
		n_port = n_port + 1
		port.ip_address = '192.168.%s.1' % noeud.name[2:]
		port.mask = '255.255.255.0'
		port.negotiation_auto = True
		noeud.interfaces[port.port] = port

		#Between CE and PE
		port = Interface('GigabitEthernet%d/0' %n_port)
		n_port = n_port + 1
		port.ip_address = '172.16.%s.1' % noeud.name[2:]
		port.mask = '255.255.255.0'
		port.negotiation_auto = True
		noeud.interfaces[port.port] = port
		
	else:
		for neighbor in noeud.neighbors:
			port = Interface('GigabitEthernet%d/0'%n_port)
			n_port = n_port+1
			if noeud.name[:2] == 'PE' or noeud.name[:2] == 'CE':
				num_noeud = int(noeud.name[2:])
			else:
				num_noeud = int(noeud.name[1:])
			if neighbor[:2] == 'PE' or neighbor[:2] == 'CE':
				num_neighbor = int(neighbor[2:])
			else:
				num_neighbor = int(neighbor[1:])

			if neighbor[:2] == 'CE':
				port.ip_address = '172.168.%s.2' % neighbor[2:]
			elif noeud.name[:2] == 'PE' and neighbor[:2] == 'PE':
				if num_noeud < num_neighbor:
					port.ip_address = '10.1%.2d.1%.2d.1' %(num_noeud,num_neighbor)
				else:
					port.ip_address = '10.1%.2d.1%.2d.2' %(num_neighbor,num_noeud)
			elif noeud.name[:2] == 'PE':
				port.ip_address = '10.1%.2d.%d.1' %(num_noeud,num_neighbor)
			elif neighbor[:2] == 'PE':
				port.ip_address = '10.1%.2d.%d.2' %(num_neighbor,num_noeud)
			else:
				if num_noeud < num_neighbor:
					port.ip_address = '10.%d.%d.1' %(num_noeud,num_neighbor)
				else:
					port.ip_address = '10.%d.%d.2' %(num_neighbor,num_noeud)
			port.mask = '255.255.255.0'
			port.negotiation_auto = True
			noeud.interfaces[port.port] = port
	return noeud

def define_pc(client):
	num_client = client.name[2:]
	num_router = client.router[2:] 
	client.ip = '192.168.%s.%s' %(num_router,num_client)
	client.gateway = '192.168.%s.1' %num_router
	client.mask = '255.255.255.0'
	return client		
		
def define_ospf(noeud):
	#define ospf process
	if noeud.name[:2]!='CE':
		noeud.set_router_ospf(10,('%d.%d.%d.%d') %(noeud.number,noeud.number,noeud.number,noeud.number))
		for intf in noeud.interfaces.keys():
			noeud.interfaces[intf].ospf = 10
			noeud.interfaces[intf].area = 0
			if noeud.interfaces[intf].ip_address[:3] == '172':
				 noeud.add_passive_ospf(intf)
	return noeud

def define_bgp(noeuds):
	for noeud in noeuds.keys():
		if noeuds[noeud].name[:2] == 'CE':
			bgp = BGP()
			bgp.area = '1%.2d' %int(noeuds[noeud].name[2:])
			num = noeuds[noeud].number
			bgp.router_id = '%d.%d.%d.%d' %(num,num,num,num)
			bgp.add_neighbor('172.168.%s.2' %noeuds[noeud].name[2:], '%d' %int(noeuds[noeud].name[2:]), False)
			bgp.add_family('192.168.%s.0' %noeuds[noeud].name[2:], False, None)
			bgp.add_family('172.168.%s.2' %noeuds[noeud].name[2:], True, None)
			noeuds[noeud].router_bgp = bgp
		elif noeuds[noeud].name[:2] == 'PE':
			bgp = BGP()
			bgp.area = '100'
			num = noeuds[noeud].number
			bgp.router_id = '%d.%d.%d.%d' %(num,num,num,num)
			
			for n in noeuds.keys():
				if noeuds[n].name[:2] == 'PE' and noeuds[n].name != noeuds[noeud].name:
					num = noeuds[n].number
					bgp.add_neighbor('%d.%d.%d.%d' %(num,num,num,num), 100, True)
					bgp.add_family('%d.%d.%d.%d' %(num,num,num,num), True, None)
				elif noeuds[n].name[:1] == 'P' and noeuds[n].name != noeuds[noeud].name:
					num = noeuds[n].number
					bgp.add_neighbor('%d.%d.%d.%d' %(num,num,num,num), 100, True)
					bgp.add_family('%d.%d.%d.%d' %(num,num,num,num), True, None)
				elif n in noeuds[noeud].neighbors and noeuds[n].name != noeuds[noeud].name:
					num = noeuds[n].name[2:]
					bgp.add_neighbor('172.168.%s.1' %noeuds[noeud].name[2:], '1%.2d' %int(noeuds[noeud].name[2:]), False)
					
					routemap = RouteMap('RM_%s' %n)
					access_list = {}
					access_list['name'] = 1
					access_list['permit'] = []
					access_list['permit'].append('192.168.%s.0 0.0.0.255' %noeuds[noeud].name[2:])
					noeuds[noeud].access_list.append(access_list)
					routemap.process = 10
					routemap.access_list = access_list['name']
					connect_type = noeuds[noeud].connect_type
					if n in connect_type.keys():
						if connect_type[n] == 'client':
							routemap.local_preference = 150
						elif connect_type[n] == 'peer':
							routemap.local_preference =100
						else:
							routemap.local_preference = 50
					noeuds[noeud].route_map.append(routemap)
					bgp.add_family('172.168.%s.0' %noeuds[noeud].name[2:], False, routemap.name)
			noeuds[noeud].router_bgp = bgp
		else:
			bgp = BGP()
			bgp.area = '100'
			for n in noeuds.keys():
				if noeuds[n].name[:1] == 'P' and noeuds[n].name != noeuds[noeud].name:
					num = noeuds[n].number
					bgp.add_neighbor('%d.%d.%d.%d' %(num,num,num,num), 100, True)
					#bgp.add_family('%d.%d.%d.%d' %(num,num,num,num), True, None)
			noeuds[noeud].router_bgp = bgp
	return noeuds

def define_mpls(noeud):
	if noeud.name[:1] == 'P':
		for interface in noeud.interfaces.keys():
			if noeud.interfaces[interface].ip_address[:3] == '10.':
				noeud.interfaces[interface].mpls = 'ip'
	return noeud
			