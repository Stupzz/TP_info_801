class Message:
    #pour la caisse/le client/les pompes
    GET_CODE = "get code" #Pour client également

    #Pour pompe
    ADD_CARBURANT = "add carburant"

    PRINT_POMPE_CARBURANT_DISPONNIBLE = "print pompe carburant disponnible"
    SERT_CLIENT = "sert client"

    #client
    SELECT_CLIENT = "select_client"
    CREER_CLIENT = "creer_client"
    GET_CODE_CAISSE = "get_code_caisse"
    PRINT_CLIENT = "print_client"



    STOP = "stop"

    def __init__(self, type, contenu, client=None):
        self.type = type
        self.contenu = contenu
        self.client = client

    def __str__(self):
        return "Message: " + str(self.type) + ". Contient: " + str(self.contenu) + ". Avec le client: " + str(self.client) + "."

