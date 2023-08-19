import asyncio
from datetime import datetime, timedelta
import json
import discord
from discord import app_commands
from discord.ext import commands
from discord import Intents
from discord.ext import tasks
from typing import List, Literal
import requests
from discord.ext import tasks
from bs4 import BeautifulSoup
from discord import Button, ButtonStyle
from discord.ui import View



client = commands.Bot(command_prefix="-", intents=discord.Intents.all())
client.remove_command("help")

with open("config.json", "r") as f:
    config = json.load(f)

log_channel = config["log_channel"]
moderation_channel = config["moderation_channel"]
faq_file = config["faq_file"]
TOKEN = config["token"]
server_id = config["server_id"]
support_id = config["support_id"]
flag = False
high_priority = config["high_priority"]
dm_channel = config["dm_channel"]


class HelpView(discord.ui.View):
    foo : bool = None
    
    async def disable_all_buttons(self):
        for item in self.children:
            item.disabled = True

    async def on_timeout(self) -> None:
        await self.disable_all_buttons()
        await self.firstinteraction.edit_original_response(content="⏰ **| Timed out.**", view=self)


    @discord.ui.button(label="Yes", style=discord.ButtonStyle.success)
    async def priohelpyes(self, interaction: discord.Interaction, button: discord.ui.Button):
        embed = discord.Embed(color=0xf23f42)
        embed.set_author(name=f"📨 Asked for priority help in #{interaction.channel.name}",
                     icon_url=interaction.user.display_avatar.url)
        # fade out the buttons

        await interaction.response.send_message(embed=embed, ephemeral=True)
        self.foo = True
        self.stop()

    @discord.ui.button(label="No", style=discord.ButtonStyle.red)
    async def priohelpno(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message("**👍 | Canceling**", ephemeral=True)
        self.foo = False
        self.stop()

# when the bot gets mentioned
@client.event
async def on_message(message):
    if message.author.bot:
        return
    if client.user.mentioned_in(message) and message.mention_everyone is False:
        embed = discord.Embed(color=0x3d82e3)
        embed.set_author(name=f"👋 Hey {message.author.name}!", icon_url=message.author.display_avatar.url)
        embed.add_field(name=" ", value=f"If you need help in {message.guild.name}, please open a ticket in https://discord.com/channels/1085583960513458226/1085601455081279519")
        support = discord.Embed(color=0x3d82e3)
        support.set_author(name=f"👋 {message.author.name} pinged the mod bot!", icon_url=message.author.display_avatar.url)
        # show the original message
        support.add_field(name="Message", value=f"{message.content}", inline=False)
        support.add_field(name="Link", value=f"{message.jump_url}", inline=False)
        await client.get_channel(moderation_channel).send(embed=support)
        await message.author.send(embed=embed)

@client.event
async def on_message(message):
    #listen to messages that are send in dm to the bot
    if message.guild is None:
        if message.author.bot:
            return
        else:
            dmchannel = client.get_channel(dm_channel)
            embed = discord.Embed(color=0x3d82e3)
            embed.set_author(name=f"📨 New message from {message.author.name}#{message.author.discriminator}", icon_url=message.author.display_avatar.url)
            embed.add_field(name="Message", value=f"{message.content}", inline=False)
            embed.set_footer(text=f"ID: {message.author.id}")
            await dmchannel.send(f"{message.author.mention}",embed=embed)

# when a user joins the server
@client.event
async def on_member_join(member):
    # check if the username of the user contains "powered" and "bitcheck" and if the discriminator is not 0001
    if ("powered" in member.name.lower() and "bitcheck" in member.name.lower() or member.name.lower() == "powered") and member.id != 420652281076383749:
        # check if the user is a bot
        if member.bot:
            return
        else:
            # kick the user
            nicetry = discord.Embed(color=0xf23f42)
            nicetry.set_author(name=f"🚫 Nice try", icon_url=member.display_avatar.url)
            nicetry.add_field(name=" ", value="You are banned from the server for impersonating Powered")
            await member.send(embed=nicetry)
            await member.ban(reason="Impersonating Powered")
            # send a message in the moderation channel

            embed = discord.Embed(color=0xf23f42)
            embed.set_author(name=f"🚫 {member.name}#{member.discriminator} has been kicked", icon_url=member.display_avatar.url)
            embed.add_field(name="Reason", value="Impersonating Powered")
            embed.set_image(url="https://cdn-icons-png.flaticon.com/512/2014/2014825.png")
            await client.get_channel(moderation_channel).send(embed=embed)
            print(f"{member.name}#{member.discriminator} has been kicked for impersonating Powered")

# check when a user changes their username
@client.event
async def on_user_update(before, after):
    # user is not the server owner
    if ("powered" in after.name.lower() and "bitcheck" in after.name.lower() or after.name.lower() == "powered") and after.id != 420652281076383749:
        if after.bot:
            return
        else:
            # kick the user
            nicetry = discord.Embed(color=0xf23f42)
            nicetry.set_author(name=f"🚫 Nice try", icon_url=after.display_avatar.url)
            nicetry.add_field(name=" ", value="You are banned from the server for impersonating Powered")
            await after.send(embed=nicetry)
            await after.ban(reason="Impersonating Powered")
            # send a message in the moderation channel

            embed = discord.Embed(color=0xf23f42)
            embed.set_author(name=f"🚫 {after.name}#{after.discriminator} has been kicked", icon_url=after.display_avatar.url)
            embed.add_field(name="Reason", value="Impersonating Powered")
            embed.set_image(url="https://cdn-icons-png.flaticon.com/512/2014/2014825.png")
            await client.get_channel(moderation_channel).send(embed=embed)
            print(f"{after.name}#{after.discriminator} has been kicked for impersonating Powered")

# when they change their nickname
@client.event
async def on_member_update(before, after):
    # check if the user is the server owner
    if ("powered" in after.display_name.lower() and "bitcheck" in after.display_name.lower() or after.display_name.lower() == "powered") and after.id != 420652281076383749:
        if after.bot:
            return
        else:
            # kick the user
            nicetry = discord.Embed(color=0xf23f42)
            nicetry.set_author(name=f"🚫 Nice try", icon_url=after.display_avatar.url)
            nicetry.add_field(name=" ", value="You are banned from the server for impersonating Powered")
            await after.send(embed=nicetry)
            await after.ban(reason="Impersonating Powered")
            # send a message in the moderation channel

            embed = discord.Embed(color=0xf23f42)
            embed.set_author(name=f"🚫 {after.name}#{after.discriminator} has been kicked", icon_url=after.display_avatar.url)
            embed.add_field(name="Reason", value="Impersonating Powered")
            embed.set_image(url="https://cdn-icons-png.flaticon.com/512/2014/2014825.png")
            await client.get_channel(moderation_channel).send(embed=embed)
            print(f"{after.name}#{after.discriminator} has been kicked for impersonating Powered")

@client.event
async def on_ready():
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="BitCheck server"))
    try:
        synced = await client.tree.sync()
        print(f"Synced {len(synced)} commands")
    except Exception as e:
        print(f"Failed to sync commands: {e}")
    print("Bot is ready.")

    @tasks.loop(minutes=3)
    async def uptimecheck():
        website = requests.get("https://bitcheck.me")
        server = client.get_guild(server_id)
        user = server.get_member(1084499351461703821)
        admin = server.get_member(420652281076383749)
        if website.status_code != 200 and user.status != discord.Status.online:
            embed = discord.Embed(color=0x3d83e3)
            embed.set_author(name=f"⚠️ BitCheck is completely down!", username=user.avatar.url)
            embed.add_field(name="Website", value=f"Status code: {website.status_code}")
            embed.add_field(name="Bot", value=f"Status: {user.status}")
            await admin.send(embed=embed)
        elif website.status_code != 200:
            embed = discord.Embed(color=0x3d83e3)
            embed.set_author(name=f"⚠️ BitCheck website is down!", username=user.avatar.url)
            embed.add_field(name="Status code", value=f"{website.status_code}")
            await admin.send(embed=embed)
        elif user.status != discord.Status.online:
            embed = discord.Embed(color=0x3d83e3)
            embed.set_author(name=f"⚠️ BitCheck bot is down!", username=user.avatar.url)
            embed.add_field(name="Status", value=f"{user.status}")
            await admin.send(embed=embed)
        else:
            pass
    @tasks.loop(minutes=10)
    async def walletcheck():
        url = "https://api.bitcheck.me/stats"
        response = requests.get(url)
        data = response.json()
        #get "flags" from config.json
        with open("config.json", "r") as f:
            config = json.load(f)
        flag = config["flag"]
        if data["wallets"] > 20000 and flag == 0:
            with open("config.json", "w") as f:
                config["flag"] = 1
                json.dump(config, f, indent=4)
            embed = discord.Embed(color=0xf7931a)
            embed.set_author(name=f"🥳 We have reached 20.000 Wallets!", icon_url="https://bitcheck.me/logo.png")
            await client.get_guild(server_id).get_channel(moderation_channel).send(f"@everyone", embed=embed)
    @tasks.loop(minutes=10)
    async def serverscheck():
        guilds = [guild.name for guild in client.guilds]
        if len(guilds) > 1:
            guilds = ", ".join(guilds)
            embed = discord.Embed(color=0xf7931a)
            embed.set_author(name=f"⚠️ Moderation bot compromised", icon_url="https://bitcheck.me/logo.png")
            embed.add_field(name="Guilds", value=f"{guilds}")
            await client.get_guild(server_id).get_channel(moderation_channel).send(f"@everyone", embed=embed)
    uptimecheck.start()
    walletcheck.start()
    serverscheck.start()

