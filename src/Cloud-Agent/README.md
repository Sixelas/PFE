# Tutoriel pour lancer des Agent Cloud en local :

## Installation 
Pour pouvoir lancer des Agents Clouds, il faut se relier à un réseau de noeuds Indy, normalement mis en place avec Von Network. 
Nous pouvons avoir notre propre réseau de noeuds ou utiliser un déjà mis en place (c'est le prof qui nous a donné celui-ci).

### Avoir son propre réseau de noeuds
Pour avoir son propre réseau de noeuds il faut installer/build Von Network :

```
git clone https://github.com/bcgov/von-network
cd von-network
./manage build
```

Pour lancer notre réseau il suffit de faire :
```
./manage start logs
```

Pour l'arrêter on fait simplement :
```
./manage stop
```

### ACA-PY
Il faut installer aca-py :
```
pip install aries-cloudagent
```

- Si jamais il y a une erreur du type : ModuleNotFoundError: No module named 'indy'
- Il faut installer indy : 
```
pip install python3_indy
```

### libindy, rust et libsodium
Il faut installer libindy et rust, j'ai installé libsodium différemment car le dépôt de la partie 3. est vieux : [Tuto installation libindy+rust](https://hyperledger-indy.readthedocs.io/projects/sdk/en/latest/docs/build-guides/ubuntu-build.html)

Pour installer libsodium : 

```
git clone https://github.com/jedisct1/libsodium --branch stable
./configure
make && make check
sudo make install
```

## Lancement Réseau noeuds Indy

Pour cette partie j'ai suivi ce [tutoriel](https://ldej.nl/post/becoming-a-hyperledger-aries-developer-getting-started/)
Il y a deux autres tutoriels qui explorent plus le procès de connexion et de délivrance de VC, ils sont à la fin du premier tuto. 

### Lancement du réseau de noeuds Indy (OPTIONNEL)
Pour lancer le réseau il faut juste faire :
```
./manage start logs
```

## Enregistrement DID

Avant de lancer un agent, il faut enregistrer notre DID auprès du réseau Indy. C'est à nous de faire ceci. 
Nous pouvons faire ceci de deux manières en passant par le webserver ou en utilisant POST : 

1. Nous allons au lien où notre réseau Von Network est hosté : https://localhost:9000
En gauche-bas, il y a un formulaire à remplir. On choisit **“Authenticate a New DID”**. Comme indiqué sur le tutoriel, un DID est dérivé d'une clé publique. La paire clé pub/priv est générée avec une valeur appellée **seed value**. On enregistre un DID, et nous obtenons un seed value. Exemple:  résultat de formulaire avec DID=Alice000000000000000000000000000 est:
```
Seed: Alice000000000000000000000000000
DID: UpFt248WuA5djSFThNjBhq
Verkey: GAHDkEKJDZpcpVVcnn5wFpgbtfkrvaceS4oMdki4cU2P 
```
2. Nous pouvons aussi faire une requête POST : 
Exemple :
```
curl -X POST "http://localhost:9000/register" \
-d '{"seed": "Alice000000000000000000000000001", "role": "TRUST_ANCHOR", "alias": "Alice"}
```

## Agents

Avant de lancer un agent, il nous faut la genesis URL, ceci est une URL qui décrit notre réseau de noeuds Indy. Si on a notre réseau en local c'est http://localhost:9000/genesis. Sinon on peut utiliser celle du prof : http://dev.greenlight.bcovrin.vonx.io/genesis

### Lancement Agents
-Il y a deux 'modes' de lancer aca-py, le mode **provision** et le mode **start**. 
-Le mode **provision**  crée un wallet avant de lancer un agent
-Le mode **start** lance notre agent
-Dans le tutoriel, la personne utilise l'argument **--auto-provision** qui permet de créer un wallet quand on en a pas un, et donc on peut 'éviter' de devoir éxecuter provision avant start. 

Pour créer un wallet :
```
aca-py provision [arguments]
```
Pour voir les différents arguments : 
```
aca-py provision -h
```

Pour lancer un Agent - dans ce cas Alice il faut faire :
```
aca-py start [arguments]
```
Pour avoir accès aux différents arguments :
```
aca-py start -h
```


Exemple lancement Agent Alice (ISSUER): 
```
aca-py start \
  --label Alice \
  -it http 0.0.0.0 8000 \
  -ot http \
  --admin 0.0.0.0 11000 \
  --admin-insecure-mode \
  --genesis-url http://localhost:9000/genesis \
  --seed Alice000000000000000000000000000 \
  --endpoint http://localhost:8000/ \
  --debug-connections \
  --public-invites \
  --auto-provision \
  --wallet-type indy \
  --wallet-name Alice \
  --wallet-key secret
```

Il y a des précisions sur les différents arguments ici, mais pour moi les plus 'importantes' sont :
- --admin 0.0.0.0 11000 : le port que nous ouvrons pour avoir des connections
- --admin-insecure-mode : dans ce mode il y a pas d'authentification, donc n'importe qui ayant notre invitation peut se connecter à nous
- --endpoint http://localhost:8000/ : si on va à cette adresse, nous pouvons voir la doc 
- --wallet-name Alice : chaque nom de wallet est unique, c'est à dire, que si on met un autre nom de wallet on aura un autre wallet
--wallet-key secret : secret = mdp pour accèder à son wallet, donc si au lieu de secret vous mettez 123 vous devrez mettre 123 au lieu de secret

Exemple lancement Agent Bob (HOLDER) :
```aca-py start \
  --label Bob \
  -it http 0.0.0.0 8001 \
  -ot http \
  --admin 0.0.0.0 11001 \
  --admin-insecure-mode \
  --genesis-url http://localhost:9000/genesis \
  --seed Bob00000000000000000000000000000 \
  --endpoint http://localhost:8001/ \
  --debug-connections \
  --auto-provision \
  --wallet-type indy \
  --wallet-name Bob \
  --wallet-key secret
```

### Connection des Agents - Invitations
Comme dans la demo, il faut que Alice génère des invitations et que Bob les accepte pour que les deux Agents puissent connecter entre eux. 
Si nous regardons la doc dans l'endpoint de Alice, nous pouvons voir les différents champs des invitations. Nous devons éxecuter ces commandes dans une autre instance du terminal évidemment. 

Un exemple d'invitation  : 
``` 
curl -X POST "http://localhost:11000/out-of-band/create-invitation" \
    -H 'Content-Type: application/json' \
    -d '{
   "handshake_protocols": [
     "did:sov:BzCbsNYhMrjHiqZDTUASHg;spec/didexchange/1.0"
   ],
   "use_public_did": false
 }'

```
Le mode **attachments** ne fonctionnait pas pour la personne du tutoriel, donc vaut mieux utiliser le mode **handshake_protocol**.
Il y a deux types d'invitations, publiques et privées. Celle-ci est publique. 
Plus d'info dans le [tutoriel sur les connections](https://ldej.nl/post/becoming-a-hyperledger-aries-developer-part-3-connecting-using-didcomm-exchange/)

Quand nous produisons cette invitation, dans la même instance du terminal nous avons un résultat de ce type là :
```{"state": "initial", "invitation": {"@type": "did:sov:BzCbsNYhMrjHiqZDTUASHg;spec/out-of-band/1.0/invitation", "@id": "f99ca578-7d1e-4d5d-a46f-4272c907ea61", "label": "Alice", "handshake_protocols": ["did:sov:BzCbsNYhMrjHiqZDTUASHg;spec/didexchange/1.0"], "services": [{"id": "#inline", "type": "did-communication", "recipientKeys": ["did:key:z6MkowCqyNXof1gLdbMifvAx1UjNPyfYceoq62ifY35RinMG"], "serviceEndpoint": "http://localhost:8000/"}]}, "invi_msg_id": "f99ca578-7d1e-4d5d-a46f-4272c907ea61", "trace": false, "invitation_url": "http://localhost:8000/?oob=eyJAdHlwZSI6ICJkaWQ6c292OkJ6Q2JzTlloTXJqSGlxWkRUVUFTSGc7c3BlYy9vdXQtb2YtYmFuZC8xLjAvaW52aXRhdGlvbiIsICJAaWQiOiAiZjk5Y2E1NzgtN2QxZS00ZDVkLWE0NmYtNDI3MmM5MDdlYTYxIiwgImxhYmVsIjogIkFsaWNlIiwgImhhbmRzaGFrZV9wcm90b2NvbHMiOiBbImRpZDpzb3Y6QnpDYnNOWWhNcmpIaXFaRFRVQVNIZztzcGVjL2RpZGV4Y2hhbmdlLzEuMCJdLCAic2VydmljZXMiOiBbeyJpZCI6ICIjaW5saW5lIiwgInR5cGUiOiAiZGlkLWNvbW11bmljYXRpb24iLCAicmVjaXBpZW50S2V5cyI6IFsiZGlkOmtleTp6Nk1rb3dDcXlOWG9mMWdMZGJNaWZ2QXgxVWpOUHlmWWNlb3E2MmlmWTM1UmluTUciXSwgInNlcnZpY2VFbmRwb2ludCI6ICJodHRwOi8vbG9jYWxob3N0OjgwMDAvIn1dfQ=="}
```
Notre invitation est donc ici. Nous devons utiliser cette invitation du côté de Bob.

Du côté de Bob, il faut en premier recevoir cette invitation, en prennant l'invitation générée par Alice.
Pour ceci nous faisons : 
```
curl -X POST "http://localhost:11001/out-of-band/receive-invitation" \
   -H 'Content-Type: application/json' \
   -d '{"@type": "did:sov:BzCbsNYhMrjHiqZDTUASHg;spec/out-of-band/1.0/invitation", "@id": "f99ca578-7d1e-4d5d-a46f-4272c907ea61", "label": "Alice", "handshake_protocols": ["did:sov:BzCbsNYhMrjHiqZDTUASHg;spec/didexchange/1.0"], "services": [{"id": "#inline", "type": "did-communication", "recipientKeys": ["did:key:z6MkowCqyNXof1gLdbMifvAx1UjNPyfYceoq62ifY35RinMG"], "serviceEndpoint": "http://localhost:8000/"}]}'
```
Quand nous l'avons bien reçue, il faut l'accepter. Dans l'invitation, il y a un champ **@id**, en le copiant nous faison : 

```
curl -X POST "http://localhost:11001/didexchange/f99ca578-7d1e-4d5d-a46f-4272c907ea61/accept-invitation" -H 'Content-Type: application/json'
```

Et voilà normalement, la connexion devrait être établie !

















# Tutoriel Agent Serveur Wireguard et Agent Indy

- agentb.py = Agent Indy

- agentw.py = Agent Serveur Wireguard

## Installation :
### Dans le cas où vous n'utilisez pas notre réseau virtuel et VMs  (qui se trouve [ici](https://github.com/Sixelas/PFE/tree/main/src/NEmu)):
- Après avoir récupéré nos fichiers, clonez les fichiers de Aries Cloud Agent et allez au dossier /demo
``` 
git clone https://github.com/hyperledger/aries-cloudagent-python.git
cd aries-cloudagent-python/demo

```

## Préparation des fichiers :
- Remplacer le fichier run_demo dans le dossier par celui proposé ici
- Mettre les fichiers agentb.py et agentw.py dans le dossier aries-coudagent-python/demo/runners

## Éxecution des agents
Pour lancer l'Agent Indy : 
```
LEDGER_URL=http://dev.greenlight.bcovrin.vonx.io ./run_demo agentb
```

Pour lancer l'Agent Serveur Wireguard : 
```
LEDGER_URL=http://dev.greenlight.bcovrin.vonx.io ./run_demo agentw
```

- Après avoir lancé les deux agents, copier l'invitation de l'Agent Indy (au dessus du QR) et la copier du côté du serveur Wireguard.
- Une fois la connexion entre les deux établie, choisir les différentes options pour :
- Créer et envoyer un VC
- Demander une Proof Request 
