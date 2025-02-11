import discord
from discord import app_commands
from typing import Optional

import json

from src.utils import *

from src.cmd.crypt import zn_ch_en 
from src.cmd.ai import *
from src.cmd.ban import ban_user
from src.cmd.purge import message_purge
from src.cmd.kick import kick_user
from src.cmd.rulet import rulet

intents = discord.Intents.default()
intents.message_content = True
intents.members = True
intents.messages = True
intents.guilds = True

client = discord.Client(command_prefix="!", intents=intents)
slash = app_commands.CommandTree(client)

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

GOS_KAYITSIZ = config["GOS_KAYITSIZ"]
GOS_KAYIT_CH = config["GOS_KAYIT_CH"]

GATE_KEEPER = config["GATE_KEEPER"]
LUM_ROL = config["LUM_ROL"]

NV_USER_LOG_CH = config["NV_USER_LOG_CH"]

VERSION = config["VERSION"]

@client.event
async def on_ready():
    await slash.sync()
    print(f"[work]: {client.user}")

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    if message.webhook_id:
        return

    content = message.content.lower()
    args = message.content.split()

    ###################
    #      PURGE      #
    ###################
    if content.startswith("!purge"):
        await message_purge(message, args)
        return

    ###################
    #       BAN       #
    ###################
    if content.startswith("!ban"):
        await ban_user(message, args)
        return

    ###################
    #       KICK      #
    ###################
    if content.startswith("!kick"):
        await kick_user(message, args)
        return

    ###################
    #       RULET     #
    ###################
    if content.startswith("!rulet"):
        await rulet(message)
        return

    ###################
    #     ZINCIRLI    #
    ###################
    if message.channel.id == ZN_CH:
        await zn_ch_en(message)
        return

    ###################
    #     KURISU CH   #
    ###################
    if message.channel.id == 1338301496923652137:
        await kurisu_ch(message)
        return

    if content.startswith("!version"):
        await message.reply(f"[info]: Amadeus System {VERSION}")
        return

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
            return

    if lum_guild:
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

