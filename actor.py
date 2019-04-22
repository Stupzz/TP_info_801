import json
from time import sleep
from patron import Patron
from message import Message
from client import Client
import threading
import sys
from termcolor import cprint


class Actor(Patron):
    def __init__(self, context):
        super(Actor, self).__init__('Actor', context)
        self.client_selectionne = False

    def run(self):
        while self.command():
            sleep(0.2)

    def get_msg(self):
        while self.attente_msg():
            pass

    def command(self):
        cprint("Commands: ajoutClient, selectionClient, printClient, caisse, sertClient, stop?", "green")
        command = input()

        if command == 'ajoutClient':
            client = Client.creer_client(self)
            msg_send = Message(Message.CREER_CLIENT, None, client)
            self.envoie_message("Clients", msg_send)
            self.client_selectionne = True

        elif command == 'ajoutRapide':
            client = Client("Mathieu")
            client.carburant = "diesel"
            client.capacite_reservoir = 45
            msg_send = Message(Message.CREER_CLIENT, None, client)
            self.envoie_message("Clients", msg_send)
            self.client_selectionne = True


        elif command == 'selectionClient':
            msg_send = Message(Message.PRINT_CLIENT, None, None)
            self.envoie_message("Clients", msg_send)
            sleep(0.2)
            choix = input("Veuillez selectionner un client (index): ")
            msg_send = Message(Message.SELECT_CLIENT, choix, None)
            self.envoie_message("Clients", msg_send)


        elif command == 'caisse':
            if self.client_selectionne:
                quantite = int(input("Quelle quantite de carburant souhaitez vous? "))
                while quantite < 0:
                    print("Veuillez selectionner une quantite superieur à 0")
                    quantite = int(input("Quelle quantite de carburant souhaitez vous? "))

                contenu_json = {"quantite": quantite}
                self.envoie_message('Clients', Message(Message.GET_CODE, json.dumps(contenu_json), None))
            else:
                cprint("ERREUR, veuillez selectionnez un client", 'red')


        elif command == 'sertClient':
            if self.client_selectionne:
                msg_send = Message(Message.SERT_CLIENT, 0, None)
                self.envoie_message("Clients", msg_send)
                sleep(0.2)
                choix_pompe = int(input("Veuillez choisir une pompe: "))
                choix_quantite = int(input("Veuillez choisir une quantité (<= 0 pour annuler): "))
                contenu_json = {"pompe": choix_pompe, "quantite": choix_quantite}
                msg_send = Message(Message.ENVOIE_DATA_POMPE, json.dumps(contenu_json), None)
                self.envoie_message("Clients", msg_send)
            else:
                cprint("ERREUR, veuillez selectionnez un client", 'red')

        elif command == 'printClient':
            self.envoie_message('Clients', Message(Message.PRINT_CLIENT_SELECTIONNE, None, None))
        elif command == 'stop':
            message = Message(Message.STOP, None, None)
            self.envoie_message('Clients', message)
            self.envoie_message('Pompes', message)
            self.envoie_message('Caisse', message)
            return False

        return True

if __name__ == "__main__":
    actor = Actor()
    t = threading.Thread(target=actor.run())
