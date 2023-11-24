import discord
import requests
import json
from meteofrance_api import *

from Key import *
from discord.ext import commands

#autres fichiers
from Dialogues import cues, returns

#intents = droits
intents = discord.Intents.all()

client = commands.Bot(command_prefix="!", intents = intents) #préfix = début de commandes

@client.command()
async def delete(ctx):
    messages = await ctx.channel.history(limit=10)

    for each_message in messages:
        each_message.delete()

@client.command()
async def hello(ctx):
   await ctx.send("Hello, I am a youtube bot")

@client.command()
async def goodbye(ctx):
   await ctx.send("Goodbye, have a great day")

@client.event
async def on_ready():
    print("𝔹𝕠𝕥𝕤 𝕒𝕣𝕖 𝕣𝕖𝕒𝕕𝕪")
    print("--------------")



@client.event
async def on_typing(channel, user, when):
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
  if message.author == client.user:
    return

  message.content = message.content.lower()

  if message.content.startswith("hello"):
    await message.channel.send("Hello")

  if "cochon" in message.content:
    await message.channel.send("R")

  if message.content == "azerty":
    await message.channel.send("qwerty")

  await client.process_commands(message)

#Commencer à coder ici
@client.event
#ne fait pas de distinction entre qui envoie un message ( peut se répondre à lui-même )
async def on_message(message): #async 
  if message.author == client.user :
    return

  if message.content.startswith(cues()):
    #détecter un message sur un channel et renvoyer un message
    await message.channel.send(returns())
  await client.process_commands(message)

client.run(key)