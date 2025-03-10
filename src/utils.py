import json
import discord
import random

from cfg.config import NECO_PPS


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
