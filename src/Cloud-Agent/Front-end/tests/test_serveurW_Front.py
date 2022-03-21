import pytest
from tkinter import *
import sys
sys.path.append("..")


from serveurW import serveurW_Front
from serveurW.serveurW_Front import App

app = App(Tk())

def test_adresses():
    myAddressIp = "192.168.1.100"
    assert serveurW_Front.genesisIP != myAddressIp
    assert serveurW_Front.genesisIP != 'localhost'
    assert serveurW_Front.genesisIP == '192.168.1.15'

def test_loadFile():
    falsePrivateKey = "E9bRjFUnh0be0bdBd9JcFrIdgjC7SoMLD6slVahxn0="
    falsePublicKey = "PJlMSMWMRgz2AZRHEJGQwiUczZ365dzOn5gM8n+ujz0"

    privateKey = serveurW_Front.loadFile("../serveurW/privatekey")
    publicKey = serveurW_Front.loadFile("../serveurW/publickey")
    assert falsePrivateKey != privateKey
    assert falsePublicKey != publicKey
    assert publicKey != privateKey
    falsePublicKey = publicKey + "blabla"
    assert publicKey != falsePublicKey
    assert "Erreur lors de la génération des clés" == serveurW_Front.loadFile("publiqueKeyy")

### Teste du bouton "Générer clés WireGuard"
def test_GButton_1_command():
    global app
    app.GButton_1_command()

    assert app.GLineEdit_1.get() != ""
    assert app.GLineEdit_1.get() == serveurW_Front.loadFile("publickey")
    assert len(serveurW_Front.loadFile("publickey")) == len(app.GLineEdit_1.get())
    assert serveurW_Front.loadFile("publickey")[17] in app.GLineEdit_1.get()