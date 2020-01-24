import discord
from discord.ext import commands
import logging
import os
f = open('token.txt', 'r')
TOKEN = f.read().replace('\n', '')
logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)
client = commands.Bot(command_prefix="!")

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))
#@client.event
#async def on_message(message):
#	if message.content.startswith("!hi"):
#		await message.channel.send(" Hi")
@client.command()
async def ping(message):
	await message.channel.send("Pong!")

client.run(TOKEN)