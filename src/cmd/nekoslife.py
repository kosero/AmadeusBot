import nekos
import discord
from discord.ext import commands
from discord import app_commands


class Neko(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def neko(self, ctx):
        neko = nekos.img("neko")
        await ctx.reply(f"{neko}")
        print(f"[ok]: neko, author: {ctx.author}")

    @app_commands.command(name="neko", description="neko :cat:")
    async def slash_neko(self, interaction: discord.Interaction):
        neko = nekos.cat()
        await interaction.response.send_message(f"{neko}")
        print(f"[ok]: neko, author: {interaction.user}")


async def setup(bot):
    await bot.add_cog(Neko(bot))
