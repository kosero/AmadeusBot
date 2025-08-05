import discord
from discord.ext import commands

from src.utils import send_webhook_message, cipher_text
from config import ZINCIRLI_CH
from src.ai import *


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

        if (
            self.bot.user.mentioned_in(message)
            or isinstance(message.channel, discord.DMChannel)
            or message.channel.id == "1374086451846840370"
        ):
            cleaned_text = clean_discord_message(message.content)

            async with message.channel.typing():
                print(
                    "New Message FROM:" + str(message.author.id) + ": " + cleaned_text
                )
                if "RESET" in cleaned_text:
                    if message.author.id in message_history:
                        del message_history[message.author.id]
                    await message.reply(
                        "🤖 History Reset for user: " + str(message.author.name)
                    )
                    return
                await message.add_reaction("<:ayak:1245436100898717706>")

                if MAX_HISTORY == 0:
                    response_text = await generate_response_with_text(cleaned_text)
                    await split_and_send_messages(message, response_text, 1700)
                    return

                update_message_history(message.author.id, cleaned_text)
                response_text = await generate_response_with_text(
                    get_formatted_message_history(message.author.id)
                )
                update_message_history(message.author.id, response_text)
                await split_and_send_messages(message, response_text, 1700)


async def setup(bot):
    await bot.add_cog(OnMessage(bot))
