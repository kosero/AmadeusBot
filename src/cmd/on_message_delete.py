import discord
from discord.ext import commands

from src.utils import build_embed
from ..cfg.config import LUM_MSG_DEL_CH


class OnMessageDelete(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    def _is_valid_deletion(self, author, webhook_id, is_bot) -> bool:
        return author != self.bot.user and not webhook_id and not is_bot

    @commands.Cog.listener()
    async def on_message_delete(self, message):
        if not self._is_valid_deletion(
            message.author, message.webhook_id, message.author.bot
        ):
            return

        log_channel = self.bot.get_channel(LUM_MSG_DEL_CH)
        if not log_channel:
            print("[Error]: Log channel not found.")
            return

        author_avatar_url = (
            str(message.author.avatar.url)
            if message.author.avatar
            else str(self.bot.user.avatar.url)
        )

        embed_data = {
            "title": f"Message deleted in {message.channel.mention}",
            "description": message.content or "https://dar.vin/koseroayaklari",
            "color": discord.Color.blue(),
            "thumbnail_url": author_avatar_url,
            "fields": [("Author", message.author.mention)],
            "footer": f"{message.created_at}",
        }

        embed = await build_embed(embed_data)
        await log_channel.send(embed=embed)


async def setup(bot):
    await bot.add_cog(OnMessageDelete(bot))