@client.event
async def on_message_delete(message):
    if message.author.bot:
        return
    embed = discord.Embed(color=0x3d83e3)
    embed.set_author(name=f"🗑️ Message from {message.author.display_name} deleted",
                     icon_url=message.author.display_avatar.url)
    embed.add_field(name="Message", value=f"{message.content}", inline=False)
    embed.add_field(name="Channel", value=f"{message.channel.mention}")
    embed.add_field(name="Author", value=f"{message.author.mention}")
    await client.get_channel(log_channel).send(embed=embed)

# when a member gets banned
@client.event
async def on_member_ban(guild, user):
    # get the reason for the ban
    async for entry in guild.audit_logs(limit=1, action=discord.AuditLogAction.ban):
        reason = entry.reason

    embed = discord.Embed(color=0xc31615)
    embed.set_author(name=f"🔨 {user.display_name} has been banned", icon_url=user.display_avatar.url)
    embed.add_field(name="Reason:", value=reason, inline=True)

    await client.get_channel(log_channel).send(f"{user.mention}", embed=embed)

   
@client.tree.error
async def on_app_command_error(interaction: discord.Interaction, error: app_commands.AppCommandError):
    if isinstance(error, app_commands.CommandOnCooldown):
        print(f"{interaction.user} tried to use command `{interaction.command.name}` but failed because of cooldown")
        return await interaction.response.send_message(f"❌ **| You are on cooldown. Try again in `{round(error.retry_after)}` seconds.**", ephemeral=True)
    elif isinstance(error, app_commands.MissingPermissions):
        print(f"{interaction.user} tried to use command `{interaction.command.name}` but failed because of missing permissions")
        return await interaction.response.send_message("❌ **| You don't have permission to use this command.**", ephemeral=True)
    elif isinstance(error, app_commands.MissingRole):
        print(f"{interaction.user} tried to use command `{interaction.command.name}` but failed because of missing role")
        return await interaction.response.send_message("❌ **| You don't have permission to use this command.**", ephemeral=True)
    else:
        print(f"An error occured: {error}")
        return await interaction.response.send_message(f"❌ **| An error occured:** {error}", ephemeral=True)


