import discord
from discord.ext import commands
from discord import app_commands
from src.utils import cipher_text, decipher_text


class Crypt(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="encrypt", description="mesajini sifreler.")
    async def encrypt(self, interaction: discord.Interaction, text: str):
        encrypted_text = cipher_text(text)
        await interaction.response.send_message(f"{encrypted_text}")
        print(f"[ok]: encrypt, author: {interaction.user}")

    @app_commands.command(name="decrypt", description="mesajin sifresini cozer.")
    async def decrypt(self, interaction: discord.Interaction, text: str):
        decrypted_text = decipher_text(text)
        await interaction.response.send_message(f"{decrypted_text}")
        print(f"[ok]: decrypt, author: {interaction.user}")


async def setup(bot):
    await bot.add_cog(Crypt(bot))
