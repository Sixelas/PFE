import tkinter as tk
import tkinter.font as tkFont
from PIL import Image, ImageTk
import os
import sys
import subprocess
import signal
import json
from QrCode_Generation import QRCode
from socket import *
from netifaces import interfaces, ifaddresses, AF_INET


# /////// CONFIG ///////

# Chemin du dossier qui contient ce fichier .py
selfFolderPath = os.getcwd() 

# Permet de récupérer automatiquement l'@ip de l'interface de la machine reliée au LAN. 
listeAdresses = []*len(interfaces())
for ifaceName in interfaces():
    addresses = [i['addr'] for i in ifaddresses(ifaceName).setdefault(AF_INET, [{'addr':'No IP addr'}] )]
    listeAdresses.append(addresses)

genesisIP = 'localhost'

# "&" pour lancer en tâche de fond.
AgentStartCommand = "aca-py start   --label ServeurW   -it http 0.0.0.0 8000   -ot http   --admin 0.0.0.0 11000   --admin-insecure-mode   --genesis-url http://"+genesisIP+":9000/genesis   --seed ServeurW000000000000000000000000   --endpoint http://"+listeAdresses[1][0]+":8000/   --debug-connections   --public-invites   --auto-provision   --wallet-type indy   --wallet-name ServeurW   --wallet-key secret   --auto-accept-requests --auto-accept-invites &"

InvitCommand = ''' curl -X POST "http://localhost:11000/out-of-band/create-invitation" -H 'Content-Type: application/json' -d '{ "handshake_protocols": ["did:sov:BzCbsNYhMrjHiqZDTUASHg;spec/didexchange/1.0"],"use_public_did": false}' > invitClientW.json '''

backgroundColor = 'white'
windowTitle = "Agent ServeurW"
#font = 'times 12'
#setting window size
width=810
height=606

# ///// END CONFIG /////

#TODO Commande pour lancer l'agent Cloud du ServeurW (en tâche de fond si possible, faut pas qu'il bloque le terminal). 
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

        self.GButton_3=tk.Button(root)
        self.GButton_3["bg"] = "#a9e5a1"
        self.GButton_3["font"] = ft
        self.GButton_3["fg"] = "#000000"
        self.GButton_3["justify"] = "center"
        self.GButton_3["text"] = "Générer invitation pour ClientW"
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

        self.GButton_4=tk.Button(root)
        self.GButton_4["bg"] = "#a9e5a1"
        self.GButton_4["font"] = ft
        self.GButton_4["fg"] = "#000000"
        self.GButton_4["justify"] = "center"
        self.GButton_4["text"] = "Echange de proof avec ClientW"
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
        subprocess.call("echo Génération des clés WireGuard", shell=True)
        #Ici on génère le couple publickey / privatekey
        subprocess.call("umask 077", shell=True)
        subprocess.call("wg genkey | tee privatekey | wg pubkey > publickey", shell=True)
        #Ici on met à jour la zone de texte à droite du bouton
        self.GLineEdit_1.delete(0, len(self.GLineEdit_1.get()))
        self.GLineEdit_1.insert(1,loadFile("publickey"))

#TODO Fonction appelée quand on clique sur le bouton "OK"
    def GButton_2_command(self):
        subprocess.call("echo TODO : Etablir connexion avec ServeurB", shell=True)
        


# Fonction appelée quand on clique sur le bouton "Générer invitation pour ClientW"
    def GButton_3_command(self):
        subprocess.call(InvitCommand, shell=True)
        invitJson = loadJSON(selfFolderPath + "/invitClientW.json") #Enregistre l'invitation dans un fichier json.
        invitURL = invitJson['invitation_url']
        self.GLineEdit_3.delete(0, len(self.GLineEdit_3.get()))
        self.GLineEdit_3.insert(1,invitURL)
        QRCode(invitURL).toPNG(selfFolderPath + "/invitClientW.png") #Génère un QRcode d'invitation à partir de l'URL d'invitation.


#TODO Fonction appelée quand on clique sur le bouton "Echanges de Proofs avec ClientW"
    def GButton_4_command(self):
        subprocess.call("echo TODO : Echanges de Proofs avec ClientW", shell=True)


#TODO Fonction appelée quand on clique sur le bouton "Echange des clés publiques WireGuard avec ClientW"
    def GButton_5_command(self):
        subprocess.call("echo TODO : Echange des clés publiques WireGuard avec ClientW", shell=True)


#TODO Fonction appelée quand on clique sur le bouton "Configuration du Tunnel VPN"
    def GButton_6_command(self):
        subprocess.call("echo TODO : Configuration du Tunnel VPN", shell=True)

if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()
    os.killpg(Agentproc.pid, signal.SIGTERM) #Pour tuer le processus aca-py Agent lancé au départ