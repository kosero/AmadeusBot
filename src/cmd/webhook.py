import discord
import random
import json

with open('config/config.json', 'r') as file:
    config = json.load(file)

NECO_PPS = config["NECO_PPS"]

async def get_or_create_webhook(channel):
    webhooks = await channel.webhooks()
    webhook = discord.utils.get(webhooks, name="Neco Arc")
    
    if webhook is None:
        webhook = await channel.create_webhook(name="Neco Arc", reason="Bot için")
        print(f"Webhook created in {channel.name}")
    if not webhook.token:
        raise ValueError("This webhook does not have a token associated with it")
    
    return webhook

async def send_webhook_message(character, channel, message, custom_avatar=None, custom_name=None):
    webhook = await get_or_create_webhook(channel)

    if character == "neco":
        avatar_url = random.choice(NECO_PPS)
        username = "Neco Arc"
    else:
        avatar_url = custom_avatar
        username = custom_name
    
    await webhook.send(
        message,
        username=username,
        avatar_url=avatar_url,
        wait=False
    )

