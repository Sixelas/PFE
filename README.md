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
 
