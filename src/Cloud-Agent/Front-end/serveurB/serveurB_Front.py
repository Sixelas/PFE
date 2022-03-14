import tkinter as tk
import tkinter.font as tkFont
from PIL import Image, ImageTk
import os
import sys
import subprocess
import signal
import json
import time
#from QrCode_Generation import QRCode
from socket import *
from netifaces import interfaces, ifaddresses, AF_INET



# Dépendances manquantes sur les VM à installer :
#
# apt-get install python3-tk python3-pil python3-pil.imagetk
# pip install pyqrcode netifaces pypng

# ATTENTION Important :
#
# Script pensé pour être lancé sur ServeurB car il est root ! Sur pc perso faudra modif le code pour ajouter le "sudo" à von-network.
# Pour l'instant ça lance les processus von-network et aca-py en arrière plan donc faut bien les kill avant de relancer quoi que ce soit avec :
# 
# Pour aca-py :
# ps aux | grep aca-py
# kill -9 <pid aca-py> 
# 
# Pour von-network :
# ~/von-network/manage stop

# /////// CONFIG ///////

# Chemin du dossier qui contient ce fichier .py
selfFolderPath = os.getcwd() 

# Permet de récupérer automatiquement l'@ip de l'interface de la machine reliée au LAN. 
# https://stackoverflow.com/questions/166506/finding-local-ip-addresses-using-pythons-stdlib
listeAdresses = []*len(interfaces())
for ifaceName in interfaces():
    addresses = [i['addr'] for i in ifaddresses(ifaceName).setdefault(AF_INET, [{'addr':'No IP addr'}] )]
    listeAdresses.append(addresses)

# Ip de la machine reliée au von-network. Sur ServeurB c'est lui-même donc on laisse localhost
genesisIP = 'localhost'

VonStartCommand = "~/von-network/manage start logs"

# "&" pour lancer en tâche de fond.
AgentStartCommand = "aca-py start   --label ServeurB   -it http 0.0.0.0 8000   -ot http   --admin 0.0.0.0 11000   --admin-insecure-mode   --genesis-url http://"+genesisIP+":9000/genesis   --seed ServeurB000000000000000000000000   --endpoint http://"+listeAdresses[1][0]+":8000/   --debug-connections   --public-invites   --auto-provision   --wallet-type indy   --wallet-name ServeurB   --wallet-key secret   --auto-accept-requests --auto-accept-invites &"

RegisterCommand_1 = ''' curl -X POST "http://localhost:9000/register" -d '{"seed": "ServeurW000000000000000000000000", "role": "TRUST_ANCHOR", "alias": "ServeurW"}' '''
RegisterCommand_2 = ''' curl -X POST "http://localhost:9000/register" -d '{"seed": "ServeurB000000000000000000000000", "role": "TRUST_ANCHOR", "alias": "ServeurB"}' '''
RegisterCommand_3 = ''' curl -X POST "http://localhost:9000/register" -d '{"seed": "ClientW0000000000000000000000000", "role": "TRUST_ANCHOR", "alias": "ClientW"}' '''

InvitCommand = ''' curl -X POST "http://localhost:11000/out-of-band/create-invitation" -H 'Content-Type: application/json' -d '{ "handshake_protocols": ["did:sov:BzCbsNYhMrjHiqZDTUASHg;spec/didexchange/1.0"],"use_public_did": false}' > invitServeurtW.json '''

# ///// END CONFIG /////



# Commande pour lancer l'agent Von du ServeurB. 
print("Démarrage du von-network ...")
Vonproc = subprocess.Popen(VonStartCommand, shell=True, preexec_fn=os.setsid)
Vonproc.wait()
time.sleep(15)
print("von-network OK http://localhost:9000/")

# Commandes pour enregistrer les utilisateurs dans le von-network
print("Enregistrement des utilisateurs ...")
subprocess.Popen(RegisterCommand_1, shell=True, preexec_fn=os.setsid)
time.sleep(1)
subprocess.Popen(RegisterCommand_2, shell=True, preexec_fn=os.setsid)
time.sleep(1)
subprocess.Popen(RegisterCommand_3, shell=True, preexec_fn=os.setsid)
time.sleep(1)
print("Utilisateurs enregistrés")


# Commande pour lancer l'agent Cloud du ServeurB (en tâche de fond si possible, faut pas qu'il bloque le terminal). 
print("Démarrage du CloudAgent ...")
Agentproc = subprocess.Popen(AgentStartCommand, shell=True, preexec_fn=os.setsid)
Agentproc.wait()
time.sleep(5)
print("CloudAgent ServeurB OK")


#Commande pour lancer l'agent Cloud du ServeurB (en tâche de fond si possible, faut pas qu'il bloque le terminal). 
print("Création de l'invitation pour ServeurW ...")
Invitproc = subprocess.Popen(InvitCommand, shell=True, preexec_fn=os.setsid)
Invitproc.wait()
print("Invitation : ")
subprocess.Popen("cat "+selfFolderPath+"/invitServeurtW.json", shell=True, preexec_fn=os.setsid)


