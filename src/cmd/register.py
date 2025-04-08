import discord
from discord.ext import commands
from discord import app_commands
import datetime


from ..cfg.config import (
    LUM_WAIT_ROLE,
    LUM_GUILD,
    LUM_ROLE,
    LUM_USER_LOG_CH,
    REGISTER_ALLOWED_ROL_OR_MEMBER,
)


class Register(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name="register", description="Bir üyenin kaydını yapar.")
    async def register(
        self,
        interaction: discord.Interaction,
        member: discord.Member,
    ):
        if not isinstance(interaction.user, discord.Member):
            await interaction.response.send_message(
                "[error]: Bu komut sadece sunucuda çalışır.", ephemeral=True
            )
            return

        user_roles = {role.id for role in interaction.user.roles}
        if not user_roles & REGISTER_ALLOWED_ROL_OR_MEMBER:
            await interaction.response.send_message(
                "[warn]: yetkin yetmiyor", ephemeral=True
            )
            return

        register_role = discord.utils.get(interaction.guild.roles, id=LUM_ROLE)
        if register_role:
            await member.add_roles(register_role)
        else:
            if member.guild.system_channel:
                await member.guild.system_channel.send(
                    "[error]: register_role not found"
                )

        log_channel = self.bot.get_channel(LUM_USER_LOG_CH)
        if log_channel and isinstance(log_channel, discord.TextChannel):
            embed = discord.Embed(
                title="Log:",
                description=(
                    f"**member:** {member.mention}\n"
                    f"**author:** {interaction.user.mention}\n"
                    f"**date:** {datetime.datetime.now()}"
                ),
                color=discord.Color.yellow(),
            )
            await log_channel.send(embed=embed)

        if interaction.channel and isinstance(interaction.channel, discord.TextChannel):
            overwrites = {
                member: discord.PermissionOverwrite(
                    view_channel=False, send_messages=False
                )
            }
            await interaction.channel.set_permissions(
                member, overwrite=overwrites[member]
            )

        guild = self.bot.get_guild(LUM_GUILD)
        kayitsiz_role = guild.get_role(LUM_WAIT_ROLE)
        await member.remove_roles(kayitsiz_role)
        await interaction.response.send_message("Kayit ettim")
        print(f"[ok]: register {member.name}")


async def setup(bot):
    await bot.add_cog(Register(bot))
