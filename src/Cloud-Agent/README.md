# Tutoriel Agent Serveur Wireguard et Agent Indy

- agentb.py = Agent Indy

- agentw.py = Agent Serveur Wireguard

## Installation et préparation : 
- Après avoir récuperé nos fichiers, clonez les fichiers de Aries Cloud Agent et allez au dossier /demo
``` 
git clone https://github.com/hyperledger/aries-cloudagent-python.git
cd aries-cloudagent-python/demo

```
- Remplacer le fichier run_demo dans le dossier par celui proposé ici
- Mettre les fichiers agentb.py et agentw.py dans le dossier /demo/runners

## Éxecution des agents
Pour lancer l'Agent Indy : 
```
LEDGER_URL=http://dev.greenlight.bcovrin.vonx.io ./run_demo agentb
```

Pour lancer l'Agent Serveur Wireguard : 
```
LEDGER_URL=http://dev.greenlight.bcovrin.vonx.io ./run_demo agentw
```

Après avoir lancé les deux agent, choisir les différentes options pour :
- Créer et envoyer un VC
- Demander une Proof Request 
