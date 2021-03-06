import tkinter as tk
import tkinter.font as tkFont
from PIL import Image, ImageTk
import os
import subprocess
import signal
import json
import time
from socket import *
from global_fun import *
from config import *



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

address,interface = listIntAddr()

backgroundColor = 'white'
windowTitle = "Agent ServeurB"

#setting window size
width=400
height=300

# ///// END CONFIG /////


### Commande pour lancer l'agent Von du ServeurB. 
print("Démarrage du von-network ...")
Vonproc = subprocess.Popen(SB_VonStartCommand, shell=True, preexec_fn=os.setsid)
Vonproc.wait()
print("Veuillez attendre 60s ...")
time.sleep(60)
print("von-network OK : http://localhost:9000/")

### Commandes pour enregistrer les utilisateurs dans le von-network
print("Enregistrement des utilisateurs ...")
subprocess.Popen(SB_RegisterCommand_1, shell=True, preexec_fn=os.setsid)
subprocess.Popen(SB_RegisterCommand_2, shell=True, preexec_fn=os.setsid)
subprocess.Popen(SB_RegisterCommand_3, shell=True, preexec_fn=os.setsid)
time.sleep(10)
print("Utilisateurs enregistrés")

### Commande pour lancer l'agent Cloud du ServeurB. 
print("Démarrage du CloudAgent ...")
Agentproc = subprocess.Popen(SB_AgentStartCommand, shell=True, preexec_fn=os.setsid)
Agentproc.wait()
print("Veuillez attendre 30s ...")
time.sleep(30)
print("CloudAgent ServeurB OK")

### Commande pour enregistrer le Credential Schema :
print("Enregistrement du schéma de VC ...")
Credproc = subprocess.Popen(SB_CredentialSchemaCommand, shell=True, preexec_fn=os.setsid)
Credproc.wait()
CredSchema = loadJSON(selfFolderPath + "/ressources/CredSchema.json")
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

        VONimg = Image.open(IMG_von)
        VONimg = VONimg.resize((180, 50), Image.ANTIALIAS)
        VONimg = ImageTk.PhotoImage(VONimg)
        VONlabel = tk.Label(root, image=VONimg)
        VONlabel.image = VONimg
        VONlabel.place(x=15,y=15,width=180,height=50)
        VONlabel.configure(bg=backgroundColor)

        Ariesimg = Image.open(IMG_aries)
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
        #os.killpg(Agentproc.pid, signal.SIGTERM)                    #Pour tuer le processus aca-py Agent lancé au départ
        subprocess.call("~/von-network/manage stop", shell=True)    #Pour tuer le von-network


# Fonction appelée quand on clique sur le bouton "Générer invitation"
    def GButton_3_command(self):
        Invitproc = subprocess.Popen(SB_InvitCommand, shell=True, preexec_fn=os.setsid)
        Invitproc.wait()
        invitJson = loadJSON(selfFolderPath + "/ressources/invitation.json")
        invitURL = json.dumps(invitJson['invitation'])
        self.GLineEdit_3.delete(0, len(self.GLineEdit_3.get()))
        self.GLineEdit_3.insert(1,invitURL)


if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()
    os.killpg(Agentproc.pid, signal.SIGTERM)                    #Pour tuer le processus aca-py Agent lancé au départ
    #subprocess.call("~/von-network/manage stop", shell=True)    #Pour tuer le von-network

    


