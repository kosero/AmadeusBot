import discord
from discord.ext import commands
from discord import app_commands

import aiohttp
import tempfile
import os

from src.utils import text_to_wav


class Yukkiritalk(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    @commands.command()
    async def yk(self, ctx, *, text: str):
        async with ctx.typing():
            url = await text_to_wav(text)

            async with aiohttp.ClientSession() as session:
                async with session.get(url) as resp:
                    if resp.status != 200:
                        await ctx.reply("Audio file could not be downloaded.")
                        return

                    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp_file:
                        tmp_file.write(await resp.read())
                        tmp_path = tmp_file.name

            file = discord.File(tmp_path, filename="output.wav")
            await ctx.reply(file=file)
            os.remove(tmp_path)
            print(f"yukkuritalk, author: {ctx.author}")


    @app_commands.command(name="yukkuritalk", description=":speaking_head:")
    @app_commands.describe(text="metin")
    async def slash_yukkiritalk(self, interaction: discord.Interaction, text: str):
        await interaction.response.defer()
        url = await text_to_wav(text)

        async with aiohttp.ClientSession() as session:
            async with session.get(url) as resp:
                if resp.status != 200:
                    await interaction.followup.send("Audio file could not be downloaded.")
                    return

                with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp_file:
                    tmp_file.write(await resp.read())
                    tmp_path = tmp_file.name

        file = discord.File(tmp_path, filename="output.wav")
        await interaction.followup.send(file=file)
        os.remove(tmp_path)
        print(f"yukkuri, author: {interaction.user}")


async def setup(bot):
    await bot.add_cog(Yukkiritalk(bot))
