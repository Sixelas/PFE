

# Cloud Agent
1. [Explication des différents versions](#explications) 
2. [Tutoriel 1 : Lancer des Agents Cloud en local](#Tuto1)
    1. [Installation](#T1install)
    2. [Réseau noeuds Indy Local (OPTIONNEL)](#T1indy)
    3. [Enregistrement DID](#T1DID)
    4. [Agents](#T1Agents)
3. [Tutoriel 2 : Tutoriel 2 : Issue VC](#Tuto2)
    1. [Création du schema et de la credential definition](#T2CreaSCD)
    2. [Issuer des VC - Méthode étape par étape](#T2IssueE)
    3. [Issuer des VCs - Mode 'automatique'](#T2IssueA)
    4. [Agents](#T1Agents)
3. [Tutoriel 3: Requête et présentation de preuves](#Tuto3)
    1. [Créer une requête de preuve](#T3Create)
    2. [Envoyer notre requête](#T3Send)
    3. [Présentation et Vérification - Mode manuel](#T3VerPresM)
    4. [Présentation et Vérification - Mode automatique](#T3VerPresA)
	
5. [Tutoriel 4 : Agent Serveur Wireguard et Agent Indy sur Docker](#Tuto4)
    1. [Installation (facultative si on utilise le réseau virtuel)](#T4Install)
    2. [Préparation des fichiers](#T4Fichiers)
    3. [Éxecution des agents](#t4Agents)

 


# Explication des différents versions <a name="explications"></a>
Dans les tutoriels ci-dessous, on retrouve 2 types d'Agents Clouds :
- Les Agents Clouds basés sur l'image docker des démos officielles du projet [Hyperledger Aries Cloud Agent - Python - Demo](https://github.com/hyperledger/aries-cloudagent-python/tree/main/demo#the-alicefaber-python-demo).
- Les Agents Clouds Locaux (avec ou sans noeud Indy von-network).

De plus, si on se réfère à notre réseau virtuel [NEmu](https://github.com/Sixelas/PFE/tree/main/src/NEmu) on a deux Clouds Agents sur serveurB et serveurW, qui ont pour scripts agentb.py et agentw.py.


# Tutoriel 1 : lancer des Agent Cloud en local :<a name="Tuto1"></a>

## 1. Installation <a name="T1install"></a>
Pour pouvoir lancer des Agents Clouds, il faut se relier à un réseau de noeuds Indy, normalement mis en place avec Von Network. 
Nous pouvons avoir notre propre réseau de noeuds ou utiliser un déjà existant en ligne. \
Sur l'image debian11.img du réseau NEmu du projet, toutes les dépendances sont déjà installées à l'avance. 

### Avoir son propre réseau de noeuds (OPTIONNEL)
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
Installation basée sur ce tuto mais il est pas totalement à jour donc voir en dessous nos étapes : [Tuto installation libindy+rust](https://hyperledger-indy.readthedocs.io/projects/sdk/en/latest/docs/build-guides/ubuntu-build.html)

Prérequis :
```
apt-get update && \
apt-get install -y \
   build-essential \
   pkg-config \
   cmake \
   libssl-dev \
   libsqlite3-dev \
   libzmq3-dev \
   libncursesw5-dev \
   curl \
   docker.io \
   python3-pip \
   cargo

```
Docker compose : [install](https://docs.docker.com/compose/install/)


Pour installer libsodium : 

```
git clone https://github.com/jedisct1/libsodium --branch stable
cd libsodium/
./configure
make && make check
sudo make install
```

Pour installer libindy : 

```
git clone https://github.com/hyperledger/indy-sdk.git
cd ./indy-sdk/libindy
cargo build
cd
```

Pour libindy modif de path à faire dans certains cas donc on ajoute au .bashrc : 
```
export LD_LIBRARY_PATH=:/root/indy-sdk/libindy/target/debug/ 
``` 
Puis ensuite on fait :
```
sudo ldconfig
source .bashrc 
```

## 2. Réseau noeuds Indy Local (OPTIONNEL) <a name="T1indy"></a>

Pour cette partie j'ai suivi ce [tutoriel](https://ldej.nl/post/becoming-a-hyperledger-aries-developer-getting-started/).
Il y a deux autres tutoriels qui explorent plus le processus de [connexion](https://ldej.nl/post/becoming-a-hyperledger-aries-developer-part-3-connecting-using-didcomm-exchange/) et de [délivrance de VC](https://ldej.nl/post/becoming-a-hyperledger-aries-developer-issue-credentials-v2/), ils sont à la fin du premier tuto. 

### Lancement du réseau de noeuds Indy local (OPTIONNEL)
Pour lancer le réseau il faut juste faire :
```
cd von-network/
./manage start logs
```

## 3. Enregistrement DID <a name="T1DID"></a>

Avant de lancer un agent, il faut enregistrer notre DID auprès du réseau Indy. C'est à nous de faire ceci. 
Nous pouvons faire ceci de deux manières en passant par le webserver ou en utilisant POST : 

1. Nous allons au lien où notre réseau Von Network est hosté : http://localhost:9000 Ou alors si on ne lance pas un réseau, mais on utilise celui en ligne :  http://dev.greenlight.bcovrin.vonx.io
En gauche-bas, il y a un formulaire à remplir. On choisit **“Authenticate a New DID”**. Comme indiqué sur le tutoriel, un DID est dérivé d'une clé publique. La paire clé pub/priv est générée avec une valeur appelée **seed value**. On enregistre un DID, et nous obtenons un seed value.\
 **Exemple :**  Le résultat de la saisie sur le formulaire avec DID=Alice000000000000000000000000000 est :
```
Seed: Alice000000000000000000000000000
DID: UpFt248WuA5djSFThNjBhq
Verkey: GAHDkEKJDZpcpVVcnn5wFpgbtfkrvaceS4oMdki4cU2P 
```
2. Nous pouvons aussi faire une requête POST : (changer http://localost:9000/register par la URL du réseau si on a pas notre propre réseau) \
Exemple avec Alice :
```
curl -X POST "http://localhost:9000/register" \
-d '{"seed": "Alice000000000000000000000000000", "role": "TRUST_ANCHOR", "alias": "Alice"}'
```

## 4. Agents <a name="T1agents"></a>

Avant de lancer un agent, il nous faut la genesis URL, qui est une URL qui décrit notre réseau de noeuds Indy. Si on a notre réseau en local c'est http://localhost:9000/genesis. Sinon on peut utiliser celle en ligne : http://dev.greenlight.bcovrin.vonx.io/genesis

### Lancement des Agents
- Il y a deux 'modes' de lancer aca-py, le mode **provision** et le mode **start**. 
- Le mode **provision**  crée un wallet avant de lancer un agent
- Le mode **start** lance notre agent
- Dans le tutoriel, la personne utilise l'argument **--auto-provision** qui permet de créer un wallet quand on en a pas un, et donc on peut 'éviter' de devoir éxecuter provision avant start. 

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

#### Si on met les 2 Agents sur la même machine : 

Lancement Agent Alice (ISSUER): 
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
  --wallet-key secret \
  --auto-accept-requests \
  --auto-accept-invites
```

Il y a des précisions sur les différents arguments ici, mais pour moi les plus 'importantes' sont :
- --admin 0.0.0.0 11000 : le port que nous ouvrons pour avoir des connections
- --admin-insecure-mode : dans ce mode il y a pas d'authentification, donc n'importe qui ayant notre invitation peut se connecter à nous
- --endpoint http://localhost:8000/ : si on va à cette adresse, nous pouvons voir la doc 
- --wallet-name Alice : chaque nom de wallet est unique, c'est à dire, que si on met un autre nom de wallet on aura un autre wallet
--wallet-key secret : secret = mdp pour accèder à son wallet, donc si au lieu de secret vous mettez 123 vous devrez mettre 123 au lieu de secret

Lancement Agent Bob (HOLDER) :
```
aca-py start \
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
  --wallet-key secret \
  --auto-accept-requests \
  --auto-accept-invites
```

#### Si on met les 2 Agents sur 2 machines différentes :
Pensé pour être fait dans le réseau NEmu du projet sur serveurB et serveurW : [voir ici](https://github.com/Sixelas/PFE/tree/main/src/NEmu) 

1. Sur serveurB après avoir lancé le réseau de noeuds Indy : (préinstallé dans le dossier ~/von-network/ ) \
Lancement Agent Alice (ISSUER): 
```
aca-py start \
  --label Alice \
  -it http 0.0.0.0 8000 \
  -ot http \
  --admin 0.0.0.0 11000 \
  --admin-insecure-mode \
  --genesis-url http://localhost:9000/genesis \
  --seed Alice000000000000000000000000000 \
  --endpoint http://192.168.1.15:8000/ \
  --debug-connections \
  --public-invites \
  --auto-provision \
  --wallet-type indy \
  --wallet-name Alice \
  --wallet-key secret \
  --auto-accept-requests \
  --auto-accept-invites
```
2. Sur serveurW pas de réseau indy von-network à lancer vu qu'il est sur serveurB : \
Lancement Agent Bob (HOLDER) :
```
aca-py start \
  --label Bob \
  -it http 0.0.0.0 8001 \
  -ot http \
  --admin 0.0.0.0 11001 \
  --admin-insecure-mode \
  --genesis-url http://192.168.1.15:9000/genesis \
  --seed Bob00000000000000000000000000000 \
  --endpoint http://192.168.2.13:8001/ \
  --debug-connections \
  --auto-provision \
  --wallet-type indy \
  --wallet-name Bob \
  --wallet-key secret \
  --auto-accept-requests \
  --auto-accept-invites
```


### Connection des Agents - Invitations
Comme dans la demo, il faut que Alice génère des invitations et que Bob les accepte pour que les deux Agents puissent connecter entre eux. 
Si nous regardons la doc dans l'endpoint de Alice, nous pouvons voir les différents champs des invitations. Nous devons éxecuter ces commandes dans une autre instance du terminal évidemment. 

Un exemple d'invitation générée (enregistrée dans un fichier invit.txt): 
``` 
curl -X POST "http://localhost:11000/out-of-band/create-invitation" \
    -H 'Content-Type: application/json' \
    -d '{
   "handshake_protocols": [
     "did:sov:BzCbsNYhMrjHiqZDTUASHg;spec/didexchange/1.0"
   ],
   "use_public_did": false
 }' > invit.txt

```
Le mode **attachments** ne fonctionnait pas pour la personne du tutoriel, donc vaut mieux utiliser le mode **handshake_protocol**.
Il y a deux types d'invitations, publiques et privées. Celle-ci est publique. 
Plus d'info dans le [tutoriel sur les connections](https://ldej.nl/post/becoming-a-hyperledger-aries-developer-part-3-connecting-using-didcomm-exchange/)

Quand nous produisons cette invitation, dans la même instance du terminal (et dans invit.txt) nous avons un résultat de ce type là :
```
{"state": "initial", 
"invitation": 
{
  "@type": "did:sov:BzCbsNYhMrjHiqZDTUASHg;spec/out-of-band/1.0/invitation", 
  "@id": "f99ca578-7d1e-4d5d-a46f-4272c907ea61", 
  "label": "Alice", 
  "handshake_protocols": ["did:sov:BzCbsNYhMrjHiqZDTUASHg;spec/didexchange/1.0"], 
  "services": [
    {
      "id": "#inline", 
      "type": "did-communication", 
      "recipientKeys": ["did:key:z6MkowCqyNXof1gLdbMifvAx1UjNPyfYceoq62ifY35RinMG"], 
      "serviceEndpoint": "http://localhost:8000/"
     }
    ]
  }, 
 "invi_msg_id": "f99ca578-7d1e-4d5d-a46f-4272c907ea61", 
 "trace": false, 
 "invitation_url": "http://localhost:8000/?oob=eyJAdHlwZSI6ICJkaWQ6c292OkJ6Q2JzTlloTXJqSGlxWkRUVUFTSGc7c3BlYy9vdXQtb2YtYmFuZC8xLjAvaW52aXRhdGlvbiIsICJAaWQiOiAiZjk5Y2E1NzgtN2QxZS00ZDVkLWE0NmYtNDI3MmM5MDdlYTYxIiwgImxhYmVsIjogIkFsaWNlIiwgImhhbmRzaGFrZV9wcm90b2NvbHMiOiBbImRpZDpzb3Y6QnpDYnNOWWhNcmpIaXFaRFRVQVNIZztzcGVjL2RpZGV4Y2hhbmdlLzEuMCJdLCAic2VydmljZXMiOiBbeyJpZCI6ICIjaW5saW5lIiwgInR5cGUiOiAiZGlkLWNvbW11bmljYXRpb24iLCAicmVjaXBpZW50S2V5cyI6IFsiZGlkOmtleTp6Nk1rb3dDcXlOWG9mMWdMZGJNaWZ2QXgxVWpOUHlmWWNlb3E2MmlmWTM1UmluTUciXSwgInNlcnZpY2VFbmRwb2ludCI6ICJodHRwOi8vbG9jYWxob3N0OjgwMDAvIn1dfQ=="
 }
```
Notre invitation est donc ici. Nous devons utiliser cette invitation du côté de Bob. \
Petite astuce pour envoyer l'invitation à Bob si Bob et Alice son sur serveurB et serveurW du réseau NEmu (pas sécurisé, juste pour tests) :

1. Sur serverW :
```
nc -lp 1234
```

2. Sur serveurB :
```
cat invit.txt | nc 192.168.2.13 1234
```
On récupère ainsi le contenu de l'invitation avec les champs à utiliser par la suite (commence à {"@type":  .... }).

Du côté de Bob, il faut en premier recevoir cette invitation, en prennant l'invitation générée par Alice.
Pour ceci nous faisons : 
```
curl -X POST "http://localhost:11001/out-of-band/receive-invitation" \
   -H 'Content-Type: application/json' \
   -d '
   {
    "@type": "did:sov:BzCbsNYhMrjHiqZDTUASHg;spec/out-of-band/1.0/invitation", 
    "@id": "f99ca578-7d1e-4d5d-a46f-4272c907ea61", 
    "label": "Alice", 
    "handshake_protocols": ["did:sov:BzCbsNYhMrjHiqZDTUASHg;spec/didexchange/1.0"], 
    "services": [
      {
        "id": "#inline", 
        "type": "did-communication", 
        "recipientKeys": ["did:key:z6MkowCqyNXof1gLdbMifvAx1UjNPyfYceoq62ifY35RinMG"], 
        "serviceEndpoint": "http://localhost:8000/"
     }
    ]
   }'
```

À ce moment là, si on a lancé les agents avec les options --auto-accept-requests et --auto-accept-invites, le reste des étapes s'effectue automatiquement et on peut voir au terme des échanges un message "Received connection complete" sur l'Agent Alice. \
Sinon on continue avec la suite des étapes : \
Quand nous l'avons bien reçue, il faut l'accepter. Dans la réponse, il y a un champ **connection id**, en le copiant nous faisons (sur Bob): 

```
curl -X POST "http://localhost:11001/didexchange/{connection_id}/accept-invitation" -H 'Content-Type: application/json'
```

Du côté d'Alice, il faut que nous acceptions la réponse à notre requête. En prennant le **connection id** qui était dans les réponses affichées dans notre Agent Alice on fait : (ce connection id est différent de celui de Bob)
```
curl -X POST "http://localhost:11000/didexchange/{connection_id}/accept-request" -H 'Content-Type: application/json'
```

Et voilà normalement, la connexion devrait être établie !


# Tutoriel 2 : Issue VC <a name="Tuto2"></a>
Pour ce tutoriel je me suis aidée de ce [tutoriel](https://ldej.nl/post/becoming-a-hyperledger-aries-developer-issue-credentials-v2/)

Nous avons Alice **(ISSUER)** et Bob **(HOLDER)**

Avant de se lancer sur les VC, il faut que le **issuer** crée un schéma et une définition de credential qui décrivent notre VC et ses champs. 

## 1. Création du schema et de la credential definition <a name="T2CreaSCD"></a>
C'est Alice qui va créer les deux

### Création du schema
Dans cet exemple on aura un attribut public key et un attribut name. 
```
curl -X POST http://localhost:11000/schemas \
  -H 'Content-Type: application/json' \
  -d '{
    "attributes": [
      "public key",
      "name"
    ],
    "schema_name": "my-schema",
    "schema_version": "1.0"
}'

```
Ce qui donne cette réponse : 
```
{
"schema_id": "5BLDQMdotBUS3hXjNTbZqm:2:my-schema:1.0", 
"schema": 
	{
	"ver": "1.0", 
	"id": "5BLDQMdotBUS3hXjNTbZqm:2:my-schema:1.0", 
	"name": "", 
	"version": "1.0", 
	"attrNames": ["public key", "name"], 
	"seqNo": 16}
}
```

### Création de la credential definition
Nous utilisons le champ schema_id résultat de la création du schema :
```
curl http://localhost:11000/credential-definitions \
  -H 'Content-Type: application/json' \
  -d '{
    "revocation_registry_size": 4,
    "schema_id": "5BLDQMdotBUS3hXjNTbZqm:2:my-schema:1.0",
    "tag": "default"
  }'
```
Ce qui résulte en : 

```
{"credential_definition_id": "5BLDQMdotBUS3hXjNTbZqm:3:CL:16:default"}
```
 

Si jamais nous voulons récupérer ou checker la credential definition nous pouvons faire :
```
curl http://localhost:11000/credential-definitions/{credential\_definition\_id}
```

Si nous voulons chercher des objets comme schemas ou definitions de credentials dans notre ledger, on peut le faire en allant dans le webserver de notre ledger, dans le cas où c'est en local : [http://localhost:9000/browse/](http://localhost:9000/browse/) 

## 2. Issuer des VC - Méthode étape par étape : <a name="T2IssueE"></a>

Une fois le schéma et la définition créés, c'est le moment de créer des VC. Dans le tutoriel, l'agent qui lance le procès est Bob, le holder. Il y a plusieurs façons de faire : 
1. Le holder envoie une proposal (proposal = décrit un credential definition, donc le holder indique le type de VC qu'il veut recevoir)
2. Le issuer envoie une offre de VC au holder
3. Le holder saute la proposal et juste demande un VC. Le issuer lui donne un VC. 

Un schema de tout ceci peut aussi être consulté [ici](https://github.com/hyperledger/aries-rfcs/tree/main/features/0453-issue-credential-v2#states) - ainsi que des informations plus détaillées sur les états. 


Le tutoriel met en pratique le flow 1. C'est ce flow que je vais décrire ici. 
1. Le holder envoie une proposal au issuer
2. Le issuer envoie une offre au holder basée sur son proposal
3. Le holder envoie une requête pour avoir un credential
4. Le issuer envoie le credential au holder
5. Le holder store le credential
6. Le issuer a un ack

Tous les endpoints utilisés ici peuvent être trouvés dans les docs perspectives des Agents. 

### 1. Le holder envoie une proposal au issuer
Ce credential est très simple, il y a beaucoup plus de champs que nous pouvons ajouter, par exemple un champ avec des proofs. 
```
curl -X POST http://localhost:11001/issue-credential-2.0/send-proposal \
 -H "Content-Type: application/json" -d '{
  "comment": "I want this",
  "connection_id": "baf82399-dbaa-4edc-b921-1e4e6f5b4b88",
  "credential_preview": {
    "@type": "issue-credential/2.0/credential-preview",
    "attributes": [
      {
        "mime-type": "plain/text",
        "name": "name", 
        "value": "Bob"
      },
      {
        "mime-type": "plain/text",
        "name": "age", 
        "value": "120"
      }
    ]
  },
  "filter": {
    "indy": {
      
    }
  }
}'
```
Nous obtenons cette réponse :
```
{"cred_ex_id": "d54463f5-5fe1-45b6-bfcc-28505f13c794", "created_at": "2022-03-09T01:15:14.343365Z", "state": "proposal-sent", "auto_offer": false, "connection_id": "baf82399-dbaa-4edc-b921-1e4e6f5b4b88", "cred_preview": {"@type": "did:sov:BzCbsNYhMrjHiqZDTUASHg;spec/issue-credential/2.0/credential-preview", "attributes": [{"name": "name", "mime-type": "plain/text", "value": "Bob"}, {"name": "age", "mime-type": "plain/text", "value": "120"}]}, "cred_proposal": {"@type": "did:sov:BzCbsNYhMrjHiqZDTUASHg;spec/issue-credential/2.0/propose-credential", "@id": "9a156eb4-dc07-4c89-93f3-a965a93428d0", "filters~attach": [{"@id": "indy", "mime-type": "application/json", "data": {"base64": "e30="}}], "comment": "I want this", "credential_preview": {"@type": "did:sov:BzCbsNYhMrjHiqZDTUASHg;spec/issue-credential/2.0/credential-preview", "attributes": [{"name": "name", "mime-type": "plain/text", "value": "Bob"}, {"name": "age", "mime-type": "plain/text", "value": "120"}]}, "formats": [{"attach_id": "indy", "format": "hlindy/cred-filter@v2.0"}]}, "thread_id": "9a156eb4-dc07-4c89-93f3-a965a93428d0", "by_format": {"cred_proposal": {"indy": {}}}, "auto_issue": false, "updated_at": "2022-03-09T01:15:14.343365Z", "initiator": "self", "role": "holder", "auto_remove": true}
```

Mais la seule valeur que nous allons vraiment utiliser est la valeur du champ **cred_ex_id** : d54463f5-5fe1-45b6-bfcc-28505f13c794

### 2. Le issuer envoie une offre au holder basée sur son proposal
Il faut savoir que les **cred\_ex\_id** sont différentes pour Alice et Bob. Pour consulter celui de Alice, nous consultons les records :
(rien ne s'affiche sur les agents donc obligé de consulter à chaque fois.)
```
curl http://localhost:11000/issue-credential-2.0/records
```
Et nous obtenons un record qui a un champ **cred_ex_id** : 606e7b4b-e1e9-40a3-b2d2-7b992a14913a
```
{"results": [{"cred_ex_record": {"auto_remove": true, "state": "proposal-received", "initiator": "external", "thread_id": "9a156eb4-dc07-4c89-93f3-a965a93428d0", "by_format": {"cred_proposal": {"indy": {}}}, "connection_id": "9b3eb15b-e1ab-4dd0-838c-a18f1373aa76", "cred_preview": {"@type": "did:sov:BzCbsNYhMrjHiqZDTUASHg;spec/issue-credential/2.0/credential-preview", "attributes": [{"name": "name", "mime-type": "plain/text", "value": "Bob"}, {"name": "age", "mime-type": "plain/text", "value": "120"}]}, "cred_ex_id": "606e7b4b-e1e9-40a3-b2d2-7b992a14913a", "cred_proposal": {"@type": "did:sov:BzCbsNYhMrjHiqZDTUASHg;spec/issue-credential/2.0/propose-credential", "@id": "9a156eb4-dc07-4c89-93f3-a965a93428d0", "credential_preview": {"@type": "did:sov:BzCbsNYhMrjHiqZDTUASHg;spec/issue-credential/2.0/credential-preview", "attributes": [{"name": "name", "mime-type": "plain/text", "value": "Bob"}, {"name": "age", "mime-type": "plain/text", "value": "120"}]}, "comment": "I want this", "filters~attach": [{"@id": "indy", "mime-type": "application/json", "data": {"base64": "e30="}}], "formats": [{"attach_id": "indy", "format": "hlindy/cred-filter@v2.0"}]}, "trace": false, "updated_at": "2022-03-09T01:15:14.444459Z", "role": "issuer", "created_at": "2022-03-09T01:15:14.444459Z"}, "indy": null, "ld_proof": null}]}
```
Pour envoyer une offre de VC à Bob on prend ce cred\_ex\_id et on fait : 
```
curl -X POST http://localhost:11000/issue-credential-2.0/records/606e7b4b-e1e9-40a3-b2d2-7b992a14913a/send-offer
```


### 3. Le holder envoie une requête pour avoir un credential
Maintenant, le holder qui a reçu l'offre envoie une requête au issuer pour avoir son credential. Toujours en utilisant le cred\_ex\_id de Bob. 

```
curl -X POST http://localhost:11001/issue-credential-2.0/records/d54463f5-5fe1-45b6-bfcc-28505f13c794/send-request
```

### 4. Le issuer envoie le credential au holder

Le issuer envoie maintenant le credential : 
```
curl -X POST http://localhost:11000/issue-credential-2.0/records/606e7b4b-e1e9-40a3-b2d2-7b992a14913a/issue \
  -H "Content-Type: application/json" -d '{"comment": "Receive your credential"}'
```
  
### 5. Le holder store le credential
Finalement, le holder Bob peut storer le credential : 
```
curl -X POST http://localhost:11001/issue-credential-2.0/records/d54463f5-5fe1-45b6-bfcc-28505f13c794/store \
-H "Content-Type: application/json" -d '{}'
```

Pour consulter ses credentials il suffit à Bob de : 
```
curl -X GET "http://localhost:11001/credentials"
```

## 3. Issuer des VCs - Mode 'automatique' : <a name="T2IssueA"></a>
Avec le mode automatique, au lieu d'utiliser l'endpoint /issue-credential-2.0/send-offer nous utilisons l'endpoint /issue-credential-2.0/send ce qui met les champs auto\_offer et auto\_issue à true.
Il faut juste que du côté holder ça soit aussi automatisé. Pour ceci nous pouvons ajouter des options quand nous lançons nos Agents, par exemple sur Alice :

```
   aca-py start \
  --label Alice \
  -it http 0.0.0.0 8000 \
  -ot http \
  --admin 0.0.0.0 11000 \
  --admin-insecure-mode \
  --genesis-url http://localhost:9000/genesis \
  --seed Alice000000000000000000000000000 \
  --endpoint http://192.168.1.15:8000/ \
  --debug-connections \
  --public-invites \
  --auto-provision \
  --wallet-type indy \
  --wallet-name Alice \
  --wallet-key secret \
  --auto-accept-requests \
  --auto-accept-invites \
  --auto-respond-credential-proposal \
  --auto-respond-credential-offer \
  --auto-respond-credential-request \
  --auto-store-credential

```

Et sur Bob: 

```
aca-py start \
  --label Bob \
  -it http 0.0.0.0 8001 \
  -ot http \
  --admin 0.0.0.0 11001 \
  --admin-insecure-mode \
  --genesis-url http://192.168.1.15:9000/genesis \
  --seed Bob00000000000000000000000000000 \
  --endpoint http://192.168.2.13:8001/ \
  --debug-connections \
  --auto-provision \
  --wallet-type indy \
  --wallet-name Bob \
  --wallet-key secret \
  --auto-accept-requests \
  --auto-accept-invites \
  --auto-respond-credential-proposal \
  --auto-respond-credential-offer \
  --auto-respond-credential-request \
  --auto-store-credential
```

Pour faire ceci il suffit d'utiliser le endpoint indiqué en haut : /issue-credential-2.0/send 
Pas besoin de faire send-proposal du côté de Bob.


Nous le faisons du côté d'Alice : 

```
curl -X POST http://localhost:11000/issue-credential-2.0/send \
 -H "Content-Type: application/json" -d '{
  "comment": "I want this",
  "connection_id": {connection_id_issuer},
  "credential_preview": {
    "@type": "issue-credential/2.0/credential-preview",
    "attributes": [
      {
        "mime-type": "plain/text",
        "name": "name", 
        "value": "Bob"
      },
      {
        "mime-type": "plain/text",
        "name": "age", 
        "value": "120"
      }
    ]
  },
  "filter": {
    "indy": {
      
    }
  }
}'

```

Si tout s'est bien passé, le VC doit être affiché sur notre terminal, et si du côté de Bob nous consultons ses credentials dans son wallet, il devrait s'y trouver.

# Tutoriel 3 : Requête et présentation de preuves : <a name="Tuto3"></a>
Dans notre projet, le ClientW est le Verifier et le ServerW est le holder. Pour mettre en place une connexion VPN entre les deux, le ClientW devra verifier la validité des VCs du ServeurW. 
Pour visualiser l'échange nous nous réferrons au schéma disponible [ici](https://github.com/hyperledger/aries-rfcs/tree/eace815c3e8598d4a8dd7881d8c731fdb2bcc0aa/features/0454-present-proof-v2) 


##  Créer une requête de preuve <a name="T3Create"></a>
Il faut créer une requête en premier du côté **verifier** .  Dans notre requête nous demanderons deux champs, la clé publique et et le nom. 
Pour créer une preuve pas liée à une proposal nous faisons ceci du côté du verifier :
```
curl -X 'POST' \
  'http://localhost:11000/present-proof-2.0/create-request' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "comment": "ServerW proof request",
  "connection_id": "269ecf2b-6ae9-4102-be84-b39d68b0f6f1",
  "presentation_request": {
    "indy": {
      "name": "Proof of Identity",
      "version": "1.0",
      "requested_attributes": {
        "0_public_key_uuid": {
          "name": "public key",
          "restrictions": [
            {
              "cred_def_id": "NLv8K46HrFJXRxhLZCYmqr:3:CL:10:default"
            }
          ]
        },
        "0_name_uuid": {
          "name": "name",
          "restrictions": [
            {
              "cred_def_id": "NLv8K46HrFJXRxhLZCYmqr:3:CL:10:default"
            }
          ]
        },
        "0_self_attested_thing_uuid": {
          "name": "self_attested_thing"
        }
      },
      "requested_predicates": {
        
      }
    }
  }
}'
```
## Envoyer une requête <a name="T3Send"></a>
Une fois la requête est créée il faut l'envoyer. 
- En premier, nous récupérons la requête que nous avons crée. Nous faisons

```
curl -X 'GET' \
  'http://localhost:11000/present-proof-2.0/records' \
  -H 'accept: application/json'
```
- Cette requête renvoie les "dossiers" des différentes opérations que nous avons fait en relation avec des preuves. Du record correspondant, nous récupérons le champ **pres_ex_id**.
- Finalement, en utilisant **pres_ex_id** nous envoyons la requête au **holder**: 
Il faut bien remplacer : http://localhost:11000/present-proof-2.0/records/**pres_ex_id**/send-request

```
curl -X 'POST' \
  'http://localhost:11000/present-proof-2.0/records/4bb43e16-1be7-4a5a-a4aa-6930fdb464c8/send-request' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "trace": true
}'
```
## Présentation et Vérification - Mode manuel <a name="T3VerPresM"></a> 
### Serveur W récupère le record de la requête
Il faut récupèrer le record de la requête reçue du côté ServeurW. Pour faire ceci, on fait encore une fois : 
```
curl -X 'GET' \
  'http://localhost:11000/present-proof-2.0/records' \
  -H 'accept: application/json'
```

On récupère le champ **pres_ex_id**.

### ServeurW envoie la présentation
Une fois, nous avons récupéré le champ il faut l'utiliser dans le endpoint pour envoyer la présentation.
Le champ de la presentation **cred_id** est l'identifiant de notre **Verifiable Credential**. 

```
curl -X 'POST' \
  'http://localhost:11000/present-proof-2.0/records/16c43ece-0fcc-420b-9141-903177bd3f8e/send-presentation' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{

  "indy": {
    "requested_attributes": {
      "0_public_key_uuid": {
        "cred_id": "4073d1fa-f375-4441-ab7b-4de78f82277c",
        "revealed": true
      },
      "0_name_uuid": {
        "cred_id": "4073d1fa-f375-4441-ab7b-4de78f82277c",
        "revealed": true
      }
    },
    "requested_predicates": {

    },
    "self_attested_attributes": {
      "0_self_attested_thing_uuid": "self_attested_thing"
    },
    "trace": false
  },
  "trace": true
}'
```

### ClientW récupère la présentation
Il faut que le ClientW récupère encore une fois le champ **pres_ex_id**. 

### ClientW vérifie la présentation 
Une fois le champ **pres_ex_id** récupéré il suffit de verifier la présentation : 
( Ne pas oublier de remplacer le champ **pres_ex_id** dans le endpoint. )

```
curl -X 'POST' \
  'http://localhost:11000/present-proof-2.0/records/27b7b92c-9c04-4b01-a8c3-4208ac245f9d/verify-presentation' \
  -H 'accept: application/json' \
  -d ''
  ```
  
 ## Présentation et Vérification - Mode automatique <a name="T3VerPresM"></a> 
 Pour répondre à une requête de preuve et la valider, il faut juste mettre les options automatiques quand on lance nos agents. 
 On considère que Alice est notre **ServerB**, donc notre **holder**. Et que Bob est notre **ServeurW**, donc notre **verifier**. 
 
 ```
   aca-py start \
  --label Alice \
  -it http 0.0.0.0 8000 \
  -ot http \
  --admin 0.0.0.0 11000 \
  --admin-insecure-mode \
  --genesis-url http://localhost:9000/genesis \
  --seed Alice000000000000000000000000000 \
  --endpoint http://192.168.1.15:8000/ \
  --debug-connections \
  --public-invites \
  --auto-provision \
  --wallet-type indy \
  --wallet-name Alice \
  --wallet-key secret \
  --auto-accept-requests \
  --auto-accept-invites \
  --auto-respond-credential-proposal \
  --auto-respond-credential-offer \
  --auto-respond-credential-request \
  --auto-store-credential \
  --auto-respond-presentation-request 

```

Et sur Bob: 

```
aca-py start \
  --label Bob \
  -it http 0.0.0.0 8001 \
  -ot http \
  --admin 0.0.0.0 11001 \
  --admin-insecure-mode \
  --genesis-url http://192.168.1.15:9000/genesis \
  --seed Bob00000000000000000000000000000 \
  --endpoint http://192.168.2.13:8001/ \
  --debug-connections \
  --auto-provision \
  --wallet-type indy \
  --wallet-name Bob \
  --wallet-key secret \
  --auto-accept-requests \
  --auto-accept-invites \
  --auto-respond-credential-proposal \
  --auto-respond-credential-offer \
  --auto-respond-credential-request \
  --auto-store-credential \
  --auto-verify-presentation
```


# Tutoriel 4 : Agent Serveur Wireguard et Agent Indy sur Docker : <a name="Tuto4"></a>

- agentb.py = Agent Indy (sur la VM serveurB du réseau virtuel du projet).

- agentw.py = Agent Serveur Wireguard (sur la VM serveurW du réseau virtuel du projet).

## 1. Installation (facultative si on utilise le réseau virtuel) : <a name="T4Install"></a>
Dans le cas où vous n'utilisez pas notre réseau virtuel et VMs  (qui se trouve [ici](https://github.com/Sixelas/PFE/tree/main/src/NEmu)) :
- Après avoir récupéré nos fichiers, clonez les fichiers de Aries Cloud Agent et allez au dossier /demo
``` 
git clone https://github.com/hyperledger/aries-cloudagent-python.git
cd aries-cloudagent-python/demo

```

## 2. Préparation des fichiers : <a name="T4Fichiers"></a>
- Remplacer le fichier run_demo dans /demo par celui proposé ici.
- Mettre les fichiers agentb.py et agentw.py dans le dossier aries-coudagent-python/demo/runners.

## Éxecution des agents : <a name="T4Agents"></a>
Pour lancer l'Agent Indy : 
```
LEDGER_URL=http://dev.greenlight.bcovrin.vonx.io ./run_demo agentb
```

Pour lancer l'Agent Serveur Wireguard : 
```
LEDGER_URL=http://dev.greenlight.bcovrin.vonx.io ./run_demo agentw
```

- Après avoir lancé les deux agents, copier l'invitation de l'Agent Indy agentb (au dessus du QR généré) et la coller du côté du serveur Wireguard agentw.
- Une fois la connexion entre les deux établie, choisir les différentes options pour :
- Créer et envoyer un VC
- Demander une Proof Request 
