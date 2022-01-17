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
	if noeud.name[:2] == 'CE':
		flag = 0
		for neighbor in noeud.neighbors.keys():
			if neighbor[:2] == 'PC' and flag == 0:
				flag = 1
				port = Interface('GigabitEthernet%s/0' %noeud.neighbors[neighbor]['port'][2:])
				port.ip_address =  '%s' %noeud.neighbors[neighbor]['ip']
				port.mask = '255.255.255.0'
				port.negotiation_auto = True
				noeud.interfaces[port.port] = port
			elif neighbor[:2] != 'PC':
				port = Interface('GigabitEthernet%s/0' %noeud.neighbors[neighbor]['port'][2:])
				port.ip_address = '%s' %noeud.neighbors[neighbor]['ip']
				port.mask = '255.255.255.0'
				port.negotiation_auto = True
				noeud.interfaces[port.port] = port
		
	else:
		for neighbor in noeud.neighbors.keys():
			port = Interface('GigabitEthernet%s/0'%noeud.neighbors[neighbor]['port'][2:])
			port.ip_address = '%s' %noeud.neighbors[neighbor]['ip']
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
			flag = 0
			for n in noeuds[noeud].neighbors.keys():
				if n[:2] == 'PC' and flag ==0:
					flag = 1
					bgp.add_family('192.168.%s.0' %noeuds[noeud].name[2:], False, False, None,False)
				elif n[:2] != 'PC':
					bgp.add_neighbor('%s' %noeuds[n].neighbors[noeud]['ip'], '%d' %int(noeuds[n].name[2:]), False)	
					bgp.add_family('%s' %noeuds[n].neighbors[noeud]['ip'], True, False, None,False)
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
					bgp.add_family('%d.%d.%d.%d' %(num,num,num,num), True, True, None,False)
				elif noeuds[n].name[:1] == 'P' and noeuds[n].name != noeuds[noeud].name:
					num = noeuds[n].number
					bgp.add_neighbor('%d.%d.%d.%d' %(num,num,num,num), 100, True)
					bgp.add_family('%d.%d.%d.%d' %(num,num,num,num), True, True, None,False)
				elif n in noeuds[noeud].neighbors.keys() and noeuds[n].name != noeuds[noeud].name:
					num = noeuds[n].name[2:]
					bgp.add_neighbor('%s' %noeuds[n].neighbors[noeud]['ip'], '1%.2d' %int(noeuds[n].name[2:]), False)
					
					routemap = RouteMap('RM_%s' %n[2:])
					routemap.process = 10
					access_list = {}
					access_list['name'] = int(n[2:])
					access_list['permit'] = []
					access_list['permit'].append('192.168.%s.0 0.0.0.255' %n[2:])
					noeuds[noeud].access_list.append(access_list)
					routemap.access_list = access_list['name']
					connect_type = noeuds[noeud].connect_type
					if n in connect_type.keys():
						if connect_type[n] == 'client':
							routemap.local_preference = 150
							routemap.community = 6553700
						elif connect_type[n] == 'peer':
							routemap.local_preference =100
							routemap.community = 6553800
						else:
							routemap.local_preference = 50
							routemap.community = 6553900
					noeuds[noeud].route_map.append(routemap)
					bgp.add_family('%s' %noeuds[n].neighbors[noeud]['ip'], False, False, routemap.name,'in')
					
			noeuds[noeud].router_bgp = bgp
		else:
			bgp = BGP()
			bgp.area = '100'
			for n in noeuds.keys():
				if noeuds[n].name[:1] == 'P' and noeuds[n].name != noeuds[noeud].name:
					num = noeuds[n].number
					bgp.add_neighbor('%d.%d.%d.%d' %(num,num,num,num), 100, True)
			noeuds[noeud].router_bgp = bgp
	return noeuds

def define_mpls(noeud):
	if noeud.name[:1] == 'P':
		for interface in noeud.interfaces.keys():
			if noeud.interfaces[interface].ip_address[:3] == '10.':
				noeud.interfaces[interface].mpls = 'ip'
	return noeud

def add_community_list(noeuds):
	for key in noeuds.keys():
		noeud = noeuds[key]
		if key[:2] == 'PE':
			noeuds[key].community_list.append({'name':1,'number':6553700})
			noeuds[key].community_list.append({'name':2,'number':6553800})
			noeuds[key].community_list.append({'name':3,'number':6553900})
			for k in noeud.connect_type.keys():
				routemap = RouteMap('RMout_%s' %k[2:])
				routemap.process = 20
				if noeud.connect_type[k] == 'peer':
					routemap.match_community.append(1)
					routemap.match_community.append(2)
				elif noeud.connect_type[k] == 'client':
					routemap.match_community.append(1)
					routemap.match_community.append(2)
					routemap.match_community.append(3)
				else:
					routemap.match_community.append(1)
				noeuds[key].route_map.append(routemap)
				noeuds[key].router_bgp.add_family('%s' %noeuds[k].neighbors[key]['ip'], False, False, routemap.name,'out')
	return noeuds
		
				
				
			