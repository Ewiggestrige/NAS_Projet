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
		noeud.interfaces[port.port] = port

		#Between CE and PE
		port = Interface('GigabitEthernet%d/0' %n_port)
		n_port = n_port + 1
		port.ip_address = '172.16.%s.1' % noeud.name[2:]
		port.mask = '255.255.255.0'
		noeud.interfaces[port.port] = port
	else:
		for neighbor in noeud.neighbors:
			port = Interface('GigabitEthernet%d/0'%n_port)
			n_port = n_port+1
			if noeud.name[:2] == 'PE' or noeud.name[:2] == 'CE':
				num_noeud = ord(noeud.name[2:])
			else:
				num_noeud = ord(noeud.name[1:])
			if neighbor[:2] == 'PE' or neighbor[:2] == 'CE':
				num_neighbor = ord(neighbor[2:])
			else:
				num_neighbor = ord(neighbor[1:])

			if neighbor[:2] == 'CE':
				port.ip_address = '172.16.%s.2' % neighbor[2:]
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
			noeud.interfaces[port.port] = port
	return noeud

def define_pc(client):
	num_client = client.name[2:]
	num_router = client.router[2:] 
	client.ip = '192.168.%s.%s' %(num_router,num_client)
	client.gateway = '192.168.%s.1' %num_router
	client.mask = '255.255.255.0'
	return client		
		
			
