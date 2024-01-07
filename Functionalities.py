# Liaison avec discord
import asyncio
import discord
from discord.ext import commands

intents = discord.Intents.all()
client = commands.Bot(command_prefix="!", intents = intents)

# imports pour les functionalités
from discord import FFmpegPCMAudio, TextInput, TextStyle
from meteofrance_api import *

# import des deux autres parties du projet
from History import *
from Dialogues import *

L=chained_history_list() # Initialisation de notre liste enchainé représentant l'historique
Q=queue_managing_history() # Initialisation de notre file de gestion de l'historique
B=binary_tree() # Initialisation de notre questionnaire sous forme d'arbre binaire
current_index_scroll = 0

### Toutes commandes

@client.command(pass_context = True)
async def join(ctx):
  if (ctx.author.voice):
      channel = ctx.message.author.voice.channel # Si l'utilisateur est dans un channel, il le rejoind
      voice = await channel.connect()
      source = FFmpegPCMAudio('join_bot.mp3')
      voice.play(source)

      L.add_new_command("!join", str(ctx.author)) # Ajout de la commande dans l'historique
  else:
        await ctx.send("This is a command you can only run when you are in a voice channel.")

@client.command(pass_context = True)
async def leave(ctx):
  if (ctx.voice_client):
     await ctx.guild.voice_client.disconnect() # guild = server, voice_client = voice channel
     await ctx.send("Leaving the voice channel") # Laisses un message lorsqu'il quitte le channel
     
     L.add_new_command("!leave", str(ctx.author)) # Ajout de la commande dans l'historique
  else:
     await ctx.send("I'm no longer in a voice channel")


## Commandes modifiant l'historique
@client.command()
async def last_command(ctx):
   if Q.is_locked() == False: # Vérifie si l'historique est en cours de modification
      Q.lock = True
      last_command = L.get_last_command() # Renvoie la derniére commande inscrite dans l'historique
      await ctx.send(f'The last command entered was : {last_command}')
      await ctx.send("This command has now been added as well.")
      L.add_new_command("!last_command", str(ctx.author))
      Q.lock = False # Le verrou se désactive à chaque fin de commande
   else:
      error = Q.is_locked()
      await ctx.send(f'{error}')

@client.command()
async def first_command(ctx):
   if Q.is_locked() == False:
      Q.lock = True
      first_command = L.get_first_command() # Renvoie la premiére commande inscrite dans l'historique
      if first_command != None:
         await ctx.send(f'The first command entered was : {first_command}')
      else:
         await ctx.send("There are currently no commands.") 
      L.add_new_command("!first_command", str(ctx.author))
      Q.lock = False
   else:
      error = Q.is_locked()
      await ctx.send(f'{error}')

@client.command()
async def all_commands_of(ctx, *, name): # On peut spécifier l'utilisateur en question en argument au moment du lancement de la commande
   if Q.is_locked() == False:
      Q.lock = True
      user_name = str(name)
      commands = L.get_all_commands_of(user_name)
      if commands != None:
         await ctx.send(f'Here are all the commands of {user_name} : {commands}') # Renvoie toutes les commandes faites par un utilisateur
         await ctx.send("This command has now been added as well.")
         L.add_new_command("!all_commands_of", str(ctx.author)) # on ajoute la nouvelle commande à l'auteur de celle-ci, pas la personne recherchée
      else:
         await ctx.send(f'There are currently no commands for {user_name}.')
         await ctx.send("This command will now be added however.")
         L.add_new_command("!all_commands_of", str(ctx.author))
      Q.lock = False
   else:
      error = Q.is_locked()
      await ctx.send(f'{error}')

@client.command()
async def scrolling_forward_of(ctx, *, name): # Scroll en avant dans un historique précis ( droite )
   if Q.is_locked() == False:
      Q.lock = True
      user_name = str(name)
      commands = L.get_all_commands_of(user_name)
      if commands != None:
         last_index_scroll = L.size
         global current_index_scroll
         if current_index_scroll < last_index_scroll:
            current_index_scroll += 1
            scroll_result = L.get_scroll(current_index_scroll, user_name)
         await ctx.send(f'The current command is : {scroll_result}')
      else:
         await ctx.send(f'There are currently no commands for {user_name}.') 
      Q.lock = False
   else:
      error = Q.is_locked()
      await ctx.send(f'{error}')

