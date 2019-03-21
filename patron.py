import multiprocessing


class Patron:
    def __init__(self, name, context):
        context[name] = self
        self.name = name
        self.context = context
        self.process = multiprocessing.Process(target=self.run)
        self.parent, self.child = multiprocessing.Pipe()

    def print(self, msg):
        print(self.name + ": " + msg)

    def launch(self):
        self.process.start()

    def join(self):
        self.process.join()

    def run(self):
        raise NotImplementedError

    def envoie_message(self, destinataire, msg):
        self.context[destinataire].parent.send(msg)
