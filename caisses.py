import time
from time import sleep

from threading import Thread
from patron import Patron
from message import Message


class Caisse(Patron):

    def __init__(self, context):
        super(Caisse, self).__init__('Caisse', context)
        self.pompes = []
        self.carburants =

    def run(self):
        while self.attente_msg():
            pass

    def attente_msg(self):
        msg = self.child.recv()
        print(msg)
        if msg.type == Message.AFFICHE_POMPE:


        elif msg.type == Message.STOP:
            return False

        return True

    def make_transit(self, train):
        self.en_transit = True
        self.envoie_message('Transit', Message(Message.START_TRANSIT, train, None))

    def sort_train(self):
        train = self.trains_en_sortie.pop(0)
        print(str(train) + " a était accepté pour sortir de la gare")
        self.envoie_message('Plateforme', Message(Message.SORT_TRAIN, train, None))
        self.make_transit(train)

    def affiche_commande(self):
        print("Commands: ajout, retrait, ajout_multiple, clear_gare, print_gare, stop?")


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
