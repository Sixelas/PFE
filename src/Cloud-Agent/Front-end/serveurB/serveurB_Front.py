import tkinter as tk
import tkinter.font as tkFont
from PIL import Image, ImageTk
import os
import sys
import subprocess
import signal
import json
import time
from socket import *
from netifaces import interfaces, ifaddresses, AF_INET



# ATTENTION Important :
#
# Script pensé pour être lancé sur ServeurB car il est root ! Sur pc perso faudra modif le code pour ajouter le "sudo" à von-network.
# Si par erreur on ferme l'interface avec ctrl+c dans le terminal, ça kill pas les processus fils aca-py donc il faut les tuer avant de relancer :
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
AgentStartCommand = "aca-py start   --label ServeurB   -it http 0.0.0.0 8000   -ot http   --admin 0.0.0.0 11000   --admin-insecure-mode   --genesis-url http://"+genesisIP+":9000/genesis   --seed ServeurB000000000000000000000000   --endpoint http://"+listeAdresses[1][0]+":8000/   --debug-connections   --public-invites   --auto-provision   --wallet-type indy   --wallet-name ServeurB   --wallet-key secret   --auto-accept-requests --auto-accept-invites --auto-respond-credential-proposal  --auto-respond-credential-offer  --auto-respond-credential-request  --auto-store-credential &"

RegisterCommand_1 = ''' curl -X POST "http://localhost:9000/register" -d '{"seed": "ServeurW000000000000000000000000", "role": "TRUST_ANCHOR", "alias": "ServeurW"}' '''
RegisterCommand_2 = ''' curl -X POST "http://localhost:9000/register" -d '{"seed": "ServeurB000000000000000000000000", "role": "TRUST_ANCHOR", "alias": "ServeurB"}' '''
RegisterCommand_3 = ''' curl -X POST "http://localhost:9000/register" -d '{"seed": "ClientW0000000000000000000000000", "role": "TRUST_ANCHOR", "alias": "ClientW"}' '''

InvitCommand = ''' curl -X POST "http://localhost:11000/out-of-band/create-invitation" -H 'Content-Type: application/json' -d '{ "handshake_protocols": ["did:sov:BzCbsNYhMrjHiqZDTUASHg;spec/didexchange/1.0"],"use_public_did": false}' > invitServeurtW.json '''

CredentialSchemaCommand = ''' curl -X POST http://localhost:11000/schemas -H 'Content-Type: application/json' -d '{"attributes": ["public key","name"],"schema_name": "wg-schema","schema_version": "1.0"}' > CredSchema.json '''

backgroundColor = 'white'
windowTitle = "Agent ServeurB"

#setting window size
width=400
height=300

# ///// END CONFIG /////


### Cette fonction retourne le contenu d'un fichier .json
def loadJSON(filePath):
    with open(filePath, 'r') as file:
        return json.load(file)

### Cette fonction lit un fichier de nom "file" et retourne la première ligne sans le retour à la ligne \n
def loadFile(file) :
    if os.path.exists(selfFolderPath + "/"+ file):
        fichier = open(selfFolderPath + "/"+ file, "r")
        for line in fichier :
            return  line.strip('\n') 
        fichier.close()
    print( "Erreur : " + selfFolderPath + "/" + file +" non trouvé")
    return "Erreur lors de la génération des clés" #Message d'erreur à retourner au choix, ici pensé pour retourner la clé publique wireguard


### Commande pour lancer l'agent Von du ServeurB. 
print("Démarrage du von-network ...")
Vonproc = subprocess.Popen(VonStartCommand, shell=True, preexec_fn=os.setsid)
Vonproc.wait()
print("Veuillez attendre 60s ...")
time.sleep(60)
print("von-network OK : http://localhost:9000/")

### Commandes pour enregistrer les utilisateurs dans le von-network
print("Enregistrement des utilisateurs ...")
subprocess.Popen(RegisterCommand_1, shell=True, preexec_fn=os.setsid)
subprocess.Popen(RegisterCommand_2, shell=True, preexec_fn=os.setsid)
subprocess.Popen(RegisterCommand_3, shell=True, preexec_fn=os.setsid)
time.sleep(10)
print("Utilisateurs enregistrés")

### Commande pour lancer l'agent Cloud du ServeurB. 
print("Démarrage du CloudAgent ...")
Agentproc = subprocess.Popen(AgentStartCommand, shell=True, preexec_fn=os.setsid)
Agentproc.wait()
time.sleep(5)
print("CloudAgent ServeurB OK")

