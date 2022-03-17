import tkinter as tk
import tkinter.font as tkFont
from PIL import Image, ImageTk
import os
import sys
import subprocess
import signal
import json
from socket import *
from netifaces import interfaces, ifaddresses, AF_INET
import time

# Dépendances manquantes sur les VM à installer :
#
# apt-get install python3-tk python3-pil python3-pil.imagetk
# pip install pyqrcode netifaces pypng

# ATTENTION Important :
#
# Script pensé pour être lancé sur ServeurW car il est root !
# Pour l'instant ça lance le aca-py en arrière plan donc faut bien les kill avant de relancer quoi que ce soit avec :
#
# ps aux | grep aca-py
# kill -9 <pid aca-py> 
# 

# /////// CONFIG ///////

# Chemin du dossier qui contient ce fichier .py
selfFolderPath = os.getcwd() 

# Permet de récupérer automatiquement l'@ip de l'interface de la machine reliée au LAN. 
listeAdresses = []*len(interfaces())
for ifaceName in interfaces():
    addresses = [i['addr'] for i in ifaddresses(ifaceName).setdefault(AF_INET, [{'addr':'No IP addr'}] )]
    listeAdresses.append(addresses)

# Id de la connexion établie avec serveurB
#connectID = ""

pubKey = ""
credID = ""
# Si on a le von-network en local :
#genesisIP = 'localhost'
# Si le von-network est sur serveurB :
genesisIP = '192.168.1.15'

# "&" pour lancer en tâche de fond.
AgentStartCommand = "aca-py start   --label ClientW   -it http 0.0.0.0 8000   -ot http   --admin 0.0.0.0 11000   --admin-insecure-mode   --genesis-url http://"+genesisIP+":9000/genesis   --seed ClientW0000000000000000000000000   --endpoint http://"+listeAdresses[1][0]+":8000/   --debug-connections   --public-invites   --auto-provision   --wallet-type indy   --wallet-name ClientW   --wallet-key secret   --auto-accept-requests --auto-accept-invites  --auto-respond-credential-proposal  --auto-respond-credential-offer  --auto-respond-credential-request  --auto-store-credential &"

InvitRequest1 = ''' curl -X POST "http://localhost:11000/out-of-band/receive-invitation" -H 'Content-Type: application/json' -d ' '''
InvitRequest2 = ''' curl -X POST "http://localhost:11000/out-of-band/receive-invitation" -H 'Content-Type: application/json' -d ' '''

backgroundColor = 'white'
windowTitle = "Agent ClientW"
#font = 'times 12'
#setting window size
width=810
height=606

# ///// END CONFIG /////

#TODO Commande pour lancer l'agent Cloud du ClientW. 
Agentproc = subprocess.Popen(AgentStartCommand, shell=True, preexec_fn=os.setsid)

