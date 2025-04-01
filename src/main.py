import discord
from discord.ext import commands
import os

from src.cfg.config import BOT_TOKEN, BOT_STATE


class AmadeusBot(commands.Bot):
    def __init__(self):
        intents = discord.Intents.default()
        intents.message_content = True
        intents.members = True
        intents.messages = True
        intents.guilds = True

        super().__init__(command_prefix="!", intents=intents)

    async def setup_hook(self):
        for filename in os.listdir("./src/cmd"):
            if filename.endswith(".py"):
                await self.load_extension(f"src.cmd.{filename[:-3]}")
        print("[info]: all cogs loaded")

    async def on_ready(self):
        await self.tree.sync()
        print(f"[work]: {self.user}")


if BOT_STATE:
    bot = AmadeusBot()
    bot.run(BOT_TOKEN)
