# -*- coding: utf-8 -*-

#Ce script permet de créer une image de debian réutilisable ensuite comme base pour les scripts des réseaux virtuels de notre choix.
# On suit ce tuto (adapté) : https://gitlab.com/v-a/nemu/-/wikis/tuto/fs/debian 
#Ici j'utilise comme base d'installation l'image de Debian11 "debian-11.2.0-amd64-netinst.iso" mais on peut utiliser la version de son choix sur le même principe.
#iso téléchargeable ici : https://cdimage.debian.org/debian-cd/current/amd64/iso-cd/debian-11.2.0-amd64-netinst.iso

#On peut aussi créer une image Android avec creator.py ! (voir lignes commentés, ATTENTION PAS ENCORE TESTE !!!!)

# Pour exécuter ce script : "nemu --file creator.py"


InitNemu()

#VHost('debian', hds=[EmptyFs('debian11.img', size='20G', type='raw', format='ext3')], nics=[VNic()], cdrom='/home/alexis/iso/debian-11.2.0-amd64-netinst.iso', enable_kvm=None, k='fr', m=2048)
#VHost('android', hds=[EmptyFs('android.img', size='2G')], nics=[VNic()], cdrom='/home/alexis/iso/android.iso', enable_kvm=None, k='fr', m=2048)
VHost('android', hds=[EmptyFs('android.img', size='8G', type='raw', format='ext3')], nics=[VNic(model='pcnet')], cdrom='/home/alexis/iso/android.iso', enable_kvm=None, k='fr', m=2048)


# Le VSlirp permet de relier à internet la machine virtuelle créée. Elle prendra sur son interface 0 une adresse dans 192.168.1.0/24 reliée à internet.
VSlirp('slirp', net='192.168.1.0/24')
#Link('debian', 'slirp')
Link('android', 'slirp')


StartNemu()
#WaitNemu('debian')
WaitNemu('android')

#
# Ici on a la fenêtre graphique de la VM qui se lance, on procède à l'installation (voir tuto installation)
#

StopNemu()
#ExportFs('debian11.img') #Cette étape prend du temps car l'image est lourde (environ 20Gigas)
ExportFs('android.img')

DelNemu()

# On obtiens l'image voulue à la fin (debian11.img ou android.img) dans le même dossier que le script creator.py !
