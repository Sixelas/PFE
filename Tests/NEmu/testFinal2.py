# -*- coding: utf-8 -*-

### Le flag hdcopy permet de forcer la copie des VFs (images disques) dans le workspace
### Je vous déconseille de placer le workspace dans votre homedir car cela va prendre beaucoup d'espace
InitNemu(session='TESTnemuFinal2', workspace='/tmp/cache-ahenquinet', hdcopy=False)

### VHostConf permet de définir une configuration commune pour les VHosts
### Ce n'est pas une fonction obligatoire, cela permet uniquement de mutualiser les options pour ne pas avoir à les mettre systématiquement dans les VHosts
### Je vous recommande également l'option smp=<N> qui permet de donner plusieurs coeurs de CPU à une VM
### Je vous recommande également l'option rtc="base=localtime" qui permet de synchroniser l'horloge système des VMs sur celle de la machine physique
VHostConf('common', enable_kvm=None, k='fr', m='2G', smp=2)

### Il vaut mieux mettre le chemin complet vers l'image pour éviter tout souci de path
### Vous pouvez utiliser des variables car le fichier est considéré comme un code Python
### Je vous recommande d'utiliser une Debian 11 et non une Debian 10, cette dernière étant passée en legacy depuis cet été
DEBIAN_PATH="/net/stockage/PFE-VPN-2022/debian11.img";
ANDROID_PATH="/net/stockage/PFE-VPN-2022/android.img";

### Le mode cow pour les VFs va dériver l'image disque à partir de l'image de base
VHost('serveur', conf='common', hds=[VFs(DEBIAN_PATH, 'cow', tag='serveur.img')], nics=[VNic(hw='0a:0a:0a:00:01:01'), VNic(hw='0a:0a:0a:00:01:02'), VNic(hw='0c:0c:0c:00:01:01')])
VHost('client', conf='common', hds=[VFs(ANDROID_PATH, 'cow', tag='client.img')], nics=[VNic(model='pcnet', hw='0a:0a:0a:00:02:01'), VNic(model='pcnet', hw='0a:0a:0a:00:02:02')])

### L'appel à SetIface n'est nécessaire que dans le cas où vous avez besoin de construire un réseau avec des VMs externes ou bien sur différentes machines physiques
VSwitch('sw1', niface=3)
Link(client='serveur:1', core='sw1:0')
Link(client='client:1', core='sw1:1')

VSlirp('slirp1', net='192.168.1.0/24')
Link(client='serveur', core='slirp1')

VSlirp('slirp2', net='192.168.2.0/24')
Link(client='client:0', core='slirp2')

StartNemu()