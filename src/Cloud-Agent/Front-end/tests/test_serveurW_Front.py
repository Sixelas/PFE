import pytest
from tkinter import *
import sys
sys.path.append("..")


from serveurW import serveurW_Front
from serveurW.serveurW_Front import App

app = App(Toplevel())

def test_adressesServeur():
    myAddressIp = "192.168.1.100"
    assert serveurW_Front.genesisIP != myAddressIp
    assert serveurW_Front.genesisIP != 'localhost'
    assert serveurW_Front.genesisIP == '192.168.1.15'

def test_loadFileServeur():
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
def test_GButton_1_commandServeur():
    global app
    app.GButton_1_command()

    assert app.GLineEdit_1.get() != ""
    assert app.GLineEdit_1.get() == serveurW_Front.loadFile("publickey")
    assert len(serveurW_Front.loadFile("publickey")) == len(app.GLineEdit_1.get())
    assert serveurW_Front.loadFile("publickey")[10] in app.GLineEdit_1.get()

def test_loadJSONServeur():
    data = serveurW_Front.loadJSON("../../../final/ressources/WG_VC.json")
    assert len(data) != 0
    assert data['results'][0] != 'rev_reg_id'
    assert data['results'][0]['cred_def_id'] != 'NLv8K46HrFJXRxhLZCYmqr'
    assert data['results'][0]['rev_reg_id'] != 'blabla'
    assert data['results'][0]['referent'] != ''


def test_extractPubKeyServeur():
    extractKey = serveurW_Front.extractPubKey("ServeurW", "../../../final/ressources/ProofRecord.json")
    assert extractKey != 'omcZlNwEJd4wANISm0YuqLfgcgc3MPDsmwFvobFvjI='
    assert '111111' not in extractKey
    assert 'blabla' not in extractKey


def test_extractConnectIDServeur():
    connectID = serveurW_Front.extractConnectID("ServeurB","../../../final/ressources/Connection_logs.json")
    assert connectID != 'ec16362-acee-4cf7-99dc-cb99d54f204c'
    assert connectID != '0ec16362-acee-4cfcee-4cf70ec16362-acee-4cf7'
    assert '0ec16AAZ1362' not in connectID
    assert "" == serveurW_Front.extractConnectID("Serveur","../../../final/ressources/Connection_logs.json")

def test_deleteConnexionsServeur():
    data = serveurW_Front.loadJSON("../../../final/ressources/Connection_logs.json")
    assert data['results'][0]['connection_id'] != 'ec16362-acee-4cf7-99dc-cb99d54f204c'
    assert data['results'][0]['their_label'] == 'ServeurB'
    serveurW_Front.deleteConnexions("../../../final/ressources/Connection_logs.json")