@client.tree.command(name="ping", description="Ping the bot.")
@app_commands.checks.cooldown(1, 5, key=lambda i: i.user.id)
@app_commands.default_permissions(view_audit_log=True)
async def ping(interaction: discord.Interaction):
    await interaction.response.send_message(f"Pong! **{round(client.latency * 1000)}ms**")


@client.tree.command(name='ban', description='Ban a member permanently')
@app_commands.default_permissions(ban_members=True)
@app_commands.describe(member="The member you want to ban.", reason="The reason for the ban. (Optional)")
async def ban_command(interaction: discord.Interaction, member: discord.Member, reason: str = None):
    if member.top_role >= interaction.user.top_role:
        print(member.top_role, interaction.user.top_role)
        await interaction.response.send_message("❌ **| You can't ban this user because they have a higher role than you.**")
        embed = discord.Embed(color=0x3d83e3, title="Higher role ban attempt")
        embed.set_author(name=f"{interaction.user.display_name} tried to ban {member.display_name} but failed.",
                         icon_url=interaction.user.display_avatar.url)
        await client.get_channel(log_channel).send(embed=embed)
    else:
        try:
            banmsg = embed = discord.Embed(color=0xc31615)
            banmsg.set_author(name=f"🔨 You have been banned from the BitCheck Discord server", icon_url="https://bitcheck.me/logo.png")
            banmsg.add_field(name="Reason:", value=reason, inline=False)
            await member.send(embed=banmsg)
        except:
            pass
        await member.ban(reason=reason, delete_message_days=7)
        embed = discord.Embed(color=0x3d83e3)
        embed.set_author(
            name=f"{member.display_name} has been banned", icon_url=member.display_avatar.url)
        embed.add_field(name="Reason:", value=reason, inline=False)
        # send a log to the channel with id 1104164258280898682
        await interaction.response.send_message(embed=embed)


@client.tree.command(name='kick', description='Kick a member')
@app_commands.default_permissions(kick_members=True)
@app_commands.describe(member="The member you want to kick.", reason="The reason for the kick. (Optional)")
async def kick_command(interaction: discord.Interaction, member: discord.Member, reason: str = None):
    if member.top_role >= interaction.user.top_role:
        await interaction.response.send_message("❌ **| You can't kick this user because they have a higher role than you.**")
        embed = discord.Embed(color=0x3d83e3, title="Higher role kick attempt")
        embed.set_author(name=f"{interaction.user.display_name} tried to kick {member.display_name} but failed.",
                         icon_url=interaction.user.display_avatar.url)
        await client.get_channel(log_channel).send(embed=embed)
    else:
        await member.kick(reason=reason)
        embed = discord.Embed(color=0x3d83e3)
        embed.set_author(
            name=f"{member.display_name} has been kicked", icon_url=member.display_avatar.url)
        embed.add_field(name="Reason:", value=reason, inline=False)
        await client.get_channel(log_channel).send(f"{member.mention}", embed=embed)
        await interaction.response.send_message(embed=embed)


