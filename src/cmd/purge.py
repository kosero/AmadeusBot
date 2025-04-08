import discord
from discord.ext import commands
from discord import app_commands


class MessagePurge(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def purge(self, ctx, count: int = 0):
        if not ctx.channel.permissions_for(ctx.author).manage_messages:
            await ctx.reply("[warn]: No permission", delete_after=5)
            return

        if count < 1 or count > 100:
            await ctx.reply("[warn]: `!purge 1-100`", delete_after=5)
            return

        deleted = await ctx.channel.purge(limit=count + 1)
        await ctx.reply(f"[info]: {len(deleted)} messages deleted", delete_after=5)

    @app_commands.command(
        name="purge", description="Delete a certain number of messages."
    )
    @app_commands.describe(count="The number of messages to delete (1-100).")
    async def slash_purge(self, interaction: discord.Interaction, count: int = 0):
        if not interaction.channel.permissions_for(interaction.user).manage_messages:
            await interaction.response.send_message(
                "[warn]: No permission", ephemeral=True
            )
            return

        if count < 1 or count > 100:
            await interaction.response.send_message(
                "[warn]: `/purge 1-100`", ephemeral=True
            )
            return

        deleted = await interaction.channel.purge(limit=count + 1)
        await interaction.response.send_message(
            f"[info]: {len(deleted)} messages deleted", ephemeral=True
        )


async def setup(bot):
    await bot.add_cog(MessagePurge(bot))
