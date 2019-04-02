from time import sleep
from patron import Patron
from message import Message


# class Actor(Patron):
#     def __init__(self, context):
#         super(Actor, self).__init__('Actor', context)
#         self.clients = []
#
#     def run(self):
#         while self.command():
#             sleep(0.2)
#
#     def command(self):
#         print("Commands: ajoutClient, retrait, ajout_multiple, clear_gare, print_gare, stop?")
#         command = input()
#
#         if command == 'ajoutClient':
#             objs_parts.append(Plateforme(context, input('Combien de train souhaitez vous dans votre gare?')))
#
#         elif command == 'ajout':
#
#         elif command == 'stop':
#             message = Message(Message.STOP, None, None)
#             self.envoie_message('Operateur', message)
#             self.envoie_message('Plateforme', message)
#             self.envoie_message('Transit', message)
#             return False
#
#         return True

class Client():
    def __init__(self, nom, capacite_reservoir, quantite_reservoir):
        """
        creer un client, avec un code null
        :param nom: Nom du client
        :param capacite_reservoir: la capacité de carburant max du véhicule
        :param quantite_reservoir: la quantite de carburant déjà présente dans le véhicule
        """
        self.nom = nom
        self.capacite_reservoir = capacite_reservoir
        self.quantite_reservoir = quantite_reservoir
        self.code = None


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
            print(f'Vous venez de remplir votre reservoir avec {quantite} litre de carburant. Il vous reste encore {capacite_possible_restante}')
            return 0


