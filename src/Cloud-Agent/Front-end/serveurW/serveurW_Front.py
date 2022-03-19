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
import time

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

# Permet de récupérer automatiquement l'@ip et l'interface de la machine reliée au LAN. 
listeAdresses = []*len(interfaces())
listeInterfaces = []*len(interfaces())
for ifaceName in interfaces():
    addresses = [i['addr'] for i in ifaddresses(ifaceName).setdefault(AF_INET, [{'addr':'No IP addr'}] )]
    listeAdresses.append(addresses)
    listeInterfaces.append(ifaceName)


connectID = ""
pubKey = ""
credID = ""
clientPubKey = ""

# Si on a le von-network en local :
#genesisIP = 'localhost'
# Si le von-network est sur serveurB :
genesisIP = '192.168.1.15'

# "&" pour lancer en tâche de fond.
AgentStartCommand = "aca-py start   --label ServeurW   -it http 0.0.0.0 8000   -ot http   --admin 0.0.0.0 11000   --admin-insecure-mode   --genesis-url http://"+genesisIP+":9000/genesis   --seed ServeurW000000000000000000000000   --endpoint http://"+listeAdresses[1][0]+":8000/   --debug-connections   --public-invites   --auto-provision   --wallet-type indy   --wallet-name ServeurW   --wallet-key secret   --auto-accept-requests --auto-accept-invites  --auto-respond-credential-proposal  --auto-respond-credential-offer  --auto-respond-credential-request  --auto-store-credential --auto-respond-presentation-request --auto-respond-presentation-proposal --auto-verify-presentation &"

InvitCommand = ''' curl -X POST "http://localhost:11000/out-of-band/create-invitation" -H 'Content-Type: application/json' -d '{ "handshake_protocols": ["did:sov:BzCbsNYhMrjHiqZDTUASHg;spec/didexchange/1.0"],"use_public_did": false}' > invitClientW.json '''

InvitRequest = ''' curl -X POST "http://localhost:11000/out-of-band/receive-invitation" -H 'Content-Type: application/json' -d ' '''

backgroundColor = 'white'
windowTitle = "Agent ServeurW"

width=810
height=606

# ///// END CONFIG /////


### Commande pour lancer l'agent Cloud du ServeurW. 
Agentproc = subprocess.Popen(AgentStartCommand, shell=True, preexec_fn=os.setsid)

### Cette fonction lit un fichier de nom "file" et retourne la première ligne sans le retour à la ligne \n
def loadFile(file) :
    if os.path.exists(selfFolderPath + "/"+ file):
        fichier = open(selfFolderPath + "/"+ file, "r")
        for line in fichier :
            return  line.strip('\n') 
        fichier.close()
    print( "Erreur : " + selfFolderPath + "/" + file +" non trouvé")
    return "Erreur lors de la génération des clés" #Message d'erreur à retourner au choix, ici pensé pour retourner la clé publique wireguard

### Cette fonction retourne le contenu d'un fichier .json
def loadJSON(filePath):
    with open(filePath, 'r') as file:
        return json.load(file)

### Fonction qui permet d'extraire la clé publique de la Présentation 
def extractPubKey(serverName, file) :
    dataJson = loadJSON(selfFolderPath + "/"+file)
    
    for case in dataJson['results'] :
        ## Si on est l'Agent ClientW, on veut récupérer la clé de ServeurW
        if(serverName == "ClientW") :
            if(case['pres_request']['comment'] == 'ServerW proof request') :
                extractKey = case['by_format']['pres']['indy']['requested_proof']['revealed_attrs']['0_public_key_uuid']['raw']
                return ''.join(x for x in extractKey if x not in '''"''')

        ## Si on est l'Agent ServeurW, on veut récupérer la clé de ClientW
        if(serverName == "ServerW") :
            if(case['pres_request']['comment'] == 'ClientW proof request') :
                extractKey = case['by_format']['pres']['indy']['requested_proof']['revealed_attrs']['0_public_key_uuid']['raw']
                return ''.join(x for x in extractKey if x not in '''"''')
        else :
            print(serverName+" n'est pas un Agent reconnu")
            return ""

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
        self.GButton_5["text"] = "Récupérer clé publique de clientW"
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


### Fonction appelée quand on clique sur le bouton "Générer clés WireGuard"
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

