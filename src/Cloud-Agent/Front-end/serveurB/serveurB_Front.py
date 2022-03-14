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
stop = False

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



backgroundColor = 'white'
windowTitle = "Agent ServeurW"
#font = 'times 12'
#setting window size
width=810
height=606
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


# Open a json file
def loadJSON(filePath):
    with open(filePath, 'r') as file:
        return json.load(file)
        
class App:

    def __init__(self, root):

        #setting title
        root.title(windowTitle)
        root.configure(bg=backgroundColor)
        #root.option_add('*Font', font)
        
        screenwidth = root.winfo_screenwidth()
        screenheight = root.winfo_screenheight()
        alignstr = '%dx%d+%d+%d' % (width, height, (screenwidth - width) / 2, (screenheight - height) / 2)
        root.geometry(alignstr)
        root.resizable(width=False, height=False)

        ft = tkFont.Font(family='Times',size=12)

        WGimg = Image.open(selfFolderPath+"/wg.png")
        WGimg = WGimg.resize((40, 40), Image.ANTIALIAS)
        WGimg = ImageTk.PhotoImage(WGimg)
        WGlabel = tk.Label(root, image=WGimg)
        WGlabel.image = WGimg
        WGlabel.place(x=15,y=40,width=60,height=60)
        WGlabel.configure(bg=backgroundColor)

        Ariesimg = Image.open(selfFolderPath+"/Aries.png")
        Ariesimg = Ariesimg.resize((180, 40), Image.ANTIALIAS)
        Ariesimg = ImageTk.PhotoImage(Ariesimg)
        Arieslabel = tk.Label(root, image=Ariesimg)
        Arieslabel.image = Ariesimg
        Arieslabel.place(x=40,y=140,width=180,height=50)
        Arieslabel.configure(bg=backgroundColor)

        self.GButton_1=tk.Button(root)
        self.GButton_1["bg"] = "#e88787"
        self.GButton_1["font"] = ft
        self.GButton_1["fg"] = "#000000"
        self.GButton_1["borderwidth"] = "3px"
        self.GButton_1["justify"] = "center"
        self.GButton_1["text"] = "STOP"
        self.GButton_1["relief"] = "groove"
        self.GButton_1.place(x=100,y=50,width=168,height=40)
        self.GButton_1["command"] = self.GButton_1_command

        self.GButton_3=tk.Button(root)
        self.GButton_3["bg"] = "#a9e5a1"
        self.GButton_3["font"] = ft
        self.GButton_3["fg"] = "#000000"
        self.GButton_3["justify"] = "center"
        self.GButton_3["text"] = "Générer invitation pour ServeurW"
        self.GButton_3["relief"] = "groove"
        self.GButton_3["borderwidth"] = "3px"
        self.GButton_3.place(x=30,y=300,width=262,height=40)
        self.GButton_3["command"] = self.GButton_3_command

        self.GLineEdit_3=tk.Entry(root)
        self.GLineEdit_3["bg"] = "#a9e5a1"
        self.GLineEdit_3["borderwidth"] = "1px"
        self.GLineEdit_3["font"] = ft
        self.GLineEdit_3["fg"] = "#333333"
        self.GLineEdit_3["justify"] = "center"
        self.GLineEdit_3["text"] = ""
        self.GLineEdit_3.place(x=320,y=300,width=436,height=40)


# Fonction appelée quand on clique sur le bouton "STOP"
    def GButton_1_command(self):
        os.killpg(Agentproc.pid, signal.SIGTERM)                    #Pour tuer le processus aca-py Agent lancé au départ
        subprocess.call("~/von-network/manage stop", shell=True)    #Pour tuer le von-network
        stop = True


# Fonction appelée quand on clique sur le bouton "Générer invitation pour ClientW"
    def GButton_3_command(self):
        #Commande pour lancer l'agent Cloud du ServeurB (en tâche de fond si possible, faut pas qu'il bloque le terminal). 
        Invitproc = subprocess.Popen(InvitCommand, shell=True, preexec_fn=os.setsid)
        Invitproc.wait()
        invitJson = loadJSON(selfFolderPath + "/invitServeurtW.json") #Récupère l'invitation dans le fichier json.
        invitURL = invitJson['invitation_url']
        self.GLineEdit_3.delete(0, len(self.GLineEdit_3.get()))
        self.GLineEdit_3.insert(1,invitURL)


if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()
    if not stop :
        os.killpg(Agentproc.pid, signal.SIGTERM)                    #Pour tuer le processus aca-py Agent lancé au départ
        subprocess.call("~/von-network/manage stop", shell=True)    #Pour tuer le von-network

    



