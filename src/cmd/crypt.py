import discord
from discord.ext import commands
from discord import app_commands
import json
import re
from src.utils import send_webhook_message


with open("config/config.json", "r") as file:
    config = json.load(file)

ZINCIRLI_KEY = config["ZINCIRLI_KEY"]


def encrypt(plaintext, key):
    def encrypt_match(match):
        return match.group(0)

    key_length = len(key)
    key_as_int = [ord(i) for i in key.upper()]
    ciphertext = ""
    key_index = 0

    pattern = re.compile(r"<@\d+>")
    parts = pattern.split(plaintext)
    patterns = pattern.findall(plaintext)

    for i, part in enumerate(parts):
        for char in part:
            if char.isalpha():
                value = (
                    ord(char.upper()) - 65 + key_as_int[key_index % key_length] - 65
                ) % 26
                ciphertext += chr(value + 65)
                key_index += 1
            else:
                ciphertext += char
        if i < len(patterns):
            ciphertext += patterns[i]

    return ciphertext


def decrypt(ciphertext, key):
    def decrypt_match(match):
        return match.group(0)

    key_length = len(key)
    key_as_int = [ord(i) for i in key.upper()]
    plaintext = ""
    key_index = 0

    pattern = re.compile(r"<@\d+>")
    parts = pattern.split(ciphertext)
    patterns = pattern.findall(ciphertext)

    for i, part in enumerate(parts):
        for char in part:
            if char.isalpha():
                value = (
                    ord(char.upper()) - 65 - key_as_int[key_index % key_length] + 65
                ) % 26
                plaintext += chr(value + 65)
                key_index += 1
            else:
                plaintext += char
        if i < len(patterns):
            plaintext += patterns[i]

    return plaintext.lower()


async def zn_ch_en(message):
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
