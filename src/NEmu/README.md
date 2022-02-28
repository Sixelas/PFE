# Liste des fichiers .py de ce dossier :

- creator.py : Ce script permet de créer une image de debian réutilisable ensuite comme base pour les scripts des réseaux virtuels de notre choix.
- network.py : Ce script correspond à notre réseau virtuel final.


# Tuto installation NEmu au Cremi 

1. Installation de NEmu :
cd /espace/
mkdir NEmu
cd NEmu/
git clone https ://gitlab.com/v-a/nemu.git nemu.d
cd nemu.d/
./init.sh


2. On ajoute le script NetworkPFE.py dans /espace/NEmu/

3. On modifie le "workspace" ligne 5 par celui de sa session.

4. On lance le script avec "nemu -f NetworkPFE.py -i"

5. Pour enregister avant de quitter :
StopNemu()
SaveNemu("/tmp/NetworkPFE.tgz")  #Ce truc prend du temps
DelNemu()
exit()

6. On peut relancer comme ça (plus besoin du script initial, on recharge à partir de l'archive) :
nemu
RestoreNemu("/tmp/NetworkPFE.tgz", workspace="/tmp")
StartNemu()

7. Pour configurer le réseau local 10.0.0.0/24 de l'interface eth1 sur l'Android :

pkg install tsu
nano /etc/init.sh

- Juste avant le return 0 en bas mettre :

ifconfig eth1 10.0.0.2 netmask 255.255.255.0
#route add default gw 10.0.0.254 dev eth1 #pas besoin de ça
route add -net 10.0.0.0 netmask 255.255.255.0 gw 10.0.0.2

- Il faut ensuite reboot la VM Android.

- On a maintenant wlan0 (wifi, relié à internet), et eth1 relié au réseau local. 
Par contre impossible de ping 10.0.0.1 depuis android quand la wifi est activée, la règle de routage mise semble pas être prise en compte et tout sort sur wlan0. Il faut désactiver la wifi pour que le réseau local 10.0.0.0/24 fonctionne sur Android. (On peut switch comme ça entre les 2 réseaux en activant/désactivant le wifi).
Depuis Debian 10.0.0.1 on peut pourtant ping et obtenir une réponse de Android 10.0.0.2 quand la wifi est activée sur android (pas compris pk ça marche pour les echo request mais pas les echo send dans ce cas). 


8. Pour configurer l'interface de ServerB (Serveur Debian de BlockChain relié au réseau du projet 2) :\
nano /etc/network/interfaces\
Puis modifier l'@ip à 10.0.0.1 en 10.0.0.3\
Ensuite faire "service networking restart"
9. Attention à bien supprimer l'archive tgz d'avant si on veut refaire un SaveNemu() par dessus la même ! (Ou alors la retirer de l'endroit ou on met la nouvelle de même nom, parce que l'écrasement de l'archive antérieure a bug de mon côté).
 