### Commande pour enregistrer le Credential Schema :
print("Enregistrement du schéma de VC ...")
Credproc = subprocess.Popen(CredentialSchemaCommand, shell=True, preexec_fn=os.setsid)
Credproc.wait()
CredSchema = loadJSON(selfFolderPath + "/CredSchema.json")
ID_Schema = json.dumps(CredSchema['schema_id'])
CredentialDefCommand = ''' curl http://localhost:11000/credential-definitions -H 'Content-Type: application/json' -d '{"revocation_registry_size": 4,"schema_id": ''' + ID_Schema + ''',"tag": "default"}' '''
Credproc = subprocess.Popen(CredentialDefCommand, shell=True, preexec_fn=os.setsid)
Credproc.wait()


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

        VONimg = Image.open(selfFolderPath+"/von-logo.png")
        VONimg = VONimg.resize((180, 50), Image.ANTIALIAS)
        VONimg = ImageTk.PhotoImage(VONimg)
        VONlabel = tk.Label(root, image=VONimg)
        VONlabel.image = VONimg
        VONlabel.place(x=15,y=15,width=180,height=50)
        VONlabel.configure(bg=backgroundColor)

        Ariesimg = Image.open(selfFolderPath+"/Aries.png")
        Ariesimg = Ariesimg.resize((160, 45), Image.ANTIALIAS)
        Ariesimg = ImageTk.PhotoImage(Ariesimg)
        Arieslabel = tk.Label(root, image=Ariesimg)
        Arieslabel.image = Ariesimg
        Arieslabel.place(x=15,y=140,width=160,height=45)
        Arieslabel.configure(bg=backgroundColor)

        self.GButton_1=tk.Button(root)
        self.GButton_1["bg"] = "#b9b7f0"
        self.GButton_1["font"] = ft
        self.GButton_1["fg"] = "#000000"
        self.GButton_1["borderwidth"] = "3px"
        self.GButton_1["justify"] = "center"
        self.GButton_1["text"] = "Stop von-network"
        self.GButton_1["relief"] = "groove"
        self.GButton_1.place(x=220,y=20,width=130,height=40)
        self.GButton_1["command"] = self.GButton_1_command

        self.GButton_3=tk.Button(root)
        self.GButton_3["bg"] = "#a9e5a1"
        self.GButton_3["font"] = ft
        self.GButton_3["fg"] = "#000000"
        self.GButton_3["justify"] = "center"
        self.GButton_3["text"] = "Générer Invitation"
        self.GButton_3["relief"] = "groove"
        self.GButton_3["borderwidth"] = "3px"
        self.GButton_3.place(x=220,y=140,width=130,height=40)
        self.GButton_3["command"] = self.GButton_3_command

        self.GLineEdit_3=tk.Entry(root)
        self.GLineEdit_3["bg"] = "#a9e5a1"
        self.GLineEdit_3["borderwidth"] = "1px"
        self.GLineEdit_3["font"] = ft
        self.GLineEdit_3["fg"] = "#333333"
        self.GLineEdit_3["justify"] = "center"
        self.GLineEdit_3["text"] = ""
        self.GLineEdit_3.place(x=15,y=230,width=350,height=40)


# Fonction appelée quand on clique sur le bouton Stop von-network
    def GButton_1_command(self):
        global stop
        #os.killpg(Agentproc.pid, signal.SIGTERM)                    #Pour tuer le processus aca-py Agent lancé au départ
        subprocess.call("~/von-network/manage stop", shell=True)    #Pour tuer le von-network
        stop = True


# Fonction appelée quand on clique sur le bouton "Générer invitation"
    def GButton_3_command(self):
        #Commande pour lancer l'agent Cloud du ServeurB (en tâche de fond si possible, faut pas qu'il bloque le terminal). 
        Invitproc = subprocess.Popen(InvitCommand, shell=True, preexec_fn=os.setsid)
        Invitproc.wait()
        invitJson = loadJSON(selfFolderPath + "/invitServeurtW.json") #Récupère l'invitation dans le fichier json.
        invitURL = json.dumps(invitJson['invitation'])
        self.GLineEdit_3.delete(0, len(self.GLineEdit_3.get()))
        self.GLineEdit_3.insert(1,invitURL)


if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()
    os.killpg(Agentproc.pid, signal.SIGTERM)                    #Pour tuer le processus aca-py Agent lancé au départ
    #subprocess.call("~/von-network/manage stop", shell=True)    #Pour tuer le von-network

    


