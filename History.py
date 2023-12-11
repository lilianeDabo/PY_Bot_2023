# Gestion de l'historique

class node: # structure du node
    def _init_(self, data): # initialisation
        self.Data = data
        self.next_node = None

class chained_history_list: # structure de la liste enchainé
    def __init__(self): # initialisation
        self.first_node = None
        self.size = 0
    
    def get_last_command(self): # cherche la derniére commande de l'historique
        return self[self.size]

