# PFE

Projet de Fin d'Etudes de Master 2 Réseaux de Communication et Internet

## Présentation du projet :

L'objectif de ce projet est d'installer et de configurer le logiciel Wireguard sur une plateforme Android et éventuellement sur une plateforme Raspberry (toutes deux basées sur des processeurs ARM).
Des machines virtuelles seront utilisées pour créer ces équipements.
Elles s'appuieront sur les logiciels QEMU et KVM.
Un réseau virtuel sera mis en place avec le logiciel NEmu afin d'interconnecter les machines virtuelles.
Wireguard nécessite des clés de chiffrement qui seront distribuées par le projet 2 décrit ci-dessous.
Il faudra que les équipements utilisent le logiciel *Aries Static Agent - Python* pour implémenter l’agent mobile qui communiquera avec l’agent ACA-py situé sur les noeuds Indy du projet 2.
Il faudra donc coder en Python un petit logiciel permettant de récupérer les Verifiable Credentials (VC) sur la blockchain puis d'en extraire les clés à utiliser pour Wireguard.
Toutes les étapes d'installation et de configuration devront être documentées en détail et le code devra être commenté et spécifié en UML (diagramme de classe, d'états et de séquence).


![alt text](https://github.com/Sixelas/PFE/blob/main/docs/wk_reports/S7/topologieV3.jpg)

## Explication des dossiers :

- docs/ : Contient les rapports de RDV clients, le Mémoire et les rapports quotidiens.
- src/ : Contient le code du projet.
- Tests/ : Contient les scripts de test.

## Dépendances & Licence :

- [Apache License Version 2.0](https://github.com/Sixelas/PFE/blob/main/LICENSE.md)
- Projet basé sur Aries Hyperledger : [dépot original](https://github.com/hyperledger/aries)
- Dans src/Mobile-Agent nous avons repris et modifié le code du projet
[Aries Mobile Agent React Native](https://github.com/hyperledger/aries-mobile-agent-react-native)
- Dans src/Cloud-Agent nous avons repris et modifié le code du projet [Hyperledger Aries Cloud Agent - Python](https://github.com/hyperledger/aries-cloudagent-python)