@client.tree.context_menu(name="report")
@app_commands.default_permissions(send_messages=True)
async def report(interaction: discord.Interaction, message: discord.Message):
    embed = discord.Embed(color=0x3d83e3)
    embed.set_author(
        name=f"✅ Reported the message from {message.author}", icon_url=message.author.display_avatar.url)
    embed.add_field(
        name=" ", value=f"The moderators have been notified.", inline=False)
    await interaction.response.send_message(embed=embed, ephemeral=True)
    # send the report message to the staff channel
    channel = client.get_channel(moderation_channel)
    embed = discord.Embed(color=0x3d83e3)
    embed.set_author(name=f"🚩 {interaction.user.display_name} reported a message",
                     icon_url=interaction.user.display_avatar.url)
    embed.set_thumbnail(url=message.author.display_avatar.url)
    embed.add_field(name="Message Author", value=f"{message.author}")
    embed.add_field(name="Message", value=f"{message.content}")
    embed.add_field(name="Channel", value=f"{message.channel.mention}")
    embed.add_field(name="Message url",
                    value=f"[Click here]({message.jump_url})")
    await channel.send(embed=embed)


@client.tree.context_menu(name="help")
@app_commands.default_permissions(view_audit_log=True)
async def help(interaction: discord.Interaction, user: discord.User):
    embed = discord.Embed(color=0x3d83e3)
    embed.set_author(name=f"📨 Asked {user} to help in #{interaction.channel.name}",
                     icon_url=interaction.user.display_avatar.url)
    await interaction.response.send_message(embed=embed, ephemeral=True)
    embed = discord.Embed(color=0x3d83e3)
    embed.set_author(name=f"❗ {interaction.user.display_name} asked for help",
                     icon_url=interaction.user.display_avatar.url)
    embed.add_field(name="Channel", value=f"{interaction.channel.mention}")

    await user.send(embed=embed)

@client.tree.context_menu(name="prio-help")
@app_commands.checks.cooldown(1, 60, key=lambda i: i.user.id)
@app_commands.default_permissions(view_audit_log=True)
async def help(interaction: discord.Interaction, user: discord.User):
    view = HelpView()
    # ask for confirmation before sending the message
    await interaction.response.send_message(
        f"Are you sure you want to ask {user} for priority help?",
        ephemeral=True, view=view
    )
    view.firstinteraction = interaction
    await view.wait()
    await view.disable_all_buttons()

    if view.foo is None:
        # throw a discord timeout error
        return
    elif view.foo is False:
        # throw a discord cancelled error
        return
    elif view.foo is True:
        embed = discord.Embed(color=0x3d83e3)
        embed.set_author(name=f"❗ {interaction.user.display_name} asked for fast help",
                        icon_url=interaction.user.display_avatar.url)
        embed.add_field(name="Channel", value=f"{interaction.channel.mention}")

        await user.send(f"**__⚠️⏰ {interaction.user.mention} needs fast help! ⏰⚠️__**",embed=embed)


async def faq_autocomplete(interaction: discord.Interaction,
                           current: str,
                           ) -> List[app_commands.Choice[str]]:
    with open(faq_file, "r") as f:
        file = json.load(f)
        questions = []
        for question in file:
            questions.append(question)
    choices = questions
    return [
        app_commands.Choice(name=choice, value=choice)
        for choice in choices if current.lower() in choice.lower()
    ]


@client.tree.command(name="faq", description="Frequently asked questions")
@app_commands.checks.cooldown(1, 10, key=lambda i: i.user.id)
@app_commands.autocomplete(question=faq_autocomplete)
@app_commands.describe(question="The question you want the answer to.", member="The member you want to ping in the answer. (Optional)")
async def faq(interaction: discord.Interaction, question: str, member: discord.Member = None):
    with open(faq_file, "r") as f:
        file = json.load(f)
        if question in file:
            embed = discord.Embed(
                color=0x3d83e3, title=file[question]["title"], description=file[question]["description"])
            try:
                embed.set_image(url=file[question]["image"])
            except:
                pass
            if member is not None:
                await interaction.response.send_message(f"{member.mention}", embed=embed)
            else:
                await interaction.response.send_message(embed=embed)
        else:
            await interaction.response.send_message("❌ **| This question doesn't exist.**", ephemeral=True)


@client.tree.command(name="reload", description="Reload the slash commands")
@app_commands.default_permissions(administrator=True)
async def reload(interaction: discord.Interaction):
    try:
        synced = await client.tree.sync()
        embed = discord.Embed(color=0x3d83e3)
        embed.set_author(
            name=f"✅ Synced {len(synced)} commands", icon_url=interaction.user.display_avatar.url)
        await interaction.response.send_message(f" **Synced `{len(synced)}` commands**", ephemeral=True)
        print(f"Synced {len(synced)} commands")
    except Exception as e:
        await interaction.response.send_message(f"❌ **| Failed to sync commands:** {e}", ephemeral=True)
        print(f"Failed to sync commands: {e}")


