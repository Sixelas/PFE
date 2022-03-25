# Tutoriel de la version Finale

## Architecture :

final\
&emsp;&emsp;|_____    ressources&nbsp;&nbsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;-->&emsp;&emsp;Dossier contenant les images nécessaires aux GUI + les fichiers générés par les Agents.\
|&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;|____ Aries.png\
|&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;|____ von-logo.png\
|&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;|____ wg.png\
|\
&emsp;&emsp;|_____ ClientW.py&nbsp;&nbsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;-->&emsp;&emsp;Fichier python contenant l'application ClientW\
&emsp;&emsp;|_____ config.py&nbsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;-->&emsp;&emsp;Fichier python contenant les commandes et configurations des Agents\
&emsp;&emsp;|_____    global_fun.py&nbsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;-->&emsp;&emsp;Fichier python contenant les fonctions globales utiles aux Agents\
&emsp;&emsp;|_____ launcher.py&nbsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;-->&emsp;&emsp;Script qui sert à lancer l'Agent de son choix\
&emsp;&emsp;|_____ QrCode_Generation.py&emsp;&emsp;-->&emsp;&emsp;Fichier python contenant le générateur de QRCode d'invitation\
&emsp;&emsp;|_____ README.md&nbsp;&nbsp;&nbsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;-->&emsp;&emsp;Ce fichier\
&emsp;&emsp;|_____ ServeurB.py&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;-->&emsp;&emsp;Fichier python contenant l'application ServeurB\
&emsp;&emsp;|_____ ServeurW.py&nbsp;&nbsp;&nbsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;-->&emsp;&emsp;Fichier python contenant l'application ServeurW





## Etape 1 : Lancer le réseau virtuel :
Pour lancer le réseau virtuel du projet, suivre les étapes 1 à 5 de  [ce tutoriel](https://github.com/Sixelas/PFE/tree/main/src/NEmu)

## Etape 2 : Lancer les GUI des Agents :
Si le dossier PFE/src/final/ n'existe pas, faire tout d'abord un git pull dans PFE/  (valable seulement pour l'ancienne image debian11.img)\
On peut ensuite si besoin modifier les paramètres de configuration par défaut dans config.py, par exemple si les @ip des machines ne sont pas les mêmes.\
On lance le launcher sur les 3 machines en commençant par ServeurB (attendre que l'Agent ServeurB soit lancé avant de lancer les autres) :
```
cd PFE/src/final/
python3 launcher.py
```

## Etape 3 : Emettre un VC à ServeurW :
1. Sur ServeurB, appuyer sur "Générer Invitation". Une invitation en json s'affiche dans la zone de texte prévue à cet effet.
2. Sur ServeurW, appuyer sur "Générer clés WireGuard". la clé publique s'affiche dans la zone de texte prévue à cet effet.
3. Sur ServeurW, coller l'invitation json générée par ServeurB dans la zone de texte prévue à cet effet puis appuyer sur "OK"
4. Une fois que le bouton "OK" n'est plus grisé, cela veut dire que ServeurW a récupéré son VC, qui est enregistré dans le fichier ressources/WG_VC.json.

## Etape 4 : Emettre un VC à ClientW :
Il suffit de refaire la même chose qu'à l'étape 3 mais cette fois-ci remplacer ServeurW par ClientW.

## Etape 5 : Connecter ServeurW et ClientW :
1. Sur ServeurW appuyer sur "Générer Invitation pour ClientW". Une invitation en json s'affiche dans la zone de texte prévue à cet effet.
2. Sur ClientW, coller cette invitation dans le champ prévu à cet effet puis appuyer sur "OK".

## Etape 6 : Echange de proof et de clés publiques WireGuard entre ServeurW et ClientW :
1. Sur ServeurW cliquer sur "Echange de proof avec ClientW". Une fois l'échange terminé, on récupère la clé publique de ClientW extraite de son Verifiable Presentation.
2. Faire de même côté ClientW.

## Etape 7 : Etablissement du tunnel VPN WireGuard :
1. Sur ServeurW, une fois les clés publiques extraites des échanges de proof entre les deux agents, cliquer sur "Configurer Tunnel VPN WireGuard".
2. Sur ClientW, cliquer sur "Configurer Tunnel VPN WireGuard".
3. Le tunnel VPN entre les deux machines est maintenant établi, on peut tester son efficacité à l'aide de captures wireshark & pings entre machines.