import os


# Chemin du dossier qui contient ce fichier .py
selfFolderPath = os.getcwd() 


################## PATH DES IMAGES ##################
IMG_wg = selfFolderPath+"/ressources/wg.png"
IMG_aries = selfFolderPath+"/ressources/Aries.png"
IMG_von = selfFolderPath+"/ressources/von-logo.png"



################## CONFIG WIREGUARD ##################
umask = "umask 077"
WG_genkey = "wg genkey | tee ressources/privatekey | wg pubkey > ressources/publickey"
WG_up = "wg-quick up wg0"
WG_down = "wg-quick down wg0"
WG_rm = "rm /etc/wireguard/wg0.conf"



################## CONFIG LAUNCHER.PY ##################
LauncherText1 = "\n\n!!! ATTENTION !!!\nPenser à vérifier la config dans config.py avant de lancer un agent\n\n"
LauncherText2 = "Choisir l'agent à lancer :\n1 --> ServeurB\n2 --> ServeurW\n3 --> ClientW\n"



################## COMMANDES GLOBALES ##################
# Commande pour envoyer une invitation request
InvitRequest = ''' curl -X POST "http://localhost:11000/out-of-band/receive-invitation" -H 'Content-Type: application/json' -d ' '''
# Commande pour récupérer le VC obtenu et le mettre dans WG_VC.json
Credentials = ''' curl -X GET "http://localhost:11000/credentials" > '''+ selfFolderPath+'''/ressources/WG_VC.json'''
# Commande pour enregistrer les connexions dans un fichier
Connections = ''' curl http://localhost:11000/connections > '''+ selfFolderPath+'''/ressources/Connection_logs.json '''
# Commande pour enregistrer les proof records dans un fichier
proofRecord = ''' curl -X 'GET' 'http://localhost:11000/present-proof-2.0/records' -H 'accept: application/json' > '''+ selfFolderPath+'''/ressources/ProofRecord.json '''



################## CONFIG DE SERVEURB.PY ##################
ip_serveurB = "192.168.1.15"
genesisIP = "localhost"         # localhost si le von-network est en local sur ServeurB
# Commande pour lancer le von-network
SB_VonStartCommand = "~/von-network/manage start logs"
# Commande pour lancer l'agent ServeurB
SB_AgentStartCommand = "aca-py start   --label ServeurB   -it http 0.0.0.0 8000   -ot http   --admin 0.0.0.0 11000   --admin-insecure-mode   --genesis-url http://"+genesisIP+":9000/genesis   --seed ServeurB000000000000000000000000   --endpoint http://"+ip_serveurB+":8000/   --debug-connections   --public-invites   --auto-provision   --wallet-type indy   --wallet-name ServeurB   --wallet-key secret   --auto-accept-requests --auto-accept-invites --auto-respond-credential-proposal  --auto-respond-credential-offer  --auto-respond-credential-request  --auto-store-credential &"
# Commandes pour enregistrer les agents dans le von-network
SB_RegisterCommand_1 = ''' curl -X POST "http://localhost:9000/register" -d '{"seed": "ServeurW000000000000000000000000", "role": "TRUST_ANCHOR", "alias": "ServeurW"}' '''
SB_RegisterCommand_2 = ''' curl -X POST "http://localhost:9000/register" -d '{"seed": "ServeurB000000000000000000000000", "role": "TRUST_ANCHOR", "alias": "ServeurB"}' '''
SB_RegisterCommand_3 = ''' curl -X POST "http://localhost:9000/register" -d '{"seed": "ClientW0000000000000000000000000", "role": "TRUST_ANCHOR", "alias": "ClientW"}' '''
# Commande pour générer une invitation
SB_InvitCommand = ''' curl -X POST "http://localhost:11000/out-of-band/create-invitation" -H 'Content-Type: application/json' -d '{ "handshake_protocols": ["did:sov:BzCbsNYhMrjHiqZDTUASHg;spec/didexchange/1.0"],"use_public_did": false}' > '''+selfFolderPath+'''/ressources/invitation.json '''
# Commande pour générer un credential schema 
SB_CredentialSchemaCommand = ''' curl -X POST http://localhost:11000/schemas -H 'Content-Type: application/json' -d '{"attributes": ["public key","name"],"schema_name": "wg-schema","schema_version": "1.0"}' > '''+selfFolderPath+'''/ressources/CredSchema.json '''



################## CONFIG DE SERVEURW.PY ##################
ip_serveurW = "192.168.2.13"
ip_dns = "192.168.2.1"          # l'adresse ip du serveur dns, donc ici VRouter
# Commande pour lancer l'agent ServeurW
SW_AgentStartCommand = "aca-py start   --label ServeurW   -it http 0.0.0.0 8000   -ot http   --admin 0.0.0.0 11000   --admin-insecure-mode   --genesis-url http://"+ip_serveurB+":9000/genesis   --seed ServeurW000000000000000000000000   --endpoint http://"+ip_serveurW+":8000/   --debug-connections   --public-invites   --auto-provision   --wallet-type indy   --wallet-name ServeurW   --wallet-key secret   --auto-accept-requests --auto-accept-invites  --auto-respond-credential-proposal  --auto-respond-credential-offer  --auto-respond-credential-request  --auto-store-credential --auto-respond-presentation-request --auto-respond-presentation-proposal --auto-verify-presentation &"
# Commande pour générer une invitation à ClientW
SW_InvitCommand = ''' curl -X POST "http://localhost:11000/out-of-band/create-invitation" -H 'Content-Type: application/json' -d '{ "handshake_protocols": ["did:sov:BzCbsNYhMrjHiqZDTUASHg;spec/didexchange/1.0"],"use_public_did": false}' > '''+ selfFolderPath+'''/ressources/invitClientW.json '''



################## CONFIG DE CLIENTW.PY ##################
ip_clientW = "192.168.3.20"
# Commande pour lancer l'agent ClientW
CW_AgentStartCommand = "aca-py start   --label ClientW   -it http 0.0.0.0 8000   -ot http   --admin 0.0.0.0 11000   --admin-insecure-mode   --genesis-url http://"+ip_serveurB+":9000/genesis   --seed ClientW0000000000000000000000000   --endpoint http://"+ip_clientW+":8000/   --debug-connections   --public-invites   --auto-provision   --wallet-type indy   --wallet-name ClientW   --wallet-key secret   --auto-accept-requests --auto-accept-invites  --auto-respond-credential-proposal  --auto-respond-credential-offer  --auto-respond-credential-request  --auto-store-credential --auto-respond-presentation-request --auto-respond-presentation-proposal --auto-verify-presentation &"


################## COMMANDES POUR LAUNCHER.PY ##################
git = ''' git pull '''
SB = ''' python3 ServeurB.py '''
SW = ''' python3 ServeurW.py '''
CW = ''' python3 ClientW.py '''