@client.tree.command(name="editfaq", description="Edit a FAQ")
@app_commands.choices(option=[
    app_commands.Choice(name="add", value="add"),
    app_commands.Choice(name="remove", value="remove"),
])
@app_commands.default_permissions(administrator=True)
@app_commands.describe(option="Add or remove a FAQ.", question="The name of the FAQ you want to add or remove.", title="The title of the question. (Only needed when adding a question)", description="The description of the question. (Only needed when adding a question)", image="The image of the question. (Only needed when adding a question, optional)")
async def editfaq(interaction: discord.Interaction, option:  app_commands.Choice[str], question: str, title: str = None, description: str = None, image: str = None):
    if str(option.value) == 'add':
        with open(faq_file, "r") as f:
            file = json.load(f)
            if question in file:
                await interaction.response.send_message("❌ **| This question already exists.**", ephemeral=True)
                return
            if title is None or description is None:
                await interaction.response.send_message("❌ **| You need to specify a title and description.**", ephemeral=True)
                return
            if image is not None:
                file[question] = {
                    "title": title,
                    "description": description,
                    "image": image
                }
                embed = discord.Embed(
                    color=0x3d83e3, title=title, description=description)
                embed.set_image(url=image)
            else:
                file[question] = {
                    "title": title,
                    "description": description,
                }
                embed = discord.Embed(
                    color=0x3d83e3, title=title, description=description)

            await interaction.response.send_message(f"Question `{question}` added:", embed=embed, ephemeral=True)
            await client.get_channel(log_channel).send(f"**@here A new FAQ called `{question}` has been added:**",embed=embed)

    elif str(option.value) == 'remove':
        with open(faq_file, "r") as f:
            file = json.load(f)
            if question not in file:
                await interaction.response.send_message("❌ **| This question doesn't exist.**", ephemeral=True)
                return
            else:
                del file[question]
                embed = discord.Embed(color=0x3d83e3)
                embed.set_author(
                    name=f"🗑️ Question '{question}' has been removed.")
                await interaction.response.send_message(embed=embed, ephemeral=True)
                removed = discord.Embed(color=0x3d83e3)
                removed.set_author( name=f"🗑️ The FAQ '{question}' has been removed.")
                await client.get_channel(log_channel).send(embed=removed)
    with open(faq_file, "w") as f:
        json.dump(file, f, indent=4)


@app_commands.default_permissions(manage_messages=True)
@client.tree.command(name="purge", description="Purge messages from a member")
@app_commands.describe(amount="The amount of messages you want to purge.", member="The member you want to purge messages from.")
async def purge(interaction: discord.Interaction, amount: int, member: discord.Member):
    if member is None:
        await interaction.response.send_message("❌ **| You need to specify a member.**", ephemeral=True)
        return
    if amount > 100:
        await interaction.response.send_message("❌ **| You can only purge 100 messages at a time.**", ephemeral=True)
        return
    embed = discord.Embed(color=0x3d83e3)
    embed.set_author(name=f"{interaction.user.display_name} purged {amount} messages from {member.display_name}",
                     icon_url=interaction.user.display_avatar.url)
    embed.add_field(name="Channel", value=f"{interaction.channel.mention}")
    answer = discord.Embed(color=0x3d83e3)
    message = "message" if amount == 1 else "messages"
    answer.set_author(
        name=f"✅ Purging {amount} {message} from {member}", icon_url=member.display_avatar.url)
    await interaction.response.send_message(embed=answer, ephemeral=True)
    await interaction.channel.purge(limit=amount, check=lambda m: m.author == member)
    await client.get_channel(log_channel).send(embed=embed)

@client.tree.command(name="invite", description="Invite the BitCheck bot to your server")
async def invite(interaction: discord.Interaction):
    embed = discord.Embed(color=0xf7931a)
    embed.set_author(name=f"📨 Invite BitCheck to your server", icon_url="https://bitcheck.me/logo.png")
    embed.add_field(name=" ", value="[Click here](https://invite.bitcheck.me) to invite BitCheck")
    await interaction.response.send_message(embed=embed, ephemeral=True)

@client.tree.command(name="sendinvite", description="Send an invite to a person for the BitCheck bot")
@app_commands.describe(member="The member you want to send the invite to.")
@app_commands.default_permissions(view_audit_log=True)
async def sendinvite(interaction: discord.Interaction, member: discord.Member):
    embed = discord.Embed(color=0xf7931a)
    embed.set_author(name=f"📨 Invite BitCheck to your server", icon_url="https://bitcheck.me/logo.png")
    embed.add_field(name=" ", value=f"You can invite the BitCheck Discord bot by [clicking here](https://invite.bitcheck.me)")
    await interaction.response.send_message(f"{member.mention}",embed=embed)



