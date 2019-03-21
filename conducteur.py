import time
from time import sleep

from threading import Thread
from patron import Patron
from message import Message


class Conducteurs(Patron):

    def __init__(self, context):
        super(Conducteurs, self).__init__('Conducteurs', context)
        self.conducteurs = []
        self.conducteur_courant = None


    def run(self):
        while self.attente_msg():
            pass

    def attente_msg(self):
        msg = self.child.recv()
        print(msg)
        if msg.type == Message.NEW_CONDUCTEUR:
            while True:
                print("Quel nom pour votre conducteur?")
                name = input()
                conducteur_tmp = Conducteur(name, 0)

                if conducteur_tmp not in self.conducteurs:
                    print("Quel est la capacité de réservoir de son véhicule?")
                    capacite_reservoir = input()

                    conducteur_tmp.capacite_reservoir = capacite_reservoir
                    self.conducteurs += [conducteur_tmp]
                    print('Le conducteur à bien était créé')
                    break
                else:
                    print('Ce conducteur existe déjà')

        elif msg.type == Message.CHOIX_CONDUCTEUR:
            print('Veillez choisir votre conducteur:')
            for i in range(0, len(self.conducteurs)):
                print(str(i + 1) + "- " + self.conducteurs[i])

            print("Choisissez votre conducteur?")
            while True:
                indice_conducteur = int(input())
                indice_conducteur -= 1
                if not (indice_conducteur < 0 or indice_conducteur > len(self.conducteurs) - 1):
                    self.conducteur_courant = self.conducteurs[indice_conducteur]
                    break
                else:
                    print('Veuillez choisir un conducteur valide')

        elif msg.type == Message.CHOIX_CAISSE:
            self.envoie_message('Caisse', Message(Message.AFFICHE_POMPE, ""))
            time.sleep(0.2)
            self.envoie_message('Caisse', Message(Message.SELECT_POMPE, '{"id": ' + input('Choissisez votre caisse') + '}'))

        elif msg.type == Message.REPONSE_CAISSE:




            self.trains_en_entree.append(msg.train)
            if not self.en_transit:
                if len(self.trains_en_entree) == 1:
                    self.envoie_message('Plateforme', Message(Message.DEMANDE_ENTREE, self.trains_en_entree[0], None))
                else:
                    print(str(msg.train) + " a était ajouter à la file d'attente")

        elif msg.type == Message.FIN_TRANSIT:
            self.en_transit = False
            if len(self.trains_en_entree) > 0:
                self.envoie_message('Plateforme', Message(Message.DEMANDE_ENTREE, self.trains_en_entree[0], None))
            elif len(self.trains_en_sortie) > 0:
                self.sort_train()
            else:
                self.affiche_commande()


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

    def creer_conducteur(self):
        while True:
            print("Quel nom pour votre conducteur?")
            name = input()
            conducteur_tmp = Conducteur(name, 0)

            if conducteur_tmp not in self.conducteurs:
                print("Quel est la capacité de réservoir de son véhicule?")
                capacite_reservoir = input()

                conducteur_tmp.capacite_reservoir = capacite_reservoir
                self.conducteurs += [conducteur_tmp]
                print('Le conducteur à bien était créé')
                break
            else:
                print('Ce conducteur existe déjà')

class Conducteur:
    def __init__(self, name, capacite_reservoir):
        self.name = name
        self.code = None
        self.reservoir = 0
        self.capacite_reservoir = capacite_reservoir

    def __str__(self):
        return f"Conducteur de nom: {self.name}, possèdant le code: {code} et pour un réservoir rempli de: {self.reservoir}/{self.capacite_reservoir}"

    def __repr__(self):
        return f"Conducteur de nom: {self.name}, possèdant le code: {code} et pour un réservoir rempli de: {self.reservoir}/{self.capacite_reservoir}"

    def __eq__(self, other):
        return other.name == self.name


