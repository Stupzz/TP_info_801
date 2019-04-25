import json
import time
from time import sleep

from threading import Thread
from patron import Patron
from message import Message
from termcolor import cprint


SECONDE_ATTENTE_PAR_LITRE = 0.1

class Pompes(Patron):

    def __init__(self, context, nombrePompe):
        super(Pompes, self).__init__('Pompes', context)
        self.pompes = []
        self.codes_essence = dict()
        self.codes_diesel = dict()
        for i in range(int(nombrePompe)):
            id = i + 1
            carburant = "diesel" if i % 2 == 0 else "essence"
            code = self.codes_diesel if i % 2 == 0 else self.codes_essence
            pompe = Pompe(id, carburant, code)
            self.pompes.append(pompe)

    def run(self):
        while self.attente_msg():
            pass

    def attente_msg(self):
        msg = self.child.recv()
        cprint(f"Message reçu dans Pompes : {msg}", 'blue')
        if msg.type == Message.GET_CODE:
            dict = json.loads(msg.contenu)
            if dict["typeCarburant"] == "diesel":
                codes = self.codes_diesel
            else:
                codes = self.codes_essence

            totalEssence = codes.get(dict["code"], 0) + dict["quantite"]
            codes[dict["code"]] = totalEssence

        elif msg.type == Message.PRINT_POMPE_CARBURANT_DISPONNIBLE:
            dict = json.loads(msg.contenu)
            carburant = dict["typeCarburant"]
            pompes_disponnible = self.pompe_disponnible_carburant(carburant)
            print("Voici les pompes disponnible pour votre type de carburant:")
            for pompe in pompes_disponnible:
                print(pompe)

        elif msg.type == Message.SERT_CLIENT:
            dict = json.loads(msg.contenu)
            quantite = dict["quantite"]
            id_pompe = dict["pompe"] - 1
            client = msg.client
            if client.capacite_reservoir == client.quantite_reservoir:
                print("Le client a déjà le plein.")
                return True
            if id_pompe >= 0 and id_pompe < len(self.pompes):

                if self.pompes[id_pompe].disponible:
                    if self.client_deja_sur_pompe(client):
                        cprint("ERREUR, Le client n'est pas disponnible, veuillez attendre qu'il ai fini de faire son plein", 'red')
                        return True
                    if quantite > 0:
                        if client.carburant == self.pompes[id_pompe].type_carburant:
                            quantite_verse = min(client.max_quantite_possible(), self.pompes[id_pompe].codes[client.code], quantite)  # ici le min permet d'obtenir la quantité à ajouter dans le véhicule
                            self.envoie_message('Clients', Message(Message.REMPLI_CLIENT, json.dumps({"quantite" : quantite_verse}), None))
                            t = Thread(target=self.pompes[id_pompe].sert_client, args=(client, quantite_verse,))
                            t.start()
                        else:
                            cprint("Erreur, la pompe choisi ne delivre pas le bon carburant pour votre véhicule", 'red')
                else:
                    cprint("Erreur, pompe non disponnible", 'red')

            else:
                cprint("Erreur, veuillez saisir un id valide", 'red')

        elif msg.type == Message.STOP:
            return False

        return True

    def pompe_disponnible_carburant(self, typeCarburant):
        pompes_disponnible = []
        for pompe in self.pompes:
            if pompe.type_carburant == typeCarburant and pompe.disponible:
                pompes_disponnible.append(pompe)
        pompes_disponnible.sort(key=lambda p: p.id)  # on trie pour un affiche par id croissant
        return pompes_disponnible

    def client_deja_sur_pompe(self, client):
        for pompe in self.pompes:
            if pompe.client is not None:
                if pompe.client == client:
                    return True
        return False

class Pompe:
    def __init__(self, id, type_essence, codes):
        self.id = id
        self.type_carburant = type_essence
        self.disponible = True
        self.codes = codes
        self.client = None

    def sert_client(self, client, quantite):
        self.client = client
        self.disponible = False
        self.codes[client.code] -= quantite

        print(f"Le client {client.nom} et la pompe {self.id} ne sont plus disponnible. Remplissage en cours...")

        time.sleep(SECONDE_ATTENTE_PAR_LITRE * quantite)

        print(f"Le client {client.nom} et la pompe {self.id} sont de nouveau disponnible. Fin du remplissage")
        print(f"Le client à versé {quantite} dans son véhicule. Il reste donc sur le code {client.code}: {self.codes[client.code]}litre de {client.carburant} disponnible ")

        cprint("Commands: ajoutClient, selectionClient, printClient, caisse, sertClient, stop?", "green")

        self.client = None
        self.disponible = True

    def __str__(self):
        return f"{self.id} - Pompe "