@app_commands.default_permissions(view_audit_log=True)
@client.tree.command(name="mute", description="Mute a member for a certain amount of time")
@app_commands.describe(member="The member you want to mute.", seconds="The amount of seconds you want to mute the member for. (optional)", minutes="The amount of minutes you want to mute the member for. (optional)", hours="The amount of hours you want to mute the member for. (optional)", days="The amount of days you want to mute the member for. (optional)", reason="The reason for the mute. (Optional)")
async def timeout(interaction: discord.Interaction, member: discord.Member, seconds: int = 0, minutes: int = 0, hours: int = 0, days: int = 0, reason: str = None):
    duration = timedelta(seconds=seconds, minutes=minutes,
                         hours=hours, days=days)
    await member.timeout(duration, reason=reason)
    # make the string for the time the user is timed out for
    time = ""
    if days != 0:
        dagen = "days" if days > 1 else "day"
        time += f"{days} {dagen} "
    if hours != 0:
        uren = "hours" if hours > 1 else "hour"
        time += f"{hours} {uren} "
    if minutes != 0:
        minuten = "minutes" if minutes > 1 else "minute"
        time += f"{minutes} {minuten} "
    if seconds != 0:
        seconden = "seconds" if seconds > 1 else "second"
        time += f"{seconds} {seconden} "
    embed = discord.Embed(color=0x3d83e3, timestamp=datetime.utcnow()+duration)
    embed.set_author(
        name=f"🔇 {member.display_name} has been muted for {time}", icon_url=member.display_avatar.url)
    embed.add_field(name="Reason:", value=reason, inline=False)
    embed.set_footer(text=f"Until: ")
    await interaction.response.send_message(embed=embed, ephemeral=True)
    embed.add_field(name="Moderator:",
                    value=interaction.user.mention, inline=False)
    await client.get_channel(log_channel).send(f"{member.mention}", embed=embed)


@app_commands.default_permissions(view_audit_log=True)
@client.tree.context_menu(name="question")
async def question(interaction: discord.Interaction, message: discord.Message):
    embed = discord.Embed(color=0x3d83e3)
    embed.set_author(name=f"{interaction.user} needs help for a question",
                     icon_url=interaction.user.display_avatar.url)
    embed.add_field(
        name="Author", value=f"{message.author.mention}", inline=False)
    embed.add_field(name="Message", value=f"{message.content}", inline=False)
    embed.add_field(
        name="Channel", value=f"{message.channel.mention}", inline=False)
    embed.add_field(
        name="Url", value=f"[Click here]({message.jump_url})", inline=False)
    await client.get_channel(moderation_channel).send(embed=embed)
    embed = discord.Embed(color=0x3d83e3)
    embed.set_author(name=f"✅ Asked for help in the mod channel",
                     icon_url=interaction.user.display_avatar.url)
    await interaction.response.send_message(embed=embed, ephemeral=True)


def thousands(x):
    return "{:,}".format(x)


@app_commands.default_permissions(administrator=True)
@client.tree.command(name="stats", description="Check the stats of BitCheck")
async def stats(interaction: discord.Interaction):
    url = "https://api.bitcheck.me/stats"
    response = requests.get(url)
    data = response.json()

    url = 'https://api.bitcheck.me/guilds'
    servers = requests.get(url)
    serverss = len(servers.text.split('\n'))
    try:
        members = 0
        for line in servers.text.splitlines():
            if "members" in line:
                pre = line.split("members")[0]
                members += int(pre.split('-')[len(pre.split('-'))-1])
    except:
        pass

    embed = discord.Embed(color=0xf7931a)
    embed.set_author(name=f"BitCheck stats",
                     icon_url="https://bitcheck.me/logo.png")
    embed.add_field(
        name="👨 Users", value=f"{thousands(data['users'])}", inline=False)
    embed.add_field(name="💻 Profile Users",
                    value=f"{thousands(data['profileUsers'])}", inline=True)
    embed.add_field(name="👛 Wallets",
                    value=f"{thousands(data['wallets'])}", inline=True)
    embed.add_field(name="🎨 Collections",
                    value=f"{thousands(data['collections'])}", inline=True)
    embed.add_field(name="✍️ Inscriptions",
                    value=f"{thousands(data['inscriptions'])}", inline=True)
    embed.add_field(name="📈 Servers",
                    value=f"{thousands(serverss)}", inline=True)
    if members != 0:
        embed.add_field(name="👨‍👩‍👧‍👦 Discord users",
                        value=f"{thousands(members)}", inline=True)
    await interaction.response.send_message(embed=embed, ephemeral=True)


