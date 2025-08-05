import re
import discord
import aiohttp
from googletrans import Translator


translator = Translator()


async def text_to_wav(text: str):
    try:
        translated = await translator.translate(text, src="tr", dest="ja")
        jp_text = translated.text
    except Exception as e:
        return f"{e}"

    url = "https://yukkuritalk.com/"
    params = {"txt": jp_text, "submit": "ゆっくり言っていてね"}

    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url, params=params) as resp:
                html = await resp.text()
    except Exception as e:
        return f"{e}"

    match = re.search(
        r'"(https://yukkuritalkeastus2\.blob\.core\.windows\.net/yukkuriwav/.*?\.wav)"',
        html,
    )
    if match:
        return match.group(1)
    else:
        return "Audio file not found."


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
     channel, message, custom_avatar=None, custom_name=None
):
    webhook = await get_or_create_webhook(channel)

    avatar_url = custom_avatar
    username = custom_name

    await webhook.send(message, username=username, avatar_url=avatar_url, wait=False)


async def build_embed(embed_data: dict):
    """
    embed_data = {
        "title": "Test",
        "description": "test.",
        "color": discord.Color.blue(),
        "thumbnail_url": "https://i.imgur.com/0EGjE0h.gif",
        "image_url": "https://i.imgur.com/0EGjE0h.gif",
        "fields": [ ("test 1", "test 1"), ("test 2", "test 2") ],
        "footer": "Test Footer",
    }
    """
    embed = discord.Embed(
        title=embed_data.get("title"),
        description=embed_data.get("description"),
        color=embed_data.get("color", discord.Color.blue()),
    )

    thumbnail_url = embed_data.get("thumbnail_url")
    if thumbnail_url:
        embed.set_thumbnail(url=thumbnail_url)

    fields = embed_data.get("fields", [])
    image_url = embed_data.get("image_url")

    for i, field in enumerate(fields):
        embed.add_field(name=field[0], value=field[1], inline=False)
        if i == len(fields) // 2 and image_url:
            embed.set_image(url=image_url)

    footer = embed_data.get("footer")
    if footer:
        embed.set_footer(text=footer)

    return embed


CYPHER_MAP = {
    "A": "A",
    "B": "A\u0307",
    "C": "A\u0321",
    "D": "A\u0331",
    "E": "A\u0301",
    "F": "A\u032e",
    "G": "A\u030b",
    "H": "A\u0330",
    "I": "A\u0309",
    "J": "A\u0313",
    "K": "A\u0323",
    "L": "A\u0306",
    "M": "A\u030c",
    "N": "A\u0302",
    "O": "A\u030a",
    "P": "A\u032f",
    "Q": "A\u0324",
    "R": "A\u0311",
    "S": "A\u0303",
    "T": "A\u0304",
    "U": "A\u0308",
    "V": "A\u0300",
    "W": "A\u030f",
    "X": "A\u036f",
    "Y": "A\u0326",
    "Z": "A\u0337",
}
REVERSE_CYPHER_MAP = {v: k for k, v in CYPHER_MAP.items()}


def decipher_text(_text: str) -> str:
    return "".join(REVERSE_CYPHER_MAP.get(c, c) for c in _text)


def cipher_text(_text: str) -> str:
    return "".join(CYPHER_MAP.get(c.upper(), c) for c in _text)
