import os
import sys
import subprocess
import signal


confSB = ''' echo "auto ens3\niface ens3 inet static\n	address 192.168.1.15\n	netmask 255.255.255.0\n	gateway 192.168.1.1\n	dns-nameservers 8.8.8.8" >> /etc/network/interfaces '''
confSW = ''' echo "auto ens3\niface ens3 inet static\n	address 192.168.2.13\n	netmask 255.255.255.0\n	gateway 192.168.2.1\n	dns-nameservers 8.8.8.8" >> /etc/network/interfaces '''
confCW = ''' echo "auto ens3\niface ens3 inet static\n	address 192.168.3.20\n	netmask 255.255.255.0\n	gateway 192.168.3.1\n	dns-nameservers 8.8.8.8" >> /etc/network/interfaces '''
commandRestart = ''' /etc/init.d/networking restart '''

def configInt(machine) :
    if(machine == "1") :
        print("Configuration de l'interface ens3 de ServeurB")
        commandProc = subprocess.Popen(confSB, shell=True, preexec_fn=os.setsid)
        commandProc.wait()
        commandProc = subprocess.Popen(commandRestart, shell=True, preexec_fn=os.setsid)
        commandProc.wait()
    elif(machine == "2") :
        print("Configuration de l'interface ens3 de ServeurW")
        commandProc = subprocess.Popen(confSW, shell=True, preexec_fn=os.setsid)
        commandProc.wait()
        commandProc = subprocess.Popen(commandRestart, shell=True, preexec_fn=os.setsid)
        commandProc.wait()
    else :
        print("Configuration de l'interface ens3 de ClientW")
        commandProc = subprocess.Popen(confCW, shell=True, preexec_fn=os.setsid)
        commandProc.wait()
        commandProc = subprocess.Popen(commandRestart, shell=True, preexec_fn=os.setsid)
        commandProc.wait()

machine = input("Entrer :\n1 --> ServeurB,\n2 --> ServeurW,\n3 --> ClientW\n")

if machine in ["1","2","3"] :
    configInt(machine)
else :
    print("mauvaise saisie")