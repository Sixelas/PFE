import pytest
from tkinter import *
import sys
sys.path.append("..")


from clientW import clientW_Front
from clientW.clientW_Front import App

app = App(Tk())

def test_adressesClient():
    myAddressIp = "192.168.1.107"
    assert clientW_Front.genesisIP != myAddressIp
    assert clientW_Front.genesisIP != 'localhost'

def test_loadFileClient():
    falsePrivateKey = "E9bRjFUnh0be0bdBd9JcFrIdgjC7SoMLD6slVahxn0="
    falsePublicKey = "PJlMSMWMRgz2AZRHEJGQwiUczZ365dzOn5gM8n+ujz0"
    privateKey = clientW_Front.loadFile("../clientW/privatekey")
    publicKey = clientW_Front.loadFile("../clientW/publickey")
    assert falsePrivateKey != privateKey
    assert falsePublicKey != publicKey
    assert publicKey != privateKey
    falsePublicKey = publicKey + "\n"
    assert publicKey != falsePublicKey
    assert "Erreur lors de la génération des clés" == clientW_Front.loadFile("blabla")


def test_loadJSONClient():
    data = clientW_Front.loadJSON("../../../final/ressources/WG_VC.json")
    assert len(data) != 0
    assert data['results'][0] != 'result'
    assert data['results'][0]['cred_def_id'] == 'NLv8K46HrFJXRxhLZCYmqr:3:CL:10:default'
    assert data['results'][0]['rev_reg_id'] != 'blabla'


def test_extractPubKeyClient():
    extractKey = clientW_Front.extractPubKey("ServeurW", "../../../final/ressources/ProofRecord.json")
    assert extractKey == 'XomcZlNwEJd4wANISm0YuqLfgcgc3MPDsmwFvobFvjI='
    assert 'Xomc' in extractKey
    assert 'blabla' not in extractKey


def test_extractConnectIDClient():
    connectID = clientW_Front.extractConnectID("ServeurB","../../../final/ressources/Connection_logs.json")
    assert connectID != 'ec16362-acee-4cf7-99dc-cb99d54f204c'
    assert connectID != '0ec16362-acee-4cf70ec16362-acee-4cf7'
    assert '0ec16362-acxxxxee-4cf7' not in connectID
    assert "" == clientW_Front.extractConnectID("Serveur","../../../final/ressources/Connection_logs.json")

def test_deleteConnexionsClient():
    data = clientW_Front.loadJSON("../../../final/ressources/Connection_logs.json")
    assert data['results'][0]['connection_id'] != 'ec16362-acee-4cf7-99dc-cb99d54f204c'
    assert data['results'][0]['their_label'] == 'ServeurB'
    clientW_Front.deleteConnexions("../../../final/ressources/Connection_logs.json")

### Teste du bouton "Générer clés WireGuard"
def test_GButton_1_commandClient():
    global app
    app.GButton_1_command()

    assert app.GLineEdit_1.get() != " "
    assert app.GLineEdit_1.get() == clientW_Front.loadFile("publickey")
    assert len(clientW_Front.loadFile("publickey")) == len(app.GLineEdit_1.get())
    assert clientW_Front.loadFile("publickey")[7] in app.GLineEdit_1.get()


