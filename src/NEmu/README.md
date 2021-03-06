# Liste des fichiers .py de ce dossier :

- config_Interfaces.py : Ce script permet de configurer les interfaces des Vms si le service dnsmask/dhcp du VRouter est désactivé.
- creator.py : Ce script permet de créer une image de debian réutilisable ensuite comme base pour les scripts des réseaux virtuels de notre choix.
- install.txt : Ce fichier liste l'ensemble des dépendances nécessaires à installer sur l'image debian11.img de base du réseau virtuel.
- network.py : Ce script correspond à notre réseau virtuel final.

# Tuto installation NEmu au Cremi 

1. Installation de NEmu :
```
cd /espace/ 
mkdir NEmu 
cd NEmu/ 
git clone https://gitlab.com/v-a/nemu.git nemu.d 
cd nemu.d/ 
./init.sh
```
2. On ajoute nemu au path :
```
nano ∼/.bashrc
export NEMUROOT=/espace/NEmu/nemu.d
alias nemu="$NEMUROOT/nemu.py"
source ∼/.bashrc
```

3. On ajoute le script network.py dans /espace/NEmu/ :
```
cp network.py /espace/NEmu/
```

4. On modifie le "workspace" ligne 5 par celui de sa session.

5. On lance le script : 
```
nemu -f network.py -i
```

6. Pour enregister avant de quitter (dans le script par défaut tout se supprime automatiquement quand on éteint les VMs) :
```
StopNemu() 
SaveNemu("/tmp/NetworkPFE.tgz")  #Ce truc prend du temps 
DelNemu() 
exit()
```

7. On peut relancer comme ça (plus besoin du script initial, on recharge à partir de l'archive) :
```
nemu 
RestoreNemu("/tmp/NetworkPFE.tgz", workspace="/tmp") 
StartNemu()
```

8. Attention à bien supprimer l'archive NetworkPFE.tgz d'avant si on veut refaire un SaveNemu() par dessus la même ! (Ou alors la retirer de l'endroit ou on met la nouvelle de même nom, parce que l'écrasement de l'archive antérieure a bug de mon côté).

## Optionnel si on a pas de VRouter :

9. Pour configurer le réseau local 10.0.0.0/24 de l'interface eth1 sur l'Android :
```
pkg install tsu 
nano /etc/init.sh
```

- Juste avant le return 0 en bas mettre : 
```
ifconfig eth1 10.0.0.2 netmask 255.255.255.0 
#route add default gw 10.0.0.254 dev eth1 #pas besoin de ça 
route add -net 10.0.0.0 netmask 255.255.255.0 gw 10.0.0.2
```

- Il faut ensuite reboot la VM Android.

- On a maintenant wlan0 (wifi, relié à internet), et eth1 relié au réseau local. \
Par contre impossible de ping 10.0.0.1 depuis android quand la wifi est activée, la règle de routage mise semble pas être prise en compte et tout sort sur wlan0. Il faut désactiver la wifi pour que le réseau local 10.0.0.0/24 fonctionne sur Android. (On peut switch comme ça entre les 2 réseaux en activant/désactivant le wifi). \
Depuis Debian 10.0.0.1 on peut pourtant ping et obtenir une réponse de Android 10.0.0.2 quand la wifi est activée sur android (pas compris pk ça marche pour les echo request mais pas les echo send dans ce cas). 

10. Pour configurer l'interface de ServerB (Serveur Debian de BlockChain relié au réseau du projet 2) :
```
nano /etc/network/interfaces
```
Puis modifier l'@ip à 10.0.0.1 en 10.0.0.3\
Ensuite faire :
```
service networking restart
```
 
# Contenu des images Android et Debian11 :

## Sur les VMs Debian11 serveurB et serveurW est installé :
- Les deux dépôts git aries-cloudagent-python et PFE (celui-ci).
- Docker et les autres dépendances nécessaires pour lancer le Cloud-Agent.
- Wireshark pour de l'analyse réseau.
- WireGuard.
- Toutes les autres dépendances nécessaires aux démos de nos Cloud Agents qui se trouvent [ici](https://github.com/Sixelas/PFE/tree/main/src/Cloud-Agent)

## Sur la VM Android clientW est installé :
- WireGuard
- Termux