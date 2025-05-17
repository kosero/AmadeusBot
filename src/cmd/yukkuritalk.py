import re
import io
import discord
from discord.ext import commands
from googletrans import Translator
import aiohttp


class YukkuriTalk(commands.Cog):
    URL_PATTERN = re.compile(
        r'"(https:\/\/yukkuritalkeastus2\.blob\.core\.windows\.net\/yukkuriwav\/(.*?).wav)"'
    )

    def __init__(self, bot):
        self.bot = bot
        self.translator = Translator()
        self.session = aiohttp.ClientSession()

    async def cog_unload(self):
        await self.session.close()

    async def romaji_to_wav_url(self, text: str) -> str | None:
        try:
            translated = await self.translator.translate(text, src="tr", dest="ja")
            japanese_text = translated.text
        except Exception as e:
            return None

        url = (
            f"https://yukkuritalk.com/?txt={japanese_text}&submit=ゆっくり言っていてね"
        )
        try:
            async with self.session.get(url) as response:
                if response.status != 200:
                    print(f"[warn]: HTTP response status {response.status}")
                    return None
                html = await response.text()
        except Exception as e:
            print(f"[err]: HTTP error: {e}")
            return None

        m = self.URL_PATTERN.search(html)
        if m:
            return m.group(1)
        else:
            print("[warn]: WAV URL not found in response HTML")
            return None

    @commands.command()
    async def yukkuritalk(self, ctx, *, text):
        wav_url = await self.romaji_to_wav_url(text)
        if not wav_url:
            await ctx.reply("[err]: Could not retrieve WAV URL.", delete_after=5)
            return

        try:
            async with self.session.get(wav_url) as resp:
                if resp.status != 200:
                    await ctx.reply(
                        f"[err]: Failed to download audio file. Status code: {resp.status}",
                        delete_after=5,
                    )
                    return
                data = await resp.read()
        except Exception as e:
            await ctx.reply(
                f"[err]: Error occurred while downloading audio file: {e}",
                delete_after=5,
            )
            return

        file = discord.File(io.BytesIO(data), filename="yukkuri.wav")
        await ctx.reply(file=file)


async def setup(bot):
    await bot.add_cog(YukkuriTalk(bot))
