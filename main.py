
from actor import Actor
from caisses import Caisse
from pompe import Pompes
from client import Clients

if __name__ == '__main__':
    context = dict()

    caisse = Caisse(context)
    actor = Actor(context)
    clients = Clients(context)
    pompes = Pompes(context, input('Combien de pompes souhaitez vous?'))

    parts = []
    parts.append(caisse)
    parts.append(pompes)
    parts.append(clients)

    for p in parts:
        p.launch()

    actor.run()

    for p in parts:
        p.join()
