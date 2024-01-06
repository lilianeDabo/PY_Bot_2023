# Gestion de l'historique

class node: # structure du node
    def __init__(self, data): # initialisation
        self.Data = data
        self.next_node = None

class chained_history_list: # structure de la liste enchainé
    def __init__(self): # initialisation
        self.first_node = None
        self.size = 0
    
    def add_new_command(self, new_command, user_name):
        # cas du tout premier node
        if self.first_node == None:
            self.first_node = node([new_command, user_name])
            self.size += 1
            return
        
        current_node = self.first_node
        # on se place donc sur le premier pour parcourir l'historique
        # et définir l'emplacement vide suivant
        while current_node.next_node != None:
            current_node = current_node.next_node
        
        new_node = node([new_command, user_name])
        current_node.next_node = new_node
        self.size += 1
        

    def get_last_command(self): # cherche et prend la derniére commande de l'historique
        if self.first_node != None:
            current_node = self.first_node
            while current_node.next_node != None:
                current_node = current_node.next_node
            return "The last command entered was : " + current_node.Data[0]
        else:
            return "The last command entered was : None"
    

    def get_first_command(self): # cherche et prend la premiére commande de l'historique
        if self.first_node != None:
            current_node = self.first_node
            return "The first command entered was : " + current_node.Data[0]
        else:
            return "There are no commands."
    
    
    # cherche le user en question 
    # et renvoie toutes les commandes entrées depuis sa derniére connexion
    def get_all_commands_of(self, user_name): 
        all_commands = []
        if self.first_node != None:
            all_commands.append(self.first_node.Data[0])
            current_node = self.first_node
            while current_node.next_node != None:
                    if current_node.Data[1] == user_name:
                        current_node = current_node.next_node
                        all_commands.append(current_node.Data[0])
            return "Here are all the commands of " + user_name + " : " + str(all_commands)
        else:
            return "There are currently no commands for " + user_name 
    

    # avance et recule dans l'historique en fonction de l'index_scroll
    def get_scroll(self, current_index_scroll):
        count = 0
        current_node = self.first_node

        # print("count:", count)
        # print("current_index_scroll:", current_index_scroll)
        # print("current_node:", current_node.Data[0])

        while current_node.next_node != None:
            if count == current_index_scroll:
                return "The current command is : " + current_node.Data[0]
            else:
                current_node = current_node.next_node
                count += 1
        
        # print("Final count:", count)
        # print("Final current_node:", current_node.Data[0])
        return "The current command is : " + current_node.Data[0]
    
    def clear_history(self):
        self.first_node = None
        self.size = 0
        return "The user's history has been cleared."
    