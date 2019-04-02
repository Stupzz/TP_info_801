import json
import time
from time import sleep

from threading import Thread
from patron import Patron
from message import Message


SECONDE_ATTENTE_PAR_LITRE = 3

class Pompes(Patron):

    def __init__(self, context, nombrePompe):
        super(Pompes, self).__init__('Pompes', context)
        self.pompes = []
        self.codes_essence = dict()
        self.codes_diesel = dict()

    def run(self):
        while self.attente_msg():
            pass

    def attente_msg(self):
        msg = self.child.recv()
        print(msg)
        if msg.type == Message.GET_CODE:
            dict = json.loads(msg.contenue)
            codes = None
            if dict["typeCarburant"] == "diesel":
                codes = self.codes_diesel
            else:
                codes = self.codes_essence

            codes[dict["code"]] += dict["quantite"]

        elif msg.type == Message.PRINT_POMPE_CARBURANT_DISPONNIBLE:
            dict = json.loads(msg.contenue)
            carburant = dict["typeCarburant"]
            pompes_disponnible = []
            for pompe in self.pompes:
                if pompe.type_carburant == carburant and pompe.disponible:
                    pompes_disponnible.append(pompe)
            pompes_disponnible.sort(key=lambda p: p.id) #on trie pour un affiche par id croissant
            for pompe in pompes_disponnible:
                print(pompe)
        elif msg.type == Message.STOP:
            return False

        return True


class Pompe:
    def __init__(self, id, type_essence, codes):
        self.id = id
        self.type_carburant = type_essence
        self.disponible = True
        self.codes = codes

    def choix_quantite_client(self, client):
        """
        Dans un premier temps, on gère les erreurs
        Ensuite on demande s'il souhaite utiliser entièrement ou partiellement son code. Il a également le choix de quiter
        :param client: le client à la pompe
        :return: -1 si on annule l'opération, la quantite souhaitez sinon.
        """
        if client.code is None:
            print("Le client doit d'abord passer en caisse afin d'obtenir un code")
            return -1
        if self.type_carburant != client.carburant:
            print(f"Cette pompe {self.id} ne delivre que du {self.type_carburant}")
            return -1
        if self.codes[client.code] is None or self.codes[client.code] == 0:
            print(f"Votre code {self.codes[client.code]} ne correspond pas ou vous n'avez plus de carburant disponnible avec ce code")
            return -1

        print(f"Avec votre code '{client.code}', vous pouvez vous servir {self.codes[client.code]} litre au maximum.")
        choix = input(
            f"Voulez vous l'utilisez entièrement? Vous ne perdrez pas le surplus (y). L'utiliser partiellement (p). Annuler l'operation (n).")
        while choix not in ["y", "n", "p"]:
            print("Erreur d'input")
            print(f"Avec votre code '{client.code}', vous pouvez vous servir {self.codes[client.code]} litre au maximum.")
            choix = input(f"Voulez vous l'utilisez entièrement? Vous ne perdrez pas le surplus (y). L'utiliser partiellement (p). Annuler l'operation (n).")
        if choix == "n":
            return -1
        if choix == "p":
            choix = int(input(
                f"Quelle quantite souhaitez vous? (max: {self.codes[client.code]})"))
            while choix <= 0 or choix > self.codes[client.code]:
                print(f"Erreur d'input, valeur minimal: 1, valeur maximal: {self.codes[client.code]}")
                choix = int(input(
                    f"Quelle quantite souhaitez vous?"))
            return choix
        else:
            return self.codes[client.code]

    def sert_client(self, client, quantite_souhaite):
        client.attente_pompe = True
        self.disponible = False

        quantite_verse = quantite_souhaite - client.ajoute_carburant(quantite_souhaite) #C'est le client qui s'occupe de verse le carburant
        self.codes[client.code] -= quantite_verse
        print(f"Le client {client.name} et la pompe {self.id} ne sont plus disponnible. Remplissage en cours...")
        time.sleep(SECONDE_ATTENTE_PAR_LITRE * quantite_verse)
        print(f"Le client {client.name} et la pompe {self.id} sont de nouveau disponnible. Fin du remplissage")
        print(f"Avec le code {client.code}, il reste {self.codes[client.code]}litre de {client.carburant} disponnible")

        client.attente_pompe = False
        self.disponible = True

    def gestion_client(self, client):
        quantite_souhaite = self.choix_quantite_client(client)
        if quantite_souhaite != -1:
            self.sert_client(client, quantite_souhaite)
            return
        print("Annulation")

    def __str__(self):
        return f"Pompe {self.id}"




