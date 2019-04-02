import time
from time import sleep

from threading import Thread
from patron import Patron
from message import Message
from random import randint
import json


class Caisse(Patron):

    def __init__(self, context):
        super(Caisse, self).__init__('Caisse', context)
        self.codes = []

    def run(self):
        while self.attente_msg():
            pass

    def attente_msg(self):
        msg = self.child.recv()
        print(msg)
        if msg.type == Message.GET_CODE:
            """
            Demande un code à la caisse pour un quantite voulu. 
            Si le client n'a pas de code, lui en envoie un correspondant à la quantite voulu.
            On demande ensuite à la pompe d'ajouter la quantite voulu pour le code donner.
            """
            contenue = json.loads(msg.contenue)
            code = msg.client.code
            if code == None:
                code = self.genere_code()
                self.codes.append(code)
                contenue_json = { "code" : code}
                msg_send = Message(Message.GET_CODE, json.dumps(contenue_json), None)
                self.envoie_message("Actor", msg_send)
                print(f"Message envoyer vers client depuis la caisse: {msg_send}")

            contenue_json = {"code": code, "typeCarburant": msg.client.carburant, "quantite" : contenue["quantite"]}
            msg_send = Message(Message.GET_CODE, json.dumps(contenue_json), None)
            self.envoie_message("Pompe", msg_send)
            print(f"Message envoyer vers pompe depuis la caisse: {msg_send}")

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
