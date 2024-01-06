# Liaison avec discord
import discord
from discord.ext import commands

intents = discord.Intents.all()
client = commands.Bot(command_prefix="!", intents = intents)

# imports pour les functionalités
from discord import FFmpegPCMAudio, TextInput, TextStyle
from meteofrance_api import *

# import des deux autres parties du projet
from History import *
from Dialogues import cues, returns

L=chained_history_list()
current_index_scroll = 0

### Toutes commandes

@client.command(pass_context = True)
async def join(ctx):
  if (ctx.author.voice):
      channel = ctx.message.author.voice.channel # if user in a voice channel, will join it
      voice = await channel.connect()
      source = FFmpegPCMAudio('join_bot.mp3')
      player = voice.play(source)

      L.add_new_command("!join", str(ctx.author)) # Ajout de la commande dans l'historique
  else:
        await ctx.send("This is a command you can only run when you are in a voice channel.")

@client.command(pass_context = True)
async def leave(ctx):
  if (ctx.voice_client):
     await ctx.guild.voice_client.disconnect() # guild = server, voice_client = voice channel
     await ctx.send("Leaving the voice channel") # leaves a message behind when they leave the voice channel
     
     L.add_new_command("!leave", str(ctx.author)) # Ajout de la commande dans l'historique
  else:
     await ctx.send("I'm no longer in a voice channel")

@client.command()
async def last_command(ctx):
   await ctx.send(L.get_last_command()) # Renvoie la derniére commande inscrite dans l'historique
   await ctx.send("This command has now been added as well.")
   L.add_new_command("!last_command", str(ctx.author))

@client.command()
async def first_command(ctx):
   L.add_new_command("!first_command", str(ctx.author))
   await ctx.send(L.get_first_command()) # Renvoie la premiére commande inscrite dans l'historique

@client.command()
async def all_commands_of(ctx):
   user_name = str(ctx.author)
   await ctx.send(L.get_all_commands_of(user_name)) # Renvoie toutes les commandes faites par un utilisateur
   await ctx.send("This command has now been added as well.")
   L.add_new_command("!all_commands_of", str(ctx.author))

@client.command()
async def scrolling_forward(ctx):
   last_index_scroll = L.size
   global current_index_scroll
   if current_index_scroll < last_index_scroll:
      current_index_scroll += 1
   await ctx.send(L.get_scroll(current_index_scroll))

@client.command()
async def scrolling_backwards(ctx):
   global current_index_scroll
   if current_index_scroll > 0:
      current_index_scroll -= 1
   await ctx.send(L.get_scroll(current_index_scroll))

@client.command()
async def clear_history(ctx):
   await ctx.send(L.clear_history())


### Tous évènements

@client.event
async def on_typing(channel, user):
     await channel.send(user.name+" is typing")

@client.event
async def on_member_join(member):
    
    general_channel = client.get_channel(1167470292088660020) #get_channel(channel x's id)
    await general_channel.send(member.name + " , welcome !")
    Meteo = MeteoFranceClient()
    Forecast = Meteo.get_forecast(longitude=48.864716, latitude=2.349014)
    # print(Forecast.current_forecast)
    desc_weather = Forecast.current_forecast.get("weather", {}).get("desc")
    # print(desc_weather)
    await general_channel.send("Here is the current forecast : " + desc_weather)

@client.event
async def on_member_remove(member):
    general_channel = client.get_channel(1167470292088660020) #get_channel(channel x's id)
    await general_channel.send("Farewell  " + member.name + " !") 


@client.event
async def on_message(message):

  if message.author == client.user :
    return

  message.content = message.content.lower()

  if message.content.startswith("hello"):
    await message.channel.send("Hello")

  if "cochon" in message.content:
    await message.channel.send("R")

  if message.content == "azerty":
    await message.channel.send("qwerty")

  if message.content.startswith(cues()):
    #détecter un message sur un channel et renvoyer un message
    await message.channel.send(returns())
  await client.process_commands(message)