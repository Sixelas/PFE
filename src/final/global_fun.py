import os
import subprocess
import json
from socket import *
import time
from netifaces import interfaces, ifaddresses, AF_INET
from config import *


### Cette fonction lit un fichier de nom "file" et retourne la première ligne sans le retour à la ligne \n
def loadFile(file) :
    if os.path.exists(selfFolderPath + "/ressources/"+ file):
        fichier = open(selfFolderPath + "/ressources/"+ file, "r")
        for line in fichier :
            return  line.strip('\n')
        fichier.close()
    print( "Erreur : " + selfFolderPath + "/ressources/" + file +" non trouvé")
    return "Erreur lors de la génération des clés" #Message d'erreur à retourner au choix, ici pensé pour retourner la clé publique wireguard

### Cette fonction retourne le contenu d'un fichier .json
def loadJSON(filePath):
    try:
        with open(filePath, 'r') as file:
            return json.load(file)
    except IOError:
        print("Erreur: Le fichier ne semble pas exister")
        return 0


### Fonction qui permet d'extraire la clé publique de serverName qui se trouve dans le VP qu'il a envoyé 
def extractPubKey(serverName, file) :
    
    dataJson = loadJSON(selfFolderPath + "/ressources/"+file)
    
    for case in dataJson['results'] :
        if(case['by_format']['pres']['indy']['requested_proof']['revealed_attrs']['0_name_uuid']['raw'] == serverName) :
                extractKey = case['by_format']['pres']['indy']['requested_proof']['revealed_attrs']['0_public_key_uuid']['raw']
                return ''.join(x for x in extractKey if x not in '''"''')

    print(serverName+" n'est pas un Agent reconnu")
    return ""

### Fonction qui permet d'extraire l'id de la connection avec serverName
def extractConnectID(serverName, file) :

    dataJson = loadJSON(selfFolderPath + "/ressources/"+file)
    
    for case in dataJson['results'] :
        if(case['their_label'] == serverName) :
                return case['connection_id']
    print(serverName+" n'est pas un Agent reconnu")
    return ""

### Fonction qui supprime toutes les connexions actives de l'Agent
def deleteConnexions(file) :
    #A voir si dans certains cas il faut pas faire une maj du fichier de logs avant de s'en servir
    dataJson = loadJSON(selfFolderPath + "/ressources/"+file)
    
    for case in dataJson['results'] :
        id = ''.join(x for x in case['connection_id'] if x not in '''"''')
        print("\nSuppression de la connexion avec "+case['their_label']+" d'identifiant "+id+"\n")
        deleteCommand = ''' curl -X 'DELETE' 'http://localhost:11000/connections/''' + id + ''' ' -H 'accept: application/json' '''
        deleteProc = subprocess.Popen(deleteCommand, shell=True, preexec_fn=os.setsid)
        deleteProc.wait()
        time.sleep(3)

###TODO Fonction pour révoquer tous les VC possédés par l'Agent
def revokeVC(file) :
    print("TODO revokeVC")

### Fonction pour supprimer la config WireGuard active
def resetWG() :
    resetVPN = subprocess.Popen(WG_down, shell=True, preexec_fn=os.setsid)
    resetVPN.wait()
    resetVPN = subprocess.Popen(WG_rm, shell=True, preexec_fn=os.setsid)
    resetVPN.wait()


### Fonction pour récupérer automatiquement l'@ip et l'interface de la machine reliée au LAN.
# https://stackoverflow.com/questions/166506/finding-local-ip-addresses-using-pythons-stdlib
def listIntAddr():
    listeAdresses = []*len(interfaces())
    listeInterfaces = []*len(interfaces())
    for ifaceName in interfaces():
        addresses = [i['addr'] for i in ifaddresses(ifaceName).setdefault(AF_INET, [{'addr':'No IP addr'}] )]
        listeAdresses.append(addresses)
        listeInterfaces.append(ifaceName)
    return listeAdresses[1][0], listeInterfaces[1]
