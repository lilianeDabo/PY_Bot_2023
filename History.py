# Gestion de l'historique

class node: # structure du node
    def __init__(self, data): # initialisation
        self.Data = data
        self.next_node = None

class chained_history_list: # structure de la liste enchainé
    def __init__(self): # initialisation
        self.first_node = None
        self.size = 0
    
    def add_new_command(self, new_command):
        # cas du tout premier node
        if self.first_node == None:
            self.first_node = node(new_command)
            return
    
        self.size += 1

    # on se place donc sur le premier pour parcourir l'historique
    # et définir l'emplacement vide suivant
        current_node = self.first_node
        while current_node.next_node != None:
            current_node = current_node.next_node
        
        new_node = node(new_command)
        current_node.next_node = new_node
        

    def get_last_command(self): # cherche la derniére commande de l'historique
        if self.first_node != None:
            current_node = self.first_node
            while current_node.next_node != None:
                current_node = current_node.next_node
            
            return print("The last command entered was : " + current_node.Data)
        else:
            return print("The last command entered was : None")
 
