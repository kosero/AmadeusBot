import json
from discord.ext import commands

from src.cmd.crypt import encrypt
from src.utils import send_webhook_message
from src.ai import create_new_chat, send_cai
from src.utils import chg_json_var

with open("config/config.json", "r") as file:
    config = json.load(file)

CAI_CHAT_ID = config["CAI_CHAT_ID"]
CAI_TOKEN = config["CAI_TOKEN"]
CAI_CHAR = config["CAI_CHAR"]

ZINCIRLI_CH = config["ZINCIRLI_CH"]
ZINCIRLI_KEY = config["ZINCIRLI_KEY"]


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
            encrypted_message = encrypt(message.content, ZINCIRLI_KEY)
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
        if message.channel.id == 1338301496923652137:
            if message.content.startswith("!RESET"):
                chat_id = await create_new_chat(CAI_CHAR)
                chg_json_var("config/config.json", "CAI_CHAT_ID", chat_id)
                global CAI_CHAT_ID
                CAI_CHAT_ID = chat_id
                await message.reply("[ok]")
                return
            else:
                await message.channel.typing()
                message_makise = await send_cai(message.content, CAI_CHAR, CAI_CHAT_ID)
                await send_webhook_message(
                    "custom",
                    message.channel,
                    message_makise,
                    custom_avatar="https://i.pinimg.com/736x/86/60/53/86605345b8bc58bfb34151e9e0229196.jpg",
                    custom_name="Makise Kurisu",
                )


async def setup(bot):
    await bot.add_cog(OnMessage(bot))
