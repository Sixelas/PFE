# -*- coding: utf-8 -*-

#  Pour comprendre comment ajouter le VRouter au réseau final et le passer en Version3 !

InitNemu(session='TestVRouter', workspace='/tmp/cache-ahenquinet', hdcopy=False)

VHostConf('common', enable_kvm=None, k='fr', m='2G', smp=2)

### Il vaut mieux mettre le chemin complet vers l'image pour éviter tout souci de path
DEBIAN_PATH="/net/stockage/PFE-VPN-2022/debian11.img";
ANDROID_PATH="/net/stockage/PFE-VPN-2022/android.img";

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

VHost("serveurB", conf='common', hds=[VFs(DEBIAN_PATH, "cow", tag='serveurB.img')], nics=[VNic(hw='0a:0a:0a:00:01:01'), VNic(hw='0a:0a:0a:00:01:02'), VNic(hw='0c:0c:0c:00:01:01')])
VHost("serveurW", conf='common', hds=[VFs(DEBIAN_PATH, "cow", tag='serveurW.img')], nics=[VNic(hw='0a:0a:0a:00:02:01'), VNic(hw='0a:0a:0a:00:02:02'), VNic(hw='0c:0c:0c:00:02:01')])
VHost("clientW", conf='common', hds=[VFs(ANDROID_PATH, "cow", tag='clientW.img')], nics=[VNic(model='pcnet', hw='0a:0a:0a:00:03:01')])

VSlirp("slirp", net='192.168.0.0/24')

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
