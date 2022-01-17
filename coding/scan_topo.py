import os
import json
from class_noeud import *
from set import *

#open the topology file
fr = open('./topologie','r')

routeurs = {}
i = 1
clients = {}
for line in fr.readlines():
	if line != '\n':
		line = line.replace('\n','')
		noeud_pair = line.split(' ')
		if noeud_pair[0][:2] == 'PC':
			clients[noeud_pair[0]] = Client(noeud_pair[0],noeud_pair[1])
		else:
			if not noeud_pair[0] in routeurs:
				routeurs[noeud_pair[0]] = Routeur(noeud_pair[0],i)
				i = i+1
				routeurs[noeud_pair[0]].neighbors[noeud_pair[3]] = {'port':noeud_pair[1],'ip':noeud_pair[2]}
			elif not noeud_pair[3] in routeurs[noeud_pair[0]].neighbors.keys():
				routeurs[noeud_pair[0]].neighbors[noeud_pair[3]] = {'port':noeud_pair[1],'ip':noeud_pair[2]}
			else:
				print('Strange Here!')
			if noeud_pair[0][:2] == 'PE' and noeud_pair[6]!='none':
				routeurs[noeud_pair[0]].connect_type[noeud_pair[3]]=noeud_pair[6]
			elif noeud_pair[0][:2] == 'CE':
				routeurs[noeud_pair[0]].router_type = noeud_pair[6]
		if noeud_pair[3][:2] == 'PC':
			clients[noeud_pair[3]] = Client(noeud_pair[3],noeud_pair[0])
		else:
			if not noeud_pair[3] in routeurs:
				routeurs[noeud_pair[3]] = Routeur(noeud_pair[3],i)
				i = i+1
				routeurs[noeud_pair[3]].neighbors[noeud_pair[0]] = {'port':noeud_pair[4],'ip':noeud_pair[5]}
			elif not noeud_pair[0] in routeurs[noeud_pair[3]].neighbors.keys():
				routeurs[noeud_pair[3]].neighbors[noeud_pair[0]] = {'port':noeud_pair[4],'ip':noeud_pair[5]}
			else:
				print('Strange Here!')
			if noeud_pair[3][:2] == 'PE' and noeud_pair[6]!='none':
				routeurs[noeud_pair[3]].connect_type[noeud_pair[0]]=noeud_pair[6]
			elif noeud_pair[3][:2] == 'CE':
				routeurs[noeud_pair[3]].router_type = noeud_pair[6]
fr.close() 

for key in routeurs.keys():
	routeurs[key] = define_port(routeurs[key])
	routeurs[key] = define_ospf(routeurs[key])
	routeurs[key] = define_mpls(routeurs[key])
routeurs = define_bgp(routeurs)
routeurs = add_community_list(routeurs)

for key in routeurs.keys():	
	routeurs[key].interfaces_to_json()
	routeurs[key].bgp_to_json()
	routeurs[key].route_map_to_json()
	routeurs[key].to_json()
	routeurs[key] = routeurs[key].json
for key in clients.keys():
	clients[key] = define_pc(clients[key])
	clients[key].to_json()
	clients[key] = clients[key].json

fw = open('./topologie.json','w')
json_routeurs = json.dumps(routeurs,indent = 4, separators = (',',': '))
fw.write(json_routeurs)
fw.write('!')		
json_clients = json.dumps(clients,indent = 4, separators = (',',': '))
fw.write(json_clients)	
fw.close()

