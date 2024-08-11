import re

import random
import discord
import aiohttp

PPLER = ["https://i.imgur.com/0S2ygVX.png", "https://i.imgur.com/ljGAfMg.jpeg", "https://i.imgur.com/MDlYUhn.png", "https://i.imgur.com/hChEtBh.png", "https://i.imgur.com/m6K8L1x.png", "https://i.imgur.com/2Pql211.png", "https://i.imgur.com/auiZpUy.png", "https://i.imgur.com/1cifm70.png", "https://i.pinimg.com/736x/fa/a7/47/faa747a3ddcd789edd288888ef259ccf.jpg", "https://i.pinimg.com/736x/a0/68/6d/a0686da7f616774cf1fa3575b720a3b1.jpg", "https://i.pinimg.com/736x/a6/db/24/a6db247e9ca34d1768a72b0957f8d634.jpg", "https://i.pinimg.com/736x/56/a2/90/56a2909fdaff7ce15b1627129483da14.jpg", "https://i.pinimg.com/736x/36/73/c7/3673c722f56b6233471ad22705f9f583.jpg", "https://i.pinimg.com/736x/2e/fb/d5/2efbd5e3258c6d4d227c5c6db32f3e5f.jpg", "https://i.pinimg.com/736x/e9/a2/73/e9a2731b29809ee7ad433a51de721ef5.jpg"]

async def get_or_create_webhook(channel):
    webhooks = await channel.webhooks()
    webhook = discord.utils.get(webhooks, name="Neco Arc")
    if webhook is None:
        webhook = await channel.create_webhook(name="Neco Arc", reason="Bot için")
        print(f"Webhook created in {channel.name}")
    return webhook

async def send_webhook_message(character, channel, message, custom_avatar=None, custom_name=None):
    webhook = await get_or_create_webhook(channel)
    
    if character == "neco":
        avatar_url = random.choice(PPLER)
        username = "Neco Arc"
    elif character == "necopara":
        avatar_url = "https://i.imgur.com/NcqY1ff.png"
        username = "Pisi Pisi"
    else:
        avatar_url = custom_avatar
        username = custom_name
    
    await webhook.send(
        message,
        username=username,
        avatar_url=avatar_url,
        wait=False
    )

def encrypt(plaintext, key):
    def encrypt_match(match):
        return match.group(0)

    key_length = len(key)
    key_as_int = [ord(i) for i in key.upper()]
    plaintext_int = [ord(i) for i in plaintext.upper() if i.isalpha()]
    ciphertext = ''
    key_index = 0

    pattern = re.compile(r'<@\d+>')
    parts = pattern.split(plaintext)
    patterns = pattern.findall(plaintext)

    for i, part in enumerate(parts):
        for char in part:
            if char.isalpha():
                value = (ord(char.upper()) - 65 + key_as_int[key_index % key_length] - 65) % 26
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
    plaintext = ''
    key_index = 0

    pattern = re.compile(r'<@\d+>')
    parts = pattern.split(ciphertext)
    patterns = pattern.findall(ciphertext)

    for i, part in enumerate(parts):
        for char in part:
            if char.isalpha():
                value = (ord(char.upper()) - 65 - key_as_int[key_index % key_length] + 65) % 26
                plaintext += chr(value + 65)
                key_index += 1
            else:
                plaintext += char
        if i < len(patterns):
            plaintext += patterns[i]

    return plaintext.lower()

async def get_random_message_with_link(channel_id: int, link_substring: str):
    messages_with_links = []
    async for message in channel_id.history(limit=None):
        if link_substring in message.content:
            messages_with_links.append(message)

    if messages_with_links:
        return random.choice(messages_with_links)
    else:
        return None

async def search_archwiki(query: str):
    async with aiohttp.ClientSession() as session:
        url = f"https://wiki.archlinux.org/api.php?action=query&list=search&srsearch={query}&format=json"
        async with session.get(url) as response:
            data = await response.json()

    search_results = data.get("query", {}).get("search", [])
    if not search_results:
        return None, None

    best_result = search_results[0]
    page_title = best_result.get("title")
    page_url = f"https://wiki.archlinux.org/title/{page_title.replace(' ', '_')}"

    return page_title, page_url