#Cette fonction lit un fichier de nom "file" et retourne la première ligne sans le retour à la ligne \n
def loadFile(file) :
    if os.path.exists(selfFolderPath + "/"+ file):
        fichier = open(selfFolderPath + "/"+ file, "r")
        for line in fichier :
            return  line.strip('\n') 
        fichier.close()
    print( "Erreur : " + selfFolderPath + "/" + file +" non trouvé")
    return "Erreur lors de la génération des clés" #Message d'erreur à retourner au choix, ici pensé pour retourner la clé publique wireguard

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
        self.GButton_1["text"] = "Générer clés WireGuard"
        self.GButton_1["relief"] = "groove"
        self.GButton_1.place(x=100,y=50,width=168,height=40)
        self.GButton_1["command"] = self.GButton_1_command

        self.GLineEdit_1=tk.Entry(root)
        self.GLineEdit_1["bg"] = "#e88787"
        self.GLineEdit_1["borderwidth"] = "1px"
        self.GLineEdit_1["font"] = ft
        self.GLineEdit_1["fg"] = "#333333"
        self.GLineEdit_1["justify"] = "center"
        self.GLineEdit_1["text"] = ""
        self.GLineEdit_1.place(x=290,y=50,width=463,height=40)

        self.GText_1 = tk.Label(text = "Entrer l'invitation de ServeurB ci-dessous")
        self.GText_1["bg"] = "#a9e5a1"
        self.GText_1["font"] = ft
        self.GText_1["fg"] = "#333333"
        self.GText_1["justify"] = "center"
        self.GText_1.place(x=290,y=150,width=464,height=40)

        self.GLineEdit_2=tk.Entry(root)
        self.GLineEdit_2["bg"] = "#a9e5a1"
        self.GLineEdit_2["borderwidth"] = "1px"
        self.GLineEdit_2["font"] = ft
        self.GLineEdit_2["fg"] = "#333333"
        self.GLineEdit_2["justify"] = "center"
        self.GLineEdit_2["text"] = ""
        self.GLineEdit_2.place(x=30,y=220,width=581,height=40)

        self.GButton_2=tk.Button(root)
        self.GButton_2["bg"] = "#a9e5a1"
        self.GButton_2["font"] = ft
        self.GButton_2["fg"] = "#000000"
        self.GButton_2["justify"] = "center"
        self.GButton_2["text"] = "OK"
        self.GButton_2["relief"] = "groove"
        self.GButton_2["borderwidth"] = "3px"
        self.GButton_2.place(x=650,y=220,width=104,height=40)
        self.GButton_2["command"] = self.GButton_2_command

        self.GText_2 = tk.Label(text = "Entrer l'invitation de ServeurW à droite :")
        self.GText_2["bg"] = "#a9e5a1"
        self.GText_2["font"] = ft
        self.GText_2["fg"] = "#333333"
        self.GText_2["justify"] = "center"
        self.GText_2.place(x=30,y=300,width=262,height=40)

        self.GLineEdit_3=tk.Entry(root)
        self.GLineEdit_3["bg"] = "#a9e5a1"
        self.GLineEdit_3["borderwidth"] = "1px"
        self.GLineEdit_3["font"] = ft
        self.GLineEdit_3["fg"] = "#333333"
        self.GLineEdit_3["justify"] = "center"
        self.GLineEdit_3["text"] = ""
        self.GLineEdit_3.place(x=320,y=300,width=290,height=40)

        self.GButton_3=tk.Button(root)
        self.GButton_3["bg"] = "#a9e5a1"
        self.GButton_3["font"] = ft
        self.GButton_3["fg"] = "#000000"
        self.GButton_3["justify"] = "center"
        self.GButton_3["text"] = "OK"
        self.GButton_3["relief"] = "groove"
        self.GButton_3["borderwidth"] = "3px"
        self.GButton_3.place(x=650,y=300,width=104,height=40)
        self.GButton_3["command"] = self.GButton_3_command

        self.GButton_4=tk.Button(root)
        self.GButton_4["bg"] = "#a9e5a1"
        self.GButton_4["font"] = ft
        self.GButton_4["fg"] = "#000000"
        self.GButton_4["justify"] = "center"
        self.GButton_4["text"] = "Echange de proof avec ServeurW"
        self.GButton_4["relief"] = "groove"
        self.GButton_4["borderwidth"] = "3px"
        self.GButton_4.place(x=240,y=370,width=293,height=40)
        self.GButton_4["command"] = self.GButton_4_command

        self.GButton_5=tk.Button(root)
        self.GButton_5["bg"] = "#e88787"
        self.GButton_5["font"] = ft
        self.GButton_5["fg"] = "#000000"
        self.GButton_5["justify"] = "center"
        self.GButton_5["text"] = "Echange de clés publiques WireGuard"
        self.GButton_5["relief"] = "groove"
        self.GButton_5["borderwidth"] = "3px"
        self.GButton_5.place(x=30,y=450,width=261,height=40)
        self.GButton_5["command"] = self.GButton_5_command

        self.GLineEdit_4=tk.Entry(root)
        self.GLineEdit_4["bg"] = "#e88787"
        self.GLineEdit_4["borderwidth"] = "1px"
        self.GLineEdit_4["font"] = ft
        self.GLineEdit_4["fg"] = "#333333"
        self.GLineEdit_4["justify"] = "center"
        self.GLineEdit_4["text"] = "Entry"
        self.GLineEdit_4.place(x=320,y=450,width=438,height=40)

        self.GButton_6=tk.Button(root)
        self.GButton_6["bg"] = "#e88787"
        self.GButton_6["font"] = ft
        self.GButton_6["fg"] = "#000000"
        self.GButton_6["justify"] = "center"
        self.GButton_6["text"] = "Configurer Tunnel VPN WireGuard"
        self.GButton_6["relief"] = "groove"
        self.GButton_6["borderwidth"] = "3px"
        self.GButton_6.place(x=240,y=530,width=292,height=34)
        self.GButton_6["command"] = self.GButton_6_command