### Fonction appelée quand on clique sur le bouton "OK" de l'invitation ServeurB
    def GButton_2_command(self):

        global InvitRequest
        global  credID
        global connectID

        ## Etape 1 : On établit la connexion avec serveurB à l'aide de l'invitation reçue :
        reqMSG = InvitRequest + self.GLineEdit_2.get() +''' ' '''
        invitProc = subprocess.Popen(reqMSG, shell=True, preexec_fn=os.setsid)
        invitProc.wait()
        time.sleep(5)
        self.GLineEdit_2.delete(0, len(self.GLineEdit_2.get()))

        ## Etape 2 : On demande un VC selon le modèle voulu à serveurB :

        # On récupère l'identifiant de la connexion connectID
        invitProc = subprocess.Popen(''' curl http://localhost:11000/connections > Connection_logs.json ''', shell=True, preexec_fn=os.setsid)
        invitProc.wait()
        time.sleep(5)
        connectJson = loadJSON(selfFolderPath + "/Connection_logs.json") #Récupère les données d'invitation enregistrées dans le fichier json.
        connectID = json.dumps(connectJson['results'][0]['connection_id'])

        # On envoie notre demande de VC
        proposeCommand = ''' curl -X POST http://localhost:11000/issue-credential-2.0/send-proposal -H "Content-Type: application/json" -d '{"comment": "VC WG Please","connection_id": ''' +connectID+ ''',"credential_preview": {"@type": "issue-credential/2.0/credential-preview","attributes": [{"mime-type": "plain/text","name": "public key", "value": "'''+ pubKey +'''"},{"mime-type": "plain/text","name": "name", "value": "ServeurW"}]},"filter": {"indy": {  }}}' '''
        invitProc = subprocess.Popen(proposeCommand, shell=True, preexec_fn=os.setsid)
        invitProc.wait()
        time.sleep(5)

        # On récupère le VC obtenu et on le stocke dan WG_VC.json. On récupère également le credID du VC.
        print("\nVC obtenu : ")
        invitProc = subprocess.Popen(''' curl -X GET "http://localhost:11000/credentials" > WG_VC.json''', shell=True, preexec_fn=os.setsid)
        invitProc.wait()
        connectJson = loadJSON(selfFolderPath + "/WG_VC.json")
        credID = json.dumps(connectJson['results'][0]['cred_def_id'])


### Fonction appelée quand on clique sur le bouton "Générer invitation pour ClientW"
    def GButton_3_command(self):

        subprocess.call(InvitCommand, shell=True)
        invitJson = loadJSON(selfFolderPath + "/invitClientW.json")
        invitURL = json.dumps(invitJson['invitation'])
        self.GLineEdit_3.delete(0, len(self.GLineEdit_3.get()))
        self.GLineEdit_3.insert(1,invitURL)
        #Génère un QRcode d'invitation à partir de l'URL d'invitation.
        QRCode(json.dumps(invitJson['invitation_url'])).toPNG(selfFolderPath + "/invitClientW.png")


