import discord
from discord.ext import commands

from ..cfg.config import (
    GOS_GUILD,
    LUM_GUILD,
    GATE_KEEPER,
    BIG_BROTHER_WATCHING,
    LUM_WAIT_ROLE,
    GOS_WAIT_ROLE,
)


def gos_welcome_message(member):
    welcome = (
        f"Hos geldin {member}, sunucuya katilman için biraz sohbet etmen yeterli.\n"
        "Sadece steins;gate izleyenler girebilir o yuzden bizimle konusmaniz gerekli."
    )
    return welcome


def lum_welcome_message(member):
    welcome = (
        f"Hos geldin {member}, sunucuya katilman için biraz sohbet etmen yeterli.\n"
        "Burada rahatsızlık vermemeye ve insan gibi davranmaya özen göster.\n"
        f"<@&{GATE_KEEPER}> seninle ozenle ilgilenecektir."
    )
    return welcome


class MemberJoin(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_join(self, member):
        steinsgate_guild = self.bot.get_guild(GOS_GUILD)
        lum_guild = self.bot.get_guild(LUM_GUILD)

        if steinsgate_guild:
            if steinsgate_guild.get_member(member.id):
                guild = member.guild
                gos_wait_role = guild.get_role(GOS_WAIT_ROLE)
                wait_category = discord.utils.get(
                    guild.categories, name="BEKLEME YERI!"
                )

                if not wait_category:
                    channel = member.guild.system_channel
                    await channel.send("[error]: category not found")
                    return

                overwrites = {
                    guild.default_role: discord.PermissionOverwrite(view_channel=False),
                    member: discord.PermissionOverwrite(
                        view_channel=True, send_messages=True
                    ),
                }
                try:
                    await member.add_roles(gos_wait_role)
                    member_ch = await wait_category.create_text_channel(
                        name=member.name, overwrites=overwrites
                    )
                    await member_ch.send(gos_welcome_message(member.mention))
                    print(f"[info]: {member.name} joins lum guild")
                except discord.Forbidden:
                    print("[error]: No permission")
                except discord.HTTPException as e:
                    print(f"[error]: {e}")
                return

        if lum_guild:
            if lum_guild.get_member(member.id):

                guild = member.guild
                gate_keeper = guild.get_role(GATE_KEEPER)
                big_brother_watching = guild.get_role(BIG_BROTHER_WATCHING)
                kayitsiz_role = guild.get_role(LUM_WAIT_ROLE)

                wait_category = discord.utils.get(guild.categories, name="TEFTİS ODASI")

                if not wait_category:
                    channel = member.guild.system_channel
                    await channel.send("[error]: category not found")
                    return

                overwrites = {
                    guild.default_role: discord.PermissionOverwrite(view_channel=False),
                    member: discord.PermissionOverwrite(
                        view_channel=True, send_messages=True
                    ),
                    gate_keeper: discord.PermissionOverwrite(
                        view_channel=True,
                        send_messages=True,
                        embed_links=True,
                        attach_files=True,
                        add_reactions=True,
                    ),
                    big_brother_watching: discord.PermissionOverwrite(
                        view_channel=True,
                        add_reactions=True,
                    ),
                }
                try:
                    await member.add_roles(kayitsiz_role)
                    member_ch = await wait_category.create_text_channel(
                        name=member.name, overwrites=overwrites
                    )
                    await member_ch.send(lum_welcome_message(member.mention))
                    print(f"[info]: {member.name} joins lum guild")
                except discord.Forbidden:
                    print("[error]: No permission")
                except discord.HTTPException as e:
                    print(f"[error]: {e}")
                return


async def setup(bot):
    await bot.add_cog(MemberJoin(bot))