@client.tree.command(name="server", description="Check the stats of the server")
@app_commands.default_permissions(administrator=True)
async def stats(interaction: discord.Interaction):
    embed = discord.Embed(color=0x3d83e3)
    embed.set_author(name=f"📊 Server stats",
                     icon_url=interaction.user.display_avatar.url)
    embed.add_field(
        name="Members", value=f"{interaction.guild.member_count}", inline=True)
    embed.add_field(name="Channels",
                    value=f"{len(interaction.guild.channels)}", inline=True)
    embed.add_field(
        name="Roles", value=f"{len(interaction.guild.roles)}", inline=True)
    embed.add_field(
        name="Emojis", value=f"{len(interaction.guild.emojis)}", inline=True)
    embed.add_field(
        name="Boosts", value=f"{interaction.guild.premium_subscription_count}", inline=True)
    embed.add_field(
        name="Owner", value=f"{interaction.guild.owner.mention}", inline=True)
    embed.add_field(name="Created at",
                    value=f"{interaction.guild.created_at.strftime('%d/%m/%Y')}", inline=True)
    await interaction.response.send_message(embed=embed, ephemeral=True)


@client.tree.command(name="members", description="Check how many members are in the server")
@app_commands.checks.cooldown(1, 10, key=lambda i: i.user.id)
@app_commands.default_permissions(administrator=True)
async def stats(interaction: discord.Interaction):
    # membercount
    membercount = interaction.guild.member_count
    # get the amount of bots
    bots = sum(member.bot for member in interaction.guild.members)
    # get the amount of humans
    humans = membercount - bots
    embed = discord.Embed(color=0x3d83e3)
    embed.set_author(name=f"📈 Member stats")
    embed.add_field(name="📝 Total", value=f"{membercount}", inline=True)
    embed.add_field(name="👨 Humans", value=f"{humans}", inline=True)
    embed.add_field(name="🤖 Bots", value=f"{bots}", inline=True)
    await interaction.response.send_message(embed=embed, ephemeral=True)


@client.tree.command(name="lostbalance", description="View the $BIT balance lost by an address due to front running (Usable in our platform).")
@app_commands.checks.cooldown(1, 10, key=lambda i: i.user.id)
@app_commands.default_permissions(send_messages=True)
@app_commands.describe(address="The address to check")
async def lostbalance(interaction: discord.Interaction, address: str):
    # open the file lostbit.json
    with open("lostbit.json", "r") as f:
        data = json.load(f)
    try:
        embed = discord.Embed(color=0xf7931a, description=f"You will be able to use this balance in the future on the BitCheck platform.")
        embed.set_author(name=f"Lost balance due to frontrunning",icon_url="https://bitcheck.me/logo.png")
        embed.add_field(name=" ",
                        value=f"**{thousands(data[address])} $BIT**", inline=True)
        embed.set_footer(text=address)
        await interaction.response.send_message(embed=embed)
    except Exception as e:
        embed = discord.Embed(color=0xf7931a)
        embed.set_author(name=f"Lost balance due to frontrunning",
                         icon_url="https://bitcheck.me/logo.png")
        embed.add_field(
            name=" ", value=f"This address doesn't have any lost balance in $BIT.", inline=True)
        embed.set_footer(text=address)
        await interaction.response.send_message(embed=embed)

@client.tree.context_menu(name="Can't read")
@app_commands.default_permissions(view_audit_log=True)
async def cantread(interaction: discord.Interaction, message: discord.Message):
    embed = discord.Embed(color=0x3d83e3)
    embed.set_author(name=f"📝 {message.author} can't read",
                     icon_url=message.author.display_avatar.url)
    embed.add_field(name="Author", value=f"{message.author.mention}")
    embed.add_field(name="Message", value=f"{message.content}")
    embed.add_field(name="Channel", value=f"{message.channel.mention}")
    embed.add_field(name="Message url",
                    value=f"[Click here]({message.jump_url})")
    await client.get_channel(log_channel).send(embed=embed)

    author = message.author
    #give the user the role "question"
    role = discord.utils.get(message.guild.roles, name="Question")
    await author.remove_roles(discord.utils.get(message.guild.roles, name="Member"))
    await author.add_roles(role)
    msg = await client.get_channel(support_id).send(f"{author.display_name}, Please open a ticket here so we can help you.\nIf you don't need any help anymore, please react with ❌. ||{message.author.mention}||")
    await msg.add_reaction("❌")
    await interaction.response.send_message(f"{message.author.mention} **has been forced to open a ticket.**", ephemeral=True)
    try:
        await asyncio.sleep(120)
        await msg.delete()
        await asyncio.sleep(120)
        await author.remove_roles(role)
        await author.add_roles(discord.utils.get(message.guild.roles, name="Member"))
    except:
        pass

