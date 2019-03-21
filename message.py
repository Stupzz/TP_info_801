class Message:
    #pour la gare
    SORT_TRAIN = "sort train"
    SORTI_TRAIN = "sorti train"
    DEMANDE_ENTREE = "demande entree"
    PRINT_TRAINS = "print trains"
    VIDE_GARE = "vide gare"

    #Pour l'operateur
    DEMANDE_SORTI = "demande sorti"
    REPONSE_ENTREE = "reponse entree"
    ENTREE_TRAIN = "entree train"

    #Pour le transit
    START_TRANSIT = "start transit"
    FIN_TRANSIT = "fin de transit"


    STOP = "stop"

    def __init__(self, type, train, accept):
        self.type = type
        self.train = train
        self.accept = accept

    def __str__(self):
        return "Message: " + str(self.type) + ". Contient le train: " + str(self.train) + ". La réponse est: " + str(self.accept) + "."

