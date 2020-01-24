import discord
from discord.ext import commands
import logging
import os
import asyncio
from itertools import cycle

f = open('token.txt', 'r')
TOKEN = f.read().replace('\n', '')
logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)
client = commands.Bot(command_prefix="!")
status=['crying','sobbing','weeping','yeeting']
@client.event
async def change_status():
	await client.wait_until_ready()
	statusx=cycle(status)
	while not client.is_closed():
		print("working")
		current_status=next(statusx)
		await client.change_presence(activity=discord.Game(name=current_status))
		await asyncio.sleep(5)
		 
@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))
@client.event
async def on_member_join(member):
	role=discord.utils.get(member.guild.roles,name="Hero")
	await member.add_roles(role)

@client.command()
async def ping(message):
	await message.channel.send("Pong!")
@client.command()
async def clean(ctx,amount=100):
	messages=[]
	channel=ctx.channel
	async for message in channel.history(limit=int(amount)+1):
		messages.append(message)
	await channel.delete_messages(messages)
	await channel.send('Messages Deleted!')
client.loop.create_task(change_status())
client.run(TOKEN)