@client.event
async def on_raw_reaction_add(payload):

    if payload.member.bot:
        return
    if payload.channel_id == support_id:
        payloadmsg = await client.get_channel(payload.channel_id).fetch_message(payload.message_id)
        if payload.emoji.name == "❌" and payload.member.display_name in payloadmsg.content:
            await payloadmsg.delete()
            await payload.member.remove_roles(discord.utils.get(payload.member.guild.roles, name="Question"))
            await payload.member.add_roles(discord.utils.get(payload.member.guild.roles, name="Member"))
            embed = discord.Embed(color=0x3d83e3, description=f"{payload.member.mention} doesn't need help anymore")
            embed.set_author(name=f"❌ Can't read offer closed", icon_url=payload.member.display_avatar.url)
            await client.get_channel(log_channel).send(f"{payload.member.mention}", embed=embed)

@client.tree.command(name="remove-question-role", description="Remove the question role from a member that has been \"Can't read\"ed")
@app_commands.default_permissions(view_audit_log=True)
@app_commands.describe(member="The member you want to remove the question role from.")
async def removequestionrole(interaction: discord.Interaction, member: discord.Member):
    try:
        await member.remove_roles(discord.utils.get(member.guild.roles, name="Question"))
    except:
        pass
    try:
        await member.add_roles(discord.utils.get(member.guild.roles, name="Member"))
    except:
        pass
    embed = discord.Embed(color=0x3d83e3)
    embed.set_author(name=f"✅ Removed the question role from {member.display_name}", icon_url=member.display_avatar.url)
    await interaction.response.send_message(embed=embed, ephemeral=True)

@client.tree.command(name="announce-oneline", description="announce a one-liner")
@app_commands.default_permissions(administrator=True)
@app_commands.describe(message="The message you want to announce.", tag="The tag you want to announce with. (optional)")
async def announceoneline(interaction: discord.Interaction, message: str, channel: discord.TextChannel,tag: str = None):
    embed = discord.Embed(color=0xf7931a)
    embed.set_author(name=f"{message}", icon_url="https://bitcheck.me/logo.png")
    if tag is None:
        await client.get_channel(channel.id).send(embed=embed)
    else:
        await client.get_channel(channel.id).send(f"{tag}", embed=embed)
    await interaction.response.send_message(f"✅ **| Announced in {channel.mention}**", ephemeral=True)
    
@client.tree.command(name="bitprice", description="Shows the current price of $BIT. (ALLEEN GIJ KUNT DIT WARD)")
@app_commands.checks.cooldown(1, 10, key=lambda i: i.user.id)
@app_commands.default_permissions(administrator=True)
async def bit(interaction: discord.Interaction):
    url = "https://brc-20.io/token?n=$bit"
    response = requests.request("GET", url)
    soup = BeautifulSoup(response.text, "html.parser")
    price = soup.find_all(name="h1")
    # get the 2nd to last element
    price = price[-2]
    price = price.text
    await interaction.response.send_message(f"✅ **| The current price of $BIT is {price}**", ephemeral=True)

@client.tree.command(name="export-lostbit", description="Export the lost $BIT addresses to a json file")
@app_commands.default_permissions(administrator=True)
async def exportlostbit( interaction: discord.Interaction):
    await interaction.response.send_message("✅ **| Exported the lostbit file.**",file=discord.File('lostbit.json'), ephemeral=True)

@client.tree.command(name="export-questions", description="Export the questions json file")
@app_commands.default_permissions(administrator=True)
async def exportquestions( interaction: discord.Interaction):
    await interaction.response.send_message("✅ **| Exported the questions file.**",file=discord.File(f"{faq_file}"), ephemeral=True)

@client.tree.command(name="upload-questions", description="Upload the questions json file. (overwrites the current one)")
@app_commands.default_permissions(administrator=True)
@app_commands.describe(file="The json file that contains the questions.")
async def uploadquestions( interaction: discord.Interaction, file: discord.Attachment):
    await file.save(faq_file)
    await interaction.response.send_message("✅ **| Uploaded the questions file.**", ephemeral=True)

@client.tree.command(name="higher-support", description="Move a ticket to the high priority channel category")
@app_commands.default_permissions(view_audit_log=True)
@app_commands.describe(channel="The ticket channel you want to move to the high priority category. (optional)")
async def highprio(interaction: discord.Interaction, issue: str, channel: discord.TextChannel = None,):
    if channel is None:
        channel = interaction.channel
    embed = discord.Embed(color=0x3d83e3)
    embed.set_author(name=f"✅ Moved this ticket to the higher support category.", icon_url="https://bitcheck.me/logo.png")
    await interaction.response.send_message(embed=embed, ephemeral=True)
    # move it to the last position in the category
    await channel.edit(category=client.get_channel(high_priority), topic=issue, reason="Moved to high priority category")
    embed = discord.Embed(color=0x3d83e3)
    embed.set_author(name=f"Your ticket has been moved to a higher support category!", icon_url="https://bitcheck.me/logo.png")
    embed.add_field(name="Issue:", value=f"{issue}")
    await channel.send(embed=embed)


client.run(TOKEN)