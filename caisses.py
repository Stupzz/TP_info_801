import time
from time import sleep

from threading import Thread
from patron import Patron
from message import Message
from random import randint
import json
from termcolor import cprint


class Caisse(Patron):

    def __init__(self, context):
        super(Caisse, self).__init__('Caisse', context)
        self.codes = []

    def run(self):
        while self.attente_msg():
            pass

    def attente_msg(self):
        msg = self.child.recv()
        cprint(f"Message recu dans Caisse: {msg}", 'blue')

        if msg.type == Message.GET_CODE:
            """
            Demande un code à la caisse pour un quantite voulu. 
            Si le client n'a pas de code, lui en envoie un correspondant à la quantite voulu.
            On demande ensuite à la pompe d'ajouter la quantite voulu pour le code donner.
            """
            contenu = json.loads(msg.contenu)
            code = msg.client.code
            if code == None:
                code = self.genere_code()
                self.codes.append(code)
                contenu_json = {"code": code}
                msg_send = Message(Message.GET_CODE_CAISSE, json.dumps(contenu_json), None)
                self.envoie_message("Clients", msg_send)

            contenu_json = {"code": code, "typeCarburant": msg.client.carburant, "quantite": contenu["quantite"]}
            msg_send = Message(Message.GET_CODE, json.dumps(contenu_json), None)
            self.envoie_message("Pompes", msg_send)

        elif msg.type == Message.STOP:
            return False

        return True

    def genere_code(self):
        code = randint(0, 9999)
        while code in self.codes:
            code = randint(0, 9999)
        return code


class Carburant:
    def __init__(self, name, prix_par_litre):
        self.name = name
        self.prix_par_litre = prix_par_litre

    def __str__(self):
        return f"Carburant: {self.name}: {self.prix_par_litre}€/L"

    def __repr__(self):
        return f"Carburant: {self.name}: {self.prix_par_litre}€/L"

    def __eq__(self, other):
        return other.name == self.name
