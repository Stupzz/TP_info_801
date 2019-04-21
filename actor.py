import json
from time import sleep
from patron import Patron
from message import Message
from client import Client
import threading


class Actor(Patron):
    def __init__(self, context):
        super(Actor, self).__init__('Actor', context)
        self.clients = []
        self.client_selectionne = None

    def run(self):
        while self.command():
            sleep(0.2)

    def get_msg(self):
        while self.attente_msg():
            pass

    def command(self):
        print("Commands: ajoutClient, selectionClient, ajouteCarburantCode, sertClient, stop?")
        command = input()

        if command == 'ajoutClient':
            client = Client.creer_client(self)
            msg_send = Message(Message.CREER_CLIENT, None, client)
            self.envoie_message("Clients", msg_send)

        elif command == 'ajoutRapide':
            client = Client("Mathieu")
            client.carburant = "diesel"
            client.capacite_reservoir = 45
            msg_send = Message(Message.CREER_CLIENT, None, client)
            self.envoie_message("Clients", msg_send)

        elif command == 'selectionClient':
            msg_send = Message(Message.PRINT_CLIENT, None, None)
            self.envoie_message("Clients", msg_send)
            sleep(0.2)
            choix = input("Veuillez selectionner un client (index)")
            msg_send = Message(Message.SELECT_CLIENT, choix, None)
            self.envoie_message("Clients", msg_send)


        elif command == 'ajouteCarburantCode':
            quantite = int(input("Quelle quantite de carburant souhaitez vous?"))
            while quantite < 0:
                print("Veuillez selectionner une quantite superieur à 0")
                quantite = int(input("Quelle quantite de carburant souhaitez vous?"))

            contenu_json = {"quantite" : quantite}
            self.envoie_message('Clients', Message(Message.GET_CODE, json.dumps(contenu_json), None))

        elif command == 'sertClient':
            msg_send = Message(Message.SERT_CLIENT, 0, None)
            self.envoie_message("Clients", msg_send)
            sleep(0.2)

        elif command == 'stop':

            # self.envoie_message('Operateur', message)
            # message = Message(Message.STOP, None, None)
            # self.envoie_message('Plateforme', message)
            # self.envoie_message('Transit', message)
            return False

        return True

if __name__ == "__main__":
    actor = Actor()
    t = threading.Thread(target=actor.run())
