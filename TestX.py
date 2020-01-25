import discord
from discord.ext import commands
from discord.utils import get
import logging
import os
import asyncio
from itertools import cycle
import youtube_dl

players={}


f = open('token.txt', 'r')
TOKEN = f.read().replace('\n', '')
logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)
client = commands.Bot(command_prefix="!")
client.remove_command('help')

status=['crying','sobbing','weeping','yeeting']
@client.event
async def change_status():
	await client.wait_until_ready()
	statusx=cycle(status)
	while not client.is_closed():
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
	async for message in channel.history(limit=int(amount)):
		messages.append(message)
	await channel.delete_messages(messages)
	await channel.send('Messages Deleted!')
@client.command()
async def help(ctx):
	author=ctx.author
	embed=discord.Embed(
	description="This is the help you'll need",
	colour=discord.Colour.blue()
	)
	embed.set_author(name='help')
	embed.add_field(name=".ping ",value="Returns pong wont tell you how clean works",inline=False)
	embed.add_field(name=".play",value="Play with !play (url) ",inline=False)
	await ctx.channel.send(author,embed=embed)
@client.command()
async def displayembed(ctx):
	embed=discord.Embed(
	title="Title",
	description="This is the description",
	colour=discord.Colour.blue()
	)
	embed.set_footer(text="Here you go.")
	embed.set_image(url="https://i.imgur.com/rqFMhSx.jpg")
	embed.set_thumbnail(url="https://i.imgur.com/CndgMNn.jpg")
	embed.set_author(name="Author name",icon_url="https://i.imgur.com/07hQrmL.jpg")
	embed.add_field(name="Field Name",value="field value",inline=True)
	await ctx.channel.send(embed=embed)
@client.event
async def on_reaction_add(reaction,user):
	channel=reaction.message.channel
	await channel.send('{} has added {} to the message {}'.format(user.name,reaction.emoji,reaction.message.content))
@client.command()
async def join(ctx):
	if ctx.author.voice and ctx.author.voice.channel:
		channel = ctx.author.voice.channel
	else:
		await ctx.send("You are not connected to a voice channel")
		return
	global vc
	try:
		vc=await channel.connect()
	except:
		TimeoutError
@client.command()
async def leave(ctx):
	try:
		if vc.is_connected():
			await vc.disconnect()
	except:
		TimeoutError
		pass
@client.command()
async def play(ctx,url):
	if os.path.isfile("song.mp3"):
		os.remove("song.mp3")
	vc = ctx.voice_client
	ydl_opts={
	'format':'bestaudio/best',
	'postprocessors': [{
		'key':'FFmpegExtractAudio',
		'preferredcodec': 'mp3',
		'preferredquality':'192',

	}],

	}
	with youtube_dl.YoutubeDL(ydl_opts) as ydl:
		print("downloading song")
		ydl.download([url])
	for file in os.listdir("./"):
		if file.endswith(".mp3"):
			name=file
			print(f"Renamed file:{file}\n")
			os.rename(file,"song.mp3")
	vc.play(discord.FFmpegPCMAudio("song.mp3"))
	vc.source=discord.PCMVolumeTransformer(vc.source)
	vc.source.volume=0.07

client.loop.create_task(change_status())
client.run(TOKEN)