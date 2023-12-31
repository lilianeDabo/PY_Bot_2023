### Gestion de l'historique

class QueueManagingHistory: # definition de la pile
    def __init__(self):
        self.lock = False
    
    def is_locked(self):
        if self.lock == True:
            return "The user's history is currently being modified. Please try again at a later time."
        else:
            return self.lock
    

### Creation de l'historique en soi
class Node: # structure du node
    def __init__(self, data): # initialisation
        self.data = data
        self.next_node = None

class ChainedHistoryList: # structure de la liste enchainé
    def __init__(self): # initialisation
        self.first_node = None
        self.size = 0
    
    def add_new_command(self, new_command, user_name):
        # cas du tout premier node
        if self.first_node == None:
            self.first_node = Node([new_command, user_name])
            self.size += 1
            return
        
        current_node = self.first_node
        # on se place donc sur le premier pour parcourir l'historique
        # et définir l'emplacement vide suivant
        while current_node.next_node != None:
            current_node = current_node.next_node
        
        new_node = Node([new_command, user_name])
        current_node.next_node = new_node
        self.size += 1
        

    def get_last_command(self): # cherche et prend la derniére commande de l'historique
        if self.first_node != None:
            current_node = self.first_node
            while current_node.next_node != None:
                current_node = current_node.next_node
            return current_node.data[0]
        else:
            return None
    

    def get_first_command(self): # cherche et prend la premiére commande de l'historique
        if self.first_node != None:
            current_node = self.first_node
            return current_node.data[0]
        else:
            return None
    
    
    # cherche le user en question 
    # et renvoie toutes les commandes entrées depuis sa derniére connexion
    def get_all_commands_of(self, user_name): 
        all_commands = []
        if self.first_node != None:
            if self.first_node.data[1] == user_name:
                all_commands.append(self.first_node.data[0])
            current_node = self.first_node
            while current_node.next_node != None:
                    if current_node.data[1] == user_name:
                        current_node = current_node.next_node
                        all_commands.append(current_node.data[0])
            
            if all_commands == []:
                return None
            else:
                return str(all_commands)
        
    # avance et recule dans l'historique en fonction de l'index_scroll
    def get_scroll(self, current_index_scroll, user_name):
        count = 0
        current_node = self.first_node
        while current_node.next_node != None:
            if count == current_index_scroll and current_node.data[1] == user_name: # cas si l'index n'est pas le dernier
                return current_node.data[0]
            else:
                current_node = current_node.next_node # continue de se déplacer
                count += 1
        
        if current_node.data[1] == user_name:
            return current_node.data[0] # cas si l'index est le dernier
    
    def clear_history(self): # efface l'historique and effaceant le premier node
        self.first_node = None
        self.size = 0
        return "The user's history has been cleared."
    