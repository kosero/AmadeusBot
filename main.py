import discord
from discord import app_commands
from typing import Optional
from discord.ui import select

import json
import random
import time
from datetime import timedelta
import asyncio

from src.utils import *
from src.webhook import send_webhook_message
from src.crypt import encrypt, decrypt

intents = discord.Intents.default()
intents.message_content = True
intents.members = True
intents.messages = True
intents.guilds = True

client = discord.Client(command_prefix="!", intents=intents)
slash = app_commands.CommandTree(client)

random.seed(time.time())

###################
#    VARiABLES    #
###################
with open('config/config.json', 'r') as file:
    config = json.load(file)

# Token
CLIENT_TOKEN = config["CLIENT_TOKEN"]

NV_GUILD = config["NV_GUILD"]
GOS_GUILD = config["GOS_GUILD"]

ZN_CH = config["ZN_CH"]
ZN_KEY = config["ZN_KEY"]

GOS_KAYITSIZ = config["GOS_KAYITSIZ"]
GOS_KAYIT_CH = config["GOS_KAYIT_CH"]

GATE_KEEPER = config["GATE_KEEPER"]
LUM_ROL = config["LUM_ROL"]

NV_USER_LOG_CH = config["NV_USER_LOG_CH"]

VERSION = config["VERSION"]

@client.event
async def on_ready():
    print(f"[work]: {client.user}")

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    if message.webhook_id:
        return
    content = message.content.lower()

    ###################
    #      PURGE      #
    ###################
    if content.startswith("!purge"):
        if message.channel.permissions_for(message.author).manage_messages:
            args = message.content.split()
            count = int(args[1]) if len(args) > 1 and args[1].isdigit() else 0
            if count < 1 or count > 100:
                await message.reply("[warn]: `!purge 1-100`", delete_after=5)
                return
            deleted = await message.channel.purge(limit=count)
            await message.reply(f"[info]: {len(deleted)} messages deleted", delete_after=5)
        else:
            await message.reply("[warn]: No permission", delete_after=5)
    
    ###################
    #       BAN       #
    ###################
    if content.startswith("!ban"):
        if not message.author.guild_permissions.ban_members:
            await message.reply("[warn]: No permission", delete_after=5)
            return

        args = message.content.split()
        if len(args) < 2:
            await message.reply("[warn]: `!ban @user/id [reason]`", delete_after=5)
            return

        user_mention = message.mentions[0] if message.mentions else None
        user_id = args[1] if not user_mention else None
        reason = " ".join(args[2:]) if len(args) > 2 else ""
        user = None

        try:
            if user_mention:
                user = user_mention
            elif user_id and user_id.isdigit():
                user = await client.fetch_user(int(user_id))
            else:
                await message.reply("97.", delete_after=5)
                return

            if isinstance(user, discord.Member):
                if message.author.top_role <= user.top_role:
                    await message.reply("[warn]: your permission is not enough to ban this user", delete_after=5)
                    return

            await message.guild.ban(user, reason=reason)
            await message.reply(f"[info]: {user.mention} kicked by {message.author}, {reason}")

        except discord.Forbidden:
            await message.reply("[warn]: I don't have permission to kick this user", delete_after=5)
        except discord.HTTPException as e:
            await message.reply(f"[error]: {e}", delete_after=5)

    ###################
    #       KICK      #
    ###################
    if content.startswith("!kick"):
        if not message.author.guild_permissions.kick_members:
            await message.reply("[warn]: No permission")
            return

        args = message.content.split()
        if len(args) < 2:
            await message.reply("[warn]: `!kick @user/id`")
            return

        member = None
        if message.mentions:
            member = message.mentions[0]
        else:
            try:
                user_id = int(args[1])
                member = message.guild.get_member(user_id)
            except ValueError:
                await message.reply("[warn]: user id is wrong")
                return

        if not member:
            await message.reply("[warn]: user not found")
            return

        if member == message.author:
            await message.reply("[warn]: you can't kick yourself")
            return
        
        if message.guild.owner_id == member.id:
            await message.reply("[warn]: you can't kick the guild owner")
            return

        if message.author.top_role <= member.top_role:
            await message.reply("[warn]: your permission is not enough to kick this user")
            return

        try:
            await member.kick(reason=f"kicked by {message.author}")
            await message.reply(f"[info]: {member.mention} kicked by {member.author}")
        except discord.Forbidden:
            await message.reply("[warn]: I don't have permission to kick this user")
        except discord.HTTPException as e:
            await message.reply(f"[error]: {e}")

    ###################
    #       RULET     #
    ###################
    if content.startswith("!rulet"):
        user = message.author
        outcome = random.choice(["win", "lose"])
        
        await message.reply("Derin bir nefes alarak tetiğe yavaşça basıyorsun...")
        await asyncio.sleep(3)
        if outcome == "win":
            await message.channel.send("Bugün ölüm seninle boy ölçüşemedi.")
        else:
            try:
                duration = 86400
                await user.timeout(discord.utils.utcnow() + timedelta(seconds=duration), reason="Rulet kaybı")
                await message.channel.send(f"Kaderin ince dokunuşu bugün, şansın seninle vedalaşmaya karar verdiğini fısıldarcasına hissediliyor; sanki son perdenin inmesi vakti gelmiş gibi, geçmişin sessiz anılarıyla kısa bir elveda zamanı...")
            except discord.HTTPException as e:
                await message.reply(f"[error]: {e}", delete_after=5)

    ###################
    #       RULET     #
    ###################
    if message.channel.id == ZN_CH:
        encrypted_message = encrypt(content, ZN_KEY)
        avatar_url = message.author.avatar.url if message.author.avatar else "https://i.imgur.com/CSU09SU.png"
        await send_webhook_message("custom", message.channel, encrypted_message, custom_avatar=avatar_url, custom_name=message.author.name)
        await message.delete()

    if content.startswith("!version"):
        await message.reply(f"[info]: Amadeus System {VERSION}")

