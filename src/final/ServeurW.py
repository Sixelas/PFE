import tkinter as tk
import tkinter.font as tkFont
from PIL import Image, ImageTk
import os
import subprocess
import signal
import json
from QrCode_Generation import QRCode
from socket import *
import time
from global_fun import *
from config import *


# ATTENTION Important :
#
# Script pensé pour être lancé sur ServeurW car il est root !
# Si par erreur on ferme l'interface avec ctrl+c dans le terminal, ça kill pas les processus fils aca-py donc il faut les tuer avant de relancer :
#
# ps aux | grep aca-py
# kill -9 <pid aca-py> 
# 

# /////// CONFIG ///////

# Chemin du dossier qui contient ce fichier .py
selfFolderPath = os.getcwd() 

connectID = ""
pubKey = ""
credID = ""
clientPubKey = ""
address,interface = listIntAddr()


backgroundColor = 'white'
windowTitle = "Agent ServeurW"

width=810
height=606

# ///// END CONFIG /////


### Commande pour lancer l'agent Cloud du ServeurW. 
Agentproc = subprocess.Popen(SW_AgentStartCommand, shell=True, preexec_fn=os.setsid)

### Classe qui gère l'Interface Utilisateur Tkinter
class App:

    def __init__(self, root):

        root.title(windowTitle)
        root.configure(bg=backgroundColor)
        
        screenwidth = root.winfo_screenwidth()
        screenheight = root.winfo_screenheight()
        alignstr = '%dx%d+%d+%d' % (width, height, (screenwidth - width) / 2, (screenheight - height) / 2)
        root.geometry(alignstr)
        root.resizable(width=False, height=False)

        ft = tkFont.Font(family='Times',size=12)

        WGimg = Image.open(IMG_wg)
        WGimg = WGimg.resize((40, 40), Image.ANTIALIAS)
        WGimg = ImageTk.PhotoImage(WGimg)
        WGlabel = tk.Label(root, image=WGimg)
        WGlabel.image = WGimg
        WGlabel.place(x=15,y=40,width=60,height=60)
        WGlabel.configure(bg=backgroundColor)

        Ariesimg = Image.open(IMG_aries)
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

        self.GText_2 = tk.Label(text = "Clé publique de ClientW : ")
        self.GText_2["bg"] = "#e88787"
        self.GText_2["font"] = ft
        self.GText_2["fg"] = "#333333"
        self.GText_2["justify"] = "center"
        self.GText_2.place(x=30,y=450,width=261,height=40)

        self.GButton_5=tk.Button(root)
        self.GButton_5["bg"] = "#e88787"
        self.GButton_5["font"] = ft
        self.GButton_5["fg"] = "#000000"
        self.GButton_5["justify"] = "center"
        self.GButton_5["text"] = "Reset"
        self.GButton_5["relief"] = "groove"
        self.GButton_5["borderwidth"] = "3px"
        self.GButton_5.place(x=700,y=550,width=60,height=35)
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


### Fonction appelée quand on clique sur le bouton "Générer clés WireGuard"
    def GButton_1_command(self):

        global pubKey

        subprocess.call("echo Génération des clés WireGuard", shell=True)
        #Ici on génère le couple publickey / privatekey
        subprocess.call(umask, shell=True)
        subprocess.call(WG_genkey, shell=True)
        #Ici on met à jour la zone de texte à droite du bouton
        self.GLineEdit_1.delete(0, len(self.GLineEdit_1.get()))
        pubKey = loadFile("publickey")
        self.GLineEdit_1.insert(1,pubKey)

### Fonction appelée quand on clique sur le bouton "OK" de l'invitation ServeurB
    def GButton_2_command(self):

        global InvitRequest
        global  credID
        global connectID

        if (len(self.GLineEdit_2.get()) == 0):
            self.GLineEdit_2.delete(0, len(self.GLineEdit_2.get()))
            self.GLineEdit_2.insert(1, "Veillez remplir le champ inviation...")
            return

        ## Etape 1 : On établit la connexion avec serveurB à l'aide de l'invitation reçue :
        reqMSG = InvitRequest + self.GLineEdit_2.get() +''' ' '''
        invitProc = subprocess.Popen(reqMSG, shell=True, preexec_fn=os.setsid)
        invitProc.wait()
        time.sleep(5)
        self.GLineEdit_2.delete(0, len(self.GLineEdit_2.get()))

        ## Etape 2 : On demande un VC selon le modèle voulu à serveurB :

        # On récupère l'identifiant de la connexion connectID
        invitProc = subprocess.Popen(Connections, shell=True, preexec_fn=os.setsid)
        invitProc.wait()
        time.sleep(5)
        connectID = json.dumps(extractConnectID("ServeurB","Connection_logs.json"))

        # On envoie notre demande de VC
        proposeCommand = ''' curl -X POST http://localhost:11000/issue-credential-2.0/send-proposal -H "Content-Type: application/json" -d '{"comment": "VC WG Please","connection_id": ''' +connectID+ ''',"credential_preview": {"@type": "issue-credential/2.0/credential-preview","attributes": [{"mime-type": "plain/text","name": "public key", "value": "'''+ pubKey +'''"},{"mime-type": "plain/text","name": "name", "value": "ServeurW"}]},"filter": {"indy": {  }}}' '''
        invitProc = subprocess.Popen(proposeCommand, shell=True, preexec_fn=os.setsid)
        invitProc.wait()
        time.sleep(5)

        # On récupère le VC obtenu et on le stocke dans WG_VC.json. On récupère également le credID du VC.
        print("\nVC obtenu : ")
        invitProc = subprocess.Popen(Credentials, shell=True, preexec_fn=os.setsid)
        invitProc.wait()
        connectJson = loadJSON(selfFolderPath + "/ressources/WG_VC.json")
        credID = json.dumps(connectJson['results'][0]['cred_def_id'])
        print(connectJson)


