from patron import Patron
from message import Message
import json
import time


class Clients(Patron):

    def __init__(self, context):
        super(Clients, self).__init__('Clients', context)
        self.clients = []
        self.client_selectionne = None

    def run(self):
        while self.attente_msg():
            pass

    def attente_msg(self):
        msg = self.child.recv()
        print(f"Message reçu dans Client: {msg}")

        if msg.type == Message.CREER_CLIENT:
            client = msg.client
            if self.deja_client(client):
                print("Le clien existe déjà, veuillez choisir un autre nom")
                return
            self.clients.append(client)
            self.client_selectionne = client
            print(f"Le client suivant vient d'être ajouté: {client} et vien d'être sélectionné")

        elif msg.type == Message.PRINT_CLIENT:
            self.print_client()

        elif msg.type == Message.SELECT_CLIENT:
            choix = int(msg.contenu) - 1
            if choix < 0 and choix >= len(self.clients):
                print("index incorrect")
                return
            self.client_selectionne = self.clients[choix]
            print(f"Vous venez de selectionner {self.client_selectionne.nom}")


        elif msg.type == Message.GET_CODE:
            self.envoie_message('Caisse', Message(Message.GET_CODE, msg.contenu, self.client_selectionne))

        elif msg.type == Message.GET_CODE_CAISSE:
            dict = json.loads(msg.contenu)
            self.client_selectionne.code = dict["code"]

        elif msg.type == Message.PRINT_POMPE_CARBURANT_DISPONNIBLE:
            contenu_json = {"typeCarburant": self.client_selectionne.carburant}
            msg_send = Message(Message.PRINT_POMPE_CARBURANT_DISPONNIBLE, json.dumps(contenu_json), None)
            self.envoie_message("Pompes", msg_send)

        elif msg.type == Message.SERT_CLIENT:
            if self.client_selectionne is None:
                print("Veuillez d'abbord selectionnez un client.")
                return
            contenu_json = {"typeCarburant": self.client_selectionne.carburant}
            msg_send = Message(Message.PRINT_POMPE_CARBURANT_DISPONNIBLE, json.dumps(contenu_json), None)
            self.envoie_message("Pompes", msg_send)
            time.sleep(0.2)
            choix = int(input("Veuillez choisir une pompe"))
            msg_send = Message(Message.SERT_CLIENT, choix, self.client_selectionne)
            self.envoie_message("Pompes", msg_send)

        elif msg.type == Message.STOP:
            return False

        return True

    def deja_client(self, client):
        for c in self.clients:
            if client == c:
                return True
        return False

    def print_client(self):
        for i in range(len(self.clients)):
            print(f"{i + 1} - {self.clients[i].nom}")




class Client():
    def __init__(self, nom):
        """
        creer un client, avec un code null
        :param nom: Nom du client
        :param capacite_reservoir: la capacité de carburant max du véhicule
        :param quantite_reservoir: la quantite de carburant déjà présente dans le véhicule
        """
        self.nom = nom
        self.carburant = None
        self.capacite_reservoir = 0
        self.quantite_reservoir = 0
        self.code = None
        self.attente_pompe = False

    def ajoute_carburant(self, quantite):
        """
        :param quantite: int quantite de carburant a ajouter
        :return: La quantite restante de carburant à ajouter. 0 tout le carburant a été ajouter dans la voiture.
        """
        capacite_possible_restante = self.capacite_reservoir - self.quantite_reservoir
        if capacite_possible_restante < quantite:
            self.quantite_reservoir = self.capacite_reservoir
            carburant_code_restant = quantite - capacite_possible_restante
            print(f'La capacite maximal du véhicule est atteinte, il reste avec votre code: {carburant_code_restant}')
            return carburant_code_restant
        else:
            self.quantite_reservoir += quantite
            capacite_possible_restante = self.capacite_reservoir - self.quantite_reservoir
            print(
                f'Vous venez de remplir votre reservoir avec {quantite} litre de carburant. Il vous reste encore {capacite_possible_restante}')
            return 0


    def creer_client(self):
        client = Client(input("Quel nom voulez vous pour votre client?"))
        carburant = input(f"Quel est le type de carburant qu'utilise le véhicule de {client.nom}? (diesel/essence)")
        while carburant != "diesel" and carburant != "essence":
            carburant = input("Veuillez saisir un carburant valide. (diesel/essence)")
        client.carburant = carburant

        capacite_reservoir = int(input(f"Quel est la capacite de reservoir du véhicule de {client.nom}?"))
        while capacite_reservoir < 0:
            capacite_reservoir = int(input("Veuillez saisir une capacité > 0"))
        client.capacite_reservoir = capacite_reservoir

        choix = input(f"Voulez vous préremplir votre réservoir? (y/n)")
        while choix != "y" and choix != "n":
            print("Veuillez saisir une valeure correcte.")
            choix = input(f"Voulez vous préremplir votre réservoir? (y/n)")
            print(choix)

        if choix == "y":
            quantite_reservoir = int(input(f"Quel quantite de carburant vous voulez ajouter?"))
            while quantite_reservoir < 0:
                quantite_reservoir = int(input("Veuillez saisir une quantite > 0"))
            client.ajoute_carburant(quantite_reservoir)

        return client

    def __eq__(self, other):
        if not isinstance(other, Client):
            print('Erreur de comparaison, veuillez comparer deux objet de la même class')
            return NotImplemented
        else:
            return self.nom == other.nom

    def __str__(self):
        return f"{self.nom} a un véhicule pouvant contenir {self.capacite_reservoir} litre de {self.carburant}. Son reservoir est déjà rempli avec {self.quantite_reservoir} litre. Il a pour code: {self.code}"

if __name__ == "__main__":

    clients = Clients()
    client = clients.creer_client()

