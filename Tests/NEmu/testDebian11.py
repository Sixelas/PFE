
# Réseau Virtuel de Test composé de deux VMs Debian11 basées sur debian11.img générée par le creator.py

# Attention à bien modifier les chemins de fichiers/dossiers correspondants à votre pc !

# Exécuter le script avec la commande "nemu -f testDebian11.py -i"
# La première fois ça va planter à cause du mauvais lien symbolique de l'image debian11.img, il faut donc le remove puis ajouter le bon lien symbolique vers debian11.img :  
# Il faut donc aller dans /home/alexis/NEmu/TESTnemuDebian11/fs/ puis faire "rm debian11.img" puis ensuite faire "ln -s /home/alexis/NEmu/debian11.img" (changer les chemins par les votres).

# Ensuite on peut relancer "nemu -f testDebian11.py -i"

# Il faut configurer les interfaces des deux VMs reliées au switch (donc ens4) une fois qu'on est connecté sur les machines :

# Sur testeur :
# "nano /etc/network/interfaces"
# auto ens4
# iface ens4 inet static
# 	address 10.0.0.1
# 	netmask 255.255.255.0 
# On save puis ferme nano, puis on fait "/etc/init.d/networking restart"

# Sur testeur2 :
# "nano /etc/network/interfaces"
# auto ens4
# iface ens4 inet static
# 	address 10.0.0.2
# 	netmask 255.255.255.0 
# On save puis ferme nano, puis on fait "/etc/init.d/networking restart"

# Normalement les machines peuvent maintenant se ping entre elles sans problème !

# Pour quitter on éteint normalement les VMs puis dans le terminal sur lequel NEmu tourne on fait "StopNemu()" puis "exit()".


InitNemu(session='TESTnemuDebian11', workspace='/home/alexis/NEmu', hdcopy=False)

VHostConf('debian', enable_kvm=None, k='fr', m='2G')

VHost('testeur', conf='debian', hds=[VFs('debian11.img', 'cow', tag='testeur.img')], nics=[VNic(hw='0a:0a:0a:00:01:01'),VNic(hw='0a:0a:0a:00:01:02'), VNic(hw='0c:0c:0c:00:01:01')])

VHost('testeur2', conf='debian', hds=[VFs('debian11.img', 'cow', tag='testeur2.img')], nics=[VNic(hw='0a:0a:0a:00:01:03'),VNic(hw='0a:0a:0a:00:01:04'), VNic(hw='0c:0c:0c:00:01:02')])

# C'est le Switch Virtuel qui comporte 3 ports
VSwitch('sw1', niface=3)
SetIface("sw1:0", proto='udp', port=11001, lport=11002)
SetIface("sw1:1", proto='udp', port=11003, lport=11004)
SetIface("sw1:2", proto='udp', port=10002, lport=10003)

# On branche les interfaces 1 (ens4) de testeur et testeur2 sur les ports 0 et 1 du switch  
Link(client='testeur:1', core='sw1:0')
Link(client='testeur2:1', core='sw1:1')

#On relie les deux VMs à internet grâce à un lien VSlirp sur leurs interfaces 0 (ens3) 
VSlirp('slirp1', net='192.168.1.0/24')
Link(client='testeur', core='slirp1')

VSlirp('slirp2', net='192.168.2.0/24')
Link(client='testeur2', core='slirp2')

StartNemu()
