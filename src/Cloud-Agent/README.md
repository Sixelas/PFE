# Tutoriel Agent Serveur Wireguard et Agent Indy

- agentb.py = Agent Indy

- agentw.py = Agent Serveur Wireguard

## Installation :
### Dans le cas où vous n'utilisez pas notre réseau virtuel et VMs :
- Après avoir récuperé nos fichiers, clonez les fichiers de Aries Cloud Agent et allez au dossier /demo
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