@client.command()
async def scrolling_backwards_of(ctx, *, name): # Scroll en arrière dans un historique précis ( gauche )
   if Q.is_locked() == False:
      Q.lock = True
      user_name = str(name)
      commands = L.get_all_commands_of(user_name)
      if commands != None:
         global current_index_scroll
         if current_index_scroll > 0:
            current_index_scroll -= 1
            scroll_result = L.get_scroll(current_index_scroll, user_name)
         await ctx.send(f'The current command is : {scroll_result}')
      else:
         await ctx.send(f'There are currently no commands for {user_name}.') 
      Q.lock = False
   else:
      error = Q.is_locked()
      await ctx.send(f'{error}')

@client.command()
async def clear_history(ctx): # Effacement de l'historique
   if Q.is_locked() == False:
      Q.lock = True
      await ctx.send(L.clear_history())
      Q.lock = False
   else:
      error = Q.is_locked()
      await ctx.send(f'{error}')

## Dialogue sous forme d'arbre binaire

@client.command()
async def binary_dialogue(ctx): # Lancement du questionnaire
      def check(response): # Vérifie si la réponse a été fournis dans le même channel que la question
         return response.channel == ctx.channel and response.author == ctx.author
      
      await ctx.send(B.get_current_dialogue()) # Début du dialogue

      try:
         user_response = await client.wait_for('message', check=check, timeout=180.0)
         new_dialogue = B.get_on_response(user_response.content)
         await ctx.send(new_dialogue)
         user_response = await client.wait_for('message', check=check, timeout=180.0)
         new_dialogue = B.create_more_dialogue(user_response.content)
         await ctx.send(new_dialogue)
         new_dialogue = B.get_current_dialogue()
         await ctx.send(f"{new_dialogue}{user_response.content} ?") # Le dialogue s'est mis à jour
         user_response = await client.wait_for('message', check=check, timeout=180.0)
         if user_response.content == "yes":
            file_path = './italian wood fired margherita pizza.jpg'

            # Open the file in binary mode
            with open(file_path, 'rb') as file:
               image = discord.File(file)
               await ctx.send(file=image)
            
            await ctx.send("Glad I could help ! This is the end of the binary tree dialogue.")
         elif user_response.content == "no":
            await ctx.send("That's ok ! This is the end of the binary tree dialogue.")
      except asyncio.TimeoutError:
         await ctx.send("You seem busy. The dialogue has ended.")

@client.command()
async def dialogue_reset(ctx): # Réinitialisation du questionnaire
   B.get_dialogue_reset()
   await ctx.send("The binary tree dialogue has been reset.")

@client.command()
async def speak_about(ctx, *, name): # Vérification des sujets abordables
   list = ["pizza"]
   for val in list:
      if name == val:
         await ctx.send(f"Yes ! We can talk about {val} (=^ω^=) !")
      else:
         await ctx.send(f"I'm sorry... I can't talk about that yet. ᇂ_ᇂ")



### Tous évènements

@client.event
async def on_typing(channel, user, when=None):
     name = user.name
     await channel.send(f"{name} is typing")

@client.event
async def on_member_join(member):
    general_channel = client.get_channel(1167470292088660020) #get_channel(channel x's id)
    name = member.name
    await general_channel.send(f"{name}, welcome !")
    Meteo = MeteoFranceClient()
    Forecast = Meteo.get_forecast(longitude=48.864716, latitude=2.349014)
    # print(Forecast.current_forecast)
    desc_weather = Forecast.current_forecast.get("weather", {}).get("desc")
    # print(desc_weather)
    await general_channel.send(f"Here is the current forecast : {desc_weather} ")

@client.event
async def on_member_remove(member):
    general_channel = client.get_channel(1167470292088660020) #get_channel(channel x's id)
    name = member.name
    await general_channel.send(f"Farewell {name} !") 

@client.event
async def on_message(message):
  if message.author == client.user :
    return

  message.content = message.content.lower()

  if message.content == cues(message.content): # les cues and returns sont dans Dialogues.py afin de personaliser
    # détecter un message sur un channel et renvoyer un message
    await message.channel.send(returns())
  await client.process_commands(message)
