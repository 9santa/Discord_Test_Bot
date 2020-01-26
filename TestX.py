import discord
from discord.ext import commands
from discord.utils import get
import logging
import os
import asyncio
from itertools import cycle
import youtube_dl
import shutil
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
	def check_queue():
		Queue_infile=os.path.isdir("./Queue")
		if Queue_infile is True:
			DIR=os.path.abspath(os.path.realpath("Queue"))
			length=len(os.listdir(DIR))
			still_q=length-1
			try:
				first_file=os.listdir(DIR)[0]
			except:
				print("No more songs")
				queues.clear()
				return
			main_location= os.path.dirname(os.path.realpath(__file__))
			song_path=os.path.abspath(os.path.realpath("Queue")+"\\"+first_file)
			if length!=0:
				print("Playing next song")
				print(f"Songs in queue:{still_q}")
				song_there=os.path.isfile("song.mp3")
				if song_there:
					os.remove("song.mp3")
				shutil.move(song_path,main_location)
				for file in os.listdir("./"):
					if file.endswith(".mp3"):
						os.rename(file,"song.mp3")
				vc.play(discord.FFmpegPCMAudio("song.mp3"),after=lambda e: check_queue())
				vc.source=discord.PCMVolumeTransformer(vc.source)
				vc.source.volume=0.07
			else:
				queues.clear()
				return
		else:
			queues.clear()
			print("No song")
	if os.path.isfile("song.mp3"):
		os.remove("song.mp3")
		queues.clear()
	if os.path.isfile("./Queue") is True:
		shutil.rmtree("./Queue")


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
		try:
			ydl.download([url])
		except:
			ctx.send("Error downloading invalid url")
	if os.path.isfile("song.mp3"):
		os.remove("song.mp3")
	for file in os.listdir("./"):

		if file.endswith(".mp3"):
			name=file
			#print(f"Renamed file:{file}\n")
			try:
				os.rename(file,"song.mp3")
			except:
				pass
	try:
		vc.play(discord.FFmpegPCMAudio("song.mp3"),after=lambda e: check_queue())
	except:
		ctx.send("The bot may not be in voice channel")
	vc.source=discord.PCMVolumeTransformer(vc.source)
	vc.source.volume=0.07

@client.command()
async def pause(ctx):
	if vc and vc.is_playing():
		vc.pause()
		await ctx.send("Paused!")
	else:
		await ctx.send("Music not playing!")
@client.command()
async def resume(ctx):
	if vc and vc.is_paused():
		vc.resume()
		await ctx.send("Music Resumed!")
	else:
		await ctx.send("Music not paused")
@client.command()
async def stop(ctx):
	queues.clear()
	queue_infile=os.path.isdir("./Queue")
	if queue_infile is True:
		shutil.rmtree("./Queue")

	if vc and vc.is_playing:
		vc.stop()
		await ctx.send("Stopped")
	else:
		await ctx.send("Music not playing!")
queues={}

@client.command()
async def queue(ctx,url):
	Queue_infile=os.path.isdir("./Queue")
	if Queue_infile is False:
		os.mkdir("Queue")
	DIR=os.path.abspath(os.path.realpath("Queue"))
	q_num=len(os.listdir(DIR))
	q_num+=1
	add_queue=True
	while add_queue:
		if q_num in queues:
			q_num+=1
		else:
			add_queue = False
			queues[q_num]=q_num
	queue_path=os.path.abspath(os.path.realpath("./Queue")+f"\song{q_num}.%(ext)s")
	ydl_opts={
	'format':'bestaudio/best',
	'outtmpl':queue_path,
	'postprocessors': [{
		'key':'FFmpegExtractAudio',
		'preferredcodec': 'mp3',
		'preferredquality':'192',

	}],

	}
	with youtube_dl.YoutubeDL(ydl_opts) as ydl:
		print("downloading song")
		ydl.download([url])
	await ctx.send("Added to queue at no."+str(q_num))

@client.command()
@commands.has_role('admin')
async def kick(ctx,member: discord.Member,*,reason="none"):
	await member.kick(reason=reason)
	await ctx.send(f"Kicked!{user.mention}")
@client.command()
@commands.has_role('admin')
async def ban(ctx,member : discord.Member,*,reason="none"):
	await member.ban(reason=reason)
	await ctx.send(f"Banned! {user.mention}")
@client.command()
@commands.has_role('admin')
#we need user#123 member format as they are not in server
async def unban(ctx,*,member): 						
	banned_users= await ctx.guild.bans()
	member_name,member_discriminator=member.split('#')
	for ban_entry in banned_users:
		user=ban_entry.user
		if(user.name,user.discriminator)==(member_name,member_discriminator):
			await ctx.guild.unban(user)
			await ctx.send(f"Unbanned {user.mention}")
			return

@client.command
async def load(ctx,extension):
	client.load_extension(f"cogs.{extension}")
@client.command
async def unload(ctx,extension):
	client.unload_extension(f"cogs.{extension}")
for filename in os.listdir("./cogs"):
	if filename.endswith(".py"):
		client.load_extension(f"cogs.{filename[:-3]}")

client.loop.create_task(change_status())
client.run(TOKEN)