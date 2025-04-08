import discord
from discord.ext import commands
from discord import app_commands
import datetime


from ..cfg.config import LUM_ROLE, LUM_USER_LOG_CH, GATE_KEEPER


class Register(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="register", description="Bir üyenin kaydını yapar.")
    async def register(
        self,
        interaction: discord.Interaction,
        member: discord.Member,
    ):
        ALLOWED_ROLES = {1213598172040003604, GATE_KEEPER}

        user_roles = {role.id for role in interaction.user.roles}
        if not user_roles & ALLOWED_ROLES:
            await interaction.response.send_message(
                "[warn]: yetkin yetmiyor", ephemeral=True
            )
            return

        register_role = discord.utils.get(interaction.guild.roles, id=LUM_ROLE)
        if register_role:
            await member.add_roles(register_role)
        if not register_role:
            channel = member.guild.system_channel
            await channel.send("[error]: register_role not found")

        log_channel = self.bot.get_channel(LUM_USER_LOG_CH)

        embed = discord.Embed(
            title="Üye Kaydı Yapıldı",
            description=f"**member:** {member.mention}\n**author:** {interaction.user.mention}\n**date:** {datetime.datetime.now()}",
            color=discord.Color.yellow(),
        )

        await log_channel.send(embed=embed)
        overwrites = {
            member: discord.PermissionOverwrite(view_channel=False, send_messages=False)
        }

        await interaction.channel.set_permissions(member, overwrite=overwrites[member])
        await interaction.response.send_message("Kayit ettim")
        print(f"[ok]: register {member.name}")


async def setup(bot):
    await bot.add_cog(Register(bot))
