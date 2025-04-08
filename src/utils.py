import json
import discord
import random
import re
from .cfg.config import NECO_PPS, ZINCIRLI_KEY


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


def change_words(text, old_word, new_word):
    updated_text = text.replace(old_word, new_word)
    return updated_text


def chg_json_var(file_path: str, key: str, new_value):
    with open(file_path, "r", encoding="utf-8") as file:
        data = json.load(file)

    if key in data:
        data[key] = new_value

        with open(file_path, "w", encoding="utf-8") as file:
            json.dump(data, file, indent=4)
    else:
        return


async def get_or_create_webhook(channel):
    webhooks = await channel.webhooks()
    webhook = discord.utils.get(webhooks, name="Neco Arc")

    if webhook is None:
        webhook = await channel.create_webhook(name="Neco Arc", reason="Bot için")
        print(f"Webhook created in {channel.name}")
    if not webhook.token:
        raise ValueError("This webhook does not have a token associated with it")

    return webhook


async def send_webhook_message(
    character, channel, message, custom_avatar=None, custom_name=None
):
    webhook = await get_or_create_webhook(channel)

    if character == "neco":
        avatar_url = random.choice(NECO_PPS)
        username = "Neco Arc"
    else:
        avatar_url = custom_avatar
        username = custom_name

    await webhook.send(message, username=username, avatar_url=avatar_url, wait=False)
