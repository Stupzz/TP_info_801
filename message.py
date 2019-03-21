class Message:
    #pour les conducteurs
    NEW_CONDUCTEUR = "new conducteur"
    CHOIX_CONDUCTEUR = "choix conducteur"
    CHOIX_CAISSE = "choix caisse"
    REPONSE_CAISSE = "reponse caisse"
    PRINT_TRAINS = "print trains"
    VIDE_GARE = "vide gare"

    #Pour caisse
    AFFICHE_POMPE = "affiche pompe"
    SELECT_POMPE = "select pompe"
    ENTREE_TRAIN = "entree train"

    #Pour le transit
    START_TRANSIT = "start transit"
    FIN_TRANSIT = "fin de transit"


    STOP = "stop"

    def __init__(self, type, contenue, accept=None):
        self.type = type
        self.contenue = contenue
        self.accept = accept

    def __str__(self):
        return "Message: " + str(self.type) + ". Contient le train: " + str(self.train) + ". La réponse est: " + str(self.accept) + "."

