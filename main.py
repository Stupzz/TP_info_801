
from actor import Actor

if __name__ == '__main__':
    context = dict()

    parts = [Operateur, Transit]
    objs_parts = []
    actor = Actor(context)

    for p in parts:
        objs_parts += [p(context)]

    objs_parts.append(Plateforme(context, input('Combien de train souhaitez vous dans votre gare?')))

    for p in objs_parts:
        p.launch()

    actor.run()

    for p in objs_parts:
        p.join()
