import random
### Arbre binaire pour le systéme de discussion

class branch: # Définition d'une branche binaire par défaut
    def __init__(self, data, left=None, right=None):
        self.Data = data
        self.yes = left
        self.no = right

class binary_tree:
    def __init__(self):
        # Définition de l'enbranchement
        self.start = branch("Would you like to discuss a certain topic ?")
        self.yes_node = branch("Ok, what should we talk about ?")
        self.yes_node.yes = branch("Would you like me to send an image of : ")
        self.no_node = branch("That's alright, we can always talk at another time.")

        self.current_node = self.start # on se place sur le tout premier node
    
    def get_on_response(self, response): # Mouvement de l'arbre binaire selon la réponse
        if response == "yes":
            self.current_node = self.yes_node
            return self.current_node.Data
        elif response == "no":
            self.current_node = self.no_node
            return self.current_node.Data
        else:
            return "The response given was not clear. Please answer 'yes' or 'no'."

    def create_more_dialogue(self, topic):
        list = [f"I think {topic} is really great !", f"I want to learn more about {topic} but it is very hard."]
        self.current_node = self.current_node.yes
        return list[random.randint(0,1)]

    def get_current_dialogue(self): # Commence le questionnaire
        return self.current_node.Data
    
    def get_dialogue_reset(self): # Recommence le questionnaire
        self.current_node = self.start # on se replace sur le tout premier node



### Personal cues and responses ( une functionalitée )
def cues(message_content):
    list = ["hi", "bonjour"]
    for val in list:
        if val == message_content:
            return val

def returns():
    list = ["(っ◔◡◔)っ ♥ 𝙃𝙚𝙡𝙡𝙤 ♥", "＼ʕ •ᴥ•ʔ／ 𝙃𝙤𝙬 𝙖𝙧𝙚 𝙮𝙤𝙪 ? ♥ "]
    return list[random.randint(0,1)]