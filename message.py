class Message:
    #pour la caisse
    GET_CODE = "get code" #Pour client également

    #Pour pompe
    ADD_CARBURANT = "add carburant"


    #Pour caisse
    AFFICHE_POMPE = "affiche pompe"
    SELECT_POMPE = "select pompe"
    ENTREE_TRAIN = "entree train"

    #Pour le transit
    START_TRANSIT = "start transit"
    FIN_TRANSIT = "fin de transit"


    STOP = "stop"

    def __init__(self, type, contenue, client=None):
        self.type = type
        self.contenue = contenue
        self.client = client

    def __str__(self):
        return "Message: " + str(self.type) + ". Contient: " + str(self.contenue) + ". Avec le client: " + self.client + "."