@client.event
async def on_member_join(member):
    steinsGate_guild = client.get_guild(GOS_GUILD)
    lum_guild = client.get_guild(NV_GUILD)

    if steinsGate_guild:
        if steinsGate_guild.get_member(member.id):
            role = discord.utils.get(member.guild.roles, id=GOS_KAYITSIZ)
            await member.add_roles(role)

            channel = client.get_channel(GOS_KAYIT_CH)
            if channel:
                await channel.send(member.mention, delete_after=5)
            else:
                return
            return
        else:
            return

    elif lum_guild:
        if lum_guild.get_member(member.id):
            guild = member.guild
            gate_keeper = guild.get_role(GATE_KEEPER)
            category = discord.utils.get(guild.categories, name="BEKLE!")

            if not category:
                channel = member.guild.system_channel
                await channel.send("[error]: category not found")
                return

            overwrites = {
                guild.default_role: discord.PermissionOverwrite(view_channel=False),
                member: discord.PermissionOverwrite(view_channel=True, send_messages=True),
                gate_keeper: discord.PermissionOverwrite(
                    view_channel=True, 
                    send_messages=True, 
                    embed_links=True,
                    attach_files=True,
                    add_reactions=True
                ),
            }

            try:
                member_ch = await category.create_text_channel(name=member.name, overwrites=overwrites)
                await member_ch.send(welcome_message(member.mention))
            except discord.Forbidden:
                print("[error]: No permission")
            except discord.HTTPException as e:
                print(f"[error]: {e}")
        else:
            return
    else:
        return

@slash.command(
    name="register",
    description="Bir üyenin kaydını yapar.",
)
async def kayit( interaction: discord.Interaction, member: discord.Member, age: Optional[int] = None, why: Optional[str] = None ):
    ALLOWED_ROLES = {1213598172040003604, 1336209216809205822}

    user_roles = {role.id for role in interaction.user.roles}
    if not user_roles & ALLOWED_ROLES:
        await interaction.response.send_message("[warn]: yetkin yetmiyor", ephemeral=True)
        return

    kayit_rol = discord.utils.get(interaction.guild.roles, id=LUM_ROL)
    await member.add_roles(kayit_rol)

    log_channel = client.get_channel(NV_USER_LOG_CH)

    embed = discord.Embed(
        title="Üye Kaydı Yapıldı",
        description=f"**Üye:** {member.mention}\n**Yaş:** {age}\n**Katılma Sebebi:** {why}\n**Kayit eden:** {interaction.user.id}",
        color=discord.Color.yellow()
    )

    await log_channel.send(embed=embed)
    overwrites = {
        member: discord.PermissionOverwrite(view_channel=False, send_messages=False)
    }

    await interaction.channel.set_permissions(member, overwrite=overwrites[member]) 
    await interaction.response.send_message("Kayit ettim", ephemeral=True)

@slash.command(
    name="shortened_link",
    description="linki kisaltir"
)
async def short_link(interaction: discord.Interaction, url: str):
    shortened = shorten_url(f"{url}")
    await interaction.response.send_message(shortened)

client.run(CLIENT_TOKEN)

