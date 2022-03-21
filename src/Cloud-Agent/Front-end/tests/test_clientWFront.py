import pytest
#import tkinter as tk
from tkinter import *
import sys
sys.path.append("..")


from clientW import clientW_Front
from clientW.clientW_Front import App

app = App(Tk())

def test_adresses():
    myAddressIp = "192.168.1.107"
    assert clientW_Front.genesisIP != myAddressIp
    assert clientW_Front.genesisIP != 'localhost'

def test_loadFile():
    falsePrivateKey = "E9bRjFUnh0be0bdBd9JcFrIdgjC7SoMLD6slVahxn0="
    falsePublicKey = "PJlMSMWMRgz2AZRHEJGQwiUczZ365dzOn5gM8n+ujz0"
    privateKey = clientW_Front.loadFile("../clientW/privatekey")
    publicKey = clientW_Front.loadFile("../clientW/publickey")

    assert falsePrivateKey != privateKey
    assert falsePublicKey != publicKey
    # assert publicKey == privateKey
    assert publicKey != privateKey
    falsePublicKey = publicKey + "\n"
    assert publicKey != falsePublicKey
    assert "Erreur lors de la génération des clés" == clientW_Front.loadFile("blabla")



### Teste du bouton "Générer clés WireGuard"
def test_GButton_1_command():
    global app
    app.GButton_1_command()

    assert app.GLineEdit_1.get() != " "
    assert app.GLineEdit_1.get() == clientW_Front.loadFile("publickey")
    assert len(clientW_Front.loadFile("publickey")) == len(app.GLineEdit_1.get())
    assert clientW_Front.loadFile("publickey")[7] in app.GLineEdit_1.get()

### Teste de l'invitation du ServeurB
def test_GButton_2_command():
    global app
    # app.GButton_2_command()
    ...

def test_GButton_3_command():
    ...

def test_GButton_4_command():
    ...

def test_GButton_6_command():
    ...