# Fonction appelée quand on clique sur le bouton "Générer clés WireGuard"
    def GButton_1_command(self):
        global pubKey
        subprocess.call("echo Génération des clés WireGuard", shell=True)
        #Ici on génère le couple publickey / privatekey
        subprocess.call("umask 077", shell=True)
        subprocess.call("wg genkey | tee privatekey | wg pubkey > publickey", shell=True)
        #Ici on met à jour la zone de texte à droite du bouton
        self.GLineEdit_1.delete(0, len(self.GLineEdit_1.get()))
        pubKey = loadFile("publickey")
        self.GLineEdit_1.insert(1,pubKey)

# Fonction appelée quand on clique sur le bouton "OK" de l'invitation ServeurB
    def GButton_2_command(self):
        global InvitRequest1
        global credID
        reqMSG = InvitRequest1 + self.GLineEdit_2.get() +''' ' '''
        invitProc = subprocess.Popen(reqMSG, shell=True, preexec_fn=os.setsid)
        invitProc.wait()
        time.sleep(5)
        self.GLineEdit_2.delete(0, len(self.GLineEdit_2.get()))
        invitProc = subprocess.Popen(''' curl http://localhost:11000/connections > Connection_logs.json ''', shell=True, preexec_fn=os.setsid)
        invitProc.wait()
        time.sleep(5)
        connectJson = loadJSON(selfFolderPath + "/Connection_logs.json") #Enregistre l'invitation dans un fichier json.
        connectID = json.dumps(connectJson['results'][0]['connection_id'])
        proposeCommand = ''' curl -X POST http://localhost:11000/issue-credential-2.0/send-proposal -H "Content-Type: application/json" -d '{"comment": "VC WG Please","connection_id": ''' +connectID+ ''',"credential_preview": {"@type": "issue-credential/2.0/credential-preview","attributes": [{"mime-type": "plain/text","name": "public key", "value": "'''+ pubKey +'''"},{"mime-type": "plain/text","name": "name", "value": "ClientW"}]},"filter": {"indy": {  }}}' '''
        invitProc = subprocess.Popen(proposeCommand, shell=True, preexec_fn=os.setsid)
        invitProc.wait()
        time.sleep(5)
        print("VC obtenu : ")
        invitProc = subprocess.Popen(''' curl -X GET "http://localhost:11000/credentials" > WG_VC.json''', shell=True, preexec_fn=os.setsid)
        invitProc.wait()
        connectJson = loadJSON(selfFolderPath + "/WG_VC.json")
        credID = json.dumps(connectJson['results'][0]['cred_def_id'])

# Fonction appelée quand on clique sur le bouton "OK" de l'invitation ServeurW
    def GButton_3_command(self):
        global InvitRequest2
        reqMSG = InvitRequest2 + self.GLineEdit_3.get() +''' ' '''
        invitProc = subprocess.Popen(reqMSG, shell=True, preexec_fn=os.setsid)
        invitProc.wait()
        time.sleep(5)
        self.GLineEdit_3.delete(0, len(self.GLineEdit_3.get()))


#TODO Fonction appelée quand on clique sur le bouton "Echanges de Proofs avec ServeurW"
    def GButton_4_command(self):
        subprocess.call("echo TODO : Echanges de Proofs avec ServeurW", shell=True)


#TODO Fonction appelée quand on clique sur le bouton "Echange des clés publiques WireGuard avec ServeurW"
    def GButton_5_command(self):
        subprocess.call("echo TODO : Echange des clés publiques WireGuard avec ServeurW", shell=True)


#TODO Fonction appelée quand on clique sur le bouton "Configuration du Tunnel VPN"
    def GButton_6_command(self):
        subprocess.call("echo TODO : Configuration du Tunnel VPN", shell=True)

if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()
    os.killpg(Agentproc.pid, signal.SIGTERM) #Pour tuer le processus aca-py Agent lancé au départ