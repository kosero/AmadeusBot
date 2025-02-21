import discord
from discord.ext import commands
from discord import app_commands


class Ping(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def ping(self, ctx):
        latency = round(self.bot.latency * 1000)
        await ctx.reply(f"[latency]: {latency}ms")
        print(f"[ok]: ping, author: {ctx.author}")


class Slash_ping(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="ping", description="Ping Pong!")
    async def ping(self, interaction: discord.Interaction):
        latency = round(self.bot.latency * 1000)
        await interaction.response.send_message(f"[latency]: {latency}ms")
        print(f"[ok]: ping, author: {interaction.user}")


async def setup(bot):
    await bot.add_cog(Ping(bot))
    await bot.add_cog(Slash_ping(bot))
