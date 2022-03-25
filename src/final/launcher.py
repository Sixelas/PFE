import os
import subprocess
from config import *


def launcher(machine) :
    if(machine == "1") :
        print("\nMise à jour des fichiers\n")
        commandProc = subprocess.Popen(git, shell=True, preexec_fn=os.setsid)
        commandProc.wait()
        print("\nLancement de l'interface Agent ServeurB\n")
        commandProc = subprocess.Popen(SB, shell=True, preexec_fn=os.setsid)
        commandProc.wait()
    elif(machine == "2") :
        print("\nMise à jour des fichiers\n")
        commandProc = subprocess.Popen(git, shell=True, preexec_fn=os.setsid)
        commandProc.wait()
        print("\nLancement de l'interface Agent ServeurW\n")
        commandProc = subprocess.Popen(SW, shell=True, preexec_fn=os.setsid)
        commandProc.wait()
    else :
        print("\nMise à jour des fichiers\n")
        commandProc = subprocess.Popen(git, shell=True, preexec_fn=os.setsid)
        commandProc.wait()
        print("\nLancement de l'interface Agent ClientW\n")
        commandProc = subprocess.Popen(CW, shell=True, preexec_fn=os.setsid)
        commandProc.wait()

print(LauncherText1)
machine = input(LauncherText2)

if machine in ["1","2","3"] :
    launcher(machine)
else :
    print("mauvaise saisie")