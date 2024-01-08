# import des clés
import threading
from Keys import *

# imports des 3 parties du projet
from Dialogues import *
from History import *
from Functionalities import *

@client.event
async def on_ready(): # for terminal tests
    print("𝔹𝕠𝕥𝕤 𝕒𝕣𝕖 𝕣𝕖𝕒𝕕𝕪")
    print("--------------")

# lancement du bot
client.run(key)