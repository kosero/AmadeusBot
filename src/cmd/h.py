import io
from PIL import Image
import discord
from discord.ext import commands
from discord import app_commands


class Hex(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    def hex_to_color_image(self, hex_code: str, size: int = 128) -> io.BytesIO:
        hex_code = hex_code.strip().lstrip("#")
        if len(hex_code) != 6:
            raise ValueError("Hex code must have 6 characters.")

        r = int(hex_code[0:2], 16)
        g = int(hex_code[2:4], 16)
        b = int(hex_code[4:6], 16)

        width = size
        height = max(1, size // 4)

        img = Image.new("RGB", (width, height), (r, g, b))
        buffer = io.BytesIO()
        img.save(buffer, format="PNG")
        buffer.seek(0)
        return buffer

    @commands.command(name="h")
    async def h(self, ctx, hex_code: str):
        try:
            img_buffer = self.hex_to_color_image(hex_code)
        except ValueError as e:
            return await ctx.reply(f"Hata: {e}")

        file = discord.File(fp=img_buffer, filename="color.png")
        embed = discord.Embed(title=f"#{hex_code.upper()}")
        embed.set_image(url="attachment://color.png")
        await ctx.reply(embed=embed, file=file)
        print(f"[ok]: hex (text), author: {ctx.author}")

    @app_commands.command(name="h", description="hex code preview")
    async def slash_h(self, interaction: discord.Interaction, hex_code: str):
        try:
            img_buffer = self.hex_to_color_image(hex_code)
        except ValueError as e:
            return await interaction.response.send_message(f"Hata: {e}", ephemeral=True)

        file = discord.File(fp=img_buffer, filename="color.png")
        embed = discord.Embed(title=f"#{hex_code.upper()}")
        embed.set_image(url="attachment://color.png")
        await interaction.response.send_message(embed=embed, file=file)
        print(f"[ok]: hex (slash), author: {interaction.user}")


async def setup(bot):
    await bot.add_cog(Hex(bot))
