# PFE

Projet de Fin d'Etudes de Master 2 Réseaux de Communication et Internet

## Présentation du projet :

L'objectif de ce projet est d'installer et de configurer le logiciel Wireguard sur une plateforme Android et éventuellement sur une plateforme Raspberry (toutes deux basées sur des processeurs ARM). \
Des machines virtuelles seront utilisées pour créer ces équipements. Elles s'appuieront sur les logiciels QEMU et KVM. \
Un réseau virtuel sera mis en place avec le logiciel NEmu afin d'interconnecter les machines virtuelles. \
Il faudra que les équipements utilisent le logiciel *Aries Static Agent - Python* (initialement prévu, mais maintenant nous utilisons Aries Mobile Agent à la place) pour implémenter l’agent mobile qui communiquera avec l’agent ACA-py situé sur les noeuds Indy du projet 2. \
Il faudra donc coder en Python un petit logiciel permettant de récupérer les Verifiable Credentials (VC) sur la blockchain puis d'en extraire les clés à utiliser pour Wireguard. \
Toutes les étapes d'installation et de configuration devront être documentées en détail et le code devra être commenté et spécifié en UML (diagramme de classe, d'états et de séquence).

## Topologie du Réseau Virtuel et des interactions entre machines :

![alt text](https://github.com/Sixelas/PFE/blob/main/docs/wk_reports/S10/topo.png)

## Architecture :

- docs&emsp;&emsp;-->&emsp;&emsp;Contient les rapports de RDV clients, le Mémoire et les rapports quotidiens.
- src&emsp;&emsp;&emsp;-->&emsp;&emsp;Contient le code du projet.
- final&emsp;&emsp;-->&emsp;&emsp;Contient le code du rendu final du projet.
- Tests&emsp;&emsp;-->&emsp;&emsp;Contient des scripts de test initiaux.

## Tester le projet :

Pour lancer le réseau virtuel et tester les Agents, suivre [ce tutoriel](https://github.com/Sixelas/PFE/tree/main/src/final) 

Vous pouvez aussi regarder cette vidéo de démonstration :\
[![Alt text for your video](https://img.youtube.com/vi/u6M6-7f82Ew/0.jpg)](https://www.youtube.com/watch?v=u6M6-7f82Ew)
## Rapport :
Le rapport du projet est consultable [ici](https://github.com/Sixelas/PFE/tree/main/docs/report/Rendu.pdf) 

## Dépendances & Licence :

- [Apache License Version 2.0](https://github.com/Sixelas/PFE/blob/main/LICENSE.md)
- Projet basé sur Aries Hyperledger : [dépot original](https://github.com/hyperledger/aries)
- Dans src/Mobile-Agent nous avons repris et modifié le code du projet
[Aries Mobile Agent React Native](https://github.com/hyperledger/aries-mobile-agent-react-native)
- Dans src/Cloud-Agent nous avons repris et modifié le code du projet [Hyperledger Aries Cloud Agent - Python](https://github.com/hyperledger/aries-cloudagent-python)
