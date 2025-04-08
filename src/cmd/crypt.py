import discord
from discord.ext import commands
from discord import app_commands
from ..utils import send_webhook_message


class Encrypt(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="encrypt", description="Ping Pong!")
    async def encrypt(self, interaction: discord.Interaction):
        latency = round(self.bot.latency * 1000)
        await interaction.response.send_message(f"[latency]: {latency}ms")
        print(f"[ok]: encrypt, author: {interaction.user}")


class Decrypt(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="decrypt", description="Ping Pong!")
    async def decrypt(self, interaction: discord.Interaction):
        latency = round(self.bot.latency * 1000)
        await interaction.response.send_message(f"[latency]: {latency}ms")
        print(f"[ok]: decrypt, author: {interaction.user}")


async def setup(bot):
    await bot.add_cog(Encrypt(bot))
    await bot.add_cog(Decrypt(bot))