### Fonction appelée quand on clique sur le bouton "Echanges de Proofs avec ClientW"
    def GButton_4_command(self):

        global credID
        global connectID
        global clientPubKey

        ## Etape 1 : On récupère le connectID de la connexion avec clientW (nécessite de supprimer l'ancienne connexion avec serveurB)

        # Suppression de la connection avec serveurB :
        connectID = ''.join(x for x in connectID if x not in '''"''')
        deleteConnectID = ''' curl -X 'DELETE' 'http://localhost:11000/connections/''' + connectID + ''' ' -H 'accept: application/json' '''
        proofProc = subprocess.Popen(deleteConnectID, shell=True, preexec_fn=os.setsid)
        proofProc.wait()

        # Enregistrement de la connection avec clientW
        proofProc = subprocess.Popen(''' curl http://localhost:11000/connections > Connection_logs.json ''', shell=True,preexec_fn=os.setsid)
        proofProc.wait()
        connectJson = loadJSON(selfFolderPath + "/Connection_logs.json")
        connectID = json.dumps(connectJson['results'][0]['connection_id'])

        ## Etape 2 : Envoie du proof request à clientW :

        # On envoie le proof request à clientW
        proofCommand = ''' curl -X 'POST'  'http://localhost:11000/present-proof-2.0/send-request' -H 'accept: application/json' -H 'Content-Type: application/json' -d '{ "comment": "ServerW proof request", "connection_id": '''+connectID+''', "presentation_request": {"indy": {"name": "Proof of Identity","version": "1.0","requested_attributes": {"0_public_key_uuid": {"name": "public key","restrictions": [{"cred_def_id": '''+credID+'''}]},"0_name_uuid": {"name": "name","restrictions": [{"cred_def_id": '''+credID+'''}]} },"requested_predicates": { }}}} ' '''
        proofProc = subprocess.Popen(proofCommand, shell=True, preexec_fn=os.setsid)
        proofProc.wait()
        time.sleep(15)

        # On enregistre le résultat dans un fichier json pour ensuite extraire la clientPubKey WireGuard du Verifiable presentation de clientW.
        proofRecord = ''' curl -X 'GET' 'http://localhost:11000/present-proof-2.0/records' -H 'accept: application/json' > ProofRecord.json '''
        proofProc = subprocess.Popen(proofRecord, shell=True, preexec_fn=os.setsid)
        proofProc.wait()
        clientPubKey = extractPubKey("serverW","ProofRecord.json")

        #connectJson = loadJSON(selfFolderPath + "/ProofRecord.json")
        #clientPubKey = json.dumps(connectJson['results'][0]['by_format']['pres']['indy']['requested_proof']['revealed_attrs']['0_public_key_uuid']['raw'])
        #clientPubKey = ''.join(x for x in clientPubKey if x not in '''"''')
        self.GLineEdit_4.delete(0, len(self.GLineEdit_4.get()))
        self.GLineEdit_4.insert(1, clientPubKey)


### Fonction appelée quand on clique sur le bouton "Récupérer clé publique de clientW" (Inutilisable avec la nouvelle version de proof+extract dans les deux sens)
    def GButton_5_command(self):

        #global clientPubKey

        #proofRecord = ''' curl -X 'GET' 'http://localhost:11000/present-proof-2.0/records' -H 'accept: application/json' > ProofRecord.json '''
        #proofProc = subprocess.Popen(proofRecord, shell=True, preexec_fn=os.setsid)
        #proofProc.wait()
        #proofJson = loadJSON(selfFolderPath + "/ProofRecord.json")
        #clientPubKey = json.dumps(proofJson['results'][0]['pres_request']['comment'])
        #clientPubKey = ''.join(x for x in clientPubKey if x not in '''"''')
        #self.GLineEdit_4.delete(0, len(self.GLineEdit_4.get()))
        #self.GLineEdit_4.insert(1, clientPubKey)
        subprocess.Popen(''' echo "Fonctionnalité inutile à supprimer" ''', shell=True, preexec_fn=os.setsid)

### Fonction appelée quand on clique sur le bouton "Configuration du Tunnel VPN"
    def GButton_6_command(self):

        global clientPubKey
        #clientPubKey = self.GLineEdit_4.get()

        ## Etape 1 : On configure  le fichier /etc/wireguard/wg0.conf avec les informations obtenues précédemment :
        confWG = ''' echo "[Interface]\nPrivateKey = '''+loadFile("privatekey") +''' \nAddress = 120.0.0.1 \nSaveConfig = false \nListenPort = 51820 \nPostUp = iptables -A FORWARD -i wg0 -j ACCEPT; iptables -t nat -A POSTROUTING -o '''+listeInterfaces[1]+''' -j MASQUERADE \nPostDown = iptables -D FORWARD -i wg0 -j ACCEPT; iptables -t nat -D POSTROUTING -o '''+listeInterfaces[1]+''' -j MASQUERADE \nDNS = 8.8.8.8 \n\n[Peer] \n# ClientW \nPublicKey = ''' +clientPubKey+ '''\nAllowedIPs = 120.0.0.2/32" > /etc/wireguard/wg0.conf'''
        startVPN = subprocess.Popen(confWG, shell=True)
        startVPN.wait()

        ## Etape 2 : On active l'interface wg0 du VPN :
        startVPN = subprocess.Popen("wg-quick up wg0", shell=True, preexec_fn=os.setsid)
        startVPN.wait()
        subprocess.call('''echo "Serveur VPN ouvert pour clientW !" ''', shell=True)

if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()
    os.killpg(Agentproc.pid, signal.SIGTERM) #Pour tuer le processus aca-py Agent lancé au départ