# -*- coding: utf-8 -*-

##### Topologie de ce réseau dans docs/wk_reports/S7/topologieV3.jpg #####

#  Pour sauvegarder la session dans une archive .tgz voir tuto sur le README.md
# Attention Mode suppression Auto de la session activée, voir WaitNemu() et DelNemu()

### Le flag hdcopy permet de forcer la copie des VFs (images disques) dans le workspace
### Ne pas placer le workspace dans son homedir car cela va prendre beaucoup d'espace
InitNemu(session='NetworkPFE', workspace='/tmp/cache-ahenquinet', hdcopy=False)

### VHostConf permet de définir une configuration commune pour les VHosts
### Ce n'est pas une fonction obligatoire, cela permet uniquement de mutualiser les options pour ne pas avoir à les mettre systématiquement dans les VHosts
### Recommandé : option smp=<N> qui permet de donner plusieurs coeurs de CPU à une VM
### Recommandé : option rtc="base=localtime" qui permet de synchroniser l'horloge système des VMs sur celle de la machine physique
VHostConf('common', enable_kvm=None, k='fr', m='2G', smp=2)

## Il vaut mieux mettre le chemin complet vers l'image pour éviter tout souci de path
DEBIAN_PATH="/net/stockage/PFE-VPN-2022/debian11.img";
ANDROID_PATH="/net/stockage/PFE-VPN-2022/android.img";

## Routeur Virtuel qui fait DHCP + NAT MASQUERADING pour les 3 VMs du Réseau. 
VRouter("router", nics=[VNic(), VNic(), VNic(), VNic()],
        services=[Service("ipforward"),
          Service("ifup", '1:192.168.1.1', '2:192.168.2.1', '3:192.168.3.1'),
          Service("gateway", 0),
          Service("masquerade", ipsrc="192.168.0.0/16"),
          Service("dnsmasq", domain="local1", net="192.168.1.0/24", start="192.168.1.10", end="192.168.1.20", ifaces=[1]),
          Service("dnsmasq", domain="local2", net="192.168.2.0/24", start="192.168.2.10", end="192.168.2.20", ifaces=[2]),
          Service("dnsmasq", domain="local3", net="192.168.3.0/24", start="192.168.3.10", end="192.168.3.20", ifaces=[3]),
          Service("password", "root", password="plop"),
          Service("sshd")],
        m=512, enable_kvm=None)

## Le mode cow pour les VFs va dériver l'image disque à partir de l'image de base
VHost("serveurB", conf='common', hds=[VFs(DEBIAN_PATH, "cow", tag='serveurB.img')], nics=[VNic(hw='0a:0a:0a:00:01:01'), VNic(hw='0a:0a:0a:00:01:02'), VNic(hw='0c:0c:0c:00:01:01')])
VHost("serveurW", conf='common', hds=[VFs(DEBIAN_PATH, "cow", tag='serveurW.img')], nics=[VNic(hw='0a:0a:0a:00:02:01'), VNic(hw='0a:0a:0a:00:02:02'), VNic(hw='0c:0c:0c:00:02:01')])
VHost("clientW", conf='common', hds=[VFs(ANDROID_PATH, "cow", tag='clientW.img')], nics=[VNic(model='pcnet', hw='0a:0a:0a:00:03:01')])


## Le lien vers Internet relié au VRouter
VSlirp("slirp", net='192.168.0.0/24')

## L'appel à SetIface n'est nécessaire que dans le cas où on a besoin de construire un réseau avec des VMs externes ou bien sur différentes machines physiques
## les 3 switchs pour faire les liens VRouter--VM 
VSwitch("sw1", niface=2)
VSwitch("sw2", niface=2)
VSwitch("sw3", niface=2)

Link("router:0", "slirp")
Link("router:1", "sw1:0")
Link("router:2", "sw2:0")
Link("router:3", "sw3:0")

Link("serveurB", "sw1:1")
Link("serveurW", "sw2:1")
Link("clientW", "sw3:1")

StartNemu()

# Ces 3 lignes permettent de supprimer automatiquement la session et les images temporaires générées dans /tmp/ une fois qu'on éteint les 3 VMs
# Il faut les commenter si on veut enregistrer sa session avant de quitter
WaitNemu("serveurB", "serveurW", "clientW")
StopNemu()
DelNemu()

