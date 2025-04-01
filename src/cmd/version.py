import discord
from discord.ext import commands
from discord import app_commands

from src.cfg.config import VERSION


class Version(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def version(self, ctx):
        await ctx.reply(f"{VERSION}")
        print(f"[ok]: version, author: {ctx.author}")


class Slash_version(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="version", description="dupdisdup :whale:")
    async def version(self, interaction: discord.Interaction):
        await interaction.response.send_message(f"{VERSION}")
        print(f"[ok]: version, author: {interaction.user}")


async def setup(bot):
    await bot.add_cog(Version(bot))
    await bot.add_cog(Slash_version(bot))
