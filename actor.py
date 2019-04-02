import json
from time import sleep
from patron import Patron
from message import Message
import threading


class Actor(Patron):
    def __init__(self, context):
        super(Actor, self).__init__('Actor', context)
        self.clients = []
        self.client_selectionne = None

    def run(self):
        threading.Thread(target=self.get_msg())
        while self.command():
            sleep(0.2)

    def get_msg(self):
        while self.attente_msg():
            pass

    def command(self):
        print("Commands: ajoutClient, selectionClient, ajouteCarburant, stop?")
        command = input()
        if command == 'ajoutClient':
            client = self.creer_client()
            self.clients.append(client)
            print(f"Le client suivant vient d'être ajouté: {client}")

        elif command == 'selectionClient':
            for i in range(len(self.clients)):
                print(f"{i + 1} - {self.clients[i].nom}")

            choix = int(input("Quel client souhaitez vous selectionner? (index)")) - 1
            while (choix < 0 and choix >= len(self.clients)):
                print("Veuillez selectionner un index correct")
                choix = int(input("Quel client souhaitez vous selectionner? (index)")) - 1

            self.client_selectionne = self.clients[choix]
            print(f"Vous venez de selectionner {self.client_selectionne.nom}")

        elif command == 'ajouteCarburant':
            quantite = int(input("Quelle quantite de carburant souhaitez vous?"))
            while quantite < 0:
                print("Veuillez selectionner une quantite superieur à 0")
                quantite = int(input("Quelle quantite de carburant souhaitez vous?")) - 1
            contenue_json = {"quantite": quantite}
            self.envoie_message('Caisse', Message(Message.GET_CODE, json.dumps(contenue_json), self.client_selectionne))

        elif command == 'stop':

            # self.envoie_message('Operateur', message)
            # message = Message(Message.STOP, None, None)
            # self.envoie_message('Plateforme', message)
            # self.envoie_message('Transit', message)
            return False


        return True

    def attente_msg(self):
        msg = self.child.recv()
        print(msg)
        if msg.type == Message.GET_CODE:
            dict = json.loads(msg.contenu)
            self.client_selectionne.code = dict["code"]
        elif msg.type == Message.STOP:
            return False

        return True

    def deja_client(self, client):
        for c in self.clients:
            if client == c:
                return True
        return False

    def creer_client(self):
        client = Client(input("Quel nom voulez vous pour votre client?"))
        while self.deja_client(client):
            client.nom = input("Nom client déjà utilisé. Quel nom voulez vous pour votre client?")

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

    def __eq__(self, other):
        if not isinstance(other, Client):
            print('Erreur de comparaison, veuillez comparer deux objet de la même class')
            return NotImplemented
        else:
            return self.nom == other.nom

    def __str__(self):
        return f"{self.nom} a un véhicule pouvant contenir {self.capacite_reservoir} litre de {self.carburant}. Son reservoir est déjà rempli avec {self.quantite_reservoir} litre."


if __name__ == "__main__":
    actor = Actor()
    t = threading.Thread(target=actor.run())
