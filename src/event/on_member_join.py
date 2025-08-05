import discord
from discord.ext import commands

from config import (
    GOS_GUILD,
    LUM_GUILD,
    LUM_WAIT_ROLE,
    GOS_WAIT_ROLE,
)

class MemberJoin(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    def _welcome_message(self, member, guild_id):
        if guild_id == GOS_GUILD:
            return (
                f"Hos geldin {member}, sunucuya katilman için biraz sohbet etmen yeterli.\n"
                "Sadece steins;gate izleyenler girebilir o yuzden bizimle konusmaniz gerekli."
            )
        elif guild_id == LUM_GUILD:
            return (
                f"Hos geldin {member}, sadece yetkili birini beklemen yeterli, etiket falan atmaya calisma acelesi yok.\n"
            )

    async def _create_wait_channel(self, member, category, overwrites, welcome_message):
        try:
            member_ch = await category.create_text_channel(
                name=member.name, overwrites=overwrites
            )
            await member_ch.send(welcome_message)
        except discord.Forbidden:
            print("[error]: No permission to create channel or send message.")
        except discord.HTTPException as e:
            print(f"[error]: {e}")

    @commands.Cog.listener()
    async def on_member_join(self, member: discord.Member):
        guild = member.guild
        category_name = None
        overwrites = {
            guild.default_role: discord.PermissionOverwrite(view_channel=False),
            member: discord.PermissionOverwrite(view_channel=True, send_messages=True),
        }
        welcome_msg = self._welcome_message(member.mention, guild.id)

        if guild.id == GOS_GUILD:
            role = guild.get_role(GOS_WAIT_ROLE)
            category_name = "BEKLEME YERI!"

        elif guild.id == LUM_GUILD:
            role = guild.get_role(LUM_WAIT_ROLE)
            category_name = "TEFTİS ODASI"

        else:
            return  # Unknown guild

        wait_category = discord.utils.get(guild.categories, name=category_name)
        if not wait_category:
            if guild.system_channel:
                await guild.system_channel.send("[error]: category not found")
            return

        try:
            if role:
                await member.add_roles(role)
            await self._create_wait_channel(
                member, wait_category, overwrites, welcome_msg
            )
            print(f"[info]: {member.name} joined {guild.name}")
        except Exception as e:
            print(f"[error]: Unexpected error during member join handling: {e}")


async def setup(bot):
    await bot.add_cog(MemberJoin(bot))
