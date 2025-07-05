import discord
from discord.ext import commands
from discord import app_commands
from datetime import datetime

from config import (
    LUM_WAIT_ROLE,
    LUM_USER_LOG_CH,
    LUM_REGISTER_ALLOWED_ROL_OR_MEMBER,
)


class Register(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name="register", description="Bir üyenin kaydını yapar.")
    async def register(self, interaction: discord.Interaction, member: discord.Member):
        if not interaction.guild or not isinstance(interaction.user, discord.Member):
            await interaction.response.send_message(
                "[error]: Bu komut sadece sunucuda çalışır.", ephemeral=True
            )
            return

        user_roles = {role.id for role in interaction.user.roles}
        if not user_roles & LUM_REGISTER_ALLOWED_ROL_OR_MEMBER:
            await interaction.response.send_message(
                "[warn]: Yetkin yetmiyor", ephemeral=True
            )
            return

        guild = interaction.guild

        register_role = guild.get_role(LUM_WAIT_ROLE)
        if register_role:
            await member.add_roles(register_role)
        else:
            if guild.system_channel:
                await guild.system_channel.send("[error]: Kayıt rolü bulunamadı")

        log_channel = self.bot.get_channel(LUM_USER_LOG_CH)
        if isinstance(log_channel, discord.TextChannel):
            embed = discord.Embed(
                title="Kayıt Logu",
                description=(
                    f"**Kullanıcı:** {member.mention}\n"
                    f"**Kayıt Eden:** {interaction.user.mention}\n"
                    f"**Tarih:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
                ),
                color=discord.Color.yellow(),
            )
            await log_channel.send(embed=embed)

        if isinstance(interaction.channel, discord.TextChannel):
            await interaction.channel.set_permissions(
                member,
                overwrite=discord.PermissionOverwrite(
                    view_channel=False, send_messages=False
                ),
            )

        kayitsiz_role = guild.get_role(LUM_WAIT_ROLE)
        if kayitsiz_role in member.roles:
            await member.remove_roles(kayitsiz_role)

        await interaction.response.send_message(
            "[info]: Kayıt tamamlandı", ephemeral=True
        )
        print(f"[ok]: Kayit edildi -> {member.name}")


async def setup(bot):
    await bot.add_cog(Register(bot))