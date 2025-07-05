import discord
from discord.ext import commands
import os

from config import BOT_TOKEN


class AmadeusBot(commands.Bot):
    def __init__(self):
        intents = discord.Intents.default()
        intents.message_content = True
        intents.members = True
        intents.messages = True
        intents.guilds = True

        super().__init__(command_prefix=".", intents=intents)

    async def setup_hook(self):
        for filename in os.listdir("./src/cmd"):
            if filename.endswith(".py"):
                await self.load_extension(f"src.cmd.{filename[:-3]}")

        for filename in os.listdir("./src/event"):
            if filename.endswith(".py"):
                await self.load_extension(f"src.event.{filename[:-3]}")

        print("[info]: all cogs loaded")

    async def on_ready(self):
        await bot.tree.sync()
        await bot.change_presence(status=discord.Status.dnd, activity=discord.Game(""))
        print(f"[work]: {self.user}")


if __name__ == "__main__":
    bot = AmadeusBot()
    bot.run(BOT_TOKEN)
