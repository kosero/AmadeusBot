import discord
import random
import asyncio
from datetime import timedelta
import time
from discord.ext import commands
from discord import app_commands


class Roulette(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def rulet(self, ctx):
        random.seed(time.time())
        user = ctx.author
        outcome = random.choice(["win", "lose"])

        await ctx.reply("Derin bir nefes alarak tetiğe yavaşça basıyorsun...")
        await asyncio.sleep(3)
        if outcome == "win":
            await ctx.channel.send("Bugün ölüm seninle boy ölçüşemedi.")
        else:
            try:
                duration = 86400
                await user.timeout(
                    discord.utils.utcnow() + timedelta(seconds=duration),
                    reason="Rulet kaybı",
                )
                await ctx.channel.send(
                    f"Kaderin ince dokunuşu bugün, şansın seninle vedalaşmaya karar verdiğini fısıldarcasına hissediliyor; sanki son perdenin inmesi vakti gelmiş gibi, geçmişin sessiz anılarıyla kısa bir elveda zamanı..."
                )
            except discord.HTTPException as e:
                await ctx.reply(f"[error]: {e}", delete_after=5)


class SlashRoulette(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="rulet", description="Bir rulet oynayın.")
    async def slash_rulet(self, interaction: discord.Interaction):
        random.seed(time.time())
        user = interaction.user
        outcome = random.choice(["win", "lose"])

        await interaction.response.send_message(
            "Derin bir nefes alarak tetiğe yavaşça basıyorsun..."
        )
        await asyncio.sleep(3)
        if outcome == "win":
            await interaction.channel.send("Bugün ölüm seninle boy ölçüşemedi.")
        else:
            try:
                duration = 86400
                await user.timeout(
                    discord.utils.utcnow() + timedelta(seconds=duration),
                    reason="Rulet kaybı",
                )
                await interaction.channel.send(
                    f"Kaderin ince dokunuşu bugün, şansın seninle vedalaşmaya karar verdiğini fısıldarcasına hissediliyor; sanki son perdenin inmesi vakti gelmiş gibi, geçmişin sessiz anılarıyla kısa bir elveda zamanı..."
                )
            except discord.HTTPException as e:
                await interaction.response.send_message(f"[error]: {e}", ephemeral=True)


async def setup(bot):
    await bot.add_cog(Roulette(bot))
    await bot.add_cog(SlashRoulette(bot))