### Fonction appelée quand on clique sur le bouton "Générer invitation pour ClientW"
    def GButton_3_command(self):

        subprocess.call(SW_InvitCommand, shell=True)
        invitJson = loadJSON(selfFolderPath + "/ressources/invitClientW.json")
        invitURL = json.dumps(invitJson['invitation'])
        self.GLineEdit_3.delete(0, len(self.GLineEdit_3.get()))
        self.GLineEdit_3.insert(1,invitURL)
        #Génère un QRcode d'invitation à partir de l'URL d'invitation.
        QRCode(json.dumps(invitJson['invitation_url'])).toPNG(selfFolderPath + "/ressources/invitClientW.png")


### Fonction appelée quand on clique sur le bouton "Echanges de Proofs avec ClientW"
    def GButton_4_command(self):

        global credID
        global connectID
        global clientPubKey

        ## Etape 1 : On récupère le connectID de la connexion avec ClientW

        # Enregistrement de la connection avec clientW
        proofProc = subprocess.Popen(Connections, shell=True,preexec_fn=os.setsid)
        proofProc.wait()
        connectID = json.dumps(extractConnectID("ClientW","Connection_logs.json"))

        ## Etape 2 : Envoie du proof request à clientW :

        # On envoie le proof request à clientW
        proofCommand = ''' curl -X 'POST'  'http://localhost:11000/present-proof-2.0/send-request' -H 'accept: application/json' -H 'Content-Type: application/json' -d '{ "comment": "ServeurW proof request", "connection_id": '''+connectID+''', "presentation_request": {"indy": {"name": "Proof of Identity","version": "1.0","requested_attributes": {"0_public_key_uuid": {"name": "public key","restrictions": [{"cred_def_id": '''+credID+'''}]},"0_name_uuid": {"name": "name","restrictions": [{"cred_def_id": '''+credID+'''}]} },"requested_predicates": { }}}} ' '''
        proofProc = subprocess.Popen(proofCommand, shell=True, preexec_fn=os.setsid)
        proofProc.wait()
        time.sleep(15)

        # On enregistre le résultat dans un fichier json pour ensuite extraire la clientPubKey WireGuard du Verifiable presentation de clientW.
        proofProc = subprocess.Popen(proofRecord, shell=True, preexec_fn=os.setsid)
        proofProc.wait()
        clientPubKey = extractPubKey("ClientW","ProofRecord.json")

        self.GLineEdit_4.delete(0, len(self.GLineEdit_4.get()))
        self.GLineEdit_4.insert(1, clientPubKey)


### Fonction appelée quand on appuie sur le bouton Reset. Elle supprime toutes les connexions et les configs WireGuard en cours sur l'Agent.
    def GButton_5_command(self):
        deleteConnexions("Connection_logs.json")
        revokeVC("ProofRecord.json")
        resetWG()

### Fonction appelée quand on clique sur le bouton "Configuration du Tunnel VPN"
    def GButton_6_command(self):

        global clientPubKey

        ## Etape 1 : On configure  le fichier /etc/wireguard/wg0.conf avec les informations obtenues précédemment :
        confWG = ''' echo "[Interface]\nPrivateKey = '''+loadFile("privatekey") +''' \nAddress = 120.0.0.1 \nSaveConfig = false \nListenPort = 51820 \nPostUp = iptables -A FORWARD -i wg0 -j ACCEPT; iptables -A FORWARD -o wg0 -j ACCEPT; iptables -t nat -A POSTROUTING -o '''+interface+''' -j MASQUERADE \nPostDown = iptables -D FORWARD -i wg0 -j ACCEPT; iptables -D FORWARD -o wg0 -j ACCEPT; iptables -t nat -D POSTROUTING -o '''+interface+''' -j MASQUERADE \nDNS = '''+ip_dns+'''\n\n[Peer] \n# ClientW \nPublicKey = ''' +clientPubKey+ '''\nAllowedIPs = 120.0.0.2/32" > /etc/wireguard/wg0.conf'''
        startVPN = subprocess.Popen(confWG, shell=True)
        startVPN.wait()

        ## Etape 2 : On active l'interface wg0 du VPN :
        startVPN = subprocess.Popen(WG_up, shell=True, preexec_fn=os.setsid)
        startVPN.wait()
        subprocess.call('''echo "Serveur VPN ouvert pour ClientW !" ''', shell=True)

if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()
    os.killpg(Agentproc.pid, signal.SIGTERM) #Pour tuer le processus aca-py Agent lancé au départ