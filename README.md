# NAS_Projet
2022 NAS_Projet

class_noeud.py contient tout les classes qu'on utilse. (Client)  
set.py contient tout les fonction qu'on crée. (define_pc(client))  
On import ces 2 programme dans le programme scan_topo.py, on constitue le fichier topologie.json en appelant les classes et les fonctions définis.  
Le fichier topologie.json est traité par le programme print.py pour pouvoir crée des fichiers config.  

Format de Topologie  
    source  interface  adresse_ip  destination  interface   adresse_ip  tpye_de_CE
