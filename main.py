import asyncio
from datetime import datetime, timedelta
import json
import discord
from discord import app_commands
from discord.ext import commands
from discord import Intents
from discord.ext import tasks



client = commands.Bot(command_prefix="-", intents=discord.Intents.all())
client.remove_command("help")

log_channel = 1104164258280898682
moderation_channel = 1104164258280898682

@client.event
async def on_ready():
	await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching ,name="BitCheck server", url="https://www.bitcheck.me"))
	try:
		synced = await client.tree.sync()
		print(f"Synced {len(synced)} commands")
	except Exception as e:
		print(f"Failed to sync commands: {e}")
	print("Bot is ready.")

@client.tree.command(name="ping", description="Ping the bot.")
async def ping(interaction: discord.Interaction):
	await interaction.response.send_message(f"Pong! **{round(client.latency * 1000)}ms**")

# a ban command that only works for people with the ban members permission
@client.tree.command(name='ban', description='Moderator command')
@commands.has_permissions(ban_members=True)
async def ban_command(interaction: discord.Interaction, member: discord.Member, reason: str=None):
	if interaction.user.guild_permissions.ban_members:

		# check if the person who is being banned has a higher role than the person who is banning them
		if member.top_role >= interaction.user.top_role:
			print(member.top_role, interaction.user.top_role)
			await interaction.response.send_message("You can't ban this user because they have a higher role than you.")
			embed = discord.Embed(color=0x3d83e3, title="Higher role ban attempt")
			embed.set_author(name=f"{interaction.user.display_name} tried to ban {member.display_name} but failed.", icon_url=interaction.user.display_avatar.url)
			await client.get_channel(log_channel).send(embed=embed)
		else:
			#await member.ban(reason=reason)
			embed = discord.Embed(color=0x3d83e3)
			embed.set_author(name=f"{member.display_name} has been banned", icon_url=member.display_avatar.url)
			embed.add_field(name="Reason:", value=reason, inline=False)
			# send a log to the channel with id 1104164258280898682
			await client.get_channel(log_channel).send(f"{member.mention}",embed=embed)

			await interaction.response.send_message(embed=embed)
	else:
		await interaction.response.send_message("You don't have permission to use this command.", ephemeral=True)

# a kick command that only works for people with the kick members permission
@client.tree.command(name='kick', description='Moderator command')
@commands.has_permissions(kick_members=True)
async def kick_command(interaction: discord.Interaction, member: discord.Member, reason: str=None):
	if interaction.user.guild_permissions.kick_members:
		# check if the person who is being kicked has a higher role than the person who is kicking them
		if member.top_role >= interaction.user.top_role:
			await interaction.response.send_message("You can't kick this user because they have a higher role than you.")
			embed = discord.Embed(color=0x3d83e3, title="Higher role kick attempt")
			embed.set_author(name=f"{interaction.user.display_name} tried to kick {member.display_name} but failed.", icon_url=interaction.user.display_avatar.url)
			await client.get_channel(log_channel).send(embed=embed)
		else:
			#await member.kick(reason=reason)
			embed = discord.Embed(color=0x3d83e3)
			embed.set_author(name=f"{member.display_name} has been kicked", icon_url=member.display_avatar.url)
			embed.add_field(name="Reason:", value=reason, inline=False)
			await client.get_channel(log_channel).send(f"{member.mention}",embed=embed)
			await interaction.response.send_message(embed=embed)
	else:
		await interaction.response.send_message("You don't have permission to use this command.", ephemeral=True)

@client.tree.context_menu(name="report")
async def report(interaction: discord.Interaction, message: discord.Message):
	await interaction.response.send_message(f"👀 **| Reported the message from `{message.author}`**", ephemeral=True)
	# send the report message to the staff channel
	channel = client.get_channel(moderation_channel)
	embed = discord.Embed(color=0x006ec2)
	embed.set_author(name=f"{interaction.user.display_name} reported a message", icon_url=interaction.user.display_avatar.url)
	embed.set_thumbnail(url=message.author.display_avatar.url)
	embed.add_field(name="Message Author", value=f"{message.author}")
	embed.add_field(name="Message", value=f"{message.content}")
	embed.add_field(name="Channel", value=f"{message.channel.mention}")
	embed.add_field(name="Message url", value=f"[Click here]({message.jump_url})")
	await channel.send(embed=embed)

@client.tree.context_menu(name="help")
async def help(interaction: discord.Interaction, user: discord.User):
	# check if the interaction user can see the audit log
	if not interaction.user.guild_permissions.view_audit_log:
		await interaction.response.send_message("You don't have permission to use this command.", ephemeral=True)
		return
	# send a user a dm that asks for help in the current channel
	await interaction.response.send_message(f"👀 **| Asked for help from `{user}`**", ephemeral=True)
	embed = discord.Embed(color=0x006ec2)
	embed.set_author(name=f"{interaction.user.display_name} asked for help", icon_url=interaction.user.display_avatar.url)
	embed.add_field(name="Channel", value=f"{interaction.channel.mention}")

	await user.send(embed=embed)

# a command that has a list of default answers to questions
@client.tree.command(name="faq", description="Moderator command")
async def faq(interaction: discord.Interaction , question: str, member: discord.Member = None):
	# search for question in questions.json
	with open("questions.json", "r") as f:
		file = json.load(f)
	# check if the question is in the questions.json file
		if question in file:
			# send the answer to the question
			embed = discord.Embed(color=0x006ec2, title=file[question]["title"], description=file[question]["description"])
			if member is not None:
				await interaction.response.send_message(f"{member.mention}",embed=embed)
			else:
				await interaction.response.send_message(embed=embed)





	


client.run("MTEwNDE1NTI2NTY2Mzc2MjU4Mg.GzIknn.pvlWxwvM5idmlrcimNEPhfVskcKJaXVAPAcTVg")