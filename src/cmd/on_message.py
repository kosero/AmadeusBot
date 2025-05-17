import discord
import aiohttp
from discord.ext import commands

from src.utils import send_webhook_message, cipher_text
from ..cfg.config import ZINCIRLI_CH


class OnMessage(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author == self.bot.user:
            return
        if message.webhook_id:
            return
        if message.channel.id == ZINCIRLI_CH:
            encrypted_message = cipher_text(message.content)
            avatar_url = (
                message.author.avatar.url
                if message.author.avatar
                else "https://i.imgur.com/CSU09SU.png"
            )
            await send_webhook_message(
                "custom",
                message.channel,
                encrypted_message,
                custom_avatar=avatar_url,
                custom_name=message.author.name,
            )
            await message.delete()


async def setup(bot):
    await bot.add_cog(OnMessage(bot))
