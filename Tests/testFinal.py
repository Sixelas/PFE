# -*- coding: utf-8 -*-

# Réseau Virtuel de Test Final composé d'une VM Debian11 Serveur, et une VM Android Client reliés entre elles par un VSwitch.

# Attention à bien modifier les chemins de fichiers/dossiers correspondants à votre pc !
# Attention à bien se connecter en root (mdp root) sur le Serveur Debian !

# Topologie du réseau :
# 
#   Internet  ------  (ens3:192.168.1.15/24)[SERVEUR](ens4:10.0.0.1/24) ------ [SWITCH] ------ (pcnet:10.0.0.2/24)[CLIENT]
#
# En mode tunnel VPN WireGuard on a comme adresses virtuelles :
#
#   [SERVEUR](wg0:120.0.0.1/32) ------ [SWITCH] ------ (pcnet:120.0.0.2/32)[CLIENT]




# Exécuter le script avec la commande "nemu -f testFinal.py -i"
# La première fois ça va planter à cause des mauvais lien symbolique de l'image debian11.img et android.img, il faut donc les remove puis ajouter les bons lien symbolique :
# (exemple avec debian11.img)   
# Il faut donc aller dans /home/alexis/NEmu/TESTnemuDebian11/fs/ puis faire "rm debian11.img" puis ensuite faire "ln -s /home/alexis/NEmu/debian11.img" (changer les chemins par les votres).

# Ensuite on peut relancer "nemu -f testFinal.py -i"

# CLIENT ANDROID : 
# Normalement tout est déjà installé dessus (un terminal + Wireguard).
# Il faut juste aller dans les options wifi et définir le réseau Wifi connecté sur Adressage Static avec l'@ip 10.0.0.2 (au lieu de DHCP)
# Ensuite ça affiche le lego wifi connecté au réseau avec noté pas d'accès à internet mais c'est normal.
# On peut tester via le terminal de ping 10.0.0.1 (le Serveur), ou même de faire un ssh sur le serveur :
# ssh user@10.0.0.1   (mdp = user), ou id root + mdp root.

# On peut aller ensuite sur WireGuard et activer le tunnel VPN déjà configuré. 


# SERVEUR DEBIAN :
# Possède plusieurs interfaces
#	- ens3 (reliée à internet via le VSlirp, prend une @ip via DHCP en 192.168.1.0/24)
#	- ens4 (reliée au réseau local du Switch, 10.0.0.1/24)
#	- wg0 (interface virtuelle ouverte seulement quand le serveur wireguard est actif) 
#
# Possède Wireshark+tcpdump si besoin de faire des captures pour observer le réseau.
#
# Serveur WireGuard : 
#	1. S'active avec la commande "wg-quick up wg0"  ("wg-quick down wg0" pour stopper).
#	2. Une fois actif, on peut voir la nouvelle interface wg0 120.0.0.1 active et on peut ping le client 120.0.0.2.
#	3. En cas d'erreur les logs sont consultables dans le fichier kernel.log (mélangés aux autres logs de la machine).
#	4. Si jamais on veut faire du NAT/PROXY pour que le Client ait internet, il faut ajouter la commande iptable qui se trouve dans le fichier sur le bureau. (Attention ça plante, grosse latence au bout de 2-3min de proxy).

# Pour quitter on éteint normalement les VMs puis dans le terminal sur lequel NEmu tourne on fait "StopNemu()" puis "exit()".


InitNemu(session='TESTnemuFinal', workspace='/home/alexis/NEmu', hdcopy=False)

VHostConf('debian', enable_kvm=None, k='fr', m='2G')
VHostConf('android', enable_kvm=None, k='fr', m='2G')

VHost('serveur', conf='debian', hds=[VFs('debian11.img', 'cow', tag='serveur.img')], nics=[VNic(hw='0a:0a:0a:00:01:01'),VNic(hw='0a:0a:0a:00:01:02'), VNic(hw='0c:0c:0c:00:01:01')])
VHost('client', conf='android', hds=[VFs('android.img', 'cow', tag='client.img')], nics=[VNic(model='pcnet')])


# C'est le Switch Virtuel qui comporte 3 ports
VSwitch('sw1', niface=3)
SetIface("sw1:0", proto='udp', port=11001, lport=11002)
SetIface("sw1:1", proto='udp', port=11003, lport=11004)
SetIface("sw1:2", proto='udp', port=10002, lport=10003)

# On branche l'interface 1 (ens4) de serveur et la 0 de client sur les ports 0 et 1 du switch  
Link(client='serveur:1', core='sw1:0')
Link(client='client', core='sw1:1')	# !ICI

#On relie le serveur à internet grâce à un lien VSlirp sur son interface 0 (ens3) 
VSlirp('slirp1', net='192.168.1.0/24')
Link(client='serveur', core='slirp1')

#Pour relier le Client à internet ou lieu du réseau local du switch (Attention : si on choisit ce mode, il faut commenter la ligne avec le label !ICI). 
#VSlirp('slirp2', net='192.168.2.0/24')
#Link(client='client', core='slirp2')

StartNemu()
