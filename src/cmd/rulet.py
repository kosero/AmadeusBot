import discord
import random
import asyncio
from datetime import timedelta
import time

async def rulet(message):
    random.seed(time.time())
    user = message.author
    outcome = random.choice(["win", "lose"])
        
    await message.reply("Derin bir nefes alarak tetiğe yavaşça basıyorsun...")
    await asyncio.sleep(3)
    if outcome == "win":
        await message.channel.send("Bugün ölüm seninle boy ölçüşemedi.")
    else:
        try:
            duration = 86400
            await user.timeout(discord.utils.utcnow() + timedelta(seconds=duration), reason="Rulet kaybı")
            await message.channel.send(f"Kaderin ince dokunuşu bugün, şansın seninle vedalaşmaya karar verdiğini fısıldarcasına hissediliyor; sanki son perdenin inmesi vakti gelmiş gibi, geçmişin sessiz anılarıyla kısa bir elveda zamanı...")
        except discord.HTTPException as e:
            await message.reply(f"[error]: {e}", delete_after=5)
    return

