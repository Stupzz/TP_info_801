from time import sleep
from patron import Patron
from message import Message


class Actor(Patron):
    def __init__(self, context):
        super(Actor, self).__init__('Actor', context)

    def run(self):
        while self.command():
            sleep(0.2)

    def command(self):
        print("Commands: ajout, retrait, ajout_multiple, clear_gare, print_gare, stop?")
        command = input()

        if command == 'retrait':

        elif command == 'ajout':

        elif command == 'stop':
            message = Message(Message.STOP, None, None)
            self.envoie_message('Operateur', message)
            self.envoie_message('Plateforme', message)
            self.envoie_message('Transit', message)
            return False

        return True
